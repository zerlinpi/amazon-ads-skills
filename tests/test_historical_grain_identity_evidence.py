"""RED: history grain identity cannot be proved by placeholders or padded labels.

All evidence is synthetic and read-only; no Amazon Ads requests or writes.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:history-reader",
            "captured_at": "2026-10-25T12:00:00Z",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"]},
                "data_contract": {
                    "historical_availability_status": "available",
                    "historical_windows": [{
                        "grain": "daily",
                        "available_from": "2025-10-01",
                        "available_through": "2026-10-24",
                    }],
                },
                "bindings": [{
                    "binding_id": "synthetic:history-binding",
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
            "campaign-performance-read": {
                "history_window": {
                    "start_date": "2026-01-01",
                    "end_date": "2026-08-31",
                    "grain": "daily",
                }
            }
        },
    }


class HistoricalGrainIdentityEvidenceTests(unittest.TestCase):
    def assert_invalid_requested_grain(self, value):
        payload = fixture()
        payload["data_requirements"]["campaign-performance-read"]["history_window"]["grain"] = value
        payload["snapshot"]["capabilities"][0]["data_contract"]["historical_windows"][0]["grain"] = value
        with self.assertRaisesRegex(ValueError, "history_window.*grain"):
            evaluate_connector_capability_gate(payload)

    def assert_unknown_observed_grain(self, value):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["data_contract"]["historical_windows"][0]["grain"] = value
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "unknown", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_requested_unknown_is_invalid(self):
        self.assert_invalid_requested_grain("Unknown")

    def test_requested_unsupported_is_invalid(self):
        self.assert_invalid_requested_grain("Unsupported")

    def test_requested_partial_is_invalid(self):
        self.assert_invalid_requested_grain("Partial")

    def test_requested_missing_is_invalid(self):
        self.assert_invalid_requested_grain("Missing")

    def test_requested_not_available_is_invalid(self):
        self.assert_invalid_requested_grain("Not Available")

    def test_requested_not_supported_is_invalid(self):
        self.assert_invalid_requested_grain("Not-Supported")

    def test_requested_padded_daily_is_invalid(self):
        self.assert_invalid_requested_grain(" daily ")

    def test_observed_padded_daily_cannot_prove_match(self):
        self.assert_unknown_observed_grain(" daily ")

    def test_observed_unknown_does_not_prove_daily(self):
        self.assert_unknown_observed_grain("Unknown")

    def test_observed_padded_daily_with_valid_daily_still_ambiguous(self):
        payload = fixture()
        windows = payload["snapshot"]["capabilities"][0]["data_contract"]["historical_windows"]
        windows.append(dict(windows[0], grain=" daily "))
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "unknown", result)

    def test_concrete_daily_window_passes(self):
        result = evaluate_connector_capability_gate(fixture())
        self.assertEqual(result["gate_status"], "Pass", result)
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "pass", result)

    def test_concrete_case_insensitive_grain_remains_compatible(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["data_contract"]["historical_windows"][0]["grain"] = "DAILY"
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_concrete_unmatched_grain_degrades(self):
        self.assert_unknown_observed_grain("monthly")

    def test_no_history_requirement_remains_compatible(self):
        payload = fixture()
        del payload["data_requirements"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["gate_status"], "Pass", result)


if __name__ == "__main__":
    unittest.main()
