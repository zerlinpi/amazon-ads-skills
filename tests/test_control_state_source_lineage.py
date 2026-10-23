"""Read-only control-state source-lineage regressions.

All snapshots are synthetic. Distinct readback IDs may represent different
observations; acquisition/source identity cannot be silently inferred.
"""
import copy
import unittest

from scripts.compare_control_state import compare_control_state


def snapshot():
    return {
        "scope": {"marketplace_id": "ATVPDKIKX0DER", "profile_id": "synthetic-profile"},
        "observed_at": "2026-10-23T00:00:00Z",
        "source": {
            "source_system": "synthetic-ads-api",
            "acquisition_channel": "synthetic-connector",
            "connector_id": "connector-a",
            "readback_id": "baseline-read",
        },
        "coverage": {
            "required_control_types": ["base_bid"],
            "coverage_status": "Complete",
            "requirement_provenance": {
                "decision_surface": "fixture_control_comparison",
                "derivation_status": "Verified",
                "requirement_registry_id": "control-requirements@2026-09-29",
            },
        },
        "controls": [{
            "control_type": "base_bid", "state": 1.0,
            "effective_at": "2026-10-22T00:00:00Z",
            "evidence_status": "observed",
        }],
    }


class ControlStateSourceLineageTests(unittest.TestCase):
    def test_identical_source_identity_remains_comparable(self):
        self.assertEqual(compare_control_state(snapshot(), snapshot())["classification"], "Comparable")

    def test_distinct_readback_ids_are_not_source_mismatches(self):
        before, after = snapshot(), snapshot()
        after["source"]["readback_id"] = "post-read"
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")

    def test_missing_source_envelope_fails_closed(self):
        before, after = snapshot(), snapshot()
        after.pop("source")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_non_object_source_envelope_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["source"] = "synthetic-ads-api"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_missing_source_system_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["source"].pop("source_system")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_empty_acquisition_channel_fails_closed(self):
        before, after = snapshot(), snapshot()
        before["source"]["acquisition_channel"] = "  "
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_cross_source_system_without_lineage_mapping_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["source"]["source_system"] = "synthetic-warehouse"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_cross_acquisition_channel_without_lineage_mapping_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["source"]["acquisition_channel"] = "synthetic-export"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_connector_id_mismatch_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["source"]["connector_id"] = "connector-b"
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_one_sided_connector_id_fails_closed(self):
        before, after = snapshot(), snapshot()
        after["source"].pop("connector_id")
        self.assertEqual(compare_control_state(before, after)["classification"], "Unknown")

    def test_both_connector_ids_absent_preserves_legacy_snapshots(self):
        before, after = snapshot(), snapshot()
        before["source"].pop("connector_id")
        after["source"].pop("connector_id")
        self.assertEqual(compare_control_state(before, after)["classification"], "Comparable")


if __name__ == "__main__":
    unittest.main()
