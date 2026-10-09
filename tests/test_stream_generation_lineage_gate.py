"""Fail-closed Amazon Marketing Stream generation lineage regressions."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_metric_aggregation_gate.py"

class StreamGenerationLineageGateTests(unittest.TestCase):
    def evaluate(self, source):
        payload = {
            "operation": "sum",
            "metric_semantics": {"aggregation_semantics": "additive"},
            "source_relation": "disjoint",
            **source,
        }
        proc = subprocess.run(
            [sys.executable, str(GATE)], input=json.dumps(payload),
            text=True, capture_output=True, cwd=ROOT, check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_generation_and_channel_lineage(self):
        verified = {
            "record_identity_coverage": "Verified",
            "highest_version_per_record": "Verified",
        }
        cases = [
            ({"acquisition_channel": "amazon_marketing_stream", "stream_generation": "v2"}, "Unknown", False),
            ({"acquisition_channel": "Amazon Marketing Stream V2"}, "Unknown", False),
            ({"stream_generation": "v2"}, "Unknown", False),
            ({"stream_generation": "v2", "stream_record_reconciliation": verified}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream"}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream_v1", "stream_generation": "v2", "stream_record_reconciliation": verified}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream_v2", "stream_generation": "v1", "stream_record_reconciliation": verified}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream", "stream_generation": "v3"}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream", "stream_generation": "v1"}, "Not Applicable", True),
            ({"acquisition_channel": "amazon_marketing_stream_v1"}, "Not Applicable", True),
            ({"acquisition_channel": "reporting_api"}, "Not Applicable", True),
            ({"acquisition_channel": "reporting_api", "stream_record_reconciliation": verified}, "Unknown", False),
            ({"acquisition_channel": "reporting_api", "stream_dataset": "ads-performance-v1"}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream_v1", "stream_record_reconciliation": verified}, "Unknown", False),
            ({"acquisition_channel": "reporting_api", "stream_generation": "v2"}, "Unknown", False),
            ({"acquisition_channel": "marketing_stream_v2"}, "Unknown", False),
            ({"stream_record_reconciliation": verified}, "Unknown", False),
            ({"stream_dataset": "ads-performance-v1"}, "Unknown", False),
            ({"acquisition_channel": "amazon_marketing_stream", "stream_generation": "v2", "stream_record_reconciliation": verified}, "Verified", True),
        ]
        for source, expected_status, allowed in cases:
            with self.subTest(source=source):
                result = self.evaluate(source)
                self.assertEqual(result["stream_reconciliation_status"], expected_status)
                self.assertIs(result["direct_sum_allowed"], allowed)

if __name__ == "__main__":
    unittest.main()
