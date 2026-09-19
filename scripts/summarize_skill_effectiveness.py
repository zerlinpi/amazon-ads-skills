#!/usr/bin/env python3
"""Summarize provider-neutral paired with-skill/without-skill benchmark trials.

The script reports measured deltas only. It does not claim statistical
significance, causal attribution, or live Amazon Ads execution safety beyond the
recorded deterministic checks.
"""

from __future__ import annotations

import json
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
        "mean_tokens": _mean_optional(trials, "tokens"),
        "mean_latency_ms": _mean_optional(trials, "latency_ms"),
    }


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
    trials = payload.get("trials")
    if not isinstance(trials, list) or not trials:
        raise ValueError("benchmark trials must be a non-empty array")

    pairs: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    measurement_status_counts = {status: 0 for status in MEASUREMENT_STATUSES}

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
        if variant not in VARIANTS:
            raise ValueError("trial.variant must be with_skill or without_skill")
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
