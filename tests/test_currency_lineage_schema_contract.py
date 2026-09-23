import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIELDS = {
    "native_currency",
    "reporting_currency",
    "currency_conversion_status",
    "conversion_timing",
    "exchange_rate_provenance",
}


def _properties(path: str, *keys: str):
    node = json.loads((ROOT / path).read_text(encoding="utf-8"))
    for key in keys:
        node = node["properties"][key]
    return node["properties"]


def test_currency_lineage_contract_is_declared_at_event_and_history_boundaries():
    event_props = _properties("schemas/optimization-event.json", "evidence_snapshot")
    history_props = _properties("schemas/entity-history.json", "latest_measurement_state")

    assert "currency_lineage" in event_props
    assert "currency_lineage" in history_props

    event_lineage = event_props["currency_lineage"]["properties"]
    history_lineage = history_props["currency_lineage"]["properties"]
    assert EXPECTED_FIELDS <= event_lineage.keys()
    assert EXPECTED_FIELDS <= history_lineage.keys()

    assert event_lineage["currency_conversion_status"] == history_lineage["currency_conversion_status"]
    assert event_lineage["currency_conversion_status"]["enum"] == [
        "native",
        "converted",
        "unknown",
        None,
    ]
