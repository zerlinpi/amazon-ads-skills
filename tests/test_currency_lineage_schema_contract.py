import json
import unittest
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


class CurrencyLineageSchemaContractTests(unittest.TestCase):
    def test_currency_lineage_contract_is_declared_at_event_and_history_boundaries(self):
        event_props = _properties("schemas/optimization-event.json", "evidence_snapshot")
        history_props = _properties("schemas/entity-history.json", "latest_measurement_state")

        self.assertIn("currency_lineage", event_props)
        self.assertIn("currency_lineage", history_props)

        event_lineage = event_props["currency_lineage"]["properties"]
        history_lineage = history_props["currency_lineage"]["properties"]
        self.assertTrue(EXPECTED_FIELDS <= event_lineage.keys())
        self.assertTrue(EXPECTED_FIELDS <= history_lineage.keys())

        self.assertEqual(
            event_lineage["currency_conversion_status"],
            history_lineage["currency_conversion_status"],
        )
        self.assertEqual(
            event_lineage["currency_conversion_status"]["enum"],
            ["native", "converted", "unknown", None],
        )


if __name__ == "__main__":
    unittest.main()
