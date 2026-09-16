#!/usr/bin/env python3
"""Validate semantic readiness gates for Amazon Ads experiment plans.

This validator is intentionally dependency-free and narrow. JSON Schema remains the
structural contract; this script enforces cross-field safety invariants that are hard
to express cleanly in the schema without making exploratory Shadow/Hold plans overly
strict.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


READY_SCOPE_FIELDS = ("marketplace", "profile_scope", "entity_type")
HOLDOUT_ISOLATION_MECHANISMS = {
    "platform_randomization",
    "verified_hard_control",
    "verified_routing_partition",
    "verified_delivery_partition",
}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_ready_holdout(comparison: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if comparison.get("control_integrity") != "Clean":
        errors.append("Ready holdout requires comparison.control_integrity = Clean")

    isolation_evidence = comparison.get("isolation_evidence")
    if not isinstance(isolation_evidence, list) or not isolation_evidence:
        errors.append("Ready holdout requires non-empty comparison.isolation_evidence")
        return errors

    has_verified_boundary = False
    for item in isolation_evidence:
        if not isinstance(item, dict):
            continue

        mechanism = item.get("mechanism")
        if mechanism == "optimization_signal":
            errors.append(
                "optimization_signal is not a holdout isolation mechanism; provide a separate verified boundary"
            )
            continue

        if mechanism not in HOLDOUT_ISOLATION_MECHANISMS:
            errors.append(f"unsupported holdout isolation mechanism: {mechanism!r}")
            continue

        if item.get("verified") is True and _non_empty_string(item.get("evidence")):
            has_verified_boundary = True

    if not has_verified_boundary:
        errors.append(
            "Ready holdout requires at least one verified isolation_evidence item with non-empty evidence"
        )

    return errors


def validate_experiment_plan(plan: Any) -> list[str]:
    """Return semantic readiness errors for one experiment plan.

    Only `status = Ready` activates collision-safe identity requirements and, for a
    holdout design, explicit verified isolation requirements. Plans that are still
    `Shadow Only`, `Redesign`, or `Hold` may preserve unresolved scope/boundaries so
    agents can continue analysis without inventing identity or control evidence.
    """

    if not isinstance(plan, dict):
        return ["experiment plan must be a JSON object"]

    if plan.get("status") != "Ready":
        return []

    scope = plan.get("scope")
    if not isinstance(scope, dict):
        return ["Ready experiment plan requires a scope object"]

    errors: list[str] = []
    for field in READY_SCOPE_FIELDS:
        if not _non_empty_string(scope.get(field)):
            errors.append(f"Ready experiment plan requires non-empty scope.{field}")

    entity_ids = scope.get("entity_ids")
    if not isinstance(entity_ids, list) or not entity_ids:
        errors.append("Ready experiment plan requires non-empty scope.entity_ids")
    elif any(not _non_empty_string(entity_id) for entity_id in entity_ids):
        errors.append("Ready experiment plan scope.entity_ids must contain only non-empty strings")

    comparison = plan.get("comparison")
    if isinstance(comparison, dict) and comparison.get("design_type") == "holdout":
        errors.extend(_validate_ready_holdout(comparison))

    return errors


def _load_plan(path_arg: str) -> Any:
    if path_arg == "-":
        source = sys.stdin
        label = "stdin"
    else:
        path = Path(path_arg)
        source = path.open("r", encoding="utf-8")
        label = str(path)

    try:
        with source if path_arg != "-" else _nullcontext(source):
            return json.load(source)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} must contain valid JSON") from exc


class _nullcontext:
    """Tiny local context manager to avoid closing stdin."""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __enter__(self) -> Any:
        return self.value

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        return False


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: validate_experiment_plan.py <plan.json|->", file=sys.stderr)
        return 2

    try:
        plan = _load_plan(args[0])
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errors = validate_experiment_plan(plan)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2

    print("Experiment plan semantic readiness valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
