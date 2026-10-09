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
STREAM_EVIDENCE_STATES = {"Verified", "Partial", "Unknown", "Unsupported"}


def _stream_generation(payload: dict[str, Any]) -> str:
    """Classify declared Stream provenance; ambiguous versions fail closed.

    A generation without a channel cannot establish the data source.
    Explicit source/generation conflicts must never bypass v2 reconciliation.
    """
    channel = payload.get("acquisition_channel")
    generation = payload.get("stream_generation")
    has_stream_evidence = (
        generation is not None
        or payload.get("stream_record_reconciliation") is not None
        or payload.get("stream_dataset") is not None
    )
    if channel is None:
        return "unknown" if has_stream_evidence else "not_stream"
    if not isinstance(channel, str) or not channel.strip():
        return "unknown"
    if generation is not None and not isinstance(generation, str):
        return "unknown"

    normalized = "_".join(
        channel.strip().lower().replace("-", " ").replace("_", " ").split()
    )
    explicit = {
        "amazon_marketing_stream_v1": "v1",
        "amazon_marketing_stream_v2": "v2",
    }.get(normalized)
    if explicit is not None:
        if explicit == "v1" and payload.get("stream_record_reconciliation") is not None:
            return "unknown"
        return explicit if generation is None or generation == explicit else "unknown"
    if normalized == "amazon_marketing_stream":
        return generation if generation in {"v1", "v2"} else "unknown"
    if (
        "marketing_stream" in normalized
        or normalized.startswith("amazonmarketingstream")
        or has_stream_evidence
    ):
        return "unknown"
    return "not_stream"


def _stream_reconciliation_status(payload: dict[str, Any]) -> str:
    """Require highest-version record evidence for resolved Stream v2 sources."""
    generation = _stream_generation(payload)
    if generation in {"not_stream", "v1"}:
        return "Not Applicable"
    if generation != "v2":
        return "Unknown"
    evidence = payload.get("stream_record_reconciliation")
    if evidence is None:
        return "Unknown"
    if not isinstance(evidence, dict):
        raise ValueError("stream_record_reconciliation must be an object or null")
    for field in ("record_identity_coverage", "highest_version_per_record"):
        state = evidence.get(field, "Unknown")
        if not isinstance(state, str) or state not in STREAM_EVIDENCE_STATES:
            raise ValueError(
                f"stream_record_reconciliation.{field} must be one of "
                f"{sorted(STREAM_EVIDENCE_STATES)}"
            )
        if state != "Verified":
            return "Unknown"
    return "Verified"


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
    stream_reconciliation_status = _stream_reconciliation_status(payload)
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
    elif stream_reconciliation_status == "Unknown":
        status = "Unknown"
        reason = (
            "Amazon Marketing Stream v2 delivers total values per time window; "
            "direct summation requires source-supported complete record keys and "
            "highest streamBatch.version selected per record before reducing grain"
        )
        recommended_path = (
            "reconcile Stream v2 total records by full dataset record identity and "
            "highest version; preserve unknown or partial evidence rather than summing"
        )
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
        "stream_reconciliation_status": stream_reconciliation_status,
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
