"""Fail-closed regressions for descendants of registry-required list controls.

All records are synthetic. No connector calls or Amazon Ads mutations.
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


def compare_audience(state, evidence=None, post_state=None, post_evidence=None,
                     treatment="base_bid", post_bid=1.2):
    before = snapshot(1.0, PLACEMENTS)
    after = snapshot(post_bid, PLACEMENTS)
    for record, value, nested in (
        (before, state, evidence),
        (after, state if post_state is None else post_state,
         evidence if post_evidence is None else post_evidence),
    ):
        audience = next(c for c in record["controls"] if c["control_type"] == "audience_bid_adjustment")
        audience["state"] = copy.deepcopy(value)
        if nested is not None:
            audience["nested_collection_evidence"] = copy.deepcopy(nested)
    return compare_control_state(before, after, treatment)


class RequiredListDescendantEvidenceTests(unittest.TestCase):
    def test_empty_child_without_evidence_is_unknown(self):
        result = compare_audience([{"audience_id": "a", "segments": []}])
        self.assertEqual(result["classification"], "Unknown")

    def test_nonempty_child_without_evidence_is_unknown(self):
        result = compare_audience([{"audience_id": "a", "segments": ["s1"]}])
        self.assertEqual(result["classification"], "Unknown")

    def test_truncated_child_is_unknown(self):
        evidence = {"/0/segments": {**COMPLETE, "pagination_status": "Truncated"}}
        self.assertEqual(compare_audience([{"segments": []}], evidence)["classification"], "Unknown")

    def test_partial_capability_is_unknown(self):
        evidence = {"/0/segments": {**COMPLETE, "capability_status": "Partial"}}
        self.assertEqual(compare_audience([{"segments": []}], evidence)["classification"], "Unknown")

    def test_one_sided_child_evidence_is_unknown(self):
        state = [{"segments": []}]
        before = snapshot(1.0, PLACEMENTS)
        after = snapshot(1.2, PLACEMENTS)
        for record in (before, after):
            audience = next(c for c in record["controls"] if c["control_type"] == "audience_bid_adjustment")
            audience["state"] = copy.deepcopy(state)
        next(c for c in before["controls"] if c["control_type"] == "audience_bid_adjustment")[
            "nested_collection_evidence"
        ] = {"/0/segments": COMPLETE}
        self.assertEqual(compare_control_state(before, after, "base_bid")["classification"], "Unknown")

    def test_complete_child_preserves_isolated_bid(self):
        state = [{"audience_id": "a", "bid_boost": 10, "segments": ["s1"]}]
        self.assertEqual(compare_audience(state, {"/0/segments": COMPLETE})["classification"],
                         "Treatment Isolated")

    def test_complete_child_change_confounds_bid(self):
        state = [{"audience_id": "a", "bid_boost": 10, "segments": ["s1"]}]
        self.assertEqual(compare_audience(
            state, {"/0/segments": COMPLETE}, post_state=[{"audience_id": "a", "bid_boost": 10, "segments": ["s2"]}],
        )["classification"], "Confounded")

    def test_direct_nested_array_without_evidence_is_unknown(self):
        self.assertEqual(compare_audience([[]])["classification"], "Unknown")

    def test_direct_nested_array_with_evidence_is_still_invalid_audience_member(self):
        # Collection completeness cannot authenticate a non-object audience row.
        self.assertEqual(compare_audience([[]], {"/0": COMPLETE})["classification"],
                         "Unknown")

    def test_deeper_child_needs_own_evidence(self):
        state = [{"audience_id": "a", "bid_boost": 10, "segments": [{"rules": []}]}]
        self.assertEqual(compare_audience(state, {"/0/segments": COMPLETE})["classification"], "Unknown")

    def test_deeper_child_complete_is_isolated(self):
        state = [{"audience_id": "a", "bid_boost": 10, "segments": [{"rules": []}]}]
        evidence = {"/0/segments": COMPLETE, "/0/segments/0/rules": COMPLETE}
        self.assertEqual(compare_audience(state, evidence)["classification"], "Treatment Isolated")

    def test_flat_required_audience_list_remains_isolated(self):
        self.assertEqual(compare_audience([{"audience_id": "a", "bid_boost": 10}])["classification"],
                         "Treatment Isolated")


if __name__ == "__main__":
    unittest.main()
