#!/usr/bin/env python3
"""Evaluate whether direct summation is safe for a metric identity.

This helper is deliberately narrow and read-only. It does not aggregate values,
query Amazon Ads, or replace source/grain/completeness checks.
"""

from __future__ import annotations

import json
import sys
from typing import Any

AGGREGATION_SEMANTICS = {
    "additive",
    "non_additive_deduplicated",
    "ratio_or_derived",
    "unknown",
}
SOURCE_RELATIONS = {"disjoint", "overlapping", "unknown"}


def _semantics(payload: dict[str, Any]) -> str:
    value = payload.get("metric_semantics")
    if value is None:
        return "unknown"
    if not isinstance(value, dict):
        raise ValueError("metric_semantics must be an object or null")
    semantic = value.get("aggregation_semantics")
    if semantic is None:
        return "unknown"
    if not isinstance(semantic, str) or semantic not in AGGREGATION_SEMANTICS:
        raise ValueError(
            "metric_semantics.aggregation_semantics must be one of "
            f"{sorted(AGGREGATION_SEMANTICS)} or null"
        )
    return semantic


def evaluate_metric_aggregation_gate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")

    operation = payload.get("operation", "sum")
    if operation != "sum":
        raise ValueError("operation must be 'sum'")

    relation = payload.get("source_relation", "unknown")
    if not isinstance(relation, str) or relation not in SOURCE_RELATIONS:
        raise ValueError(
            f"source_relation must be one of {sorted(SOURCE_RELATIONS)}"
        )

    semantic = _semantics(payload)
    status = "Unknown"
    allowed = False
    reason = ""
    recommended_path = "resolve metric aggregation semantics and row relation"

    if semantic == "non_additive_deduplicated":
        status = "Blocked"
        reason = (
            "de-duplicated/non-additive metrics are not direct-sum safe; "
            "use a source-provided aggregate for the required scope"
        )
        recommended_path = "request the source-provided de-duplicated aggregate"
    elif semantic == "ratio_or_derived":
        status = "Blocked"
        reason = (
            "ratio/derived metrics are not direct-sum safe; "
            "recompute from compatible base components when defined"
        )
        recommended_path = "recompute from compatible base metrics"
    elif semantic == "unknown":
        status = "Unknown"
        reason = "aggregation semantics are unknown and must not default to additive"
    elif relation == "overlapping":
        status = "Blocked"
        reason = "source rows overlap and cannot be treated as independent additive pools"
        recommended_path = "choose one canonical non-overlapping grain"
    elif relation == "unknown":
        status = "Unknown"
        reason = "row overlap/disjointness is unknown"
    else:
        status = "Allowed"
        allowed = True
        reason = "metric is explicitly additive and source rows are explicitly disjoint"
        recommended_path = "direct sum permitted subject to ordinary lineage/completeness checks"

    return {
        "aggregation_status": status,
        "direct_sum_allowed": allowed,
        "operation": operation,
        "aggregation_semantics": semantic,
        "source_relation": relation,
        "missing_semantics_policy": "never_assume_additive",
        "reason": reason,
        "recommended_path": recommended_path,
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = evaluate_metric_aggregation_gate(payload)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
