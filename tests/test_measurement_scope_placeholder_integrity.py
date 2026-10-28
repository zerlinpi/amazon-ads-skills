import unittest

from scripts.project_measurement_history import project_measurement_history


def event(marketplace="US", profile_scope="profile-1", entity_type="campaign", entity_id="c1"):
    return {
        "timestamp": "2026-09-22T00:00:00Z",
        "marketplace": marketplace,
        "profile_scope": profile_scope,
        "entity": {"type": entity_type, "id": entity_id},
        "evidence_snapshot": {
            "snapshot_id": "m1",
            "captured_at": "2026-09-22T00:00:00Z",
            "reporting_generation": "unified",
            "date_attribution_semantics": "traffic_date",
        },
    }


class MeasurementScopePlaceholderTests(unittest.TestCase):
    def test_rejects_unresolved_expected_scope_placeholder(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_history(
                [event(marketplace="Unknown")],
                expected_scope={
                    "marketplace": "Unknown",
                    "profile_scope": "profile-1",
                    "entity_type": "campaign",
                    "entity_id": "c1",
                },
            )

    def test_rejects_unresolved_observed_scope_placeholder(self):
        with self.assertRaisesRegex(ValueError, "measurement event scope"):
            project_measurement_history(
                [event(marketplace="N/A")],
                expected_scope={
                    "marketplace": "US",
                    "profile_scope": "profile-1",
                    "entity_type": "campaign",
                    "entity_id": "c1",
                },
            )

    def test_rejects_padded_expected_scope_identity(self):
        with self.assertRaisesRegex(ValueError, "expected_scope"):
            project_measurement_history(
                [event()],
                expected_scope={
                    "marketplace": " US ",
                    "profile_scope": "profile-1",
                    "entity_type": "campaign",
                    "entity_id": "c1",
                },
            )

    def test_accepts_concrete_scope_with_placeholder_substring(self):
        result = project_measurement_history(
            [event(marketplace="US-UNKNOWN-TEST")],
            expected_scope={
                "marketplace": "US-UNKNOWN-TEST",
                "profile_scope": "profile-1",
                "entity_type": "campaign",
                "entity_id": "c1",
            },
        )
        self.assertEqual(result["latest_measurement_state"]["evidence_snapshot_id"], "m1")


if __name__ == "__main__":
    unittest.main()
