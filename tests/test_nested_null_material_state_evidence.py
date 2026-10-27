"""RED-first: explicitly null nested material state is not observed zero.

All inputs are synthetic normalized read-only observations. No Amazon Ads API calls.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_intervening_event_evidence import fixture


class NestedNullMaterialEvidenceTests(unittest.TestCase):
    def assert_unknown(self, before, after):
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual("Unknown", result["classification"], result)

    def test_endpoint_nested_null_on_both_sides_is_not_stability(self):
        before, after, _ = fixture()
        del after["control_events"]
        for snapshot in (before, after):
            routing = next(c for c in snapshot["controls"] if c["control_type"] == "targeting_or_routing")
            routing["state"]["unverified_dimension"] = None
        self.assert_unknown(before, after)

    def test_endpoint_nested_null_inside_rule_member_is_unknown(self):
        before, after, _ = fixture()
        del after["control_events"]
        for snapshot in (before, after):
            rules = next(c for c in snapshot["controls"] if c["control_type"] == "schedule_or_event_rule")
            rules["state"]["schedule_rules"][0]["unverified_dimension"] = None
        self.assert_unknown(before, after)

    def test_event_nested_null_before_state_is_not_observed(self):
        before, after, event = fixture("schedule_or_event_rule")
        event["before_state"]["unverified_dimension"] = None
        self.assert_unknown(before, after)

    def test_event_nested_null_after_state_is_not_observed(self):
        before, after, event = fixture("schedule_or_event_rule")
        event["after_state"]["unverified_dimension"] = None
        self.assert_unknown(before, after)

    def test_observed_zero_and_false_remain_distinct_from_null(self):
        before, after, event = fixture("schedule_or_event_rule")
        event["before_state"]["observed_zero"] = 0
        event["after_state"]["observed_zero"] = 0
        event["before_state"]["observed_false"] = False
        event["after_state"]["observed_false"] = False
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual("Confounded", result["classification"], result)

    def test_absent_optional_dimension_remains_compatible(self):
        before, after, _ = fixture("schedule_or_event_rule")
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual("Confounded", result["classification"], result)

    def test_null_optional_provenance_outside_material_state_remains_compatible(self):
        before, after, _ = fixture("schedule_or_event_rule")
        for snapshot in (before, after):
            for control in snapshot["controls"]:
                control["transition_provenance"] = None
        result = compare_control_state(before, after, "base_bid")
        self.assertEqual("Confounded", result["classification"], result)


if __name__ == "__main__":
    unittest.main()
