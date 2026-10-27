"""RED-first: observed SP mid-window budget and routing events need usable state.

All fixtures are synthetic, read-only and do not invoke Amazon Ads.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture


def budget_event(*, budget_surface=False):
    before, post, event = fixture("budget_or_pacing")
    if budget_surface:
        for snap in (before, post):
            snap["coverage"]["requirement_provenance"]["decision_surface"] = "sponsored_products_budget_change"
        next(c for c in post["controls"] if c["control_type"] == "base_bid")["state"] = 1.0
        budget = next(c for c in post["controls"] if c["control_type"] == "budget_or_pacing")["state"]
        budget["base_average_daily_budget"] = 120
        budget["effective_daily_budget"] = 120
    return before, post, event


def routing_event():
    before, post, event = fixture("base_bid")
    event["control_type"] = "targeting_or_routing"
    route = next(c for c in before["controls"] if c["control_type"] == "targeting_or_routing")["state"]
    event["before_state"] = copy.deepcopy(route)
    event["after_state"] = {"site_restriction": "AMAZON_BUSINESS"}
    return before, post, event


class InterveningBudgetRoutingSemanticsTests(unittest.TestCase):
    def check(self, before, post, expected, treatment="base_bid"):
        result = compare_control_state(before, post, treatment)
        self.assertEqual(result["classification"], expected, result)

    def test_invalid_negative_budget_amount_is_unknown(self):
        b, p, e = budget_event()
        e["after_state"]["base_average_daily_budget"] = -10
        self.check(b, p, "Unknown")

    def test_boolean_effective_budget_is_unknown(self):
        b, p, e = budget_event()
        e["after_state"]["effective_daily_budget"] = False
        self.check(b, p, "Unknown")

    def test_invalid_budget_policy_object_is_unknown(self):
        b, p, e = budget_event()
        e["after_state"]["average_daily_budget_policy"] = {}
        self.check(b, p, "Unknown")

    def test_budget_surface_missing_base_budget_is_unknown(self):
        b, p, e = budget_event(budget_surface=True)
        del e["after_state"]["base_average_daily_budget"]
        self.check(b, p, "Unknown", "budget_or_pacing")

    def test_budget_surface_missing_policy_is_unknown(self):
        b, p, e = budget_event(budget_surface=True)
        del e["after_state"]["average_daily_budget_policy"]
        self.check(b, p, "Unknown", "budget_or_pacing")

    def test_routing_unmapped_site_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"]["site_restriction"] = "NEW_SITE"
        self.check(b, p, "Unknown")

    def test_routing_missing_site_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"] = {"unmapped": "some-routing-value"}
        self.check(b, p, "Unknown")

    def test_routing_unknown_retailer_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"]["retailer_scope"] = "MIXED"
        self.check(b, p, "Unknown")

    def test_routing_structured_site_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"]["site_restriction"] = {"site": "AMAZON_BUSINESS"}
        self.check(b, p, "Unknown")

    def test_routing_array_retailer_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"]["retailer_scope"] = ["AMAZON_STORE"]
        self.check(b, p, "Unknown")

    def test_across_retailers_business_exclusive_contradiction_is_unknown(self):
        b, p, e = routing_event()
        e["after_state"]["retailer_scope"] = "ACROSS_RETAILERS"
        self.check(b, p, "Unknown")

    def test_one_sided_retailer_scope_is_not_verified_transition(self):
        b, p, e = routing_event()
        e["after_state"]["retailer_scope"] = "AMAZON_STORE"
        self.check(b, p, "Unknown")

    def test_valid_budget_event_remains_confounder(self):
        b, p, _ = budget_event()
        self.check(b, p, "Confounded")

    def test_valid_budget_surface_event_remains_isolated(self):
        b, p, _ = budget_event(budget_surface=True)
        self.check(b, p, "Treatment Isolated", "budget_or_pacing")

    def test_valid_routing_event_remains_confounder(self):
        b, p, _ = routing_event()
        self.check(b, p, "Confounded")

    def test_valid_retailer_scope_transition_remains_confounder(self):
        b, p, e = routing_event()
        e["before_state"]["retailer_scope"] = "AMAZON_STORE"
        e["after_state"]["retailer_scope"] = "ACROSS_RETAILERS"
        e["after_state"]["site_restriction"] = "ALL_ELIGIBLE"
        self.check(b, p, "Confounded")


if __name__ == "__main__":
    unittest.main()
