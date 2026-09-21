import unittest

from scripts.compare_control_state import compare_control_state

REGISTRY_ID = "control-requirements@2026-09-21"
REQUIRED = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"]


def snapshot(base_bid: float, audience_evidence: dict) -> dict:
    states = {
        "base_bid": base_bid,
        "bidding_strategy": "dynamic_down_only",
        "placement_adjustment": {"top_of_search": 0, "product_pages": 0, "rest_of_search": 0},
        "audience_bid_adjustment": [{"audience_id": "aud-1", "bid_boost": 20}],
        "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
        "budget_or_pacing": {"base_average_daily_budget": 100, "effective_daily_budget": 100, "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility"},
        "targeting_or_routing": {"site_restriction": "ALL_ELIGIBLE"},
    }
    controls = []
    for control_type, state in states.items():
        item = {"control_type": control_type, "state": state, "effective_at": "2026-09-21T00:00:00Z", "evidence_status": "observed"}
        if control_type == "audience_bid_adjustment":
            item["collection_evidence"] = audience_evidence.copy()
        if control_type == "schedule_or_event_rule":
            complete = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
            item["nested_collection_evidence"] = {"schedule_rules": complete.copy(), "event_rules": complete.copy()}
        controls.append(item)
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
        "observed_at": "2026-09-21T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": REQUIRED, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_bid_change", "derivation_status": "Verified", "capability_snapshot_id": "fixture-capability-snapshot", "requirement_registry_id": REGISTRY_ID}},
        "controls": controls,
    }


class NonemptyCollectionCompletenessTests(unittest.TestCase):
    def test_nonempty_truncated_collection_cannot_isolate_treatment(self):
        incomplete = {"enumeration_status": "Partial", "pagination_status": "Truncated", "capability_status": "Supported"}
        result = compare_control_state(snapshot(1.0, incomplete), snapshot(1.2, incomplete), "base_bid")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("collection completeness" in reason for reason in result["reasons"]))

    def test_nonempty_complete_collection_can_isolate_treatment(self):
        complete = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
        result = compare_control_state(snapshot(1.0, complete), snapshot(1.2, complete), "base_bid")
        self.assertEqual(result["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
