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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


READY_SCOPE_FIELDS = ("marketplace", "profile_scope", "entity_type")
HOLDOUT_ISOLATION_MECHANISMS = {
    "platform_randomization",
    "verified_hard_control",
    "verified_routing_partition",
    "verified_delivery_partition",
}
CONVERSION_METRIC_TOKENS = ("purchase", "sale", "roas", "conversion")


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not _non_empty_string(value):
        errors.append(f"Ready holdout requires non-empty {label}")
        return None

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        errors.append(f"Ready holdout requires valid RFC3339-style {label}")
        return None

    if parsed.tzinfo is None:
        errors.append(f"Ready holdout requires timezone-aware {label}")
        return None

    return parsed.astimezone(timezone.utc)


def _validate_ready_boundary_freshness(comparison: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    monitoring = comparison.get("boundary_monitoring")
    if not isinstance(monitoring, dict):
        return errors

    current_status = monitoring.get("current_status")
    if current_status is not None and current_status != "Clean":
        errors.append(
            "Ready holdout boundary_monitoring.current_status must be Clean when boundary monitoring is present"
        )

    material_changes = monitoring.get("material_scope_changes")
    if not isinstance(material_changes, list) or not material_changes:
        return errors

    latest_verified_at = _parse_timestamp(
        monitoring.get("latest_verified_at"),
        "comparison.boundary_monitoring.latest_verified_at",
        errors,
    )

    for index, change in enumerate(material_changes):
        if not isinstance(change, dict):
            errors.append(
                f"Ready holdout comparison.boundary_monitoring.material_scope_changes[{index}] must be an object"
            )
            continue

        if change.get("reverified") is False:
            errors.append(
                f"Ready holdout material scope change #{index + 1} is explicitly unreverified"
            )

        change_timestamp = _parse_timestamp(
            change.get("timestamp"),
            f"comparison.boundary_monitoring.material_scope_changes[{index}].timestamp",
            errors,
        )
        if latest_verified_at is not None and change_timestamp is not None:
            if change_timestamp > latest_verified_at:
                errors.append(
                    "Ready holdout boundary is stale: latest_verified_at predates a material scope change"
                )

    return errors


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

    errors.extend(_validate_ready_boundary_freshness(comparison))
    return errors


def _validate_ready_metric_semantics(primary_metric: Any) -> list[str]:
    if not isinstance(primary_metric, dict):
        return ["Ready experiment plan requires a primary_metric object"]

    name = primary_metric.get("name")
    if not _non_empty_string(name):
        return []
    if not any(token in name.lower() for token in CONVERSION_METRIC_TOKENS):
        return []

    semantics = primary_metric.get("metric_semantics")
    if not isinstance(semantics, dict):
        return ["Ready conversion primary metric requires explicit metric semantics"]

    errors: list[str] = []
    for field in ("metric_family", "attribution_family", "semantic_version"):
        if not _non_empty_string(semantics.get(field)):
            errors.append(f"Ready conversion primary metric requires non-empty metric semantics.{field}")
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

    errors.extend(_validate_ready_metric_semantics(plan.get("primary_metric")))

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
