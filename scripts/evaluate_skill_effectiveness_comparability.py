#!/usr/bin/env python3
"""Evaluate longitudinal comparability of two Skill-effectiveness benchmarks.

The helper is read-only. It does not calculate a new effectiveness delta; it only
checks whether two benchmark records share the same declared measurement identity.
"""

from __future__ import annotations

import json
import sys
from typing import Any

MISSING = object()
COMPARABILITY_FIELDS = (
    "skill",
    "fixture_id",
    "fixture_version",
    "mode",
    "harness.runtime",
    "harness.model",
    "harness.model_version",
    "harness.config_hash",
    "harness.tool_profile_hash",
    "harness.evidence_hash",
    "harness.measurement_contract.evaluator_id",
    "harness.measurement_contract.evaluator_version",
    "harness.measurement_contract.rubric_version",
)
NULL_IS_EXPLICIT = {"harness.measurement_contract.rubric_version"}


def _get_path(payload: dict[str, Any], path: str) -> Any:
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return MISSING
        value = value[part]
    return value


def _unknown(path: str, value: Any) -> bool:
    if value is MISSING:
        return True
    if value is None:
        return path not in NULL_IS_EXPLICIT
    return isinstance(value, str) and not value.strip()


def evaluate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    baseline = payload.get("baseline")
    candidate = payload.get("candidate")
    if not isinstance(baseline, dict) or not isinstance(candidate, dict):
        raise ValueError("baseline and candidate must be benchmark objects")

    mismatches: list[str] = []
    unknown_fields: list[str] = []

    for path in COMPARABILITY_FIELDS:
        left = _get_path(baseline, path)
        right = _get_path(candidate, path)
        if _unknown(path, left) or _unknown(path, right):
            unknown_fields.append(path)
            continue
        if left != right:
            mismatches.append(path)

    if mismatches:
        status = "Not Comparable"
    elif unknown_fields:
        status = "Unknown"
    else:
        status = "Comparable"

    return {
        "comparability_status": status,
        "mismatches": sorted(mismatches),
        "unknown_fields": sorted(unknown_fields),
        "compared_fields": list(COMPARABILITY_FIELDS),
        "missing_identity_policy": "never_assume_comparable",
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = evaluate(payload)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
