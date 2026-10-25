"""Feature-specific as_of decisions cannot rely on connector evidence captured later.

Synthetic read-only temporal join; no Amazon Ads calls, credentials, or writes.
The eligibility freshness horizon is not silently reused as a connector TTL.
"""
import unittest

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from tests.test_feature_eligibility_evidence_join import fixture


def check(payload):
    return evaluate_connector_capability_gate(payload)


class FeatureEligibilitySnapshotAsOfChronologyTests(unittest.TestCase):
    def assert_unknown_join(self, payload):
        result = check(payload)
        self.assertEqual(result["feature_eligibility_effect"], "pass", result)
        self.assertEqual(result["gate_status"], "Degraded", result)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "unknown", result)
        self.assertFalse(result["high_confidence_allowed"], result)
        self.assertEqual(result["missing_evidence_policy"], "never_zero", result)
        self.assertNotIn("High Confidence", result["allowed_decision_classes"])
        self.assertTrue(any("snapshot" in w and "as_of" in w for w in result["warnings"]), result)

    def test_future_snapshot_after_decision_asof_cannot_pass(self):
        p = fixture()
        p["feature_eligibility_requirement"]["as_of"] = "2026-10-25T23:30:00Z"
        self.assert_unknown_join(p)

    def test_one_second_future_snapshot_cannot_pass(self):
        p = fixture()
        p["snapshot"]["captured_at"] = "2026-10-26T00:00:01Z"
        self.assert_unknown_join(p)

    def test_timezone_offset_asof_must_compare_actual_instant(self):
        p = fixture()
        p["feature_eligibility_requirement"]["as_of"] = "2026-10-26T00:00:00+01:00"
        self.assert_unknown_join(p)

    def test_future_snapshot_with_fresh_eligibility_still_degrades(self):
        p = fixture()
        p["feature_eligibility_requirement"]["as_of"] = "2026-10-25T23:59:59Z"
        p["feature_eligibility_evidence"]["observed_at"] = "2026-10-25T23:00:00Z"
        self.assert_unknown_join(p)

    def test_equal_snapshot_and_asof_remain_compatible(self):
        result = check(fixture())
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_earlier_snapshot_does_not_invent_a_ttl(self):
        p = fixture()
        p["snapshot"]["captured_at"] = "2026-10-25T23:30:00Z"
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_equivalent_offset_capture_is_not_future(self):
        p = fixture()
        p["snapshot"]["captured_at"] = "2026-10-26T01:00:00+01:00"
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_missing_capture_cannot_prove_feature_time(self):
        p = fixture()
        del p["snapshot"]["captured_at"]
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)

    def test_unknown_offset_capture_cannot_prove_feature_time(self):
        p = fixture()
        p["snapshot"]["captured_at"] = "2026-10-26T00:00:00-00:00"
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "unknown", result)
        self.assertEqual(result["gate_status"], "Degraded", result)

    def test_verified_ineligible_still_blocks_with_future_snapshot(self):
        p = fixture()
        p["feature_eligibility_requirement"]["as_of"] = "2026-10-25T23:30:00Z"
        p["feature_eligibility_evidence"]["eligibility_status"] = "Ineligible"
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "unknown", result)
        self.assertEqual(result["feature_eligibility_effect"], "blocked", result)
        self.assertEqual(result["gate_status"], "Blocked", result)

    def test_legacy_request_not_given_an_implicit_asof(self):
        p = fixture()
        del p["feature_eligibility_requirement"]
        del p["feature_eligibility_evidence"]
        p["snapshot"]["captured_at"] = "2026-10-26T00:00:01Z"
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "not_evaluated", result)
        self.assertEqual(result["gate_status"], "Pass", result)

    def test_explicit_freshness_still_applies_independently(self):
        p = fixture()
        p["snapshot"]["capabilities"][0]["bindings"][0]["evidence"][0]["observed_at"] = "2026-10-25T23:00:00Z"
        p["freshness_requirement"] = {
            "as_of": "2026-10-26T00:00:00Z",
            "max_age_seconds": 7200,
        }
        result = check(p)
        self.assertEqual(result.get("feature_snapshot_chronology_effect"), "pass", result)
        self.assertEqual(result["gate_status"], "Pass", result)


if __name__ == "__main__":
    unittest.main()
