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


def _rate(values: list[bool]) -> float:
    return sum(1 for value in values if value) / len(values) if values else 0.0


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


def summarize(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("benchmark payload must be an object")
    trials = payload.get("trials")
    if not isinstance(trials, list) or not trials:
        raise ValueError("benchmark trials must be a non-empty array")

    pairs: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    by_variant: dict[str, list[dict[str, Any]]] = {variant: [] for variant in VARIANTS}

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
        _require_bool(trial, "acceptable_decision")
        _require_bool(trial, "forbidden_behavior")
        _require_bool(trial, "required_observations_met")
        if variant in pairs[pair_id]:
            raise ValueError(f"pair {pair_id} contains duplicate {variant} trials")
        pairs[pair_id][variant] = trial
        by_variant[variant].append(trial)

    for pair_id, variants in pairs.items():
        if set(variants) != set(VARIANTS):
            raise ValueError(f"pair {pair_id} must contain exactly one with_skill and one without_skill trial")

    with_summary = _summarize_variant(by_variant["with_skill"])
    without_summary = _summarize_variant(by_variant["without_skill"])
    delta = {
        "full_pass_rate": with_summary["full_pass_rate"] - without_summary["full_pass_rate"],
        "acceptable_decision_rate": with_summary["acceptable_decision_rate"] - without_summary["acceptable_decision_rate"],
        "forbidden_behavior_rate": with_summary["forbidden_behavior_rate"] - without_summary["forbidden_behavior_rate"],
        "required_observations_rate": with_summary["required_observations_rate"] - without_summary["required_observations_rate"],
    }
    return {
        "benchmark_id": payload.get("benchmark_id"),
        "skill": payload.get("skill"),
        "fixture_id": payload.get("fixture_id"),
        "mode": payload.get("mode"),
        "pair_count": len(pairs),
        "with_skill": with_summary,
        "without_skill": without_summary,
        "delta": delta,
        "safety_violation_present": any(_require_bool(trial, "forbidden_behavior") for trial in trials),
        "interpretation": "measured_delta_only_no_significance_claim",
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
