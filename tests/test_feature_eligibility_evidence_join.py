"""Feature-specific eligibility must be joined independently to connector capability.

Synthetic evidence only. This test does not query Amazon Ads or grant write
permission; generic product-group eligibility is not B2B campaign enrollment.
"""
import copy
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_connector_account_campaign_scope import fixture as scoped_fixture


def fixture():
    payload = scoped_fixture()
    payload["feature_eligibility_requirement"] = {
        "feature_id": "amazon-business-exclusive-sp",
        "marketplace": "US",
        "advertiser_account_id": "synthetic-account-a",
        "campaign_id": "synthetic-campaign-a",
        "as_of": "2026-10-26T00:00:00Z",
        "max_age_seconds": 7200,
    }
    payload["feature_eligibility_evidence"] = {
        "feature_id": "amazon-business-exclusive-sp",
        "marketplace": "US",
        "advertiser_account_id": "synthetic-account-a",
        "campaign_id": "synthetic-campaign-a",
        "eligibility_status": "Eligible",
        "evidence_type": "feature-specific",
        "verification_status": "Verified",
        "source_system": "synthetic:feature-eligibility",
        "source_reference": "synthetic:eligibility-record-123",
        "observed_at": "2026-10-25T23:00:00Z",
    }
    return payload


def check(payload):
    return evaluate_connector_capability_gate(payload)


class FeatureEligibilityEvidenceJoinTests(unittest.TestCase):
    def assert_conservative(self, result, status):
        self.assertEqual(result["gate_status"], status, result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero", result)
        self.assertNotIn("High Confidence", result["allowed_decision_classes"])

    def test_legacy_connector_request_still_passes_without_feature_requirement(self):
        p = fixture()
        del p["feature_eligibility_requirement"]
        del p["feature_eligibility_evidence"]
        self.assertEqual(check(p)["gate_status"], "Pass")

    def test_verified_feature_specific_eligibility_can_pass(self):
        r = check(fixture())
        self.assertEqual(r["gate_status"], "Pass", r)
        self.assertEqual(r["feature_eligibility_effect"], "pass", r)

    def test_missing_independent_eligibility_evidence_degrades(self):
        p = fixture()
        del p["feature_eligibility_evidence"]
        r = check(p)
        self.assert_conservative(r, "Degraded")
        self.assertEqual(r["feature_eligibility_effect"], "unknown")

    def test_verified_ineligible_blocks(self):
        p = fixture()
        p["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        r = check(p)
        self.assert_conservative(r, "Blocked")
        self.assertEqual(r["feature_eligibility_effect"], "blocked")

    def test_unknown_status_is_not_eligible(self):
        p = fixture()
        p["feature_eligibility_evidence"]["eligibility_status"] = "Unknown"
        self.assert_conservative(check(p), "Degraded")

    def test_partial_status_is_not_eligible(self):
        p = fixture()
        p["feature_eligibility_evidence"]["eligibility_status"] = "Partial"
        self.assert_conservative(check(p), "Degraded")

    def test_unverified_eligible_is_not_proof(self):
        p = fixture()
        p["feature_eligibility_evidence"]["verification_status"] = "Unverified"
        self.assert_conservative(check(p), "Degraded")

    def test_generic_product_group_eligibility_is_not_feature_enrollment(self):
        p = fixture()
        p["feature_eligibility_evidence"]["evidence_type"] = "advertiser-product-group"
        self.assert_conservative(check(p), "Degraded")

    def test_other_advertiser_eligibility_does_not_transfer(self):
        p = fixture()
        p["feature_eligibility_evidence"]["advertiser_account_id"] = "synthetic-account-b"
        self.assert_conservative(check(p), "Degraded")

    def test_other_campaign_eligibility_does_not_transfer(self):
        p = fixture()
        p["feature_eligibility_evidence"]["campaign_id"] = "synthetic-campaign-b"
        self.assert_conservative(check(p), "Degraded")

    def test_other_marketplace_eligibility_does_not_transfer(self):
        p = fixture()
        p["feature_eligibility_evidence"]["marketplace"] = "JP"
        self.assert_conservative(check(p), "Degraded")

    def test_other_feature_eligibility_does_not_transfer(self):
        p = fixture()
        p["feature_eligibility_evidence"]["feature_id"] = "synthetic-other-feature"
        self.assert_conservative(check(p), "Degraded")

    def test_stale_eligibility_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_evidence"]["observed_at"] = "2026-10-25T00:00:00Z"
        self.assert_conservative(check(p), "Degraded")

    def test_future_eligibility_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_evidence"]["observed_at"] = "2026-10-26T01:00:00Z"
        self.assert_conservative(check(p), "Degraded")

    def test_unknown_offset_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_evidence"]["observed_at"] = "2026-10-25T23:00:00-00:00"
        self.assert_conservative(check(p), "Degraded")

    def test_missing_source_reference_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_evidence"]["source_reference"] = "Missing"
        self.assert_conservative(check(p), "Degraded")

    def test_padded_source_system_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_evidence"]["source_system"] = " synthetic:feature-eligibility "
        self.assert_conservative(check(p), "Degraded")

    def test_invalid_requested_feature_rejected(self):
        p = fixture()
        p["feature_eligibility_requirement"]["feature_id"] = "Unknown"
        with self.assertRaisesRegex(ValueError, "feature_eligibility_requirement.feature_id"):
            check(p)

    def test_requested_identity_must_match_expected_scope(self):
        p = fixture()
        p["feature_eligibility_requirement"]["campaign_id"] = "synthetic-campaign-b"
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            check(p)

    def test_exact_scope_is_required_for_feature_eligibility(self):
        p = fixture()
        del p["expected_scope"]["advertiser_account_id"]
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            check(p)

    def test_eligibility_without_requirement_is_invalid(self):
        p = fixture()
        del p["feature_eligibility_requirement"]
        with self.assertRaisesRegex(ValueError, "feature_eligibility"):
            check(p)

    def test_ineligible_feature_cannot_be_masked_by_verified_connector(self):
        p = fixture()
        p["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        r = check(p)
        self.assertEqual(r["requirements"][0]["gate_effect"], "pass")
        self.assert_conservative(r, "Blocked")


if __name__ == "__main__":
    unittest.main()
