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
SCOPE_FIELDS = ("marketplace", "profile_scope", "entity_type", "entity_id")
ACCOUNT_IDENTITY_FIELDS = (
    "manager_account_id",
    "global_advertiser_account_id",
    "regional_advertiser_account_id",
    "legacy_advertiser_account_id",
    "advertiser_account_id",
    "regional_profile_id",
    "country_code",
)
STRONG_ACCOUNT_IDENTITY_FIELDS = (
    "global_advertiser_account_id",
    "regional_advertiser_account_id",
    "legacy_advertiser_account_id",
    "advertiser_account_id",
    "regional_profile_id",
)


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


def _normalize_expected_scope(value: Any) -> tuple[str, str, str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("expected_scope must be an object or null")
    normalized: list[str] = []
    for field in SCOPE_FIELDS:
        item = value.get(field)
        if not isinstance(item, str) or not item:
            raise ValueError(f"expected_scope.{field} must be a non-empty string")
        normalized.append(item)
    return tuple(normalized)  # type: ignore[return-value]


def _validate_scope(
    event_scope: tuple[Any, Any, Any, Any] | None,
    expected_scope: tuple[str, str, str, str] | None,
) -> tuple[Any, Any, Any, Any] | None:
    if expected_scope is None:
        return event_scope
    if event_scope is None or any(not isinstance(item, str) or not item for item in event_scope):
        raise ValueError("realization event scope is incomplete for the requested expected scope")
    if event_scope != expected_scope:
        raise ValueError("realization event scope does not match the requested expected scope")
    return event_scope


def _event_account_identity(event: dict[str, Any]) -> dict[str, Any] | None:
    value = event.get("account_identity")
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("account identity must be an object or null")

    normalized: dict[str, Any] = {}
    for field in ACCOUNT_IDENTITY_FIELDS:
        item = value.get(field)
        if item is None:
            continue
        if not isinstance(item, str) or not item:
            raise ValueError(f"account identity {field} must be a non-empty string or null")
        normalized[field] = item

    if not any(field in normalized for field in STRONG_ACCOUNT_IDENTITY_FIELDS):
        return None

    provenance = value.get("identity_mapping_provenance")
    if provenance is not None:
        normalized["identity_mapping_provenance"] = provenance
    return normalized


def _merge_account_identity(
    resolved: dict[str, Any] | None,
    current: dict[str, Any] | None,
    *,
    missing_seen: bool,
) -> tuple[dict[str, Any] | None, bool]:
    if current is None:
        if resolved is not None:
            raise ValueError("realization account identity is incomplete across the event slice")
        return None, True

    if missing_seen:
        raise ValueError("realization account identity is incomplete across the event slice")
    if resolved is None:
        return dict(current), False

    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in resolved and field in current and resolved[field] != current[field]:
            raise ValueError(f"realization account identity conflicts on {field}")

    shared_strong = [
        field
        for field in STRONG_ACCOUNT_IDENTITY_FIELDS
        if field in resolved and field in current and resolved[field] == current[field]
    ]
    if not shared_strong:
        raise ValueError("realization account identity cannot be reconciled across the event slice")

    merged = dict(resolved)
    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in current and field not in merged:
            merged[field] = current[field]
    if "identity_mapping_provenance" in current:
        merged["identity_mapping_provenance"] = current["identity_mapping_provenance"]
    return merged, False


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


def project_realization_history(
    events: list[dict[str, Any]],
    *,
    expected_scope: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return canonical realization projections for a single-entity event slice.

    Event order is not trusted. Observation time uses realization_snapshot.captured_at
    when present and otherwise falls back to the event timestamp. Equal timestamps are
    resolved by later input position, matching append-order semantics without turning
    list order into the primary clock.

    When valid optimization-event entity scopes are present, mixed scopes fail closed
    rather than silently merging realization histories across entities/accounts. A
    caller may additionally provide expected_scope to require every realization event
    to carry the complete marketplace/profile/entity identity and match the requested
    replay scope exactly. Explicit account identities must also be mutually compatible;
    missing and known account identity must not be silently merged.
    """

    normalized_expected_scope = _normalize_expected_scope(expected_scope)
    observations: list[tuple[datetime, int, str, dict[str, Any]]] = []
    observed_scopes: set[tuple[Any, Any, Any, Any]] = set()
    account_identity: dict[str, Any] | None = None
    missing_account_identity_seen = False

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError("each event must be an object")
        snapshot = event.get("realization_snapshot")
        if snapshot is None:
            continue
        if not isinstance(snapshot, dict):
            raise ValueError("realization_snapshot must be an object or null")

        scope = _validate_scope(_event_scope(event), normalized_expected_scope)
        if scope is not None:
            observed_scopes.add(scope)
            if len(observed_scopes) > 1:
                raise ValueError("realization projection requires a single entity scope")

        account_identity, missing_account_identity_seen = _merge_account_identity(
            account_identity,
            _event_account_identity(event),
            missing_seen=missing_account_identity_seen,
        )

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

    result = {
        "last_observed_realization": last_observed,
        "current_realization_observability": _project_observability(newest_snapshot, newest_time),
    }
    if account_identity is not None:
        result["account_identity"] = account_identity
    return result


def _load_payload() -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError("stdin must contain valid JSON") from exc

    expected_scope = None
    if isinstance(payload, list):
        events = payload
    elif isinstance(payload, dict):
        events = payload.get("events")
        expected_scope = payload.get("expected_scope")
    else:
        events = None

    if not isinstance(events, list):
        raise ValueError("input must be an event array or an object with an events array")
    if expected_scope is not None and not isinstance(expected_scope, dict):
        raise ValueError("expected_scope must be an object or null")
    return events, expected_scope


def main() -> int:
    try:
        events, expected_scope = _load_payload()
        projected = project_realization_history(events, expected_scope=expected_scope)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    json.dump(projected, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
