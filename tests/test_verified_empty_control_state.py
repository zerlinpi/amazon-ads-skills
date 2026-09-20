import unittest

from scripts.compare_control_state import compare_control_state

REGISTRY_ID = "control-requirements@2026-09-20"


def sp_snapshot(base_bid: float, audience_complete=False):
    required = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing"]
    audience = {"control_type": "audience_bid_adjustment", "state": [], "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"}
    if audience_complete:
        audience["collection_evidence"] = {
            "enumeration_status": "Complete",
            "pagination_status": "Complete",
            "capability_status": "Supported",
        }
    controls = [
        {"control_type": "base_bid", "state": base_bid, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"},
        {"control_type": "bidding_strategy", "state": "dynamic_down_only", "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"},
        {"control_type": "placement_adjustment", "state": {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"},
        audience,
        {"control_type": "schedule_or_event_rule", "state": {"schedule_rules": [], "event_rules": []}, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"},
        {"control_type": "budget_or_pacing", "state": {"base_average_daily_budget": 100, "effective_daily_budget": 100, "active_budget_rules": [], "average_daily_budget_policy": "monthly_average_with_daily_flexibility"}, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"},
    ]
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-1"},
        "observed_at": "2026-09-20T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": required, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_bid_change", "derivation_status": "Verified", "capability_snapshot_id": "fixture-capability-snapshot", "requirement_registry_id": REGISTRY_ID}},
        "controls": controls,
    }


class VerifiedEmptyControlStateTests(unittest.TestCase):
    def test_empty_audience_adjustment_without_collection_completeness_is_unknown(self):
        before = sp_snapshot(1.0)
        after = sp_snapshot(1.2)
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Unknown")

    def test_verified_empty_audience_adjustment_can_isolate_treatment(self):
        before = sp_snapshot(1.0, audience_complete=True)
        after = sp_snapshot(1.2, audience_complete=True)
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
