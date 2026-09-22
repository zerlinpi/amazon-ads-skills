import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    "modeled_conversion_inclusion",
    "direct_modeled_split_available",
    "allocation_coverage_status",
    "unallocated_rows_present",
    "allocation_grain",
}


class MeasurementCompositionSchemaContractTests(unittest.TestCase):
    def schema(self, name):
        return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

    def test_measurement_composition_is_declared_at_event_and_history_boundaries(self):
        event = self.schema("optimization-event.json")
        history = self.schema("entity-history.json")

        event_props = event["properties"]["evidence_snapshot"]["properties"]
        history_props = history["properties"]["latest_measurement_state"]["properties"]

        self.assertIn("measurement_composition", event_props)
        self.assertIn("measurement_composition", history_props)

        event_composition = event_props["measurement_composition"]
        history_composition = history_props["measurement_composition"]

        self.assertEqual(event_composition["type"], ["object", "null"])
        self.assertEqual(history_composition["type"], ["object", "null"])
        self.assertEqual(set(event_composition["properties"]), FIELDS)
        self.assertEqual(set(history_composition["properties"]), FIELDS)

    def test_measurement_composition_unknowns_are_nullable_not_defaulted(self):
        event = self.schema("optimization-event.json")
        composition = event["properties"]["evidence_snapshot"]["properties"]["measurement_composition"]

        for field in FIELDS:
            spec = composition["properties"][field]
            self.assertIn("null", spec["type"])
            self.assertNotIn("default", spec)


if __name__ == "__main__":
    unittest.main()
