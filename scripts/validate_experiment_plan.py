#!/usr/bin/env python3
"""Validate semantic readiness gates for Amazon Ads experiment plans.

This validator is intentionally dependency-free and narrow. JSON Schema remains the
structural contract; this script enforces cross-field safety invariants that are hard
to express cleanly in the schema without making exploratory Shadow/Hold plans overly
strict.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any


READY_SCOPE_FIELDS = ("marketplace", "profile_scope", "entity_type")
HOLDOUT_ISOLATION_MECHANISMS = {
    "platform_randomization",
    "verified_hard_control",
    "verified_routing_partition",
    "verified_delivery_partition",
}
CONVERSION_METRIC_TOKENS = ("purchase", "roas", "conversion")
CONVERSION_METRIC_NAME_PATTERNS = (
    r"\b(?:sales?|adsales?)\b",
    r"\bacos\b",
    r"\bcvr\b",
    r"\battributed[\s_-]+(?:orders?|units?)\b",
    r"\bunits[\s_-]+sold\b",
)
AGGREGATION_SEMANTICS = {
    "additive",
    "non_additive_deduplicated",
    "ratio_or_derived",
    "unknown",
}
READY_RESOLVED_AGGREGATION_SEMANTICS = AGGREGATION_SEMANTICS - {"unknown"}


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


UNAVAILABLE_IDENTITY_LABELS = {
    "unknown", "unsupported", "partial", "missing", "unavailable",
    "not_available", "not_supported",
}


def _concrete_identity(value: Any) -> bool:
    """Reject evidence placeholders as Ready identities, not embedded ID text."""
    if not _non_empty_string(value) or value != value.strip():
        return False
    normalized = re.sub(r"[\s-]+", "_", value.casefold())
    return normalized not in UNAVAILABLE_IDENTITY_LABELS


def _is_conversion_metric(name: Any, semantics: Any) -> bool:
    # A caller-provided non-conversion family must not hide an obvious
    # conversion display name from the Ready attribution-identity gate.
    normalized_name = name.casefold().strip() if _non_empty_string(name) else ""
    # Retail/organic sales and sales rank are not ad-attributed conversion
    # metrics. Only whole, unambiguous labels are exempt: "Attributed Retail
    # Sales" and bare "Sales" remain subject to the conversion gate.
    non_attributed_retail_name = bool(re.fullmatch(
        r"(?:total[\s_-]+)?retail[\s_-]+sales|organic[\s_-]+sales|sales[\s_-]+rank",
        normalized_name,
    ))
    name_indicates_conversion = bool(
        normalized_name and not non_attributed_retail_name and (
            any(token in normalized_name for token in CONVERSION_METRIC_TOKENS)
            or any(re.search(pattern, normalized_name) for pattern in CONVERSION_METRIC_NAME_PATTERNS)
        )
    )
    family = semantics.get("metric_family") if isinstance(semantics, dict) else None
    return bool(name_indicates_conversion or (
        _non_empty_string(family) and family.strip().casefold() == "conversion"
    ))


def _parse_timestamp(value: Any, label: str, errors: list[str]) -> tuple[datetime, Decimal] | None:
    if not _non_empty_string(value):
        errors.append(f"Ready holdout requires non-empty {label}")
        return None

    normalized = value.strip()
    # datetime.fromisoformat also accepts space separators, fractional timezone
    # offsets, and -00:00. These cannot establish the repository's required
    # known-offset RFC3339 verification instant.
    match = re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.(?P<fraction>\d+))?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)",
        normalized,
    )
    if match is None or normalized.endswith("-00:00"):
        errors.append(f"Ready holdout requires valid known-offset RFC3339 {label}")
        return None
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

    # datetime truncates digits beyond microseconds. Retain the original
    # fractional second for exact UTC chronology instead of losing ordering.
    return (parsed.astimezone(timezone.utc).replace(microsecond=0),
            Decimal("0." + (match.group("fraction") or "0")))


def _validate_ready_boundary_freshness(
    comparison: dict[str, Any], verified_isolation_instants: list[tuple[int, tuple[datetime, Decimal]]]
) -> list[str]:
    errors: list[str] = []
    if "boundary_monitoring" not in comparison:
        return errors
    monitoring = comparison["boundary_monitoring"]
    if not isinstance(monitoring, dict):
        errors.append("Ready holdout comparison.boundary_monitoring must be an object when supplied")
        return errors

    # An optional monitoring record is not proof unless its claimed current
    # boundary state and latest verification instant are both resolved.
    if monitoring.get("current_status") != "Clean":
        errors.append(
            "Ready holdout boundary_monitoring.current_status must be Clean when boundary monitoring is present"
        )

    latest_verified_at = _parse_timestamp(
        monitoring.get("latest_verified_at"),
        "comparison.boundary_monitoring.latest_verified_at",
        errors,
    )
    # A later verified isolation check cannot coexist with an older claimed
    # "latest" clean boundary check. Compare actual UTC instants, not strings.
    if latest_verified_at is not None:
        for index, verified_at in verified_isolation_instants:
            if verified_at > latest_verified_at:
                errors.append(
                    f"Ready holdout boundary_monitoring.latest_verified_at predates "
                    f"verified isolation_evidence[{index}].verified_at"
                )

    if "launch_verified_at" in monitoring:
        launch_verified_at = _parse_timestamp(
            monitoring["launch_verified_at"],
            "comparison.boundary_monitoring.launch_verified_at",
            errors,
        )
        if (
            launch_verified_at is not None
            and latest_verified_at is not None
            and launch_verified_at > latest_verified_at
        ):
            errors.append(
                "Ready holdout boundary_monitoring.launch_verified_at cannot be after latest_verified_at"
            )

    material_changes = monitoring.get("material_scope_changes")
    if "material_scope_changes" in monitoring and not isinstance(material_changes, list):
        errors.append("Ready holdout comparison.boundary_monitoring.material_scope_changes must be an array when supplied")
        return errors
    if not material_changes:
        return errors

    for index, change in enumerate(material_changes):
        if not isinstance(change, dict):
            errors.append(
                f"Ready holdout comparison.boundary_monitoring.material_scope_changes[{index}] must be an object"
            )
            continue

        if change.get("reverified") is not True:
            errors.append(
                f"Ready holdout material scope change #{index + 1} is not positively reverified"
            )

        change_timestamp = _parse_timestamp(
            change.get("timestamp"),
            f"comparison.boundary_monitoring.material_scope_changes[{index}].timestamp",
            errors,
        )
        # Optional explicit re-verification is evidence, not a decoration.
        # Preserve legacy omissions, but do not accept an impossible supplied
        # instant before the change or after the claimed latest clean check.
        if "reverified_at" in change:
            reverified_at = _parse_timestamp(
                change["reverified_at"],
                f"comparison.boundary_monitoring.material_scope_changes[{index}].reverified_at",
                errors,
            )
            if reverified_at is not None and change_timestamp is not None:
                if reverified_at < change_timestamp:
                    errors.append(
                        f"Ready holdout material_scope_changes[{index}].reverified_at "
                        "cannot predate its material scope change"
                    )
            if reverified_at is not None and latest_verified_at is not None:
                if reverified_at > latest_verified_at:
                    errors.append(
                        f"Ready holdout material_scope_changes[{index}].reverified_at "
                        "cannot be after latest_verified_at"
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
    verified_isolation_instants: list[tuple[int, tuple[datetime, Decimal]]] = []
    for index, item in enumerate(isolation_evidence):
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

        if item.get("verified") is not True:
            continue

        # A positive flag cannot turn a placeholder into independent boundary
        # evidence. Optional provenance fields, when supplied, must be resolved.
        if not _concrete_identity(item.get("evidence")):
            errors.append(
                f"Ready holdout isolation_evidence[{index}].evidence must be concrete"
            )
            continue
        if "source" in item and not _concrete_identity(item.get("source")):
            errors.append(
                f"Ready holdout isolation_evidence[{index}].source must be concrete when supplied"
            )
            continue
        verified_at = None
        if "verified_at" in item:
            verified_at = _parse_timestamp(
                item.get("verified_at"),
                f"comparison.isolation_evidence[{index}].verified_at",
                errors,
            )
            if verified_at is None:
                continue

        has_verified_boundary = True
        if verified_at is not None:
            verified_isolation_instants.append((index, verified_at))

    if not has_verified_boundary:
        errors.append(
            "Ready holdout requires at least one verified isolation_evidence item with non-empty evidence"
        )

    errors.extend(_validate_ready_boundary_freshness(comparison, verified_isolation_instants))
    return errors


def _validate_conversion_identity(semantics: Any, label: str) -> list[str]:
    if not isinstance(semantics, dict):
        return [f"{label} requires explicit metric semantics"]

    errors: list[str] = []
    family = semantics.get("metric_family")
    if not (
        _non_empty_string(family)
        and family == family.strip()
        and family.casefold() == "conversion"
    ):
        errors.append(f"{label} requires metric semantics.metric_family = conversion")

    for field in ("attribution_family", "semantic_version"):
        value = semantics.get(field)
        if not _concrete_identity(value) or re.sub(
            r"[\s-]+", "_", value.casefold()
        ) == "not_applicable":
            errors.append(f"{label} requires concrete metric semantics.{field}")
    return errors


def _validate_ready_metric_semantics(primary_metric: Any) -> list[str]:
    if not isinstance(primary_metric, dict):
        return ["Ready experiment plan requires a primary_metric object"]

    name = primary_metric.get("name")
    semantics = primary_metric.get("metric_semantics")
    if not _is_conversion_metric(name, semantics):
        return []
    return _validate_conversion_identity(semantics, "Ready conversion primary metric")


def _validate_ready_guardrail_metric_semantics(guardrails: Any) -> list[str]:
    if not isinstance(guardrails, list):
        return []

    errors: list[str] = []
    for index, guardrail in enumerate(guardrails):
        if not isinstance(guardrail, dict):
            continue
        name = guardrail.get("metric")
        semantics = guardrail.get("metric_semantics")
        if _is_conversion_metric(name, semantics):
            errors.extend(_validate_conversion_identity(
                semantics, f"Ready conversion guardrail #{index + 1}"
            ))
    return errors




def _known_ratio_metric(name: Any) -> bool:
    """Bounded name contradictions for canonical KPIs and official benchmark rates.

    Names only detect obvious additive contradictions. They never authenticate
    source, attribution, compatible denominators, or actual report coverage.
    """
    if not isinstance(name, str) or not name.strip():
        return False
    label = name.casefold()
    return bool(
        re.search(
            r"(?<![a-z0-9])(?:acos|tacos|roas|cvr|ctr|cpc|cpa|cpm|vcpm|roi)(?![a-z0-9])",
            label,
        )
        or re.search(
            r"(?<![a-z0-9])(?:purchase|add[\s_-]+to[\s_-]+cart|detail[\s_-]+page[\s_-]+view|branded[\s_-]+search)[\s_-]+rate\b",
            label,
        )
        or re.search(
            r"(?<![a-z0-9])cost[\s_-]+per[\s_-]+(?:purchase|detail[\s_-]+page[\s_-]+view)\b",
            label,
        )
        or re.search(
            r"(?<![a-z0-9])percent[\s_-]+of[\s_-]+purchases[\s_-]+new[\s_-]+to[\s_-]+brand\b",
            label,
        )
    )

def _unresolved_combined_metric_name(name: Any) -> bool:
    """A Ready combined readout needs a concrete metric identity, not a label placeholder."""
    if not _concrete_identity(name):
        return True
    normalized = re.sub(r"[\s_-]+", " ", name.casefold())
    return normalized in {"not applicable", "n/a"}


def _validate_ready_combined_readout_semantics(
    primary_metric: Any,
    guardrails: Any,
    comparison: Any,
) -> list[str]:
    if not isinstance(comparison, dict):
        return []
    if ("requires_combined_readout" in comparison
            and type(comparison["requires_combined_readout"]) is not bool):
        return ["Ready comparison.requires_combined_readout must be boolean when supplied"]
    if comparison.get("requires_combined_readout") is not True:
        return []

    errors: list[str] = []

    if not isinstance(primary_metric, dict):
        errors.append("Ready combined readout requires a primary_metric object")
    else:
        if _unresolved_combined_metric_name(primary_metric.get("name")):
            errors.append("Ready combined readout primary metric requires concrete metric identity")
        semantics = primary_metric.get("metric_semantics")
        aggregation = semantics.get("aggregation_semantics") if isinstance(semantics, dict) else None
        if aggregation not in READY_RESOLVED_AGGREGATION_SEMANTICS:
            errors.append(
                "Ready combined readout primary metric requires explicit metric semantics.aggregation_semantics"
            )
        elif _known_ratio_metric(primary_metric.get("name")) and aggregation != "ratio_or_derived":
            errors.append(
                "Ready combined readout ratio primary metric requires metric semantics.aggregation_semantics = ratio_or_derived"
            )

    if isinstance(guardrails, list):
        for index, guardrail in enumerate(guardrails):
            if not isinstance(guardrail, dict):
                continue
            if _unresolved_combined_metric_name(guardrail.get("metric")):
                errors.append(
                    f"Ready combined readout guardrail #{index + 1} requires concrete metric identity"
                )
            semantics = guardrail.get("metric_semantics")
            aggregation = semantics.get("aggregation_semantics") if isinstance(semantics, dict) else None
            if aggregation not in READY_RESOLVED_AGGREGATION_SEMANTICS:
                errors.append(
                    f"Ready combined readout guardrail #{index + 1} requires explicit metric semantics.aggregation_semantics"
                )
            elif _known_ratio_metric(guardrail.get("metric")) and aggregation != "ratio_or_derived":
                errors.append(
                    f"Ready combined readout ratio guardrail #{index + 1} requires metric semantics.aggregation_semantics = ratio_or_derived"
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
        if not _concrete_identity(scope.get(field)):
            errors.append(f"Ready experiment plan requires concrete scope.{field} identity")

    entity_ids = scope.get("entity_ids")
    if not isinstance(entity_ids, list) or not entity_ids:
        errors.append("Ready experiment plan requires non-empty scope.entity_ids")
    elif any(not _concrete_identity(entity_id) for entity_id in entity_ids):
        errors.append("Ready experiment plan scope.entity_ids must contain only concrete identities")
    elif len(entity_ids) != len(set(entity_ids)):
        errors.append("Ready experiment plan scope.entity_ids contains duplicate identities")

    comparison = plan.get("comparison")
    if isinstance(comparison, dict) and "control_entity_ids" in comparison:
        control_ids = comparison["control_entity_ids"]
        if not isinstance(control_ids, list) or any(not _concrete_identity(value) for value in control_ids):
            errors.append("Ready experiment plan comparison.control_entity_ids must contain only concrete identities")
        elif len(control_ids) != len(set(control_ids)):
            errors.append("Ready experiment plan comparison.control_entity_ids contains duplicate identities")
        elif isinstance(entity_ids, list) and all(_concrete_identity(value) for value in entity_ids):
            if set(entity_ids) & set(control_ids):
                errors.append("Ready experiment plan comparison.control_entity_ids overlaps treatment scope.entity_ids")

    errors.extend(_validate_ready_metric_semantics(plan.get("primary_metric")))
    errors.extend(_validate_ready_guardrail_metric_semantics(plan.get("guardrails")))

    comparison = plan.get("comparison")
    errors.extend(
        _validate_ready_combined_readout_semantics(
            plan.get("primary_metric"),
            plan.get("guardrails"),
            comparison,
        )
    )
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
