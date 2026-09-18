import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_measurement_history.py"


class MeasurementProjectorMetricSemanticsTests(unittest.TestCase):
    def run_projector(self, events):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps({"events": events}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_entity_history_schema_preserves_per_metric_and_outcome_semantics(self):
        schema = json.loads((ROOT / "schemas/entity-history.json").read_text(encoding="utf-8"))
        props = schema["properties"]["latest_measurement_state"]["properties"]
        self.assertIn("metric_semantics", props)
        self.assertIn("outcome_metric_semantics", props)

        metric_props = props["metric_semantics"]["items"]["properties"]
        outcome_props = props["outcome_metric_semantics"]["properties"]
        for field in ("metric_name", "metric_family", "attribution_family", "semantic_version"):
            self.assertIn(field, metric_props)
            self.assertIn(field, outcome_props)

    def test_projector_preserves_semantics_from_selected_newest_snapshot_event(self):
        projected = self.run_projector([
            {
                "event_id": "older",
                "event_type": "evaluated",
                "timestamp": "2026-09-18T01:00:00Z",
                "entity": {"type": "campaign", "id": "c1"},
                "action_type": "budget_change",
                "outcome_metric_semantics": {
                    "metric_name": "Purchases",
                    "metric_family": "conversion",
                    "attribution_family": "old-default",
                    "semantic_version": "metric-v1"
                },
                "evidence_snapshot": {
                    "snapshot_id": "s1",
                    "captured_at": "2026-09-18T01:00:00Z",
                    "semantic_version": "dataset-v1",
                    "metric_semantics": [
                        {
                            "metric_name": "Purchases",
                            "metric_family": "conversion",
                            "attribution_family": "old-default",
                            "semantic_version": "metric-v1"
                        }
                    ],
                    "date_attribution_semantics": "traffic_date"
                }
            },
            {
                "event_id": "newer",
                "event_type": "evaluated",
                "timestamp": "2026-09-18T02:00:00Z",
                "entity": {"type": "campaign", "id": "c1"},
                "action_type": "budget_change",
                "outcome_metric_semantics": {
                    "metric_name": "Purchases",
                    "metric_family": "conversion",
                    "attribution_family": "shopping-signal-enhanced-last-touch",
                    "semantic_version": "metric-v2"
                },
                "evidence_snapshot": {
                    "snapshot_id": "s2",
                    "captured_at": "2026-09-18T02:00:00Z",
                    "semantic_version": "dataset-v2",
                    "metric_semantics": [
                        {
                            "metric_name": "Purchases",
                            "metric_family": "conversion",
                            "attribution_family": "shopping-signal-enhanced-last-touch",
                            "semantic_version": "metric-v2"
                        },
                        {
                            "metric_name": "Sales",
                            "metric_family": "conversion",
                            "attribution_family": "shopping-signal-enhanced-last-touch",
                            "semantic_version": "metric-v2"
                        }
                    ],
                    "date_attribution_semantics": "traffic_date"
                }
            }
        ])

        state = projected["latest_measurement_state"]
        self.assertEqual(state["evidence_snapshot_id"], "s2")
        self.assertEqual(state["semantic_version"], "dataset-v2")
        self.assertEqual(len(state["metric_semantics"]), 2)
        self.assertEqual(
            state["metric_semantics"][0]["attribution_family"],
            "shopping-signal-enhanced-last-touch",
        )
        self.assertEqual(
            state["outcome_metric_semantics"]["semantic_version"],
            "metric-v2",
        )

    def test_missing_semantics_remain_unknown_not_inferred_from_dataset_version(self):
        projected = self.run_projector([
            {
                "event_id": "e1",
                "event_type": "evaluated",
                "timestamp": "2026-09-18T03:00:00Z",
                "entity": {"type": "campaign", "id": "c1"},
                "action_type": "budget_change",
                "evidence_snapshot": {
                    "snapshot_id": "s3",
                    "captured_at": "2026-09-18T03:00:00Z",
                    "semantic_version": "dataset-v3"
                }
            }
        ])
        state = projected["latest_measurement_state"]
        self.assertEqual(state["semantic_version"], "dataset-v3")
        self.assertEqual(state["metric_semantics"], [])
        self.assertIsNone(state["outcome_metric_semantics"])


if __name__ == "__main__":
    unittest.main()
