"""Fail closed when a Global SP campaign-state gate receives unverified intent.

An otherwise valid campaign state readback must not certify an ad-group/target
bid change or an arbitrary future expected_* field that this gate never reads.
"""
import unittest

from test_global_sp_readback_evidence import evaluate, fixture
from test_global_sp_marketplace_budget_readback import budget_fixture


class GlobalSpUnverifiedIntentTests(unittest.TestCase):
    def test_ad_group_marketplace_bid_change_not_state_confirmed(self):
        evidence = fixture()
        evidence["request"]["expected_ad_group_bids"] = {
            "synthetic-adgroup-1": {"US": {"currency_code": "USD", "amount": "0.98"}}
        }
        self.assertEqual(evaluate(evidence)["application_status"], "Unknown")

    def test_target_marketplace_bid_change_not_state_confirmed(self):
        evidence = fixture()
        evidence["request"]["expected_target_bids"] = {
            "synthetic-target-1": {"GB": {"currency_code": "GBP", "amount": "0.57"}}
        }
        self.assertEqual(evaluate(evidence)["application_status"], "Unknown")

    def test_marketplace_bid_change_not_state_confirmed(self):
        evidence = fixture()
        evidence["request"]["expected_marketplace_bids"] = {
            "US": {"currency_code": "USD", "amount": "0.98"},
            "GB": {"currency_code": "GBP", "amount": "0.57"},
        }
        self.assertEqual(evaluate(evidence)["application_status"], "Unknown")

    def test_empty_unsupported_expectation_not_silently_ignored(self):
        evidence = fixture()
        evidence["request"]["expected_marketplace_bids"] = {}
        self.assertEqual(evaluate(evidence)["application_status"], "Unknown")

    def test_future_unrecognized_expected_field_not_confirmed(self):
        evidence = fixture()
        evidence["request"]["expected_placement_adjustments"] = {"US": 20}
        self.assertEqual(evaluate(evidence)["application_status"], "Unknown")

    def test_supported_campaign_state_only_still_confirmed(self):
        self.assertEqual(evaluate(fixture())["application_status"], "Confirmed")

    def test_supported_budget_and_state_still_confirmed(self):
        self.assertEqual(evaluate(budget_fixture())["application_status"], "Confirmed")

    def test_non_intent_request_metadata_remains_compatible(self):
        evidence = fixture()
        evidence["request"]["request_note"] = "synthetic external tracking"
        self.assertEqual(evaluate(evidence)["application_status"], "Confirmed")

    def test_partial_receipt_remains_partial_with_unverified_intent(self):
        evidence = fixture()
        evidence["request"]["expected_target_bids"] = {"synthetic-target-1": {"US": "0.98"}}
        evidence["receipt"]["success"] = []
        evidence["receipt"]["partialSuccess"] = [{"index": 0}]
        self.assertEqual(evaluate(evidence)["application_status"], "Partial")


if __name__ == "__main__":
    unittest.main()
