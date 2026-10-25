"""RED regression: unknown scope membership must not become an exclusion verdict.

Synthetic read-only fixtures; no live Amazon Ads calls or writes.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:reader",
            "captured_at": "2026-10-25T12:00:00Z",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"]},
                "bindings": [{
                    "binding_id": "synthetic:verified",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-report",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T11:00:00Z",
                    "scope": {"marketplaces": ["US"]},
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US"},
    }


class ConnectorUnknownScopeGateClassificationTests(unittest.TestCase):
    def assert_unknown_not_exclusion(self, members, requested="US", status="Supported"):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = requested
        cap = payload["snapshot"]["capabilities"][0]
        cap["status"] = status
        cap["scope"]["marketplaces"] = members
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["requirements"][0]["scope_effect"], "unknown", result)
        self.assertEqual(result["requirements"][0]["gate_effect"], "degraded", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_unknown_only_marketplace_is_not_definitive_exclusion(self):
        self.assert_unknown_not_exclusion(["Unknown"])

    def test_mixed_known_unknown_does_not_prove_other_marketplace_excluded(self):
        self.assert_unknown_not_exclusion(["US", "Unknown"], requested="JP")

    def test_null_scope_member_is_not_definitive_exclusion(self):
        self.assert_unknown_not_exclusion(["JP", None])

    def test_blank_scope_member_is_not_definitive_exclusion(self):
        self.assert_unknown_not_exclusion([""])

    def test_malformed_scope_member_is_not_definitive_exclusion(self):
        self.assert_unknown_not_exclusion(["JP", 123])

    def test_partial_capability_with_unknown_scope_is_degraded(self):
        self.assert_unknown_not_exclusion(["Unknown"], status="Partial")

    def test_fully_known_mismatch_still_blocks(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = ["JP"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["requirements"][0]["scope_effect"], "blocked")
        self.assertEqual(result["gate_status"], "Blocked")

    def test_omitted_capability_scope_still_blocks_without_global_assumption(self):
        payload = fixture()
        del payload["snapshot"]["capabilities"][0]["scope"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["requirements"][0]["scope_effect"], "unknown")
        self.assertEqual(result["gate_status"], "Blocked")

    def test_concrete_match_still_passes(self):
        self.assertEqual(evaluate_connector_capability_gate(fixture())["gate_status"], "Pass")

    def test_unknown_binding_scope_stays_degraded(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["Unknown"]
        result = evaluate_connector_capability_gate(payload)
        self.assertEqual(result["requirements"][0]["binding_effect"], "unknown")
        self.assertEqual(result["gate_status"], "Degraded")


if __name__ == "__main__":
    unittest.main()
