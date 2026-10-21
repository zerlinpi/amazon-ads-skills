"""Project the latest effective measurement-comparison audit for one entity."""

from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import re

from scripts.project_measurement_history import (
    _event_account_identity,
    _merge_account_identity,
    _normalize_expected_scope,
    _normalize_expected_account_identity,
    _validate_scope,
    _validate_expected_account_identity,
)


_REQUIRED_AUDIT_FIELDS = (
    "comparator_id",
    "classification",
    "changed_fields",
    "reasons",
    "baseline_snapshot_id",
    "post_snapshot_id",
)


def _scope_key(event):
    entity = event.get("entity") or {}
    return (
        event.get("marketplace"),
        event.get("profile_scope"),
        entity.get("type"),
        entity.get("id"),
    )


def _timestamp(event):
    """Order audit evidence by UTC instant, never by RFC3339 display text."""
    value = event.get("timestamp")
    match = (
        re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.(?P<fraction>\d+))?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)",
            value,
        ) if isinstance(value, str) else None
    )
    if match is None or value.endswith("-00:00"):
        raise ValueError("measurement comparison timestamp must be timezone-aware RFC3339")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("measurement comparison timestamp must be timezone-aware RFC3339") from exc
    fraction = Decimal("0." + (match.group("fraction") or "0"))
    return parsed.astimezone(timezone.utc).replace(microsecond=0), fraction

def project_measurement_comparison_history(events, *, expected_scope=None):
    """Return a bounded projection without resurrecting superseded audit evidence."""
    expected = _normalize_expected_scope(expected_scope)
    expected_account_identity = _normalize_expected_account_identity(expected_scope)
    events = list(events or [])
    if not events:
        return {
            "latest_measurement_comparison": None,
            "measurement_comparison_status": "No Comparison",
            "measurement_comparison_warnings": [],
        }

    scopes = {_scope_key(event) for event in events}
    if len(scopes) != 1:
        raise ValueError("measurement comparison history requires a single entity scope")

    # Account identity is a stronger boundary than legacy marketplace/profile/entity.
    # Reuse the existing read-only projection's fail-closed identity contract.
    account_identity = None
    missing_account_identity_seen = False
    for event in events:
        _validate_scope(event, expected)
        current_identity = _event_account_identity(event)
        _validate_expected_account_identity(current_identity, expected_account_identity)
        account_identity, missing_account_identity_seen = _merge_account_identity(
            account_identity,
            current_identity,
            missing_seen=missing_account_identity_seen,
        )

    by_id = {}
    for event in events:
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError("measurement comparison history requires nonempty event_id")
        if event_id in by_id:
            raise ValueError("measurement comparison history has duplicate event_id")
        by_id[event_id] = event

    # Predecessors may be absent from bounded history; cycles wholly inside
    # the supplied slice cannot represent a valid audit correction chain.
    visited = set()
    for event_id in by_id:
        if event_id in visited:
            continue
        path = set()
        cursor = event_id
        while cursor in by_id and cursor not in visited:
            if cursor in path:
                raise ValueError("measurement comparison supersession contains a cycle")
            path.add(cursor)
            current = by_id[cursor]
            cursor = (
                current.get("supersedes_event_id")
                if current.get("event_type") == "corrected"
                else None
            )
        visited.update(path)
    superseded = set()
    for event in events:
        if event.get("event_type") != "corrected":
            continue
        target = event.get("supersedes_event_id")
        if target not in by_id:
            continue  # Bounded history may omit the predecessor.
        # A correction cannot supersede a different or unidentified action.
        parent_action_id = event.get("parent_action_id")
        if (
            not isinstance(parent_action_id, str)
            or not parent_action_id.strip()
            or parent_action_id != by_id[target].get("parent_action_id")
        ):
            raise ValueError("measurement comparison correction crosses parent_action_id boundary")
        if target in superseded:
            raise ValueError("measurement comparison supersession has an ambiguous correction fork")
        superseded.add(target)
    active = [
        event
        for event in events
        if event.get("event_id") not in superseded
        and event.get("event_type") in {"evaluated", "corrected"}
    ]
    active.sort(key=lambda event: (_timestamp(event), event.get("event_id") or ""))

    if active:
        latest = active[-1]
        audit = latest.get("measurement_comparison")
        if audit is not None:
            projected = {
                "source_event_id": latest.get("event_id"),
                "source_event_type": latest.get("event_type"),
                "observed_at": latest.get("timestamp"),
                "parent_action_id": latest.get("parent_action_id"),
            }
            projected.update(
                {field: deepcopy(audit.get(field)) for field in _REQUIRED_AUDIT_FIELDS}
            )
            missing = [field for field in _REQUIRED_AUDIT_FIELDS if audit.get(field) is None]
            warnings = []
            status = "Available"
            if missing:
                status = "Unknown"
                warnings.append(
                    "Latest measurement comparison audit is incomplete; missing: "
                    + ", ".join(missing)
                    + "."
                )
            return {
                "latest_measurement_comparison": projected,
                "measurement_comparison_status": status,
                "measurement_comparison_warnings": warnings,
            }

        if latest.get("event_type") == "corrected" and latest.get("supersedes_event_id"):
            return {
                "latest_measurement_comparison": None,
                "measurement_comparison_status": "Superseded Without Replacement",
                "measurement_comparison_warnings": [
                    "The latest correction superseded prior measurement comparison audit evidence without a replacement; do not reuse the stale comparison."
                ],
            }

    return {
        "latest_measurement_comparison": None,
        "measurement_comparison_status": "No Comparison",
        "measurement_comparison_warnings": [],
    }
