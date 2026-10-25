"""Synthetic regression cases: unknown scope is not proven support or absence.

No live Amazon Ads data or mutation. Scope labels are repository-normalized.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    return {
        "snapshot": {
            "connector_id": "synthetic:scope-reader",
            "captured_at": "2026-10-25T11:00:00Z",
            "default_access_mode": "Read-only",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"], "ad_products": ["Sponsored Products"]},
                "bindings": [{
                    "binding_id": "synthetic:scope-report",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-report",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T10:00:00Z",
                    "scope": {"marketplaces": ["US"], "ad_products": ["Sponsored Products"]},
                    "evidence": [{"kind": "contract-test", "reference": "synthetic:scope-probe"}],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US", "ad_product": "Sponsored Products"},
    }


def evaluate(payload):
    return evaluate_connector_capability_gate(payload)


class ConnectorScopePlaceholderEvidenceTests(unittest.TestCase):
    def test_valid_explicit_marketplace_passes(self):
        self.assertEqual(evaluate(fixture())["gate_status"], "Pass")

    def test_unknown_requested_marketplace_is_not_a_valid_identity(self):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = "Unknown"
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = ["Unknown"]
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["Unknown"]
        with self.assertRaisesRegex(ValueError, "expected_scope.marketplace"):
            evaluate(payload)

    def test_unsupported_requested_marketplace_is_not_a_valid_identity(self):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = "Not-Supported"
        with self.assertRaisesRegex(ValueError, "expected_scope.marketplace"):
            evaluate(payload)

    def test_partial_requested_ad_product_is_not_a_valid_identity(self):
        payload = fixture()
        payload["expected_scope"]["ad_product"] = "Partial"
        with self.assertRaisesRegex(ValueError, "expected_scope.ad_product"):
            evaluate(payload)

    def test_padded_requested_marketplace_is_not_proven_identity(self):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = " US "
        with self.assertRaisesRegex(ValueError, "expected_scope.marketplace"):
            evaluate(payload)

    def test_missing_requested_account_type_is_not_valid(self):
        payload = fixture()
        payload["expected_scope"]["account_type"] = "Missing"
        with self.assertRaisesRegex(ValueError, "expected_scope.account_type"):
            evaluate(payload)

    def assert_unknown_capability_scope(self, values, requested="US"):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = requested
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = values
        result = evaluate(payload)
        self.assertEqual(result["requirements"][0]["scope_effect"], "unknown", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero")

    def test_unknown_only_capability_scope_is_not_proven_absence(self):
        self.assert_unknown_capability_scope(["Unknown"])

    def test_unknown_and_us_does_not_prove_jp_absent(self):
        self.assert_unknown_capability_scope(["US", "Unknown"], requested="JP")

    def test_unsupported_and_jp_does_not_prove_us_absent(self):
        self.assert_unknown_capability_scope(["JP", "Not Available"])

    def test_empty_scope_member_is_not_proven_absence(self):
        self.assert_unknown_capability_scope([""])

    def test_null_scope_member_is_not_proven_absence(self):
        self.assert_unknown_capability_scope([None])

    def test_malformed_member_with_known_other_scope_is_unknown(self):
        self.assert_unknown_capability_scope(["JP", 123])

    def test_fully_known_mismatch_remains_blocked(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = ["JP"]
        result = evaluate(payload)
        self.assertEqual(result["requirements"][0]["scope_effect"], "blocked")
        self.assertEqual(result["gate_status"], "Blocked")

    def test_explicit_matching_scope_with_extra_unknown_still_passes(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = ["US", "Unknown"]
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["US", "Unknown"]
        self.assertEqual(evaluate(payload)["gate_status"], "Pass")

    def test_unknown_binding_scope_cannot_prove_us(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["Unknown"]
        result = evaluate(payload)
        self.assertEqual(result["requirements"][0]["binding_effect"], "unknown")
        self.assertEqual(result["gate_status"], "Degraded")

    def test_unknown_binding_scope_does_not_prove_us_absent(self):
        payload = fixture()
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["JP", "Unknown"]
        result = evaluate(payload)
        self.assertEqual(result["requirements"][0]["binding_effect"], "unknown")
        self.assertTrue(any("unavailable" in w.lower() for w in result["requirements"][0]["warnings"]))

    def test_explicit_known_jp_scope_remains_supported(self):
        payload = fixture()
        payload["expected_scope"]["marketplace"] = "JP"
        payload["snapshot"]["capabilities"][0]["scope"]["marketplaces"] = ["JP"]
        payload["snapshot"]["capabilities"][0]["bindings"][0]["scope"]["marketplaces"] = ["JP"]
        self.assertEqual(evaluate(payload)["gate_status"], "Pass")


if __name__ == "__main__":
    unittest.main()
