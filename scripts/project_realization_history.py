#!/usr/bin/env python3
"""Project canonical realized-ad history views from optimization events.

This reducer is intentionally read-only and dependency-free. It projects only the
realization-related derived views; the append-first optimization event ledger
remains the source of truth.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any


MATERIAL_DIMENSIONS = (
    ("realized_surfaces", "surface"),
    ("realized_product_ids", "product"),
    ("realized_creative_or_message_ids", "creative_or_message"),
)
BOUNDED_COVERAGE = {"Complete", "Partial"}
OBSERVABILITY_STATUSES = {"Complete", "Partial", "Unavailable", "Unknown"}


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


def _observation_time(event: dict[str, Any], snapshot: dict[str, Any]) -> tuple[datetime, str]:
    value = snapshot.get("captured_at") or event.get("timestamp")
    return _parse_timestamp(value, field="realization observation time"), value


def _material_dimensions(snapshot: dict[str, Any]) -> list[str]:
    dimensions: list[str] = []
    for field, label in MATERIAL_DIMENSIONS:
        if field in snapshot and isinstance(snapshot[field], list):
            dimensions.append(label)
    return dimensions


def _has_bounded_identity(snapshot: dict[str, Any]) -> bool:
    if snapshot.get("coverage_status") not in BOUNDED_COVERAGE:
        return False
    if _material_dimensions(snapshot):
        return True
    identity_hash = snapshot.get("identity_hash")
    return isinstance(identity_hash, str) and bool(identity_hash)


def _event_scope(event: dict[str, Any]) -> tuple[Any, Any, Any, Any] | None:
    entity = event.get("entity")
    if not isinstance(entity, dict):
        return None
    entity_type = entity.get("type")
    entity_id = entity.get("id")
    if not isinstance(entity_type, str) or not entity_type:
        return None
    if not isinstance(entity_id, str) or not entity_id:
        return None
    return (
        event.get("marketplace"),
        event.get("profile_scope"),
        entity_type,
        entity_id,
    )


def _project_last_observed(snapshot: dict[str, Any], observed_at: str) -> dict[str, Any]:
    projected: dict[str, Any] = {
        "snapshot_id": snapshot.get("snapshot_id"),
        "observed_at": observed_at,
        "realization_mode": snapshot.get("realization_mode", "unknown"),
        "coverage_status": snapshot.get("coverage_status"),
        "comparability_status": snapshot.get("comparability_status", "Unknown"),
        "freshness_status": "Unknown",
        "freshness_basis": "Requires decision-horizon evaluation; projector does not invent a repository-wide age threshold.",
        "identity_hash": snapshot.get("identity_hash"),
        "warnings": list(snapshot.get("warnings") or []),
    }
    for field, _ in MATERIAL_DIMENSIONS:
        if field in snapshot and isinstance(snapshot[field], list):
            projected[field] = list(snapshot[field])
    return projected


def _project_observability(snapshot: dict[str, Any], checked_at: str) -> dict[str, Any]:
    status = snapshot.get("coverage_status")
    if status not in OBSERVABILITY_STATUSES:
        status = "Unknown"
    return {
        "checked_at": checked_at,
        "status": status,
        "source_dataset": snapshot.get("source_dataset"),
        "acquisition_channel": snapshot.get("acquisition_channel"),
        "material_dimensions": _material_dimensions(snapshot),
        "warnings": list(snapshot.get("warnings") or []),
    }


def project_realization_history(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Return canonical realization projections for a single-entity event slice.

    Event order is not trusted. Observation time uses realization_snapshot.captured_at
    when present and otherwise falls back to the event timestamp. Equal timestamps are
    resolved by later input position, matching append-order semantics without turning
    list order into the primary clock.

    When valid optimization-event entity scopes are present, mixed scopes fail closed
    rather than silently merging realization histories across entities/accounts.
    """

    observations: list[tuple[datetime, int, str, dict[str, Any]]] = []
    observed_scopes: set[tuple[Any, Any, Any, Any]] = set()

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("each event must be an object")
        snapshot = event.get("realization_snapshot")
        if snapshot is None:
            continue
        if not isinstance(snapshot, dict):
            raise ValueError("realization_snapshot must be an object or null")

        scope = _event_scope(event)
        if scope is not None:
            observed_scopes.add(scope)
            if len(observed_scopes) > 1:
                raise ValueError("realization projection requires a single entity scope")

        parsed_time, raw_time = _observation_time(event, snapshot)
        observations.append((parsed_time, index, raw_time, snapshot))

    if not observations:
        return {
            "last_observed_realization": None,
            "current_realization_observability": None,
        }

    observations.sort(key=lambda item: (item[0], item[1]))
    _, _, newest_time, newest_snapshot = observations[-1]

    last_observed = None
    for _, _, observed_at, snapshot in reversed(observations):
        if _has_bounded_identity(snapshot):
            last_observed = _project_last_observed(snapshot, observed_at)
            break

    return {
        "last_observed_realization": last_observed,
        "current_realization_observability": _project_observability(newest_snapshot, newest_time),
    }


def _load_payload() -> list[dict[str, Any]]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError("stdin must contain valid JSON") from exc

    if isinstance(payload, list):
        events = payload
    elif isinstance(payload, dict):
        events = payload.get("events")
    else:
        events = None

    if not isinstance(events, list):
        raise ValueError("input must be an event array or an object with an events array")
    return events


def main() -> int:
    try:
        projected = project_realization_history(_load_payload())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json.dump(projected, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
