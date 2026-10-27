"""Synthetic RED-first coverage: mid-window SP events need usable control values.

Only read-side comparator calls; no live Ads API, writes, or external imports.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture


def with_event(control_type, before_state, after_state):
    before, post, event = fixture("base_bid")
    event["control_type"] = control_type
    event["before_state"] = copy.deepcopy(before_state)
    event["after_state"] = copy.deepcopy(after_state)
    return before, post


class InterveningSPEventStateValuesTests(unittest.TestCase):
    def assert_class(self, control_type, before_state, after_state, expected):
        before, post = with_event(control_type, before_state, after_state)
        result = compare_control_state(before, post, "base_bid")
        self.assertEqual(result["classification"], expected, result)

    def test_base_bid_unverified_string_is_unknown(self):
        self.assert_class("base_bid", "unverified bid", 1.2, "Unknown")

    def test_base_bid_boolean_is_unknown(self):
        self.assert_class("base_bid", 1.0, True, "Unknown")

    def test_base_bid_negative_is_unknown(self):
        self.assert_class("base_bid", 1.0, -0.5, "Unknown")

    def test_video_modifier_unverified_string_is_unknown(self):
        self.assert_class("video_bid_adjustment", 0, "unverified", "Unknown")

    def test_video_modifier_negative_is_unknown(self):
        self.assert_class("video_bid_adjustment", 0, -10, "Unknown")

    def test_placement_unverified_numeric_field_is_unknown(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": "not measured", "rest_of_search": 0, "product_pages": 0},
            "Unknown")

    def test_placement_negative_modifier_is_unknown(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": -5, "rest_of_search": 0, "product_pages": 0},
            "Unknown")

    def test_placement_missing_surface_is_unknown(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": 20}, "Unknown")

    def test_placement_boolean_modifier_is_unknown(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": 20, "rest_of_search": 0, "product_pages": False},
            "Unknown")

    def test_audience_unverified_boost_is_unknown(self):
        self.assert_class("audience_bid_adjustment", [],
            [{"audience_id": "aud-1", "bid_boost": "not observed"}], "Unknown")

    def test_audience_negative_boost_is_unknown(self):
        self.assert_class("audience_bid_adjustment", [],
            [{"audience_id": "aud-1", "bid_boost": -5}], "Unknown")

    def test_audience_duplicate_identity_is_unknown(self):
        self.assert_class("audience_bid_adjustment", [],
            [{"audience_id": "aud-1", "bid_boost": 10},
             {"audience_id": "aud-1", "bid_boost": 20}], "Unknown")

    def test_strategy_unrecognized_state_is_unknown(self):
        self.assert_class("bidding_strategy", "dynamic_down_only", "unrecognized", "Unknown")

    def test_strategy_invalid_roas_guardrail_is_unknown(self):
        self.assert_class("bidding_strategy", "dynamic_down_only",
            {"strategy": "rule_based", "roas_guardrail": 0}, "Unknown")

    def test_valid_base_bid_event_remains_isolated(self):
        self.assert_class("base_bid", 1.0, 1.2, "Treatment Isolated")

    def test_valid_decimal_string_base_bid_remains_isolated(self):
        self.assert_class("base_bid", 1.0, "1.20", "Treatment Isolated")

    def test_valid_placement_event_remains_confounder(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": 20, "rest_of_search": 0, "product_pages": 0},
            "Confounded")

    def test_valid_audience_event_remains_confounder(self):
        self.assert_class("audience_bid_adjustment", [],
            [{"audience_id": "aud-1", "bid_boost": 20}], "Confounded")

    def test_valid_strategy_event_remains_confounder(self):
        self.assert_class("bidding_strategy", "dynamic_down_only", "fixed", "Confounded")

    def test_valid_video_event_remains_confounder(self):
        self.assert_class("video_bid_adjustment", 0, 10, "Confounded")

    def test_rule_based_strategy_alias_remains_compatible(self):
        self.assert_class("bidding_strategy", "dynamic_down_only",
            {"strategy": "rule-based", "roas_guardrail": 3}, "Confounded")

    def test_rule_based_strategy_case_remains_compatible(self):
        self.assert_class("bidding_strategy", "dynamic_down_only",
            {"strategy": "RULE_BASED", "roas_guardrail": "3.0"}, "Confounded")

    def test_valid_amazon_business_placement_remains_confounder(self):
        self.assert_class("placement_adjustment",
            {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
            {"top_of_search": 20, "rest_of_search": 0, "product_pages": 0,
             "amazon_business": 10}, "Confounded")


if __name__ == "__main__":
    unittest.main()
