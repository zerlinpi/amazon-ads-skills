"""Regression coverage for deep collection evidence in extra material controls.

Synthetic read-only snapshots; no Ads API or mutation.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_state_extra_nested_collections import snapshot, add_extra, COMPLETE


class DeepExtraCollectionTests(unittest.TestCase):
    def compare_extra(self, state, evidence=None, after_state=None, after_evidence=None,
                      after_bid=1.0, treatment=None):
        before, after = snapshot(), snapshot(after_bid)
        add_extra(before, copy.deepcopy(state), copy.deepcopy(evidence))
        add_extra(after, copy.deepcopy(state if after_state is None else after_state),
                  copy.deepcopy(evidence if after_evidence is None else after_evidence))
        return compare_control_state(before, after, treatment)

    def test_deep_empty_list_without_evidence_is_unknown(self):
        self.assertEqual(self.compare_extra({"policy": {"rules": []}})["classification"], "Unknown")

    def test_deep_nonempty_list_without_evidence_is_unknown(self):
        self.assertEqual(self.compare_extra({"policy": {"rules": ["r1"]}})["classification"], "Unknown")

    def test_deep_partial_pagination_is_unknown(self):
        evidence = {"/policy/rules": {**COMPLETE, "pagination_status": "Truncated"}}
        self.assertEqual(self.compare_extra({"policy": {"rules": []}}, evidence)["classification"], "Unknown")

    def test_deep_partial_capability_is_unknown(self):
        evidence = {"/policy/rules": {**COMPLETE, "capability_status": "Partial"}}
        self.assertEqual(self.compare_extra({"policy": {"rules": ["r1"]}}, evidence)["classification"], "Unknown")

    def test_one_sided_deep_evidence_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, {"policy": {"rules": []}}, {"/policy/rules": COMPLETE})
        add_extra(after, {"policy": {"rules": []}})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_nested_list_within_verified_parent_list_needs_own_evidence(self):
        state = {"policies": [{"overrides": []}]}
        self.assertEqual(self.compare_extra(state, {"policies": COMPLETE})["classification"], "Unknown")

    def test_nested_list_within_verified_parent_list_partial_is_unknown(self):
        state = {"policies": [{"overrides": ["r1"]}]}
        evidence = {"policies": COMPLETE, "/policies/0/overrides": {**COMPLETE, "enumeration_status": "Partial"}}
        self.assertEqual(self.compare_extra(state, evidence)["classification"], "Unknown")

    def test_verified_deep_empty_list_is_comparable(self):
        evidence = {"/policy/rules": COMPLETE}
        self.assertEqual(self.compare_extra({"policy": {"rules": []}}, evidence)["classification"], "Comparable")

    def test_verified_nested_list_in_list_is_comparable(self):
        state = {"policies": [{"overrides": []}]}
        evidence = {"policies": COMPLETE, "/policies/0/overrides": COMPLETE}
        self.assertEqual(self.compare_extra(state, evidence)["classification"], "Comparable")

    def test_verified_deep_control_change_confounds_bid(self):
        evidence = {"/policy/rules": COMPLETE}
        result = self.compare_extra({"policy": {"rules": ["r1"]}}, evidence,
                                    after_state={"policy": {"rules": ["r2"]}},
                                    after_bid=1.2, treatment="base_bid")
        self.assertEqual(result["classification"], "Confounded")

    def test_verified_deep_control_allows_isolated_bid(self):
        evidence = {"/policy/rules": COMPLETE}
        result = self.compare_extra({"policy": {"rules": ["r1"]}}, evidence,
                                    after_bid=1.2, treatment="base_bid")
        self.assertEqual(result["classification"], "Treatment Isolated")

    def test_deep_json_pointer_escaped_key(self):
        evidence = {"/a~1b/rules": COMPLETE}
        self.assertEqual(self.compare_extra({"a/b": {"rules": []}}, evidence)["classification"], "Comparable")

    def test_direct_legacy_nested_evidence_still_works(self):
        self.assertEqual(self.compare_extra({"rules": []}, {"rules": COMPLETE})["classification"], "Comparable")


if __name__ == "__main__":
    unittest.main()
