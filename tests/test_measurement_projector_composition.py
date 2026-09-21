import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_measurement_history.py"


class MeasurementProjectorCompositionTests(unittest.TestCase):
    def run_projector(self, snapshot):
        event = {
            "event_id": "e1",
            "event_type": "evaluated",
            "timestamp": "2026-09-22T00:00:00Z",
            "entity": {"type": "campaign", "id": "c1"},
            "action_type": "bid_change",
            "evidence_snapshot": snapshot,
        }
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps({"events": [event]}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["latest_measurement_state"]

    def test_preserves_modeled_measurement_composition_and_allocation_coverage(self):
        state = self.run_projector({
            "snapshot_id": "m1",
            "captured_at": "2026-09-22T00:00:00Z",
            "reporting_generation": "unified",
            "date_attribution_semantics": "traffic_date",
            "measurement_composition": {
                "modeled_conversion_inclusion": "combined_with_direct",
                "direct_modeled_split_available": False,
                "allocation_coverage_status": "Partial",
                "unallocated_rows_present": True,
                "allocation_grain": "targeting",
            },
        })
        self.assertEqual(state["measurement_composition"]["modeled_conversion_inclusion"], "combined_with_direct")
        self.assertFalse(state["measurement_composition"]["direct_modeled_split_available"])
        self.assertEqual(state["measurement_composition"]["allocation_coverage_status"], "Partial")
        self.assertTrue(state["measurement_composition"]["unallocated_rows_present"])

    def test_unknown_composition_is_not_inferred_as_direct_only_or_complete(self):
        state = self.run_projector({
            "snapshot_id": "m2",
            "captured_at": "2026-09-22T00:00:00Z",
            "reporting_generation": "unified",
            "date_attribution_semantics": "traffic_date",
        })
        self.assertIsNone(state["measurement_composition"])
        warnings = " ".join(state["warnings"]).lower()
        self.assertIn("measurement composition", warnings)
        self.assertNotIn("direct_only", warnings)
        self.assertNotIn("complete allocation", warnings)


if __name__ == "__main__":
    unittest.main()
