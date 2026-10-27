"""RED-first: one source readback identity cannot attest conflicting states.

Read-only synthetic snapshots. The source readback_id identifies an individual
observation, not a reusable campaign or connector identifier.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def pair(*, budget=False, changed=True):
    surface = "sponsored_products_budget_change" if budget else "sponsored_products_bid_change"
    before = snapshot(surface, base_bid=1.0, base_budget=100)
    after = snapshot(
        surface,
        base_bid=1.0 if budget or not changed else 1.2,
        base_budget=120 if budget and changed else 100,
    )
    treatment = "budget_or_pacing" if budget else "base_bid"
    return before, after, treatment


class ReadbackIdentityReuseTests(unittest.TestCase):
    def assert_reused_unknown(self, before, after, treatment):
        for item in (before, after):
            item["source"]["readback_id"] = "same-readback-observation"
        result = compare_control_state(before, after, treatment)
        self.assertEqual("Unknown", result["classification"], result)
        self.assertIn("readback_id", " | ".join(result["reasons"]), result)

    def test_changed_bid_cannot_reuse_same_observation(self):
        self.assert_reused_unknown(*pair())

    def test_changed_budget_cannot_reuse_same_observation(self):
        self.assert_reused_unknown(*pair(budget=True))

    def test_confounded_bid_and_placement_cannot_reuse_same_observation(self):
        before, after, treatment = pair()
        next(c for c in after["controls"] if c["control_type"] == "placement_adjustment")["state"]["top_of_search"] = 20
        self.assert_reused_unknown(before, after, treatment)

    def test_changed_schedule_rule_cannot_reuse_same_observation(self):
        before, after, treatment = pair()
        next(c for c in after["controls"] if c["control_type"] == "schedule_or_event_rule")["state"]["schedule_rules"][0]["bid_increase"] = 30
        self.assert_reused_unknown(before, after, treatment)

    def test_distinct_readbacks_preserve_isolated_bid(self):
        before, after, treatment = pair()
        before["source"]["readback_id"] = "before-observation"
        after["source"]["readback_id"] = "after-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, treatment)["classification"])

    def test_distinct_readbacks_preserve_isolated_budget(self):
        before, after, treatment = pair(budget=True)
        before["source"]["readback_id"] = "before-observation"
        after["source"]["readback_id"] = "after-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, treatment)["classification"])

    def test_legacy_omitted_readback_id_remains_compatible(self):
        self.assertEqual("Treatment Isolated", compare_control_state(*pair())["classification"])

    def test_same_readback_with_unchanged_state_is_not_false_change(self):
        before, after, _ = pair(changed=False)
        for item in (before, after):
            item["source"]["readback_id"] = "same-readback-observation"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_one_sided_optional_readback_id_remains_compatible(self):
        before, after, treatment = pair()
        before["source"]["readback_id"] = "before-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, treatment)["classification"])


if __name__ == "__main__":
    unittest.main()
