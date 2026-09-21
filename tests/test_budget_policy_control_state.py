import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_ID = "control-requirements@2026-09-21"
REQUIRED = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"]
COMPLETE_COLLECTION = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}


def budget_snapshot(base_budget=100, effective_budget=100, policy="monthly_average_with_daily_flexibility"):
    states = {
        "base_bid": 1.0,
        "bidding_strategy": "dynamic_down_only",
        "placement_adjustment": {"top_of_search": 0, "product_pages": 0, "rest_of_search": 0},
        "audience_bid_adjustment": [],
        "schedule_or_event_rule": {"schedule_rules": [], "event_rules": []},
        "budget_or_pacing": {"base_average_daily_budget": base_budget, "effective_daily_budget": effective_budget, "active_budget_rules": [], "average_daily_budget_policy": policy},
        "targeting_or_routing": {"site_restriction": "ALL_ELIGIBLE"},
    }
    controls = []
    for control_type, state in states.items():
        item = {"control_type": control_type, "state": state, "effective_at": "2026-09-20T00:00:00Z", "evidence_status": "observed"}
        if control_type == "audience_bid_adjustment":
            item["collection_evidence"] = COMPLETE_COLLECTION.copy()
        controls.append(item)
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
        "observed_at": "2026-09-20T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {"required_control_types": REQUIRED, "coverage_status": "Complete", "requirement_provenance": {"decision_surface": "sponsored_products_budget_change", "derivation_status": "Verified", "capability_snapshot_id": "fixture-capability-snapshot", "requirement_registry_id": REGISTRY_ID, "evidence_note": "Deterministic Sponsored Products budget-policy fixture."}},
        "controls": controls,
    }


def control(snapshot, control_type):
    return next(item for item in snapshot["controls"] if item["control_type"] == control_type)


class BudgetPolicyControlStateTests(unittest.TestCase):
    def test_budget_change_contract_requires_average_daily_budget_policy_state(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        surface = registry["decision_surfaces"]["sponsored_products_budget_change"]
        notes = surface["notes"].lower()
        self.assertIn("average_daily_budget_policy", notes)
        self.assertIn("sponsored-ads-daily-budgeting-policy", " ".join(surface["evidence_basis"]))
        self.assertIn("unavailable rule or average_daily_budget_policy state keeps coverage incomplete/unknown", notes)

    def test_comparator_fails_closed_when_average_daily_budget_policy_is_missing(self):
        before = budget_snapshot(100, 100); after = budget_snapshot(120, 120)
        control(after, "budget_or_pacing")["state"].pop("average_daily_budget_policy")
        result = compare_control_state(before, after, "budget_or_pacing")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("average_daily_budget_policy" in reason for reason in result["reasons"]))

    def test_comparator_fails_closed_when_average_daily_budget_policy_is_unknown(self):
        result = compare_control_state(budget_snapshot(100, 100), budget_snapshot(120, 120, policy=None), "budget_or_pacing")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("average_daily_budget_policy" in reason for reason in result["reasons"]))

    def test_budget_change_cannot_isolate_with_collapsed_bid_rule_state(self):
        before = budget_snapshot(100, 100); after = budget_snapshot(120, 120)
        for snap in (before, after):
            rule = control(snap, "schedule_or_event_rule")
            rule["state"] = []
            rule["collection_evidence"] = COMPLETE_COLLECTION.copy()
        result = compare_control_state(before, after, "budget_or_pacing")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("bid-rule state" in reason for reason in result["reasons"]))

    def test_budget_change_can_isolate_when_both_bid_rule_surfaces_are_observed(self):
        result = compare_control_state(budget_snapshot(100, 100), budget_snapshot(120, 120), "budget_or_pacing")
        self.assertEqual(result["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
