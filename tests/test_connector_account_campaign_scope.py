"""Exact advertiser-account and campaign scope must be evidenced, not inferred from marketplace.

Synthetic read-only connector fixtures. This is an identity/coverage gate, NOT
proof of advertiser or campaign eligibility, raw API authenticity or delivery.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate


def fixture():
    scope = {
        "marketplaces": ["US"],
        "ad_products": ["Sponsored Products"],
        "advertiser_account_ids": ["synthetic-account-a"],
        "campaign_ids": ["synthetic-campaign-a"],
    }
    return {
        "snapshot": {
            "connector_id": "synthetic:scoped-reader",
            "captured_at": "2026-10-26T00:00:00Z",
            "capabilities": [{
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": copy.deepcopy(scope),
                "bindings": [{
                    "binding_id": "synthetic:scoped-report",
                    "surface_type": "report",
                    "surface_id": "synthetic:campaign-performance",
                    "verification_status": "Verified",
                    "observed_at": "2026-10-25T23:00:00Z",
                    "scope": copy.deepcopy(scope),
                    "evidence": [{
                        "kind": "contract-test",
                        "reference": "synthetic:scoped-probe",
                    }],
                }],
            }],
        },
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {
            "marketplace": "US",
            "ad_product": "Sponsored Products",
            "advertiser_account_id": "synthetic-account-a",
            "campaign_id": "synthetic-campaign-a",
        },
    }


def check(payload):
    return evaluate_connector_capability_gate(payload)


def cap(p):
    return p["snapshot"]["capabilities"][0]


def binding(p):
    return cap(p)["bindings"][0]


class ExactAccountCampaignScopeTests(unittest.TestCase):
    def test_exact_account_and_campaign_match_pass(self):
        r = check(fixture())
        self.assertEqual(r["gate_status"], "Pass", r)
        self.assertEqual(r["requirements"][0]["binding_effect"], "pass", r)

    def test_other_advertiser_in_capability_is_blocked(self):
        p = fixture()
        cap(p)["scope"]["advertiser_account_ids"] = ["synthetic-account-b"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Blocked", r)
        self.assertEqual(r["requirements"][0]["scope_effect"], "blocked", r)

    def test_other_campaign_in_capability_is_blocked(self):
        p = fixture()
        cap(p)["scope"]["campaign_ids"] = ["synthetic-campaign-b"]
        self.assertEqual(check(p)["gate_status"], "Blocked")

    def test_same_marketplace_other_advertiser_binding_is_not_verified(self):
        p = fixture()
        binding(p)["scope"]["advertiser_account_ids"] = ["synthetic-account-b"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Degraded", r)
        self.assertEqual(r["requirements"][0]["verified_binding_ids"], [], r)

    def test_same_marketplace_other_campaign_binding_is_not_verified(self):
        p = fixture()
        binding(p)["scope"]["campaign_ids"] = ["synthetic-campaign-b"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Degraded", r)
        self.assertEqual(r["requirements"][0]["verified_binding_ids"], [], r)

    def test_missing_advertiser_capability_scope_cannot_be_global(self):
        p = fixture()
        del cap(p)["scope"]["advertiser_account_ids"]
        self.assertEqual(check(p)["gate_status"], "Blocked")

    def test_missing_campaign_binding_scope_cannot_verify_campaign(self):
        p = fixture()
        del binding(p)["scope"]["campaign_ids"]
        self.assertEqual(check(p)["gate_status"], "Degraded")

    def test_unknown_advertiser_membership_is_not_proven_exclusion(self):
        p = fixture()
        cap(p)["scope"]["advertiser_account_ids"] = ["synthetic-account-b", "Unknown"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Degraded", r)
        self.assertEqual(r["requirements"][0]["scope_effect"], "unknown", r)
        self.assertFalse(r["high_confidence_allowed"], r)

    def test_unknown_campaign_membership_is_not_proven_exclusion(self):
        p = fixture()
        cap(p)["scope"]["campaign_ids"] = ["synthetic-campaign-b", "Partial"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Degraded", r)
        self.assertEqual(r["requirements"][0]["scope_effect"], "unknown", r)

    def test_unknown_requested_advertiser_rejected(self):
        p = fixture()
        p["expected_scope"]["advertiser_account_id"] = "Unknown"
        with self.assertRaisesRegex(ValueError, "expected_scope.advertiser_account_id"):
            check(p)

    def test_unsupported_requested_campaign_rejected(self):
        p = fixture()
        p["expected_scope"]["campaign_id"] = "Not-Supported"
        with self.assertRaisesRegex(ValueError, "expected_scope.campaign_id"):
            check(p)

    def test_padded_requested_advertiser_rejected(self):
        p = fixture()
        p["expected_scope"]["advertiser_account_id"] = " synthetic-account-a "
        with self.assertRaisesRegex(ValueError, "expected_scope.advertiser_account_id"):
            check(p)

    def test_real_identifier_containing_unknown_word_is_allowed(self):
        p = fixture()
        p["expected_scope"]["advertiser_account_id"] = "synthetic-unknown-account"
        cap(p)["scope"]["advertiser_account_ids"] = ["synthetic-unknown-account"]
        binding(p)["scope"]["advertiser_account_ids"] = ["synthetic-unknown-account"]
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_valid_secondary_binding_can_verify_exact_campaign(self):
        p = fixture()
        other = copy.deepcopy(binding(p))
        other["binding_id"] = "synthetic:other-campaign-binding"
        other["scope"]["campaign_ids"] = ["synthetic-campaign-b"]
        cap(p)["bindings"].insert(0, other)
        r = check(p)
        self.assertEqual(r["gate_status"], "Pass", r)
        self.assertEqual(r["requirements"][0]["verified_binding_ids"], ["synthetic:scoped-report"], r)

    def test_legacy_marketplace_only_request_still_passes(self):
        p = fixture()
        del p["expected_scope"]["advertiser_account_id"]
        del p["expected_scope"]["campaign_id"]
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_unknown_scope_never_converts_to_zero(self):
        p = fixture()
        cap(p)["scope"]["campaign_ids"] = ["Unknown"]
        r = check(p)
        self.assertEqual(r["gate_status"], "Degraded", r)
        self.assertEqual(r["missing_evidence_policy"], "never_zero", r)


    def test_advertiser_ids_are_opaque_and_case_sensitive(self):
        p = fixture()
        cap(p)["scope"]["advertiser_account_ids"] = ["SYNTHETIC-ACCOUNT-A"]
        self.assertEqual(check(p)["gate_status"], "Blocked")

    def test_campaign_ids_are_opaque_and_case_sensitive(self):
        p = fixture()
        cap(p)["scope"]["campaign_ids"] = ["SYNTHETIC-CAMPAIGN-A"]
        self.assertEqual(check(p)["gate_status"], "Blocked")

    def test_binding_campaign_id_case_difference_is_not_verified(self):
        p = fixture()
        binding(p)["scope"]["campaign_ids"] = ["SYNTHETIC-CAMPAIGN-A"]
        self.assertEqual(check(p)["gate_status"], "Degraded")

    def test_legacy_ad_product_case_insensitive_matching_retained(self):
        p = fixture()
        p["expected_scope"]["ad_product"] = "sponsored products"
        self.assertEqual(check(p)["gate_status"], "Pass")

if __name__ == "__main__":
    unittest.main()
