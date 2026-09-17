import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EntityMeasurementProjectionTests(unittest.TestCase):
    def test_entity_history_exposes_bounded_measurement_state(self):
        text = (ROOT / "schemas/entity-history.json").read_text(encoding="utf-8")
        self.assertIn('"latest_measurement_state"', text)
        for field in (
            '"evidence_snapshot_id"',
            '"source_system"',
            '"source_dataset"',
            '"acquisition_channel"',
            '"reporting_generation"',
            '"semantic_version"',
            '"date_attribution_semantics"',
            '"historical_availability_status"',
            '"comparability_status"',
            '"observed_at"',
        ):
            self.assertIn(field, text)

    def test_memory_contract_keeps_summary_uncertainty_fail_closed(self):
        text = (ROOT / "references/optimization-memory.md").read_text(encoding="utf-8").lower()
        self.assertIn("latest_measurement_state", text)
        self.assertIn("worked / keep", text)
        self.assertIn("not comparable", text)
        self.assertIn("retired_or_deleted", text)
        self.assertIn("manual review", text)


if __name__ == "__main__":
    unittest.main()
