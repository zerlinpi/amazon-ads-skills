#!/usr/bin/env python3
"""Summarize provider-neutral paired with-skill/without-skill benchmark trials.

The script reports measured deltas only. It does not claim statistical
significance, causal attribution, or live Amazon Ads execution safety beyond the
recorded deterministic checks.
"""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from statistics import mean
from typing import Any

VARIANTS = ("with_skill", "without_skill")
MEASUREMENT_STATUSES = (
    "measured",
    "insufficient_evidence",
    "scorer_error",
    "harness_error",
)
DECISION_FIELDS = (
    "acceptable_decision",
    "forbidden_behavior",
    "required_observations_met",
)


def _measurement_status(trial: dict[str, Any]) -> str:
    status = trial.get("measurement_status", "measured")
    if status not in MEASUREMENT_STATUSES:
        raise ValueError(
            "trial.measurement_status must be measured, insufficient_evidence, scorer_error, or harness_error"
        )
    return status


def _validate_measurement(trial: dict[str, Any]) -> str:
    status = _measurement_status(trial)
    if status == "measured":
        for field in DECISION_FIELDS:
            _require_bool(trial, field)
        return status

    for field in DECISION_FIELDS:
        if field not in trial:
            raise ValueError(f"non-measured trial must preserve explicit null trial.{field}")
        if trial.get(field) is not None:
            raise ValueError(
                f"non-measured trial.{field} must be null rather than an invented pass/fail value"
            )
    return status



def _require_bool(trial: dict[str, Any], field: str) -> bool:
    value = trial.get(field)
    if not isinstance(value, bool):
        raise ValueError(f"trial.{field} must be boolean")
    return value


def _full_pass(trial: dict[str, Any]) -> bool:
    return (
        _require_bool(trial, "acceptable_decision")
        and not _require_bool(trial, "forbidden_behavior")
        and _require_bool(trial, "required_observations_met")
    )


def _rate(values: list[bool]) -> float | None:
    return sum(1 for value in values if value) / len(values) if values else None


def _validate_resource_metrics(trial: dict[str, Any]) -> None:
    """Keep optional resource measurements faithful to the benchmark schema.

    Missing/null means unmeasured, never zero. A present value must not be
    silently omitted from a mean or serialized as non-standard NaN/Infinity.
    """
    tokens = trial.get("tokens")
    if tokens is not None and (type(tokens) is not int or tokens < 0):
        raise ValueError("trial.tokens must be a non-negative integer or null")

    latency = trial.get("latency_ms")
    if latency is not None:
        try:
            valid = (
                isinstance(latency, (int, float))
                and not isinstance(latency, bool)
                and latency >= 0
                and math.isfinite(latency)
            )
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError("trial.latency_ms must be a finite non-negative number or null")


def _validate_trigger_measurement(trial: dict[str, Any]) -> None:
    """Reject supplied non-boolean trigger telemetry without inventing zeros."""
    triggered = trial.get("triggered")
    if triggered is not None and not isinstance(triggered, bool):
        raise ValueError("trial.triggered must be boolean or null")


def _mean_optional(trials: list[dict[str, Any]], field: str) -> float | None:
    values = [trial.get(field) for trial in trials if isinstance(trial.get(field), (int, float)) and not isinstance(trial.get(field), bool)]
    return mean(values) if values else None


def _summarize_variant(trials: list[dict[str, Any]]) -> dict[str, Any]:
    full_pass = [_full_pass(trial) for trial in trials]
    acceptable = [_require_bool(trial, "acceptable_decision") for trial in trials]
    forbidden = [_require_bool(trial, "forbidden_behavior") for trial in trials]
    observations = [_require_bool(trial, "required_observations_met") for trial in trials]
    trigger_values = [trial.get("triggered") for trial in trials if isinstance(trial.get("triggered"), bool)]
    return {
        "trial_count": len(trials),
        "full_pass_count": sum(full_pass),
        "full_pass_rate": _rate(full_pass),
        "acceptable_decision_rate": _rate(acceptable),
        "forbidden_behavior_rate": _rate(forbidden),
        "required_observations_rate": _rate(observations),
        "trigger_rate": _rate(trigger_values) if trigger_values else None,
        "trigger_observed_count": len(trigger_values),
        "trigger_observation_coverage": (
            len(trigger_values) / len(trials) if trials else 0.0
        ),
        "trigger_observation_status": (
            "complete"
            if len(trigger_values) == len(trials)
            else "partial"
            if trigger_values
            else "unmeasured"
        ),
        "mean_tokens": _mean_optional(trials, "tokens"),
        "mean_latency_ms": _mean_optional(trials, "latency_ms"),
    }



# Keep single-run summaries from claiming measured evidence with unresolved
# identity. The longitudinal comparator independently treats these labels as
# Unknown; repeating a placeholder is not a verified model/fixture identity.
UNRESOLVED_IDENTITIES = {
    "unknown", "partial", "missing", "unsupported", "unavailable",
    "not available", "not supported", "not applicable", "n/a",
}
VALID_MODES = {"Discovery", "Forced invocation", "Negative control", "Ablation"}


