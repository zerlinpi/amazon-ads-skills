"""RED-first: complete SP rule collections still need trustworthy member evidence.

These are repository-owned normalized read-side examples, not Amazon Ads API
payloads. All tests are deterministic and perform no account mutations.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def compare_rules(kind, before_members, after_members=None, *, budget_treatment=False):
    surface = "sponsored_products_budget_change" if budget_treatment else "sponsored_products_bid_change"
    before = snapshot(surface, base_bid=1.0, base_budget=100)
    after = snapshot(surface, base_bid=1.0 if budget_treatment else 1.2,
                     base_budget=120 if budget_treatment else 100)
    if after_members is None:
        after_members = copy.deepcopy(before_members)
    for record, members in ((before, before_members), (after, after_members)):
        control_type = "budget_or_pacing" if kind == "active_budget_rules" else "schedule_or_event_rule"
        control = next(c for c in record["controls"] if c["control_type"] == control_type)
        control["state"][kind] = copy.deepcopy(members)
    treatment = "budget_or_pacing" if budget_treatment else "base_bid"
    return compare_control_state(before, after, treatment)


def bid_rule(**changes):
    return {"rule_id": "rule-1", "bid_increase": 10, **changes}


def budget_rule(**changes):
    return {"rule_id": "budget-1", "increase_percent": 20, **changes}


class SponsoredProductsRuleMemberEvidenceTests(unittest.TestCase):
    def unknown(self, kind, members, *, budget_treatment=False):
        result = compare_rules(kind, members, budget_treatment=budget_treatment)
        self.assertEqual(result["classification"], "Unknown", result)

    def test_schedule_unknown_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase="Unknown")])

    def test_schedule_unsupported_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase="Unsupported")])

    def test_schedule_partial_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase="Partial")])

    def test_schedule_missing_bid_increase(self):
        self.unknown("schedule_rules", [{"rule_id": "rule-1"}])

    def test_schedule_boolean_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase=False)])

    def test_schedule_negative_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase=-1)])

    def test_schedule_nonfinite_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase=float("inf"))])

    def test_schedule_nan_bid_increase(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase=float("nan"))])

    def test_schedule_percent_string_not_normalized(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase="10%")])

    def test_schedule_structured_placeholder(self):
        self.unknown("schedule_rules", [bid_rule(bid_increase={"status": "Unknown"})])

    def test_schedule_missing_rule_identity(self):
        self.unknown("schedule_rules", [{"bid_increase": 10}])

    def test_schedule_blank_rule_identity(self):
        self.unknown("schedule_rules", [bid_rule(rule_id="")])

    def test_schedule_whitespace_rule_identity(self):
        self.unknown("schedule_rules", [bid_rule(rule_id=" rule-1 ")])

    def test_schedule_duplicate_rule_identity(self):
        self.unknown("schedule_rules", [bid_rule(), bid_rule(bid_increase=20)])

    def test_schedule_nonobject_member(self):
        self.unknown("schedule_rules", ["Unknown"])

    def test_event_unknown_bid_increase(self):
        self.unknown("event_rules", [bid_rule(bid_increase="Unknown")])

    def test_event_duplicate_rule_identity(self):
        self.unknown("event_rules", [bid_rule(), bid_rule()])

    def test_event_missing_rule_identity(self):
        self.unknown("event_rules", [{"bid_increase": 10}])

    def test_event_missing_bid_increase(self):
        self.unknown("event_rules", [{"rule_id": "rule-1"}])

    def test_event_boolean_bid_increase(self):
        self.unknown("event_rules", [bid_rule(bid_increase=True)])

    def test_budget_unknown_increase_percent(self):
        self.unknown("active_budget_rules", [budget_rule(increase_percent="Unknown")],
                     budget_treatment=True)

    def test_budget_missing_rule_identity(self):
        self.unknown("active_budget_rules", [{"increase_percent": 20}],
                     budget_treatment=True)

    def test_budget_duplicate_rule_identity(self):
        self.unknown("active_budget_rules", [budget_rule(), budget_rule()],
                     budget_treatment=True)

    def test_budget_boolean_increase_percent(self):
        self.unknown("active_budget_rules", [budget_rule(increase_percent=True)],
                     budget_treatment=True)

    def test_budget_negative_increase_percent(self):
        self.unknown("active_budget_rules", [budget_rule(increase_percent=-2)],
                     budget_treatment=True)

    def test_budget_missing_increase_percent(self):
        self.unknown("active_budget_rules", [{"rule_id": "budget-1"}],
                     budget_treatment=True)

    def test_budget_nonobject_member(self):
        self.unknown("active_budget_rules", ["Unknown"], budget_treatment=True)

    def test_budget_unknown_rule_during_bid_treatment(self):
        self.unknown("active_budget_rules", [budget_rule(increase_percent="Unknown")])

    def test_valid_schedule_zero_is_observed_not_missing(self):
        result = compare_rules("schedule_rules", [bid_rule(bid_increase=0)])
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_event_decimal_string(self):
        result = compare_rules("event_rules", [bid_rule(bid_increase="15.5")])
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_budget_decimal_string(self):
        result = compare_rules("active_budget_rules", [budget_rule(increase_percent="20.5")],
                               budget_treatment=True)
        self.assertEqual(result["classification"], "Treatment Isolated", result)

    def test_valid_rule_change_confounds_base_bid(self):
        result = compare_rules("schedule_rules", [bid_rule()], [bid_rule(bid_increase=20)])
        self.assertEqual(result["classification"], "Confounded", result)

    def test_valid_budget_rule_change_confounds_base_bid(self):
        result = compare_rules("active_budget_rules", [budget_rule()],
                               [budget_rule(increase_percent=30)])
        self.assertEqual(result["classification"], "Confounded", result)

    def test_verified_empty_rule_surfaces_still_valid(self):
        result = compare_rules("schedule_rules", [])
        self.assertEqual(result["classification"], "Treatment Isolated", result)


if __name__ == "__main__":
    unittest.main()
