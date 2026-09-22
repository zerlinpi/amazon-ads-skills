import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "modeled_conversion_inclusion",
    "direct_modeled_split_available",
    "allocation_coverage_status",
    "unallocated_rows_present",
    "allocation_grain",
}


def _schema(name):
    return json.loads((ROOT / "schemas" / name).read_text())


def test_measurement_composition_is_declared_at_event_and_history_boundaries():
    event = _schema("optimization-event.json")
    history = _schema("entity-history.json")

    event_props = event["properties"]["evidence_snapshot"]["properties"]
    history_props = history["properties"]["latest_measurement_state"]["properties"]

    assert "measurement_composition" in event_props
    assert "measurement_composition" in history_props

    event_composition = event_props["measurement_composition"]
    history_composition = history_props["measurement_composition"]

    assert event_composition["type"] == ["object", "null"]
    assert history_composition["type"] == ["object", "null"]
    assert set(event_composition["properties"]) == FIELDS
    assert set(history_composition["properties"]) == FIELDS


def test_measurement_composition_unknowns_are_nullable_not_defaulted():
    event = _schema("optimization-event.json")
    composition = event["properties"]["evidence_snapshot"]["properties"]["measurement_composition"]

    for field in FIELDS:
        spec = composition["properties"][field]
        assert "null" in spec["type"]
        assert "default" not in spec
