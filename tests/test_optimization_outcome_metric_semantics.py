import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/optimization-event.json"


class OptimizationOutcomeMetricSemanticsTests(unittest.TestCase):
    def test_schema_exposes_outcome_metric_semantics_envelope(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        props = schema["properties"]
        self.assertIn("outcome_metric_semantics", props)
        semantic_props = props["outcome_metric_semantics"]["properties"]
        for field in ("metric_family", "attribution_family", "semantic_version"):
            self.assertIn(field, semantic_props)

    def test_evidence_snapshot_exposes_per_metric_semantics(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        snapshot_props = schema["properties"]["evidence_snapshot"]["properties"]
        self.assertIn("metric_semantics", snapshot_props)
        metric_items = snapshot_props["metric_semantics"]["items"]["properties"]
        for field in ("metric_name", "metric_family", "attribution_family", "semantic_version"):
            self.assertIn(field, metric_items)


if __name__ == "__main__":
    unittest.main()
