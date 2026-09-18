#!/usr/bin/env python3
"""Evaluate connector capability evidence before metric interpretation.

Read-only, dependency-free gate. It never calls a connector, never mutates an
advertiser account, and never converts missing/unsupported capability evidence
into a numeric metric observation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

KNOWN_STATUSES = {"Supported", "Partial", "Unsupported", "Unknown"}
BINDING_VERIFICATION_STATUSES = {"Verified", "Unverified", "Unknown"}
BINDING_SURFACE_TYPES = {
    "tool",
    "report",
    "dataset",
    "stream",
    "export",
    "endpoint",
    "warehouse_table",
    "manual_export",
}
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

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_CATALOG = ROOT / "references" / "connector-capability-catalog.json"


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load_capability_catalog() -> tuple[set[str], str | None]:
    try:
        catalog = json.loads(CAPABILITY_CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("connector capability catalog is unavailable or invalid") from exc
    if not isinstance(catalog, dict):
        raise ValueError("connector capability catalog must be an object")

    capabilities = catalog.get("capabilities")
    if not isinstance(capabilities, list):
        raise ValueError("connector capability catalog capabilities must be an array")

    registered: set[str] = set()
    for index, item in enumerate(capabilities):
        if not isinstance(item, dict) or not _non_empty_string(item.get("capability_id")):
            raise ValueError(
                f"connector capability catalog capabilities[{index}] has invalid capability_id"
            )
        capability_id = item["capability_id"].strip()
        if capability_id in registered:
            raise ValueError(
                f"connector capability catalog contains duplicate capability_id {capability_id!r}"
            )
        registered.add(capability_id)

    version = catalog.get("catalog_version")
    if version is not None and not _non_empty_string(version):
        raise ValueError("connector capability catalog version must be a non-empty string or null")
    return registered, version


def _normalize_requirements(value: Any, registered: set[str]) -> list[str]:
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
        if capability_id not in registered:
            raise ValueError(
                f"required_capabilities contains unregistered capability_id {capability_id!r}"
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


def _evaluate_binding_scope(
    binding: dict[str, Any],
    expected_scope: dict[str, str],
) -> tuple[str, list[str]]:
    if not expected_scope:
        return "pass", []

    scope = binding.get("scope")
    if not isinstance(scope, dict):
        return "unknown", [
            "verified connector binding does not expose bounded decision scope"
        ]

    warnings: list[str] = []
    unknown = False
    blocked = False
    for expected_field, expected_value in expected_scope.items():
        binding_field = SCOPE_FIELDS[expected_field]
        observed_values = scope.get(binding_field)
        if not isinstance(observed_values, list) or not observed_values:
            unknown = True
            warnings.append(
                f"connector binding does not expose bounded {expected_field} scope"
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
                f"connector binding does not cover requested {expected_field} {expected_value!r}"
            )

    if blocked:
        return "blocked", warnings
    if unknown:
        return "unknown", warnings
    return "pass", warnings


def _evaluate_bindings(
    capability: dict[str, Any],
    expected_scope: dict[str, str],
) -> tuple[str, list[str], list[str]]:
    bindings = capability.get("bindings")
    if not bindings:
        return "unknown", [], [
            "supported capability has no verified connector surface binding"
        ]
    if not isinstance(bindings, list):
        raise ValueError("capability.bindings must be an array")

    verified_binding_ids: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    saw_unverified = False
    saw_verified = False

    for index, binding in enumerate(bindings):
        field = f"capability.bindings[{index}]"
        if not isinstance(binding, dict):
            raise ValueError(f"{field} must be an object")

        binding_id = binding.get("binding_id")
        surface_type = binding.get("surface_type")
        surface_id = binding.get("surface_id")
        verification_status = binding.get("verification_status")
        observed_at = binding.get("observed_at")
        evidence = binding.get("evidence")

        if not _non_empty_string(binding_id):
            raise ValueError(f"{field}.binding_id must be a non-empty string")
        binding_id = binding_id.strip()
        if binding_id in seen_ids:
            raise ValueError(f"capability.bindings contains duplicate binding_id {binding_id!r}")
        seen_ids.add(binding_id)

        if surface_type not in BINDING_SURFACE_TYPES:
            raise ValueError(
                f"{field}.surface_type must be one of {sorted(BINDING_SURFACE_TYPES)}"
            )
        if not _non_empty_string(surface_id):
            raise ValueError(f"{field}.surface_id must be a non-empty string")
        if verification_status not in BINDING_VERIFICATION_STATUSES:
            raise ValueError(
                f"{field}.verification_status must be one of "
                f"{sorted(BINDING_VERIFICATION_STATUSES)}"
            )
        if not _non_empty_string(observed_at):
            raise ValueError(f"{field}.observed_at must be a non-empty string")
        if not isinstance(evidence, list):
            raise ValueError(f"{field}.evidence must be an array")

        if verification_status != "Verified":
            if verification_status == "Unverified":
                saw_unverified = True
            continue

        saw_verified = True
        if not evidence:
            raise ValueError(
                f"{field} is Verified but has no evidence supporting the binding"
            )

        scope_effect, scope_warnings = _evaluate_binding_scope(binding, expected_scope)
        warnings.extend(scope_warnings)
        if scope_effect == "pass":
            verified_binding_ids.append(binding_id)

    if verified_binding_ids:
        return "pass", verified_binding_ids, warnings
    if saw_unverified:
        warnings.append(
            "connector surface binding exists but is not independently verified"
        )
        return "unverified", [], warnings
    if saw_verified:
        warnings.append(
            "verified connector surface binding does not prove the requested decision scope"
        )
    return "unknown", [], warnings


def evaluate_connector_capability_gate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")

    registered_capabilities, catalog_version = _load_capability_catalog()
    requirements = _normalize_requirements(
        payload.get("required_capabilities"),
        registered_capabilities,
    )
    expected_scope = _normalize_expected_scope(payload.get("expected_scope"))
    indexed, snapshot = _index_capabilities(payload.get("snapshot"))

    evaluated: list[dict[str, Any]] = []
    has_partial = False
    has_blocked = False

    for capability_id in requirements:
        capability = indexed.get(capability_id)
        scope_effect = "not_evaluated"
        binding_effect = "unknown"
        verified_binding_ids: list[str] = []
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
            binding_effect, verified_binding_ids, binding_warnings = _evaluate_bindings(
                capability,
                expected_scope,
            )
            warnings.extend(binding_warnings)

            if status == "Supported":
                if scope_effect not in {"pass", "not_evaluated"}:
                    gate_effect = "blocked"
                    has_blocked = True
                elif binding_effect == "pass":
                    gate_effect = "pass"
                else:
                    gate_effect = "degraded"
                    has_partial = True
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
                "binding_effect": binding_effect,
                "verified_binding_ids": verified_binding_ids,
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
        "catalog_version": catalog_version,
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
