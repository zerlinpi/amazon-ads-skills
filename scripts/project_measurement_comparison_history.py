"""Project the latest effective measurement-comparison audit for one entity."""

from copy import deepcopy
from datetime import datetime, timezone
import re


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
    if (
        not isinstance(value, str)
        or not re.fullmatch(
            r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d+)?(?:Z|[+-]\\d{2}:\\d{2})",
            value,
        )
        or value.endswith("-00:00")  # RFC3339 unknown-local-offset convention
    ):
        raise ValueError("measurement comparison timestamp must be timezone-aware RFC3339")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("measurement comparison timestamp must be timezone-aware RFC3339") from exc
    return parsed.astimezone(timezone.utc)


def project_measurement_comparison_history(events):
    """Return a bounded projection without resurrecting superseded audit evidence."""
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

    by_id = {
        event.get("event_id"): event
        for event in events
        if event.get("event_id")
    }
    superseded = {
        event.get("supersedes_event_id")
        for event in events
        if event.get("event_type") == "corrected"
        and event.get("supersedes_event_id") in by_id
    }
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
