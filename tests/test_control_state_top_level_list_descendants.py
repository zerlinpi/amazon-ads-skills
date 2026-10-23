"""Fail-closed regressions for list-valued extra material controls with descendant lists.

Synthetic control snapshots only; no Amazon Ads API calls or live writes.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state
from test_control_state_extra_nested_collections import snapshot, add_extra, COMPLETE


class TopLevelListDescendantEvidenceTests(unittest.TestCase):
    def compare_extra(self, state, nested=None, after_state=None, after_nested=None,
                      after_bid=1.0, treatment=None, root_evidence=COMPLETE):
        before, after = snapshot(), snapshot(after_bid)
        add_extra(before, copy.deepcopy(state), copy.deepcopy(nested))
        add_extra(after, copy.deepcopy(state if after_state is None else after_state),
                  copy.deepcopy(nested if after_nested is None else after_nested))
        for item in (before["controls"][-1], after["controls"][-1]):
            if root_evidence is not None:
                item["collection_evidence"] = copy.deepcopy(root_evidence)
        return compare_control_state(before, after, treatment)

    def test_root_list_object_empty_child_without_evidence_is_unknown(self):
        self.assertEqual(self.compare_extra([{"rules": []}])["classification"], "Unknown")

    def test_root_list_object_nonempty_child_without_evidence_is_unknown(self):
        self.assertEqual(self.compare_extra([{"rules": ["r1"]}])["classification"], "Unknown")

    def test_root_list_child_truncated_pagination_is_unknown(self):
        evidence = {"/0/rules": {**COMPLETE, "pagination_status": "Truncated"}}
        self.assertEqual(self.compare_extra([{"rules": []}], evidence)["classification"], "Unknown")

    def test_root_list_child_partial_capability_is_unknown(self):
        evidence = {"/0/rules": {**COMPLETE, "capability_status": "Partial"}}
        self.assertEqual(self.compare_extra([{"rules": []}], evidence)["classification"], "Unknown")

    def test_root_list_child_one_sided_evidence_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, [{"rules": []}], {"/0/rules": COMPLETE})
        add_extra(after, [{"rules": []}])
        for item in (before["controls"][-1], after["controls"][-1]):
            item["collection_evidence"] = copy.deepcopy(COMPLETE)
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_root_list_direct_nested_list_requires_own_evidence(self):
        self.assertEqual(self.compare_extra([[]])["classification"], "Unknown")

    def test_root_list_complete_child_allows_comparable(self):
        self.assertEqual(self.compare_extra([{"rules": []}], {"/0/rules": COMPLETE})["classification"], "Comparable")

    def test_root_list_complete_child_allows_isolated_bid(self):
        result = self.compare_extra([{"rules": ["r1"]}], {"/0/rules": COMPLETE},
                                    after_bid=1.2, treatment="base_bid")
        self.assertEqual(result["classification"], "Treatment Isolated")

    def test_root_list_complete_child_change_confounds_bid(self):
        result = self.compare_extra([{"rules": ["r1"]}], {"/0/rules": COMPLETE},
                                    after_state=[{"rules": ["r2"]}],
                                    after_bid=1.2, treatment="base_bid")
        self.assertEqual(result["classification"], "Confounded")

    def test_root_list_direct_nested_list_complete_is_comparable(self):
        self.assertEqual(self.compare_extra([[]], {"/0": COMPLETE})["classification"], "Comparable")

    def test_root_list_escaped_json_pointer_complete(self):
        state = [{"a/b": {"rules": []}}]
        self.assertEqual(self.compare_extra(state, {"/0/a~1b/rules": COMPLETE})["classification"], "Comparable")

    def test_root_flat_list_still_only_needs_root_evidence(self):
        self.assertEqual(self.compare_extra(["r1"])["classification"], "Comparable")

    def test_root_list_without_root_evidence_remains_unknown(self):
        self.assertEqual(self.compare_extra(["r1"], root_evidence=None)["classification"], "Unknown")


if __name__ == "__main__":
    unittest.main()
