#!/usr/bin/env python3
"""Project bounded measurement-lineage state from optimization events.

Read-only, dependency-free reducer. The append-first optimization event ledger
remains authoritative; this script only builds a retrieval summary.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any

SCOPE_FIELDS = ("marketplace", "profile_scope", "entity_type", "entity_id")
HISTORY_STATUSES = {
    "available",
    "partially_available",
    "unavailable",
    "retired_or_deleted",
    "unknown",
}
COMPARABILITY_STATUSES = {
    "Comparable",
    "Reconcilable",
    "Directional",
    "Not Comparable",
    "Unknown",
}


def _parse_timestamp(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty RFC3339 date-time string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid RFC3339 date-time string") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a timezone offset")
    return parsed


def _normalize_expected_scope(value: Any) -> tuple[str, str, str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("expected_scope must be an object or null")
    result: list[str] = []
    for field in SCOPE_FIELDS:
        item = value.get(field)
        if not isinstance(item, str) or not item:
            raise ValueError(f"expected_scope.{field} must be a non-empty string")
        result.append(item)
    return tuple(result)  # type: ignore[return-value]


def _event_scope(event: dict[str, Any]) -> tuple[Any, Any, Any, Any] | None:
    entity = event.get("entity")
    if not isinstance(entity, dict):
        return None
    return (
        event.get("marketplace"),
        event.get("profile_scope"),
        entity.get("type"),
        entity.get("id"),
    )


def _validate_scope(event: dict[str, Any], expected: tuple[str, str, str, str] | None) -> None:
    if expected is None:
        return
    actual = _event_scope(event)
    if actual is None or any(not isinstance(item, str) or not item for item in actual):
        raise ValueError("measurement event scope is incomplete for expected_scope")
    if actual != expected:
        raise ValueError("measurement event scope does not match expected_scope")


def _warnings(snapshot: dict[str, Any], history_status: str, comparability: str) -> list[str]:
    warnings = list(snapshot.get("warnings") or [])
    for field in ("reporting_generation", "date_attribution_semantics"):
        if not snapshot.get(field):
            warnings.append(f"missing {field}; measurement identity is incomplete")
    if history_status in {"unavailable", "retired_or_deleted", "unknown"}:
        warnings.append(
            f"historical_availability_status={history_status}; missing history is an availability state, not a metric observation"
        )
    if comparability in {"Not Comparable", "Unknown"}:
        warnings.append(
            f"comparability_status={comparability}; historical outcome must not be promoted to current action-safe evidence"
        )
    return warnings


def _project(snapshot: dict[str, Any], observed_at: str) -> dict[str, Any]:
    history_status = snapshot.get("historical_availability_status")
    if history_status not in HISTORY_STATUSES:
        history_status = "unknown"
    comparability = snapshot.get("comparability_status")
    if comparability not in COMPARABILITY_STATUSES:
        comparability = "Unknown"
    return {
        "evidence_snapshot_id": snapshot.get("snapshot_id"),
        "observed_at": observed_at,
        "source_system": snapshot.get("source_system"),
        "source_dataset": snapshot.get("source_dataset"),
        "acquisition_channel": snapshot.get("acquisition_channel"),
        "reporting_generation": snapshot.get("reporting_generation"),
        "semantic_version": snapshot.get("semantic_version"),
        "date_attribution_semantics": snapshot.get("date_attribution_semantics"),
        "historical_availability_status": history_status,
        "comparability_status": comparability,
        "warnings": _warnings(snapshot, history_status, comparability),
    }


def project_measurement_history(
    events: list[dict[str, Any]], *, expected_scope: dict[str, Any] | None = None
) -> dict[str, Any]:
    expected = _normalize_expected_scope(expected_scope)
    candidates: list[tuple[datetime, int, str, dict[str, Any]]] = []
    observed_scope: tuple[Any, Any, Any, Any] | None = None

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("each event must be an object")
        snapshot = event.get("evidence_snapshot")
        if snapshot is None:
            continue
        if not isinstance(snapshot, dict):
            raise ValueError("evidence_snapshot must be an object or null")
        _validate_scope(event, expected)
        scope = _event_scope(event)
        if expected is None and scope is not None and all(isinstance(item, str) and item for item in scope):
            if observed_scope is None:
                observed_scope = scope
            elif scope != observed_scope:
                raise ValueError("measurement projection requires a single entity scope")
        raw_time = snapshot.get("captured_at") or event.get("timestamp")
        parsed = _parse_timestamp(raw_time, field="measurement observation time")
        candidates.append((parsed, index, raw_time, snapshot))

    if not candidates:
        return {"latest_measurement_state": None}

    candidates.sort(key=lambda item: (item[0], item[1]))
    _, _, observed_at, snapshot = candidates[-1]
    return {"latest_measurement_state": _project(snapshot, observed_at)}


def _load_payload() -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError("stdin must contain valid JSON") from exc
    if isinstance(payload, list):
        return payload, None
    if not isinstance(payload, dict) or not isinstance(payload.get("events"), list):
        raise ValueError("input must be an event array or an object with an events array")
    expected_scope = payload.get("expected_scope")
    if expected_scope is not None and not isinstance(expected_scope, dict):
        raise ValueError("expected_scope must be an object or null")
    return payload["events"], expected_scope


def main() -> int:
    try:
        events, expected_scope = _load_payload()
        result = project_measurement_history(events, expected_scope=expected_scope)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
