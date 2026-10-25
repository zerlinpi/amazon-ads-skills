"""Deterministic guard against non-finite connector freshness horizons.

Synthetic evidence only. A NaN/infinite TTL cannot silently make stale
connector snapshots and verified bindings pass freshness checks.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture(max_age_seconds, captured_at="2026-10-24T00:00:00Z"):
    return {
        "required_capabilities": ["campaign-performance-read"],
        "freshness_requirement": {
            "as_of": "2026-10-25T00:00:00Z",
            "max_age_seconds": max_age_seconds,
        },
        "snapshot": {
            "connector_id": "synthetic-read-only",
            "connector_version": "1.0",
            "captured_at": captured_at,
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "bindings": [{
                    "binding_id": "synthetic:report",
                    "surface_type": "report",
                    "surface_id": "synthetic-report",
                    "verification_status": "Verified",
                    "observed_at": captured_at,
                    "evidence": [{
                        "kind": "contract-test",
                        "reference": "synthetic",
                        "observed_at": captured_at,
                    }],
                }],
            }],
        },
    }


class ConnectorFreshnessFiniteHorizonTests(unittest.TestCase):
    def test_nan_horizon_must_not_pass(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_connector_capability_gate(fixture(float("nan")))

    def test_positive_infinite_horizon_must_not_pass(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_connector_capability_gate(fixture(float("inf")))

    def test_overflowed_json_numeric_horizon_must_not_pass(self):
        # Python JSON parsers may decode a 1e309 numeric literal as +Infinity.
        with self.assertRaisesRegex(ValueError, "finite"):
            evaluate_connector_capability_gate(fixture(float("1e309")))

    def test_negative_infinite_horizon_is_invalid(self):
        with self.assertRaises(ValueError):
            evaluate_connector_capability_gate(fixture(float("-inf")))

    def test_finite_stale_horizon_degrades(self):
        result = evaluate_connector_capability_gate(fixture(3600))
        self.assertEqual(result["gate_status"], "Degraded")
        self.assertFalse(result["high_confidence_allowed"])
        self.assertEqual(result["snapshot_freshness_effect"], "stale")

    def test_zero_horizon_accepts_exact_observation(self):
        result = evaluate_connector_capability_gate(
            fixture(0, captured_at="2026-10-25T00:00:00Z")
        )
        self.assertEqual(result["gate_status"], "Pass")
        self.assertTrue(result["high_confidence_allowed"])

    def test_zero_horizon_rejects_older_observation(self):
        result = evaluate_connector_capability_gate(fixture(0))
        self.assertEqual(result["gate_status"], "Degraded")
        self.assertFalse(result["high_confidence_allowed"])

    def test_boolean_horizon_is_not_numeric(self):
        with self.assertRaises(ValueError):
            evaluate_connector_capability_gate(fixture(True))


if __name__ == "__main__":
    unittest.main()
