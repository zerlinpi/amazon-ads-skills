import unittest
from scripts.project_measurement_comparison_history import project_measurement_comparison_history, _timestamp


def event(event_id, timestamp):
    return {
        "event_id": event_id,
        "event_type": "evaluated",
        "timestamp": timestamp,
        "marketplace": "US",
        "profile_scope": "fixture-profile",
        "parent_action_id": "fixture-action",
        "entity": {"type": "campaign", "id": "fixture-campaign"},
        "measurement_comparison": {
            "comparator_id": "fixture",
            "classification": "Comparable",
            "changed_fields": [],
            "reasons": [],
            "baseline_snapshot_id": "before",
            "post_snapshot_id": "after",
        },
    }


class SubmicrosecondOrderingTests(unittest.TestCase):
    def test_seventh_fractional_digit_orders_instant_not_event_id(self):
        older = event("z-older", "2026-10-15T00:00:00.1234561Z")
        newer = event("a-newer", "2026-10-15T00:00:00.1234569Z")
        result = project_measurement_comparison_history([newer, older])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "a-newer")

    def test_fractional_offset_equivalent_instants(self):
        a = event("a", "2026-10-15T08:00:00.1234567+08:00")
        b = event("b", "2026-10-15T00:00:00.1234567Z")
        result = project_measurement_comparison_history([a, b])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "b")

    def test_nine_digit_fraction_preserved(self):
        self.assertLess(_timestamp(event("a", "2026-10-15T00:00:00.123456789Z")),
                        _timestamp(event("b", "2026-10-15T00:00:00.123456790Z")))

    def test_existing_microsecond_and_offset_ordering(self):
        a = event("z", "2026-10-15T08:00:00.123455+08:00")
        b = event("a", "2026-10-15T00:00:00.123456Z")
        result = project_measurement_comparison_history([a, b])
        self.assertEqual(result["latest_measurement_comparison"]["source_event_id"], "a")

class ExistingContractSmokeTests(unittest.TestCase):
    def test_invalid_rfc3339_offsets_still_rejected(self):
        for suffix in ("+00:60", "+01:99", "-00:00", "", "Zjunk"):
            with self.subTest(suffix=suffix):
                with self.assertRaisesRegex(ValueError, "timezone-aware RFC3339"):
                    _timestamp(event("bad", "2026-10-15T00:00:00" + suffix))

    def test_correction_fork_still_fails_closed(self):
        original = event("original", "2026-10-15T00:00:00Z")
        c1 = event("corr-1", "2026-10-15T01:00:00Z")
        c2 = event("corr-2", "2026-10-15T02:00:00Z")
        for c in (c1, c2):
            c["event_type"] = "corrected"
            c["supersedes_event_id"] = "original"
        with self.assertRaisesRegex(ValueError, "ambiguous correction fork"):
            project_measurement_comparison_history([original, c1, c2])


if __name__ == "__main__":
    unittest.main()
