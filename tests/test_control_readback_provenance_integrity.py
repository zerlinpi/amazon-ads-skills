"""Read-only RED-first tests: explicit readback provenance must be usable and consistent.

A readback_id names one observation, not a reusable account/connector label.
These are synthetic snapshots; no Amazon Ads API access or writes.
"""
import unittest

from scripts.compare_control_state import compare_control_state
from test_nested_collection_completeness import snapshot


def pair(changed=True):
    before = snapshot("sponsored_products_bid_change", base_bid=1.0)
    after = snapshot("sponsored_products_bid_change", base_bid=1.2 if changed else 1.0)
    return before, after


class ControlReadbackProvenanceIntegrityTests(unittest.TestCase):
    def assert_unknown_readback(self, before, after, treatment="base_bid"):
        result = compare_control_state(before, after, treatment)
        self.assertEqual("Unknown", result["classification"], result)
        self.assertIn("readback_id", " | ".join(result["reasons"]), result)

    def test_unknown_before_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "Unknown"
        after["source"]["readback_id"] = "post-1"
        self.assert_unknown_readback(before, after)

    def test_partial_after_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "baseline-1"
        after["source"]["readback_id"] = "Partial"
        self.assert_unknown_readback(before, after)

    def test_not_available_before_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "Not Available"
        after["source"]["readback_id"] = "post-1"
        self.assert_unknown_readback(before, after)

    def test_not_supported_after_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "baseline-1"
        after["source"]["readback_id"] = "Not-Supported"
        self.assert_unknown_readback(before, after)

    def test_not_applicable_before_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "Not Applicable"
        after["source"]["readback_id"] = "post-1"
        self.assert_unknown_readback(before, after)

    def test_na_after_id_cannot_isolate_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "baseline-1"
        after["source"]["readback_id"] = "N/A"
        self.assert_unknown_readback(before, after)

    def test_blank_readback_id_is_not_evidence(self):
        before, after = pair()
        before["source"]["readback_id"] = "  "
        after["source"]["readback_id"] = "post-1"
        self.assert_unknown_readback(before, after)

    def test_padded_readback_id_is_not_evidence(self):
        before, after = pair()
        before["source"]["readback_id"] = " before-1 "
        after["source"]["readback_id"] = "after-1"
        self.assert_unknown_readback(before, after)

    def test_non_string_readback_id_is_not_evidence(self):
        before, after = pair()
        before["source"]["readback_id"] = 0
        after["source"]["readback_id"] = "after-1"
        self.assert_unknown_readback(before, after)

    def test_boolean_readback_id_is_not_evidence(self):
        before, after = pair()
        before["source"]["readback_id"] = False
        after["source"]["readback_id"] = "after-1"
        self.assert_unknown_readback(before, after)

    def test_same_id_different_observation_times_cannot_prove_comparable(self):
        before, after = pair(changed=False)
        before["source"]["readback_id"] = "same-observation"
        after["source"]["readback_id"] = "same-observation"
        after["observed_at"] = "2026-09-21T01:00:00Z"
        self.assert_unknown_readback(before, after, treatment=None)

    def test_same_id_submicrosecond_time_difference_is_not_same_observation(self):
        before, after = pair(changed=False)
        before["source"]["readback_id"] = "same-observation"
        after["source"]["readback_id"] = "same-observation"
        after["observed_at"] = "2026-09-21T00:00:00.000000001Z"
        self.assert_unknown_readback(before, after, treatment=None)

    def test_same_id_equal_utc_instant_different_offsets_is_compatible(self):
        before, after = pair(changed=False)
        before["source"]["readback_id"] = "same-observation"
        after["source"]["readback_id"] = "same-observation"
        after["observed_at"] = "2026-09-21T08:00:00+08:00"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_same_id_same_time_same_state_remains_comparable(self):
        before, after = pair(changed=False)
        before["source"]["readback_id"] = "same-observation"
        after["source"]["readback_id"] = "same-observation"
        self.assertEqual("Comparable", compare_control_state(before, after)["classification"])

    def test_distinct_valid_readbacks_preserve_isolated_bid(self):
        before, after = pair()
        before["source"]["readback_id"] = "before-observation"
        after["source"]["readback_id"] = "after-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])

    def test_real_id_containing_unknown_substring_remains_valid(self):
        before, after = pair()
        before["source"]["readback_id"] = "unknown-campaign-readback-123"
        after["source"]["readback_id"] = "after-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])

    def test_legacy_omitted_readback_id_remains_compatible(self):
        before, after = pair()
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])

    def test_optional_null_readback_id_remains_compatible(self):
        before, after = pair()
        before["source"]["readback_id"] = None
        after["source"]["readback_id"] = None
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])

    def test_one_sided_valid_readback_id_remains_compatible(self):
        before, after = pair()
        before["source"]["readback_id"] = "before-observation"
        self.assertEqual("Treatment Isolated", compare_control_state(before, after, "base_bid")["classification"])


if __name__ == "__main__":
    unittest.main()
