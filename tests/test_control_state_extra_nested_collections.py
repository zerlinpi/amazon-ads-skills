"""Fail-closed regressions for nested collections in extra material controls.

Synthetic snapshots only. No Amazon Ads mutation or API calls.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


REGISTRY_ID = "control-requirements@2026-09-29"
COMPLETE = {
    "enumeration_status": "Complete",
    "pagination_status": "Complete",
    "capability_status": "Supported",
}


def snapshot(base_bid=1.0):
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile"},
        "observed_at": "2026-10-23T00:00:00Z",
        "source": {"source_system": "fixture", "acquisition_channel": "test"},
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "requirement_registry_id": REGISTRY_ID,
            },
        },
        "controls": [{
            "control_type": "base_bid",
            "state": base_bid,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        }],
    }


def add_extra(value, state, nested=None):
    item = {
        "control_type": "other_material_control",
        "state": state,
        "effective_at": "2026-10-22T00:00:00Z",
        "evidence_status": "observed",
    }
    if nested is not None:
        item["nested_collection_evidence"] = nested
    value["controls"].append(item)


class ExtraMaterialNestedCollectionTests(unittest.TestCase):
    def compare_extra(self, state, evidence=None, post_state=None, post_evidence=None, base_after=1.0, treatment=None):
        before, after = snapshot(), snapshot(base_after)
        add_extra(before, copy.deepcopy(state), copy.deepcopy(evidence))
        add_extra(after, copy.deepcopy(state if post_state is None else post_state),
                  copy.deepcopy(evidence if post_evidence is None else post_evidence))
        return compare_control_state(before, after, treatment)

    def test_empty_nested_list_without_evidence_is_unknown(self):
        result = self.compare_extra({"rules": []})
        self.assertEqual(result["classification"], "Unknown")

    def test_nonempty_nested_list_without_evidence_is_unknown(self):
        result = self.compare_extra({"rules": [{"id": "synthetic-rule"}]})
        self.assertEqual(result["classification"], "Unknown")

    def test_truncated_nested_pagination_is_unknown(self):
        partial = {**COMPLETE, "pagination_status": "Truncated"}
        result = self.compare_extra({"rules": ["r1"]}, {"rules": partial})
        self.assertEqual(result["classification"], "Unknown")

    def test_partial_nested_enumeration_is_unknown(self):
        partial = {**COMPLETE, "enumeration_status": "Partial"}
        result = self.compare_extra({"rules": ["r1"]}, {"rules": partial})
        self.assertEqual(result["classification"], "Unknown")

    def test_unsupported_nested_capability_is_unknown(self):
        unsupported = {**COMPLETE, "capability_status": "Unsupported"}
        result = self.compare_extra({"rules": []}, {"rules": unsupported})
        self.assertEqual(result["classification"], "Unknown")

    def test_missing_one_of_two_nested_evidence_fields_is_unknown(self):
        result = self.compare_extra({"rules": [], "overrides": []}, {"rules": COMPLETE})
        self.assertEqual(result["classification"], "Unknown")

    def test_one_sided_nested_evidence_is_unknown(self):
        before, after = snapshot(), snapshot()
        add_extra(before, {"rules": []}, {"rules": COMPLETE})
        add_extra(after, {"rules": []})
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_verified_empty_nested_list_remains_comparable(self):
        result = self.compare_extra({"rules": []}, {"rules": COMPLETE})
        self.assertEqual(result["classification"], "Comparable")

    def test_verified_nonempty_nested_list_allows_isolated_bid_treatment(self):
        result = self.compare_extra(
            {"rules": ["r1"]}, {"rules": COMPLETE}, base_after=1.2, treatment="base_bid"
        )
        self.assertEqual(result["classification"], "Treatment Isolated")

    def test_verified_nested_list_change_confounds_bid_treatment(self):
        result = self.compare_extra(
            {"rules": ["r1"]}, {"rules": COMPLETE},
            post_state={"rules": ["r2"]}, base_after=1.2, treatment="base_bid"
        )
        self.assertEqual(result["classification"], "Confounded")

    def test_extra_scalar_object_without_list_remains_comparable(self):
        result = self.compare_extra({"enabled": False})
        self.assertEqual(result["classification"], "Comparable")


if __name__ == "__main__":
    unittest.main()
