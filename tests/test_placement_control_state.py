import unittest

from scripts.compare_control_state import compare_control_state

REGISTRY_ID = "control-requirements@2026-09-20"
REQUIRED = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing"]


def snapshot(base_bid, placement_state):
    states = {
        "base_bid": base_bid,
        "bidding_strategy": "dynamic_down_only",
        "placement_adjustment": placement_state,
        "audience_bid_adjustment": [],
        "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
        "budget_or_pacing": {"base_average_daily_budget": 100, "effective_daily_budget": 100, "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility"},
    }
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
        "observed_at": "2026-09-20T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": REQUIRED, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_bid_change", "derivation_status": "Verified", "requirement_registry_id": REGISTRY_ID}},
        "controls": [{"control_type": key, "state": value, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"} for key, value in states.items()],
    }


class PlacementControlStateTests(unittest.TestCase):
    def test_collapsed_placement_value_cannot_prove_all_sp_placement_surfaces(self):
        result = compare_control_state(snapshot(1.0, 0), snapshot(1.2, 0), "base_bid")
        self.assertEqual(result["classification"], "Unknown")

    def test_partial_placement_map_cannot_prove_all_sp_placement_surfaces(self):
        partial = {"top_of_search": 0, "product_pages": 0}
        result = compare_control_state(snapshot(1.0, partial), snapshot(1.2, partial), "base_bid")
        self.assertEqual(result["classification"], "Unknown")

    def test_complete_placement_surfaces_can_isolate_base_bid_change(self):
        complete = {"top_of_search": 0, "product_pages": 0, "rest_of_search": 0}
        result = compare_control_state(snapshot(1.0, complete), snapshot(1.2, complete), "base_bid")
        self.assertEqual(result["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
