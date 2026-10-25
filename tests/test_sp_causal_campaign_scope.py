"""A campaign-specific Sponsored Products causal review needs a campaign identity.

Read-only synthetic control-state evidence. A shared profile/marketplace does
not identify the same campaign when both snapshots omit campaign_id.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def comparison(surface="sponsored_products_bid_change"):
    before = snapshot(surface, base_bid=1.0, base_budget=100)
    after = snapshot(
        surface,
        base_bid=1.2 if surface == "sponsored_products_bid_change" else 1.0,
        base_budget=120 if surface == "sponsored_products_budget_change" else 100,
    )
    treatment = "base_bid" if surface == "sponsored_products_bid_change" else "budget_or_pacing"
    return before, after, treatment


class SponsoredProductsCampaignScopeTests(unittest.TestCase):
    def assert_missing_campaign_unknown(self, before, after, treatment):
        result = compare_control_state(before, after, treatment)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("campaign_id" in reason for reason in result["reasons"]), result)

    def test_bid_change_without_campaign_id_on_either_side_cannot_isolate(self):
        before, after, treatment = comparison()
        del before["scope"]["campaign_id"]
        del after["scope"]["campaign_id"]
        self.assert_missing_campaign_unknown(before, after, treatment)

    def test_budget_change_without_campaign_id_on_either_side_cannot_isolate(self):
        before, after, treatment = comparison("sponsored_products_budget_change")
        del before["scope"]["campaign_id"]
        del after["scope"]["campaign_id"]
        self.assert_missing_campaign_unknown(before, after, treatment)

    def test_explicit_null_campaign_ids_cannot_isolate(self):
        before, after, treatment = comparison()
        before["scope"]["campaign_id"] = None
        after["scope"]["campaign_id"] = None
        self.assert_missing_campaign_unknown(before, after, treatment)

    def test_entity_identity_does_not_substitute_for_campaign(self):
        before, after, treatment = comparison()
        for item in (before, after):
            item["scope"].pop("campaign_id")
            item["scope"]["entity_id"] = "keyword-123"
            item["scope"]["entity_type"] = "keyword"
        self.assert_missing_campaign_unknown(before, after, treatment)

    def test_valid_campaign_scope_retains_isolated_treatment(self):
        before, after, treatment = comparison()
        result = compare_control_state(before, after, treatment)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_legitimate_campaign_id_containing_unknown_word_is_not_placeholder(self):
        before, after, treatment = comparison()
        before["scope"]["campaign_id"] = "campaign-unknown-legacy-23"
        after["scope"]["campaign_id"] = "campaign-unknown-legacy-23"
        result = compare_control_state(before, after, treatment)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_one_sided_campaign_scope_remains_unknown(self):
        before, after, treatment = comparison()
        del before["scope"]["campaign_id"]
        self.assert_missing_campaign_unknown(before, after, treatment)


if __name__ == "__main__":
    unittest.main()
