"""Fail closed on invalid Sponsored Products base-bid value evidence.

Synthetic read-only control-state tests; never execute Amazon Ads writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot


PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def bid_comparison(before_value, after_value, *, surface="sponsored_products_bid_change"):
    baseline = snapshot(1.0, dict(PLACEMENTS))
    post = snapshot(1.2, dict(PLACEMENTS))
    baseline["coverage"]["requirement_provenance"]["decision_surface"] = surface
    post["coverage"]["requirement_provenance"]["decision_surface"] = surface
    for record, value in ((baseline, before_value), (post, after_value)):
        next(item for item in record["controls"] if item["control_type"] == "base_bid")["state"] = value
    if surface == "sponsored_products_budget_change":
        # Budget is the treatment; the invalid bid is an unchanged confounder.
        for record, amount in ((baseline, 100), (post, 120)):
            state = next(item for item in record["controls"] if item["control_type"] == "budget_or_pacing")["state"]
            state["base_average_daily_budget"] = amount
            state["effective_daily_budget"] = amount
        return compare_control_state(baseline, post, "budget_or_pacing")
    return compare_control_state(baseline, post, "base_bid")


class BaseBidValueEvidenceTests(unittest.TestCase):
    def assert_unknown(self, before, after=1.2, *, surface="sponsored_products_bid_change"):
        result = bid_comparison(before, after, surface=surface)
        self.assertEqual(result["classification"], "Unknown", result)
        self.assertTrue(any("base_bid" in reason for reason in result["reasons"]), result)

    def test_unknown_label(self):
        self.assert_unknown("Unknown")

    def test_unsupported_label(self):
        self.assert_unknown("Unsupported")

    def test_partial_label(self):
        self.assert_unknown("Partial")

    def test_missing_label(self):
        self.assert_unknown("Missing")

    def test_boolean_false(self):
        self.assert_unknown(False)

    def test_boolean_true(self):
        self.assert_unknown(True)

    def test_negative_bid(self):
        self.assert_unknown(-1)

    def test_infinity_bid(self):
        self.assert_unknown(float("inf"))

    def test_negative_infinity_bid(self):
        self.assert_unknown(float("-inf"))

    def test_nan_bid(self):
        self.assert_unknown(float("nan"))

    def test_percentage_string(self):
        self.assert_unknown("15%")

    def test_structured_unknown(self):
        self.assert_unknown({"status": "Unknown"})

    def test_list_placeholder(self):
        self.assert_unknown(["Unknown"])

    def test_empty_string(self):
        self.assert_unknown("")

    def test_missing_null(self):
        self.assert_unknown(None)

    def test_invalid_post_value(self):
        self.assert_unknown(1.0, "Unsupported")

    def test_invalid_unchanged_bid_during_budget_treatment(self):
        self.assert_unknown("Unknown", "Unknown", surface="sponsored_products_budget_change")

    def test_valid_numeric_bid_change_is_isolated(self):
        self.assertEqual(bid_comparison(1.0, 1.2)["classification"], "Treatment Isolated")

    def test_plain_decimal_string_is_valid(self):
        self.assertEqual(bid_comparison("1.00", "1.20")["classification"], "Treatment Isolated")

    def test_observed_zero_not_missing(self):
        self.assertEqual(bid_comparison(0, 1.2)["classification"], "Treatment Isolated")

    def test_valid_bid_during_budget_treatment(self):
        self.assertEqual(bid_comparison(1.0, 1.0, surface="sponsored_products_budget_change")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
