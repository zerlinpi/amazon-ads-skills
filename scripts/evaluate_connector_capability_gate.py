#!/usr/bin/env python3
"""Evaluate connector capability evidence before metric interpretation.

Read-only, dependency-free gate. It never calls a connector, never mutates an
advertiser account, and never converts missing/unsupported capability evidence
into a numeric metric observation.
"""

from __future__ import annotations

import json
import sys
from typing import Any

KNOWN_STATUSES = {"Supported", "Partial", "Unsupported", "Unknown"}
PASS_DECISIONS = ["High Confidence", "Suggest", "Shadow"]
DEGRADED_DECISIONS = [
    "Directional",
    "Hold",
    "Alternate Source",
    "Missing Data",
    "Manual Review",
]
BLOCKED_DECISIONS = ["Hold", "Alternate Source", "Missing Data", "Manual Review"]
SCOPE_FIELDS = {
    "region": "regions",
    "marketplace": "marketplaces",
    "ad_product": "ad_products",
    "account_type": "account_types",
}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _normalize_requirements(value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("required_capabilities must be a non-empty array")
    result: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not _non_empty_string(item):
            raise ValueError(
                f"required_capabilities[{index}] must be a non-empty string"
            )
        capability_id = item.strip()
        if capability_id in seen:
            raise ValueError(
                f"required_capabilities contains duplicate capability_id {capability_id!r}"
            )
        seen.add(capability_id)
        result.append(capability_id)
    return result


def _normalize_expected_scope(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError("expected_scope must be an object or null")
    unknown = sorted(set(value) - set(SCOPE_FIELDS))
    if unknown:
        raise ValueError(f"expected_scope contains unsupported fields: {unknown}")
    normalized: dict[str, str] = {}
    for field, item in value.items():
        if not _non_empty_string(item):
            raise ValueError(f"expected_scope.{field} must be a non-empty string")
        normalized[field] = item.strip()
    return normalized


def _index_capabilities(snapshot: Any) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    if snapshot is None:
        return {}, {}
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be an object or null")

    capabilities = snapshot.get("capabilities")
    if capabilities is None:
        capabilities = []
    if not isinstance(capabilities, list):
        raise ValueError("snapshot.capabilities must be an array")

    indexed: dict[str, dict[str, Any]] = {}
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, dict):
            raise ValueError(f"snapshot.capabilities[{index}] must be an object")
        capability_id = capability.get("capability_id")
        if not _non_empty_string(capability_id):
            raise ValueError(
                f"snapshot.capabilities[{index}].capability_id must be a non-empty string"
            )
        capability_id = capability_id.strip()
        if capability_id in indexed:
            raise ValueError(
                f"snapshot.capabilities contains duplicate capability_id {capability_id!r}"
            )
        status = capability.get("status", "Unknown")
        if status not in KNOWN_STATUSES:
            raise ValueError(
                f"snapshot.capabilities[{index}].status must be one of {sorted(KNOWN_STATUSES)}"
            )
        indexed[capability_id] = capability
    return indexed, snapshot


def _evaluate_scope(capability: dict[str, Any], expected_scope: dict[str, str]) -> tuple[str, list[str]]:
    if not expected_scope:
        return "not_evaluated", []

    scope = capability.get("scope")
    if not isinstance(scope, dict):
        return "unknown", [
            "decision scope was requested but connector capability scope is not exposed"
        ]

    warnings: list[str] = []
    unknown = False
    blocked = False
    for expected_field, expected_value in expected_scope.items():
        capability_field = SCOPE_FIELDS[expected_field]
        observed_values = scope.get(capability_field)
        if not isinstance(observed_values, list) or not observed_values:
            unknown = True
            warnings.append(
                f"connector capability does not expose bounded {expected_field} scope"
            )
            continue
        normalized_values = {
            item.strip().casefold()
            for item in observed_values
            if _non_empty_string(item)
        }
        if expected_value.casefold() not in normalized_values:
            blocked = True
            warnings.append(
                f"required capability is not supported for requested {expected_field} {expected_value!r}"
            )

    if blocked:
        return "blocked", warnings
    if unknown:
        return "unknown", warnings
    return "pass", warnings


def evaluate_connector_capability_gate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")

    requirements = _normalize_requirements(payload.get("required_capabilities"))
    expected_scope = _normalize_expected_scope(payload.get("expected_scope"))
    indexed, snapshot = _index_capabilities(payload.get("snapshot"))

    evaluated: list[dict[str, Any]] = []
    has_partial = False
    has_blocked = False

    for capability_id in requirements:
        capability = indexed.get(capability_id)
        scope_effect = "not_evaluated"
        if capability is None:
            status = "Unknown"
            access_mode = "unknown"
            gate_effect = "blocked"
            has_blocked = True
            warnings = ["required capability is absent from the observed connector snapshot"]
        else:
            status = capability.get("status", "Unknown")
            access_mode = capability.get("access_mode", "unknown")
            warnings = list(capability.get("warnings") or [])
            scope_effect, scope_warnings = _evaluate_scope(capability, expected_scope)
            warnings.extend(scope_warnings)
            if status == "Supported" and scope_effect in {"pass", "not_evaluated"}:
                gate_effect = "pass"
            elif status == "Partial" and scope_effect in {"pass", "not_evaluated"}:
                gate_effect = "degraded"
                has_partial = True
            else:
                gate_effect = "blocked"
                has_blocked = True

        evaluated.append(
            {
                "capability_id": capability_id,
                "status": status,
                "access_mode": access_mode,
                "scope_effect": scope_effect,
                "gate_effect": gate_effect,
                "warnings": warnings,
            }
        )

    if has_blocked:
        gate_status = "Blocked"
        allowed = BLOCKED_DECISIONS
        high_confidence_allowed = False
    elif has_partial:
        gate_status = "Degraded"
        allowed = DEGRADED_DECISIONS
        high_confidence_allowed = False
    else:
        gate_status = "Pass"
        allowed = PASS_DECISIONS
        high_confidence_allowed = True

    return {
        "gate_status": gate_status,
        "high_confidence_allowed": high_confidence_allowed,
        "missing_evidence_policy": "never_zero",
        "allowed_decision_classes": allowed,
        "connector_id": snapshot.get("connector_id"),
        "connector_version": snapshot.get("connector_version"),
        "captured_at": snapshot.get("captured_at"),
        "expected_scope": expected_scope or None,
        "requirements": evaluated,
    }


def _load_payload() -> Any:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError("stdin must contain valid JSON") from exc


def main() -> int:
    try:
        result = evaluate_connector_capability_gate(_load_payload())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
