import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_SCRIPT = ROOT / "scripts/project_measurement_history.py"
REALIZATION_SCRIPT = ROOT / "scripts/project_realization_history.py"


def invoke(script: Path, event, expected_scope):
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps({"events": [event], "expected_scope": expected_scope}),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


def expected(global_id: str):
    return {
        "marketplace": "US",
        "profile_scope": "profile-a",
        "entity_type": "campaign",
        "entity_id": "campaign-1",
        "account_identity": {"global_advertiser_account_id": global_id},
    }


def event(global_id: str):
    return {
        "event_id": "e1",
        "timestamp": "2026-09-17T12:00:00Z",
        "marketplace": "US",
        "profile_scope": "profile-a",
        "account_identity": {"global_advertiser_account_id": global_id, "country_code": "US"},
        "entity": {"type": "campaign", "id": "campaign-1"},
    }


class ExpectedAccountIdentityBindingTests(unittest.TestCase):
    def test_measurement_rejects_single_event_from_wrong_advertiser(self):
        payload = event("global-b")
        payload["evidence_snapshot"] = {"snapshot_id": "m1", "captured_at": "2026-09-17T12:00:00Z"}
        result = invoke(MEASUREMENT_SCRIPT, payload, expected("global-a"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("expected account identity", result.stderr.lower())

    def test_realization_rejects_single_event_from_wrong_advertiser(self):
        payload = event("global-b")
        payload["realization_snapshot"] = {
            "snapshot_id": "r1",
            "captured_at": "2026-09-17T12:00:00Z",
            "coverage_status": "Complete",
            "realized_surfaces": ["shopping_results"],
        }
        result = invoke(REALIZATION_SCRIPT, payload, expected("global-a"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("expected account identity", result.stderr.lower())

    def test_measurement_accepts_compatible_expected_account_identity(self):
        payload = event("global-a")
        payload["evidence_snapshot"] = {"snapshot_id": "m1", "captured_at": "2026-09-17T12:00:00Z"}
        result = invoke(MEASUREMENT_SCRIPT, payload, expected("global-a"))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_expected_scope_without_account_identity_remains_supported(self):
        payload = event("global-a")
        payload["evidence_snapshot"] = {"snapshot_id": "m1", "captured_at": "2026-09-17T12:00:00Z"}
        legacy = expected("global-a")
        legacy.pop("account_identity")
        result = invoke(MEASUREMENT_SCRIPT, payload, legacy)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
