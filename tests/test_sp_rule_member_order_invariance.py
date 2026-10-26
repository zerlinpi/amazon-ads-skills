"""Deterministic replay: rule collection order is not a control-state change.

Normalized Sponsored Products schedule/event/budget rule collections are
identity-keyed by rule_id. This does not prove continuous rule execution or
claim a vendor ordering contract. Synthetic read-only fixtures only.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def compare_members(field, before_members, after_members, *, budget_treatment=False):
    surface = "sponsored_products_budget_change" if budget_treatment else "sponsored_products_bid_change"
    before = snapshot(surface, base_bid=1.0, base_budget=100)
    after = snapshot(
        surface,
        base_bid=1.0 if budget_treatment else 1.2,
        base_budget=120 if budget_treatment else 100,
    )
    control_type = "budget_or_pacing" if field == "active_budget_rules" else "schedule_or_event_rule"
    for record, members in ((before, before_members), (after, after_members)):
        control = next(c for c in record["controls"] if c["control_type"] == control_type)
        control["state"][field] = copy.deepcopy(members)
    treatment = "budget_or_pacing" if budget_treatment else "base_bid"
    return compare_control_state(before, after, treatment)


def bid_rules():
    return [
        {"rule_id": "rule-a", "bid_increase": 10, "activation_status": "active"},
        {"rule_id": "rule-b", "bid_increase": 20, "activation_status": "scheduled"},
    ]


def budget_rules():
    return [
        {"rule_id": "budget-a", "increase_percent": 10, "activation_status": "active"},
        {"rule_id": "budget-b", "increase_percent": 20, "activation_status": "scheduled"},
    ]


class SponsoredProductsRuleOrderInvarianceTests(unittest.TestCase):
    def assert_isolated(self, result):
        self.assertEqual(result["classification"], "Treatment Isolated", result)
        self.assertEqual(result["changed_controls"], ["base_bid"] if "base_bid" in result["changed_controls"] else ["budget_or_pacing"], result)

    def test_schedule_rules_reordered_are_same_control(self):
        rows = bid_rules()
        self.assert_isolated(compare_members("schedule_rules", rows, list(reversed(rows))))

    def test_event_rules_reordered_are_same_control(self):
        rows = bid_rules()
        self.assert_isolated(compare_members("event_rules", rows, list(reversed(rows))))

    def test_budget_rules_reordered_during_bid_change_are_same_control(self):
        rows = budget_rules()
        self.assert_isolated(compare_members("active_budget_rules", rows, list(reversed(rows))))

    def test_budget_rules_reordered_during_budget_change_are_same_control(self):
        rows = budget_rules()
        self.assert_isolated(compare_members("active_budget_rules", rows, list(reversed(rows)), budget_treatment=True))

    def test_rule_modifier_change_remains_confounder_despite_reorder(self):
        rows = bid_rules()
        changed = list(reversed(copy.deepcopy(rows)))
        changed[0]["bid_increase"] = 30
        result = compare_members("schedule_rules", rows, changed)
        self.assertEqual(result["classification"], "Confounded", result)
        self.assertIn("schedule_or_event_rule", result["changed_controls"])

    def test_activation_status_change_remains_confounder_despite_reorder(self):
        rows = bid_rules()
        changed = list(reversed(copy.deepcopy(rows)))
        changed[0]["activation_status"] = "inactive"
        result = compare_members("event_rules", rows, changed)
        self.assertEqual(result["classification"], "Confounded", result)

    def test_added_rule_remains_confounder(self):
        rows = bid_rules()
        changed = list(reversed(rows)) + [{"rule_id": "rule-c", "bid_increase": 5}]
        result = compare_members("schedule_rules", rows, changed)
        self.assertEqual(result["classification"], "Confounded", result)

    def test_duplicate_rule_id_remains_unknown(self):
        rows = bid_rules()
        changed = [rows[0], copy.deepcopy(rows[0])]
        result = compare_members("schedule_rules", rows, changed)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_one_sided_activation_status_remains_unknown(self):
        rows = bid_rules()
        changed = copy.deepcopy(rows)
        del changed[0]["activation_status"]
        result = compare_members("event_rules", rows, changed)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_other_material_list_order_stays_significant(self):
        before = snapshot("sponsored_products_bid_change", base_bid=1.0)
        after = snapshot("sponsored_products_bid_change", base_bid=1.2)
        rows = [
            {"audience_id": "aud-a", "bid_boost": 10},
            {"audience_id": "aud-b", "bid_boost": 20},
        ]
        for record, members in ((before, rows), (after, list(reversed(rows)))):
            next(c for c in record["controls"] if c["control_type"] == "audience_bid_adjustment")["state"] = copy.deepcopy(members)
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual(result["classification"], "Confounded", result)


if __name__ == "__main__":
    unittest.main()
