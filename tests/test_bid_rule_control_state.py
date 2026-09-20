import unittest

from scripts.compare_control_state import compare_control_state

REGISTRY_ID = "control-requirements@2026-09-20"
REQUIRED = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing"]
COMPLETE_COLLECTION = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}


def snapshot(base_bid, rule_state):
    states = {
        "base_bid": base_bid,
        "bidding_strategy": "dynamic_down_only",
        "placement_adjustment": {"top_of_search": 0, "product_pages": 0, "rest_of_search": 0},
        "audience_bid_adjustment": [],
        "schedule_or_event_rule": rule_state,
        "budget_or_pacing": {"base_average_daily_budget": 100, "effective_daily_budget": 100, "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility"},
    }
    controls = []
    for key, value in states.items():
        item = {"control_type": key, "state": value, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"}
        if key == "audience_bid_adjustment" or (key == "schedule_or_event_rule" and isinstance(value, list)):
            item["collection_evidence"] = COMPLETE_COLLECTION.copy()
        controls.append(item)
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
        "observed_at": "2026-09-20T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": REQUIRED, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_bid_change", "derivation_status": "Verified", "requirement_registry_id": REGISTRY_ID}},
        "controls": controls,
    }


class BidRuleControlStateTests(unittest.TestCase):
    def test_collapsed_rule_list_cannot_prove_schedule_and_event_rule_coverage(self):
        result = compare_control_state(snapshot(1.0, []), snapshot(1.2, []), "base_bid")
        self.assertEqual(result["classification"], "Unknown")

    def test_separate_rule_surfaces_can_isolate_base_bid_change(self):
        rules = {"schedule_rules": [], "event_rules": []}
        result = compare_control_state(snapshot(1.0, rules), snapshot(1.2, rules), "base_bid")
        self.assertEqual(result["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
