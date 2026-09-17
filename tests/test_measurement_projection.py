import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MeasurementProjectionContractTests(unittest.TestCase):
    def test_entity_history_exposes_latest_measurement_state_without_collapsing_uncertainty(self):
        text = (ROOT / "schemas/entity-history.json").read_text(encoding="utf-8")
        self.assertIn('"latest_measurement_state"', text)
        self.assertIn('"reporting_generation"', text)
        self.assertIn('"date_attribution_semantics"', text)
        self.assertIn('"historical_availability_status"', text)
        self.assertIn('"comparability_status"', text)
        self.assertIn('"evidence_snapshot_id"', text)

    def test_memory_contract_prevents_worked_keep_from_overriding_measurement_uncertainty(self):
        text = (ROOT / "references/optimization-memory.md").read_text(encoding="utf-8").lower()
        self.assertIn("latest_measurement_state", text)
        self.assertIn("worked / keep", text)
        self.assertIn("not comparable", text)
        self.assertIn("retired/deleted", text)
        self.assertIn("manual review", text)


if __name__ == "__main__":
    unittest.main()
