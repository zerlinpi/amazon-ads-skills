"""RED-first tests: an unverified SP bidding strategy cannot prove causal isolation.

Read-only synthetic fixtures. The accepted strategy labels are repository-normalized
evidence, not a claim about exact Amazon Ads API enum values.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_strategy(before_strategy, after_strategy=None, *, budget_treatment=False):
    if after_strategy is None:
        after_strategy = before_strategy
    baseline = snapshot(1.0, dict(PLACEMENTS), bidding_strategy=before_strategy)
    post = snapshot(1.2, dict(PLACEMENTS), bidding_strategy=after_strategy)
    if budget_treatment:
        for record, budget in ((baseline, 100), (post, 120)):
            record["coverage"]["requirement_provenance"]["decision_surface"] = "sponsored_products_budget_change"
            next(c for c in record["controls"] if c["control_type"] == "base_bid")["state"] = 1.0
            state = next(c for c in record["controls"] if c["control_type"] == "budget_or_pacing")["state"]
            state["base_average_daily_budget"] = budget
            state["effective_daily_budget"] = budget
        treatment = "budget_or_pacing"
    else:
        treatment = "base_bid"
    return compare_control_state(baseline, post, treatment)


class SponsoredProductsBiddingStrategyEvidenceTests(unittest.TestCase):
    def assert_unknown(self, value, *, budget_treatment=False):
        result = compare_strategy(value, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("bidding strategy" in reason.replace("_", " ") for reason in result["reasons"]), result)

    def test_unknown_label(self):
        self.assert_unknown("Unknown")

    def test_unsupported_label(self):
        self.assert_unknown("Unsupported")

    def test_partial_label(self):
        self.assert_unknown("Partial")

    def test_missing_label(self):
        self.assert_unknown("Missing")

    def test_unavailable_label(self):
        self.assert_unknown("Unavailable")

    def test_blank_label(self):
        self.assert_unknown("")

    def test_whitespace_label(self):
        self.assert_unknown("   ")

    def test_boolean_false(self):
        self.assert_unknown(False)

    def test_boolean_true(self):
        self.assert_unknown(True)

    def test_numeric_zero_not_strategy(self):
        self.assert_unknown(0)

    def test_list_placeholder(self):
        self.assert_unknown(["dynamic_down_only"])

    def test_structured_unknown(self):
        self.assert_unknown({"status": "Unknown"})

    def test_unrecognized_enum(self):
        self.assert_unknown("future_unverified_strategy")

    def test_unknown_unchanged_during_budget_treatment(self):
        self.assert_unknown("Unknown", budget_treatment=True)

    def test_valid_dynamic_down_only(self):
        self.assertEqual(compare_strategy("dynamic_down_only")["classification"], "Treatment Isolated")

    def test_valid_dynamic_up_and_down(self):
        self.assertEqual(compare_strategy("dynamic_up_and_down")["classification"], "Treatment Isolated")

    def test_valid_fixed(self):
        self.assertEqual(compare_strategy("fixed")["classification"], "Treatment Isolated")

    def test_valid_rule_based_with_observed_roas_guardrail(self):
        state = {"strategy": "rule_based", "roas_guardrail": 3}
        self.assertEqual(compare_strategy(state)["classification"], "Treatment Isolated")

    def test_valid_legacy_hyphen_alias(self):
        self.assertEqual(compare_strategy("dynamic-down-only")["classification"], "Treatment Isolated")

    def test_strategy_change_is_confounded(self):
        self.assertEqual(compare_strategy("dynamic_down_only", "fixed")["classification"], "Confounded")

    def test_valid_strategy_during_budget_treatment(self):
        self.assertEqual(compare_strategy("dynamic_down_only", budget_treatment=True)["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
