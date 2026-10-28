import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "project_measurement_history.py"
SPEC = importlib.util.spec_from_file_location("project_measurement_history", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def snapshot():
    return {
        "snapshot_id": "snap-1",
        "captured_at": "2026-10-28T10:00:00Z",
        "source_system": "synthetic",
    }


class ObservedScopeIntegrityTests(unittest.TestCase):
    def test_unresolved_observed_scope_is_rejected_without_expected_scope(self):
        event = {
            "marketplace": "Unknown",
            "profile_scope": "profile-1",
            "entity": {"type": "campaign", "id": "campaign-1"},
            "evidence_snapshot": snapshot(),
        }
        with self.assertRaisesRegex(ValueError, r"measurement event scope\.marketplace"):
            MODULE.project_measurement_history([event])

    def test_padded_observed_scope_is_rejected_without_expected_scope(self):
        event = {
            "marketplace": "US ",
            "profile_scope": "profile-1",
            "entity": {"type": "campaign", "id": "campaign-1"},
            "evidence_snapshot": snapshot(),
        }
        with self.assertRaisesRegex(ValueError, "measurement event scope\.marketplace"):
            MODULE.project_measurement_history([event])


    def test_legacy_entity_only_event_remains_accepted_without_scope(self):
        event = {
            "entity": {"type": "campaign", "id": "campaign-legacy"},
            "evidence_snapshot": snapshot(),
        }
        result = MODULE.project_measurement_history([event])
        self.assertEqual(result["latest_measurement_state"]["evidence_snapshot_id"], "snap-1")

    def test_concrete_observed_scope_remains_accepted_without_expected_scope(self):
        event = {
            "marketplace": "US",
            "profile_scope": "profile-1",
            "entity": {"type": "campaign", "id": "campaign-1"},
            "evidence_snapshot": snapshot(),
        }
        result = MODULE.project_measurement_history([event])
        self.assertEqual(result["latest_measurement_state"]["evidence_snapshot_id"], "snap-1")


if __name__ == "__main__":
    unittest.main()
