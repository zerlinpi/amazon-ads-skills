#!/usr/bin/env python3
"""Deterministically compare two measurement-composition evidence states.

This helper is read-only. It classifies whether baseline/post conversion
measurement composition is sufficiently comparable for causal review; it never
authorizes or performs Amazon Ads writes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FIELDS = (
    "modeled_conversion_inclusion",
    "direct_modeled_split_available",
    "allocation_coverage_status",
    "unallocated_rows_present",
    "allocation_grain",
)
BOOLEAN_FIELDS = {
    "direct_modeled_split_available",
    "unallocated_rows_present",
}
HARD_INCOMPATIBILITY_FIELDS = {
    "modeled_conversion_inclusion",
    "allocation_grain",
}
UNKNOWN_STRINGS = {
    "unknown",
    "unsupported",
    "unavailable",
    "not available",
    "not_available",
}


def _normalize(
    state: Any,
    *,
    side: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if not isinstance(state, dict):
        return None, [f"{side} measurement state must be an object"]

    composition = state.get("measurement_composition")
    if composition is None:
        return None, [f"{side} measurement_composition is missing"]
    if not isinstance(composition, dict):
        return None, [f"{side} measurement_composition must be an object"]

    normalized: dict[str, Any] = {}
    problems: list[str] = []
    for field in FIELDS:
        if field not in composition or composition.get(field) is None:
            problems.append(f"{side} measurement_composition.{field} is missing or unknown")
            continue

        value = composition[field]
        if field in BOOLEAN_FIELDS:
            if not isinstance(value, bool):
                problems.append(
                    f"{side} measurement_composition.{field} must be boolean when known"
                )
                continue
        else:
            if not isinstance(value, str) or not value.strip():
                problems.append(
                    f"{side} measurement_composition.{field} must be a non-empty string when known"
                )
                continue
            if value.strip().lower() in UNKNOWN_STRINGS:
                problems.append(
                    f"{side} measurement_composition.{field} is explicitly unknown/unavailable"
                )
                continue
            value = value.strip()

        normalized[field] = value

    if problems:
        return None, problems
    return normalized, []


def compare_measurement_composition(
    baseline: dict[str, Any],
    post: dict[str, Any],
) -> dict[str, Any]:
    """Return a fail-closed baseline/post measurement-composition classification."""
    before, before_problems = _normalize(baseline, side="baseline")
    after, after_problems = _normalize(post, side="post")
    problems = before_problems + after_problems
    if problems:
        return {
            "classification": "Unknown",
            "reasons": problems,
            "changed_fields": [],
        }

    assert before is not None and after is not None
    changed_fields = [field for field in FIELDS if before[field] != after[field]]
    if not changed_fields:
        return {
            "classification": "Comparable",
            "reasons": [
                "all decision-relevant measurement-composition fields match with explicit known evidence"
            ],
            "changed_fields": [],
        }

    hard_changes = [
        field for field in changed_fields if field in HARD_INCOMPATIBILITY_FIELDS
    ]
    if hard_changes:
        return {
            "classification": "Not Comparable",
            "reasons": [
                "measurement definition or allocation grain changed: "
                + ", ".join(hard_changes)
            ],
            "changed_fields": changed_fields,
        }

    return {
        "classification": "Directional",
        "reasons": [
            "modeled/direct split observability or lower-grain allocation coverage changed; "
            "affected conversion movement must not be promoted directly to a causal outcome"
        ],
        "changed_fields": changed_fields,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare measurement-composition evidence without executing writes"
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("post", type=Path)
    args = parser.parse_args()

    try:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        post = json.loads(args.post.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(
        json.dumps(
            compare_measurement_composition(baseline, post),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
