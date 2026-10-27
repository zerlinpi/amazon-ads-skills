"""RED-first: one-sided optional SP event evidence cannot certify a transition.

Synthetic normalized read-only observations; no Amazon Ads API calls or writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture
from test_intervening_budget_routing_semantics import budget_event


class InterveningSPOptionalEvidenceParityTests(unittest.TestCase):
    def check(self, baseline, post, expected, field=None):
        result = compare_control_state(baseline, post, "base_bid")
        self.assertEqual(expected, result["classification"], result)
        if field is not None:
            self.assertIn(field, " | ".join(result["reasons"]), result)

    def budget_one_sided(self, field, side):
        baseline, post, event = budget_event()
        del event[side + "_state"][field]
        self.check(baseline, post, "Unknown", field)

    def placement_one_sided(self, side):
        baseline, post, event = fixture("placement_adjustment")
        event[side + "_state"]["amazon_business"] = 0
        self.check(baseline, post, "Confounded")

    def test_missing_before_base_budget_is_unknown(self):
        self.budget_one_sided("base_average_daily_budget", "before")

    def test_missing_after_base_budget_is_unknown(self):
        self.budget_one_sided("base_average_daily_budget", "after")

    def test_missing_before_effective_budget_is_unknown(self):
        self.budget_one_sided("effective_daily_budget", "before")

    def test_missing_after_effective_budget_is_unknown(self):
        self.budget_one_sided("effective_daily_budget", "after")

    def test_missing_before_budget_policy_is_unknown(self):
        self.budget_one_sided("average_daily_budget_policy", "before")

    def test_missing_after_budget_policy_is_unknown(self):
        self.budget_one_sided("average_daily_budget_policy", "after")

    def test_amazon_business_only_before_placement_remains_confounder(self):
        self.placement_one_sided("before")

    def test_amazon_business_only_after_placement_remains_confounder(self):
        self.placement_one_sided("after")

    def test_bid_surface_both_absent_optional_base_budget_remains_compatible(self):
        baseline, post, event = budget_event()
        for side in ("before_state", "after_state"):
            del event[side]["base_average_daily_budget"]
        self.check(baseline, post, "Confounded")

    def test_bid_surface_both_absent_optional_policy_remains_compatible(self):
        baseline, post, event = budget_event()
        for side in ("before_state", "after_state"):
            del event[side]["average_daily_budget_policy"]
        self.check(baseline, post, "Confounded")

    def test_both_absent_amazon_business_placement_remains_compatible(self):
        baseline, post, _ = fixture("placement_adjustment")
        self.check(baseline, post, "Confounded")

    def test_both_present_amazon_business_placement_remains_compatible(self):
        baseline, post, event = fixture("placement_adjustment")
        event["before_state"]["amazon_business"] = 0
        event["after_state"]["amazon_business"] = 0
        self.check(baseline, post, "Confounded")


if __name__ == "__main__":
    unittest.main()
