import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/project_realization_history.py"


class RealizationProjectorTests(unittest.TestCase):
    def run_projector(self, events):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps({"events": events}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"projector failed: stdout={result.stdout!r} stderr={result.stderr!r}",
        )
        return json.loads(result.stdout)

    def test_newer_unavailable_observation_preserves_last_bounded_identity(self):
        projected = self.run_projector(
            [
                {
                    "event_id": "e1",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "realization_snapshot": {
                        "snapshot_id": "r1",
                        "captured_at": "2026-09-14T07:59:00Z",
                        "realization_mode": "platform_managed",
                        "realized_surfaces": ["shopping_results"],
                        "realized_product_ids": ["ASIN-A", "ASIN-B"],
                        "coverage_status": "Complete",
                        "comparability_status": "Comparable",
                        "identity_hash": "identity-a",
                        "source_dataset": "prompt-performance",
                        "acquisition_channel": "api",
                    },
                },
                {
                    "event_id": "e2",
                    "timestamp": "2026-09-14T09:00:00Z",
                    "realization_snapshot": {
                        "snapshot_id": "r2",
                        "captured_at": "2026-09-14T08:59:00Z",
                        "coverage_status": "Unavailable",
                        "comparability_status": "Unknown",
                        "source_dataset": "prompt-performance",
                        "acquisition_channel": "connector-x",
                        "warnings": ["realization dimensions unavailable via active connector"],
                    },
                },
            ]
        )

        self.assertEqual(projected["last_observed_realization"]["snapshot_id"], "r1")
        self.assertEqual(
            projected["last_observed_realization"]["realized_product_ids"],
            ["ASIN-A", "ASIN-B"],
        )
        self.assertEqual(projected["last_observed_realization"]["freshness_status"], "Unknown")
        self.assertEqual(projected["current_realization_observability"]["checked_at"], "2026-09-14T08:59:00Z")
        self.assertEqual(projected["current_realization_observability"]["status"], "Unavailable")
        self.assertNotIn("realized_product_ids", projected["current_realization_observability"])

    def test_newest_bounded_snapshot_advances_both_views_without_inventing_freshness(self):
        projected = self.run_projector(
            [
                {
                    "event_id": "e1",
                    "timestamp": "2026-09-14T08:00:00Z",
                    "realization_snapshot": {
                        "snapshot_id": "r1",
                        "captured_at": "2026-09-14T07:59:00Z",
                        "realized_surfaces": ["shopping_results"],
                        "coverage_status": "Complete",
                    },
                },
                {
                    "event_id": "e2",
                    "timestamp": "2026-09-14T10:00:00Z",
                    "realization_snapshot": {
                        "snapshot_id": "r2",
                        "captured_at": "2026-09-14T09:59:00Z",
                        "realized_surfaces": ["product_detail_page"],
                        "realized_creative_or_message_ids": ["prompt-42"],
                        "coverage_status": "Partial",
                        "comparability_status": "Directional",
                    },
                },
            ]
        )

        self.assertEqual(projected["last_observed_realization"]["snapshot_id"], "r2")
        self.assertEqual(
            projected["last_observed_realization"]["realized_surfaces"],
            ["product_detail_page"],
        )
        self.assertEqual(projected["last_observed_realization"]["freshness_status"], "Unknown")
        self.assertEqual(projected["current_realization_observability"]["status"], "Partial")
        self.assertEqual(
            projected["current_realization_observability"]["material_dimensions"],
            ["surface", "creative_or_message"],
        )


if __name__ == "__main__":
    unittest.main()
