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

METRIC_SEMANTIC_FIELDS = ("metric_name", "metric_family", "attribution_family", "semantic_version")


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


def _normalize_expected_account_identity(value: Any) -> dict[str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("expected_scope must be an object or null")
    account_identity = value.get("account_identity")
    if account_identity is None:
        return None
    if not isinstance(account_identity, dict):
        raise ValueError("expected_scope account identity must be an object or null")

    normalized: dict[str, str] = {}
    for field in ACCOUNT_IDENTITY_FIELDS:
        item = account_identity.get(field)
        if item is None:
            continue
        if not isinstance(item, str) or not item:
            raise ValueError(
                f"expected_scope account identity {field} must be a non-empty string or null"
            )
        normalized[field] = item

    if not any(field in normalized for field in STRONG_ACCOUNT_IDENTITY_FIELDS):
        raise ValueError(
            "expected_scope account identity must include at least one advertiser or regional profile identifier"
        )
    return normalized


def _validate_expected_account_identity(
    current: dict[str, Any] | None,
    expected: dict[str, str] | None,
) -> None:
    if expected is None:
        return
    if current is None:
        raise ValueError("measurement account identity is incomplete for expected_scope")
    for field, expected_value in expected.items():
        if current.get(field) != expected_value:
            raise ValueError(
                f"measurement account identity does not match expected_scope on {field}"
            )


def _merge_account_identity(
    resolved: dict[str, Any] | None,
    current: dict[str, Any] | None,
    *,
    missing_seen: bool,
) -> tuple[dict[str, Any] | None, bool]:
    if current is None:
        if resolved is not None:
            raise ValueError("measurement account identity is incomplete across the event slice")
        return None, True

    if missing_seen:
        raise ValueError("measurement account identity is incomplete across the event slice")
    if resolved is None:
        return dict(current), False

    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in resolved and field in current and resolved[field] != current[field]:
            raise ValueError(f"measurement account identity conflicts on {field}")

    shared_strong = [
        field
        for field in STRONG_ACCOUNT_IDENTITY_FIELDS
        if field in resolved and field in current and resolved[field] == current[field]
    ]
    if not shared_strong:
        raise ValueError("measurement account identity cannot be reconciled across the event slice")

    merged = dict(resolved)
    for field in ACCOUNT_IDENTITY_FIELDS:
        if field in current and field not in merged:
            merged[field] = current[field]
    if "identity_mapping_provenance" in current:
        merged["identity_mapping_provenance"] = current["identity_mapping_provenance"]
    return merged, False


def _normalize_metric_semantic_item(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    result: dict[str, Any] = {}
    for name in METRIC_SEMANTIC_FIELDS:
        item = value.get(name)
        if item is not None and (not isinstance(item, str) or not item):
            raise ValueError(f"{field}.{name} must be a non-empty string or null")
        result[name] = item
    return result


def _normalize_metric_semantics(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError("evidence_snapshot.metric_semantics must be an array")
    return [
        _normalize_metric_semantic_item(item, field=f"evidence_snapshot.metric_semantics[{index}]")
        for index, item in enumerate(value)
    ]


def _normalize_outcome_metric_semantics(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    return _normalize_metric_semantic_item(value, field="outcome_metric_semantics")


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


def _project(
    snapshot: dict[str, Any],
    observed_at: str,
    outcome_metric_semantics: Any,
) -> dict[str, Any]:
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
        "metric_semantics": _normalize_metric_semantics(snapshot.get("metric_semantics")),
        "outcome_metric_semantics": _normalize_outcome_metric_semantics(outcome_metric_semantics),
        "date_attribution_semantics": snapshot.get("date_attribution_semantics"),
        "historical_availability_status": history_status,
        "comparability_status": comparability,
        "warnings": _warnings(snapshot, history_status, comparability),
    }


def project_measurement_history(
    events: list[dict[str, Any]], *, expected_scope: dict[str, Any] | None = None
) -> dict[str, Any]:
    expected = _normalize_expected_scope(expected_scope)
    expected_account_identity = _normalize_expected_account_identity(expected_scope)
    candidates: list[tuple[datetime, int, str, dict[str, Any], Any]] = []
    observed_scope: tuple[Any, Any, Any, Any] | None = None
    account_identity: dict[str, Any] | None = None
    missing_account_identity_seen = False

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

        current_account_identity = _event_account_identity(event)
        _validate_expected_account_identity(current_account_identity, expected_account_identity)
        account_identity, missing_account_identity_seen = _merge_account_identity(
            account_identity,
            current_account_identity,
            missing_seen=missing_account_identity_seen,
        )

        raw_time = snapshot.get("captured_at") or event.get("timestamp")
        parsed = _parse_timestamp(raw_time, field="measurement observation time")
        candidates.append((parsed, index, raw_time, snapshot, event.get("outcome_metric_semantics")))

    if not candidates:
        return {"latest_measurement_state": None}

    candidates.sort(key=lambda item: (item[0], item[1]))
    _, _, observed_at, snapshot, outcome_metric_semantics = candidates[-1]
    result = {
        "latest_measurement_state": _project(
            snapshot,
            observed_at,
            outcome_metric_semantics,
        )
    }
    if account_identity is not None:
        result["account_identity"] = account_identity
    return result


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
