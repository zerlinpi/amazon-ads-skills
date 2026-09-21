import json
import unittest
from pathlib import Path

from scripts.compare_control_state import compare_control_state

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_ID = "control-requirements@2026-09-21"
REQUIRED = ["base_bid", "bidding_strategy", "placement_adjustment", "audience_bid_adjustment", "schedule_or_event_rule", "budget_or_pacing", "targeting_or_routing"]
COMPLETE = {"enumeration_status": "Complete", "pagination_status": "Complete", "capability_status": "Supported"}
TRUNCATED = {"enumeration_status": "Partial", "pagination_status": "Truncated", "capability_status": "Supported"}


def snapshot(surface: str, base_bid: float = 1.0, base_budget: float = 100.0, rule_evidence=None, budget_rule_evidence=None) -> dict:
    controls = [
        {"control_type": "base_bid", "state": base_bid, "effective_at": "2026-09-21T00:00:00Z", "evidence_status": "observed"},
        {"control_type": "bidding_strategy", "state": "dynamic_down_only", "effective_at": "2026-09-21T00:00:00Z", "evidence_status": "observed"},
        {"control_type": "placement_adjustment", "state": {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}, "effective_at": "2026-09-21T00:00:00Z", "evidence_status": "observed"},
        {
            "control_type": "audience_bid_adjustment",
            "state": [],
            "effective_at": "2026-09-21T00:00:00Z",
            "evidence_status": "observed",
            "collection_evidence": COMPLETE.copy(),
        },
        {
            "control_type": "schedule_or_event_rule",
            "state": {
                "schedule_rules": [{"rule_id": "schedule-1", "bid_increase": 10}],
                "event_rules": [],
            },
            "effective_at": "2026-09-21T00:00:00Z",
            "evidence_status": "observed",
            "nested_collection_evidence": rule_evidence or {
                "schedule_rules": COMPLETE.copy(),
                "event_rules": COMPLETE.copy(),
            },
        },
        {
            "control_type": "budget_or_pacing",
            "state": {
                "base_average_daily_budget": base_budget,
                "effective_daily_budget": base_budget,
                "active_budget_rules": [{"rule_id": "budget-rule-1", "increase_percent": 20}],
                "average_daily_budget_policy": "monthly_average_with_daily_flexibility",
            },
            "effective_at": "2026-09-21T00:00:00Z",
            "evidence_status": "observed",
            "nested_collection_evidence": budget_rule_evidence or {
                "active_budget_rules": COMPLETE.copy(),
            },
        },
        {
            "control_type": "targeting_or_routing",
            "state": {"site_restriction": "ALL_ELIGIBLE"},
            "effective_at": "2026-09-21T00:00:00Z",
            "evidence_status": "observed",
        },
    ]
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "p1", "campaign_id": "sp-campaign-1"},
        "observed_at": "2026-09-21T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": REQUIRED,
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": surface,
                "derivation_status": "Verified",
                "capability_snapshot_id": "fixture-capability-snapshot",
                "requirement_registry_id": REGISTRY_ID,
            },
        },
        "controls": controls,
    }


class NestedCollectionCompletenessTests(unittest.TestCase):
    def test_schema_exposes_nested_collection_evidence_map(self):
        schema = json.loads((ROOT / "schemas/control-state-snapshot.json").read_text(encoding="utf-8"))
        control = schema["properties"]["controls"]["items"]
        nested = control["properties"]["nested_collection_evidence"]
        self.assertEqual(nested["type"], "object")
        self.assertEqual(nested["additionalProperties"]["$ref"], "#/$defs/collectionEvidence")

    def test_truncated_schedule_rule_collection_cannot_isolate_bid_change(self):
        nested = {"schedule_rules": TRUNCATED.copy(), "event_rules": COMPLETE.copy()}
        before = snapshot("sponsored_products_bid_change", base_bid=1.0, rule_evidence=nested)
        after = snapshot("sponsored_products_bid_change", base_bid=1.2, rule_evidence=nested)
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("schedule_rules" in reason and "completeness" in reason for reason in result["reasons"]))

    def test_complete_nested_rule_collections_can_isolate_bid_change(self):
        before = snapshot("sponsored_products_bid_change", base_bid=1.0)
        after = snapshot("sponsored_products_bid_change", base_bid=1.2)
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Treatment Isolated")

    def test_truncated_active_budget_rules_cannot_isolate_budget_change(self):
        nested = {"active_budget_rules": TRUNCATED.copy()}
        before = snapshot("sponsored_products_budget_change", base_budget=100.0, budget_rule_evidence=nested)
        after = snapshot("sponsored_products_budget_change", base_budget=120.0, budget_rule_evidence=nested)
        result = compare_control_state(before, after, "budget_or_pacing")
        self.assertEqual(result["classification"], "Unknown")
        self.assertTrue(any("active_budget_rules" in reason and "completeness" in reason for reason in result["reasons"]))

    def test_complete_nested_budget_rule_collection_can_isolate_budget_change(self):
        before = snapshot("sponsored_products_budget_change", base_budget=100.0)
        after = snapshot("sponsored_products_budget_change", base_budget=120.0)
        self.assertEqual(compare_control_state(before, after, "budget_or_pacing")["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
