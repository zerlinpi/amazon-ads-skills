"""Read-side reporting sunset metadata must be consistent with snapshot capture.

Synthetic, deterministic connector evidence; no Amazon Ads calls or writes.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:report-reader",
            "captured_at": "2026-10-25T12:00:00Z",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"]},
                "data_contract": {
                    "reporting_generation": "legacy-reporting",
                    "reporting_generation_status": "sunset_scheduled",
                    "sunset_at": "2026-12-31T23:59:59Z",
                },
                "bindings": [{
                    "binding_id": "synthetic:report-binding",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-performance",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T11:00:00Z",
                    "scope": {"marketplaces": ["US"]},
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US"},
        "data_requirements": {
            "campaign-performance-read": {"required_reporting_generation": "legacy-reporting"}
        },
    }


def check(payload):
    return evaluate_connector_capability_gate(payload)


class ReportingSunsetCaptureConsistencyTests(unittest.TestCase):
    def assert_overdue_degraded(self, payload):
        result = check(payload)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "unknown", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")
        self.assertIn("sunset", " ".join(result["requirements"][0]["warnings"]).lower())

    def test_scheduled_sunset_before_capture_is_not_currently_verified(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["data_contract"]["sunset_at"] = "2026-09-30T00:00:00Z"
        self.assert_overdue_degraded(p)

    def test_active_generation_with_overdue_declared_sunset_is_ambiguous(self):
        p = fixture()
        c = p["snapshot"]["capabilities"][0]["data_contract"]
        c["reporting_generation_status"] = "active"
        c["sunset_at"] = "2026-10-01T00:00:00Z"
        self.assert_overdue_degraded(p)

    def test_offset_aware_sunset_before_capture_is_not_verified(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["data_contract"]["sunset_at"] = "2026-10-25T19:00:00+09:00"
        self.assert_overdue_degraded(p)

    def test_future_scheduled_sunset_is_usable_with_warning(self):
        result = check(fixture())
        self.assertEqual(result["gate_status"], "Pass")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "pass")
        self.assertIn("sunset", " ".join(result["requirements"][0]["warnings"]).lower())

    def test_future_sunset_with_active_status_is_not_forced_to_retired(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["data_contract"]["reporting_generation_status"] = "active"
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_sunset_at_snapshot_capture_is_not_overdue(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["data_contract"]["sunset_at"] = "2026-10-25T12:00:00Z"
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_retired_status_remains_blocked(self):
        p = fixture()
        c = p["snapshot"]["capabilities"][0]["data_contract"]
        c["reporting_generation_status"] = "retired"
        c["sunset_at"] = "2026-10-01T00:00:00Z"
        self.assertEqual(check(p)["gate_status"], "Blocked")

    def test_without_reporting_requirement_does_not_infer_retirement(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["data_contract"]["sunset_at"] = "2026-09-01T00:00:00Z"
        del p["data_requirements"]
        result = check(p)
        self.assertEqual(result["gate_status"], "Pass")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()
