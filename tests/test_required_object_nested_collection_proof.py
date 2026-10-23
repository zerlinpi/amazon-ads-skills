"""Fail-closed regressions for nested collections in registry-required object controls.

Synthetic observations only. No live connector or Amazon Ads writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_placement_control_state import snapshot

COMPLETE = {
    "enumeration_status": "Complete",
    "pagination_status": "Complete",
    "capability_status": "Supported",
}
PLACEMENTS = {"top_of_search": 0, "rest_of_search": 0, "product_pages": 0}


def compare_object(control_type, state, before_evidence=None, after_evidence=None,
                   post_state=None, post_bid=1.2):
    before = snapshot(1.0, PLACEMENTS)
    after = snapshot(post_bid, PLACEMENTS)
    for record, value, evidence in (
        (before, state, before_evidence),
        (after, state if post_state is None else post_state, after_evidence),
    ):
        control = next(c for c in record["controls"] if c["control_type"] == control_type)
        control["state"] = copy.deepcopy(value)
        if evidence is not None:
            control["nested_collection_evidence"] = copy.deepcopy(evidence)
    return compare_control_state(before, after, "base_bid")


class RequiredObjectNestedCollectionProofTests(unittest.TestCase):
    def test_routing_empty_list_without_proof_is_unknown(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": []}
        self.assertEqual(compare_object("targeting_or_routing", state)["classification"], "Unknown")

    def test_routing_nonempty_list_without_proof_is_unknown(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": [{"id": "r1"}]}
        self.assertEqual(compare_object("targeting_or_routing", state)["classification"], "Unknown")

    def test_placement_extra_list_without_proof_is_unknown(self):
        state = {**PLACEMENTS, "marketplace_overrides": []}
        self.assertEqual(compare_object("placement_adjustment", state)["classification"], "Unknown")

    def test_routing_partial_pagination_is_unknown(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": []}
        evidence = {"routing_rules": {**COMPLETE, "pagination_status": "Truncated"}}
        self.assertEqual(compare_object("targeting_or_routing", state, evidence, evidence)["classification"], "Unknown")

    def test_routing_one_sided_proof_is_unknown(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": []}
        self.assertEqual(compare_object("targeting_or_routing", state, {"routing_rules": COMPLETE})["classification"], "Unknown")

    def test_deep_routing_list_needs_own_proof(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing": {"rules": []}}
        self.assertEqual(compare_object("targeting_or_routing", state)["classification"], "Unknown")

    def test_complete_direct_routing_list_can_isolate_bid(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": []}
        evidence = {"routing_rules": COMPLETE}
        self.assertEqual(compare_object("targeting_or_routing", state, evidence, evidence)["classification"], "Treatment Isolated")

    def test_complete_deep_routing_list_can_isolate_bid(self):
        state = {"site_restriction": "ALL_ELIGIBLE", "routing": {"rules": []}}
        evidence = {"/routing/rules": COMPLETE}
        self.assertEqual(compare_object("targeting_or_routing", state, evidence, evidence)["classification"], "Treatment Isolated")

    def test_complete_routing_change_confounds_bid(self):
        before = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": ["r1"]}
        after = {"site_restriction": "ALL_ELIGIBLE", "routing_rules": ["r2"]}
        evidence = {"routing_rules": COMPLETE}
        self.assertEqual(compare_object("targeting_or_routing", before, evidence, evidence, post_state=after)["classification"], "Confounded")

    def test_required_budget_rule_list_without_proof_is_unknown(self):
        before, after = snapshot(1.0, PLACEMENTS), snapshot(1.2, PLACEMENTS)
        for record in (before, after):
            budget = next(c for c in record["controls"] if c["control_type"] == "budget_or_pacing")
            budget.pop("nested_collection_evidence", None)
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Unknown")

    def test_required_budget_rule_list_with_proof_can_isolate_bid(self):
        before, after = snapshot(1.0, PLACEMENTS), snapshot(1.2, PLACEMENTS)
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"],
                         "Treatment Isolated")

    def test_flat_required_routing_object_remains_isolated(self):
        state = {"site_restriction": "ALL_ELIGIBLE"}
        self.assertEqual(compare_object("targeting_or_routing", state)["classification"], "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