def _require_concrete_identity(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{field} must be a concrete unpadded string")
    normalized = " ".join(value.casefold().replace("_", " ").replace("-", " ").split())
    if normalized in UNRESOLVED_IDENTITIES:
        raise ValueError(f"{field} must not be an unresolved identity placeholder")
    return value


def _validate_measurement_identity(payload: dict[str, Any]) -> None:
    for field in ("benchmark_id", "skill", "fixture_id", "fixture_version"):
        _require_concrete_identity(payload.get(field), field)
    mode = payload.get("mode")
    if not isinstance(mode, str) or mode not in VALID_MODES:
        raise ValueError("mode must be a supported Skill-effectiveness evaluation mode")

    harness = payload.get("harness")
    if not isinstance(harness, dict):
        raise ValueError("harness must be an object")
    for field in ("runtime", "model", "model_version"):
        _require_concrete_identity(harness.get(field), f"harness.{field}")
    # Optional hashes can be omitted or explicitly null. A supplied non-null
    # identity must be concrete; null is unmeasured, never a fabricated hash.
    for field in ("config_hash", "tool_profile_hash", "evidence_hash"):
        if harness.get(field) is not None:
            _require_concrete_identity(harness[field], f"harness.{field}")

    contract = harness.get("measurement_contract")
    if not isinstance(contract, dict):
        raise ValueError("harness.measurement_contract must be an object")
    for field in ("evaluator_id", "evaluator_version"):
        _require_concrete_identity(
            contract.get(field), f"harness.measurement_contract.{field}"
        )
    if "rubric_version" not in contract:
        raise ValueError(
            "harness.measurement_contract.rubric_version must be explicit; use null when no semantic rubric is used"
        )
    if contract["rubric_version"] is not None:
        _require_concrete_identity(
            contract["rubric_version"], "harness.measurement_contract.rubric_version"
        )


def _measurement_identity(payload: dict[str, Any]) -> dict[str, Any]:
    harness = payload.get("harness")
    if not isinstance(harness, dict):
        harness = {}
    contract = harness.get("measurement_contract")
    if not isinstance(contract, dict):
        contract = {}
    return {
        "fixture_id": payload.get("fixture_id"),
        "fixture_version": payload.get("fixture_version"),
        "mode": payload.get("mode"),
        "runtime": harness.get("runtime"),
        "model": harness.get("model"),
        "model_version": harness.get("model_version"),
        "config_hash": harness.get("config_hash"),
        "tool_profile_hash": harness.get("tool_profile_hash"),
        "evidence_hash": harness.get("evidence_hash"),
        "evaluator_id": contract.get("evaluator_id"),
        "evaluator_version": contract.get("evaluator_version"),
        "rubric_version": contract.get("rubric_version"),
    }


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("benchmark payload must be an object")
    _validate_measurement_identity(payload)
    trials = payload.get("trials")
    if not isinstance(trials, list) or not trials:
        raise ValueError("benchmark trials must be a non-empty array")

    pairs: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    measurement_status_counts = {status: 0 for status in MEASUREMENT_STATUSES}
    seen_trial_ids: set[str] = set()

    for trial in trials:
        if not isinstance(trial, dict):
            raise ValueError("each benchmark trial must be an object")
        pair_id = trial.get("pair_id")
        trial_id = trial.get("trial_id")
        variant = trial.get("variant")
        if not isinstance(pair_id, str) or not pair_id:
            raise ValueError("each trial must have a non-empty pair_id")
        if not isinstance(trial_id, str) or not trial_id:
            raise ValueError("each trial must have a non-empty trial_id")
        # One execution cannot contribute multiple independent observations,
        # even when another pair/variant later excludes its measured result.
        if trial_id in seen_trial_ids:
            raise ValueError(f"duplicate trial_id across benchmark trials: {trial_id}")
        seen_trial_ids.add(trial_id)
        if variant not in VARIANTS:
            raise ValueError("trial.variant must be with_skill or without_skill")
        _validate_resource_metrics(trial)
        _validate_trigger_measurement(trial)
        status = _validate_measurement(trial)
        measurement_status_counts[status] += 1
        if variant in pairs[pair_id]:
            raise ValueError(f"pair {pair_id} contains duplicate {variant} trials")
        pairs[pair_id][variant] = trial

    for pair_id, variants in pairs.items():
        if set(variants) != set(VARIANTS):
            raise ValueError(f"pair {pair_id} must contain exactly one with_skill and one without_skill trial")

    comparable_pairs = {
        pair_id: variants
        for pair_id, variants in pairs.items()
        if all(_measurement_status(variants[variant]) == "measured" for variant in VARIANTS)
    }
    by_variant: dict[str, list[dict[str, Any]]] = {
        variant: [variants[variant] for variants in comparable_pairs.values()]
        for variant in VARIANTS
    }

    with_summary = _summarize_variant(by_variant["with_skill"])
    without_summary = _summarize_variant(by_variant["without_skill"])

    def paired_delta(field: str) -> float | None:
        left = with_summary[field]
        right = without_summary[field]
        if left is None or right is None:
            return None
        return left - right

    delta = {
        "full_pass_rate": paired_delta("full_pass_rate"),
        "acceptable_decision_rate": paired_delta("acceptable_decision_rate"),
        "forbidden_behavior_rate": paired_delta("forbidden_behavior_rate"),
        "required_observations_rate": paired_delta("required_observations_rate"),
    }
    return {
        "benchmark_id": payload.get("benchmark_id"),
        "skill": payload.get("skill"),
        "fixture_id": payload.get("fixture_id"),
        "mode": payload.get("mode"),
        "measurement_identity": _measurement_identity(payload),
        "pair_count": len(pairs),
        "comparable_pair_count": len(comparable_pairs),
        "excluded_pair_count": len(pairs) - len(comparable_pairs),
        "measurement_status_counts": measurement_status_counts,
        "effectiveness_status": "Measured" if comparable_pairs else "Insufficient Evidence",
        "with_skill": with_summary,
        "without_skill": without_summary,
        "delta": delta,
        "safety_violation_present": any(
            _measurement_status(trial) == "measured"
            and _require_bool(trial, "forbidden_behavior")
            for trial in trials
        ),
        "interpretation": (
            "measured_delta_only_no_significance_claim"
            if comparable_pairs
            else "insufficient_evidence_no_zero_imputation"
        ),
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = summarize(payload)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
