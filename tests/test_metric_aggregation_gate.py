import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_metric_aggregation_gate.py"


def run_gate(payload):
    return subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


class MetricAggregationGateTests(unittest.TestCase):
    def test_additive_metric_with_disjoint_rows_allows_direct_sum(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "additive"},
            "source_relation": "disjoint",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Allowed")
        self.assertTrue(out["direct_sum_allowed"])

    def test_non_additive_deduplicated_metric_blocks_direct_sum(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "non_additive_deduplicated"},
            "source_relation": "disjoint",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Blocked")
        self.assertFalse(out["direct_sum_allowed"])

    def test_ratio_or_derived_metric_blocks_direct_sum(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "ratio_or_derived"},
            "source_relation": "disjoint",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Blocked")
        self.assertFalse(out["direct_sum_allowed"])

    def test_unknown_metric_semantics_never_defaults_to_additive(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "unknown"},
            "source_relation": "disjoint",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Unknown")
        self.assertFalse(out["direct_sum_allowed"])
        self.assertEqual(out["missing_semantics_policy"], "never_assume_additive")

    def test_additive_metric_with_overlapping_rows_blocks_direct_sum(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "additive"},
            "source_relation": "overlapping",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Blocked")
        self.assertFalse(out["direct_sum_allowed"])

    def test_additive_metric_with_unknown_row_relation_is_not_sum_safe(self):
        proc = run_gate({
            "metric_semantics": {"aggregation_semantics": "additive"},
            "source_relation": "unknown",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Unknown")
        self.assertFalse(out["direct_sum_allowed"])

    def test_missing_metric_semantics_is_unknown_not_additive(self):
        proc = run_gate({
            "source_relation": "disjoint",
            "operation": "sum",
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["aggregation_status"], "Unknown")
        self.assertFalse(out["direct_sum_allowed"])


if __name__ == "__main__":
    unittest.main()
