"""Read-side historical availability must not claim dates after its snapshot capture."""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def snapshot():
    return {
        "connector_id": "fixture",
        "captured_at": "2026-09-19T00:00:00Z",
        "default_access_mode": "Read-only",
        "capabilities": [{
            "capability_id": "campaign-performance-read",
            "status": "Supported",
            "access_mode": "report",
            "scope": {"marketplaces": ["US"]},
            "data_contract": {
                "historical_availability_status": "available",
                "historical_windows": [{
                    "grain": "daily",
                    "available_from": "2025-09-01",
                    "available_through": "2026-09-18",
                }],
            },
            "bindings": [{
                "binding_id": "fixture:history",
                "surface_type": "report",
                "surface_id": "daily-history",
                "verification_status": "Verified",
                "observed_at": "2026-09-19T00:00:00Z",
                "scope": {"marketplaces": ["US"]},
                "evidence": [{
                    "kind": "contract-test",
                    "reference": "fixture",
                    "observed_at": "2026-09-19T00:00:00Z",
                }],
            }],
        }],
    }


def check(s, start="2026-08-01", end="2026-08-31", *, horizon=False, history=True):
    payload = {
        "snapshot": s,
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US"},
    }
    if history:
        payload["data_requirements"] = {
            "campaign-performance-read": {
                "history_window": {
                    "start_date": start,
                    "end_date": end,
                    "grain": "daily",
                },
            },
        }
    if horizon:
        payload["freshness_requirement"] = {
            "as_of": "2026-09-19T00:00:00Z",
            "max_age_seconds": 3600,
        }
    return evaluate_connector_capability_gate(payload)


class HistoricalCaptureHorizonTests(unittest.TestCase):
    def test_future_requested_history_cannot_be_verified_by_earlier_snapshot(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2026-10-31"
        result = check(s, "2026-10-01", "2026-10-15")
        self.assertEqual(result["gate_status"], "Degraded")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "unknown")
        self.assertFalse(result["high_confidence_allowed"])

    def test_future_observed_availability_cannot_prove_even_earlier_request(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2027-01-01"
        result = check(s)
        self.assertEqual(result["gate_status"], "Degraded")
        self.assertEqual(result["requirements"][0]["data_contract_effect"], "unknown")

    def test_explicit_freshness_does_not_make_future_historical_window_real(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2026-12-31"
        result = check(s, horizon=True)
        self.assertEqual(result["snapshot_freshness_effect"], "pass")
        self.assertEqual(result["gate_status"], "Degraded")
        self.assertFalse(result["high_confidence_allowed"])

    def test_same_day_availability_remains_compatible(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2026-09-19"
        self.assertEqual(check(s, "2026-09-18", "2026-09-19")["gate_status"], "Pass")

    def test_one_day_date_boundary_remains_conservative_for_timezones(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2026-09-20"
        self.assertEqual(check(s)["gate_status"], "Pass")

    def test_historical_window_before_capture_remains_valid(self):
        self.assertEqual(check(snapshot())["gate_status"], "Pass")

    def test_no_history_requirement_does_not_infer_historical_availability(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"][0]["available_through"] = "2027-01-01"
        self.assertEqual(check(s, history=False)["gate_status"], "Pass")

    def test_explicitly_unavailable_history_remains_blocked(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_availability_status"] = "unavailable"
        self.assertEqual(check(s)["gate_status"], "Blocked")

    def test_missing_history_bounds_remains_degraded(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_windows"] = []
        self.assertEqual(check(s)["gate_status"], "Degraded")

    def test_explicitly_unknown_history_remains_degraded(self):
        s = snapshot()
        s["capabilities"][0]["data_contract"]["historical_availability_status"] = "unknown"
        self.assertEqual(check(s)["gate_status"], "Degraded")


if __name__ == "__main__":
    unittest.main()
