"""RED-first evidence tests: a complete audience collection still needs valid members."""
import copy
import unittest

from scripts.compare_control_state import compare_control_state

REQUIRED = [
    "base_bid", "bidding_strategy", "placement_adjustment",
    "audience_bid_adjustment", "video_bid_adjustment", "schedule_or_event_rule",
    "budget_or_pacing", "targeting_or_routing",
]
COMPLETE = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}


def snapshot(bid, audience):
    states = {
        "base_bid": bid,
        "bidding_strategy": "dynamic_down_only",
        "placement_adjustment": {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0},
        "audience_bid_adjustment": copy.deepcopy(audience),
        "video_bid_adjustment": 0,
        "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
        "budget_or_pacing": {
            "base_average_daily_budget": 100, "effective_daily_budget": 100,
            "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility",
        },
        "targeting_or_routing": {"site_restriction": "ALL_ELIGIBLE"},
    }
    controls = []
    for control_type, state in states.items():
        item = {"control_type": control_type, "state": state, "effective_at": "2026-10-24T00:00:00Z", "evidence_status": "observed"}
        if control_type == "audience_bid_adjustment":
            item["collection_evidence"] = COMPLETE.copy()
        if control_type in {"schedule_or_event_rule", "budget_or_pacing"}:
            fields = ("schedule_rules", "event_rules") if control_type == "schedule_or_event_rule" else ("active_budget_rules",)
            item["nested_collection_evidence"] = {field: COMPLETE.copy() for field in fields}
        controls.append(item)
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "c1"},
        "observed_at": "2026-10-24T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": REQUIRED,
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "sponsored_products_bid_change",
                "derivation_status": "Verified",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": controls,
    }


def classify(before_audience, after_audience=None):
    if after_audience is None:
        after_audience = before_audience
    return compare_control_state(
        snapshot(1.0, before_audience),
        snapshot(1.2, after_audience),
        "base_bid",
    )["classification"]


class SponsoredProductsAudienceMemberEvidenceTests(unittest.TestCase):
    def test_invalid_unknown_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "Unknown"}]), "Unknown")

    def test_invalid_unsupported_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "Unsupported"}]), "Unknown")

    def test_invalid_partial_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "Partial"}]), "Unknown")

    def test_invalid_missing_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "Missing"}]), "Unknown")

    def test_invalid_blank_boost_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": ""}]), "Unknown")

    def test_invalid_boolean_false_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": False}]), "Unknown")

    def test_invalid_boolean_true_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": True}]), "Unknown")

    def test_invalid_negative_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": -1}]), "Unknown")

    def test_invalid_infinity_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": float("inf")}]), "Unknown")

    def test_invalid_nan_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": float("nan")}]), "Unknown")

    def test_invalid_percent_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "15%"}]), "Unknown")

    def test_invalid_object_boost_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": {"status": "Unknown"}}]), "Unknown")

    def test_invalid_array_boost_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": [10]}]), "Unknown")

    def test_invalid_null_boost_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": None}]), "Unknown")

    def test_invalid_missing_boost_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a"}]), "Unknown")

    def test_invalid_missing_id_cannot_isolate_bid(self):
        self.assertEqual(classify([{"bid_boost": 10}]), "Unknown")

    def test_invalid_empty_id_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "", "bid_boost": 10}]), "Unknown")

    def test_invalid_whitespace_id_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "   ", "bid_boost": 10}]), "Unknown")

    def test_invalid_numeric_id_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": 123, "bid_boost": 10}]), "Unknown")

    def test_invalid_duplicate_id_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}, {"audience_id": "a", "bid_boost": 20}]), "Unknown")

    def test_invalid_malformed_item_cannot_isolate_bid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}, "Unknown"]), "Unknown")

    def test_one_sided_invalid_audience_member_is_unknown(self):
        valid = [{"audience_id": "a", "bid_boost": 10}]
        invalid = [{"audience_id": "a", "bid_boost": "Unknown"}]
        self.assertEqual(classify(valid, invalid), "Unknown")

    def test_complete_valid_single_audience_is_isolated(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}]), "Treatment Isolated")

    def test_complete_valid_multiple_audiences_is_isolated(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}, {"audience_id": "b", "bid_boost": 20}]), "Treatment Isolated")

    def test_observed_zero_is_not_missing(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 0}]), "Treatment Isolated")

    def test_plain_decimal_string_is_valid(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": "12.50"}]), "Treatment Isolated")

    def test_verified_empty_collection_is_valid(self):
        self.assertEqual(classify([]), "Treatment Isolated")

    def test_real_audience_modifier_change_is_confounded(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}], [{"audience_id": "a", "bid_boost": 20}]), "Confounded")

    def test_real_audience_membership_change_is_confounded(self):
        self.assertEqual(classify([{"audience_id": "a", "bid_boost": 10}], [{"audience_id": "b", "bid_boost": 10}]), "Confounded")


if __name__ == "__main__":
    unittest.main()
