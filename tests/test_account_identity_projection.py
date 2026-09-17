import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_SCRIPT = ROOT / "scripts/project_measurement_history.py"
REALIZATION_SCRIPT = ROOT / "scripts/project_realization_history.py"
EVENT_SCHEMA = ROOT / "schemas/optimization-event.json"
HISTORY_SCHEMA = ROOT / "schemas/entity-history.json"


def invoke(script: Path, events, expected_scope=None):
    payload = {"events": events}
    if expected_scope is not None:
        payload["expected_scope"] = expected_scope
    return subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


def identity(global_id: str, *, regional_id: str | None = None):
    value = {
        "global_advertiser_account_id": global_id,
        "country_code": "US",
    }
    if regional_id is not None:
        value["regional_advertiser_account_id"] = regional_id
    return value


def expected_scope(global_id: str):
    return {
        "marketplace": "US",
        "profile_scope": "profile-a",
        "entity_type": "campaign",
        "entity_id": "campaign-1",
        "account_identity": {
            "global_advertiser_account_id": global_id,
        },
    }


def base_event(event_id: str, account_identity, *, timestamp: str):
    return {
        "event_id": event_id,
        "timestamp": timestamp,
        "marketplace": "US",
        "profile_scope": "profile-a",
        "account_identity": account_identity,
        "entity": {"type": "campaign", "id": "campaign-1"},
    }


class AccountIdentityProjectionTests(unittest.TestCase):
    def test_entity_history_can_preserve_event_account_identity_envelope(self):
        event_schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))
        history_schema = json.loads(HISTORY_SCHEMA.read_text(encoding="utf-8"))

        self.assertIn("account_identity", history_schema["properties"])
        event_fields = event_schema["properties"]["account_identity"]["properties"]
        history_fields = history_schema["properties"]["account_identity"]["properties"]
        for field in (
            "manager_account_id",
            "global_advertiser_account_id",
            "regional_advertiser_account_id",
            "legacy_advertiser_account_id",
            "advertiser_account_id",
            "regional_profile_id",
            "country_code",
            "identity_mapping_provenance",
        ):
            self.assertIn(field, event_fields)
            self.assertIn(field, history_fields)

    def test_measurement_projection_rejects_conflicting_account_identity_with_same_legacy_scope(self):
        first = base_event("e1", identity("global-a"), timestamp="2026-09-17T08:00:00Z")
        first["evidence_snapshot"] = {
            "snapshot_id": "m1",
            "captured_at": "2026-09-17T08:00:00Z",
        }
        second = base_event("e2", identity("global-b"), timestamp="2026-09-17T09:00:00Z")
        second["evidence_snapshot"] = {
            "snapshot_id": "m2",
            "captured_at": "2026-09-17T09:00:00Z",
        }

        result = invoke(MEASUREMENT_SCRIPT, [first, second])

        self.assertEqual(result.returncode, 2)
        self.assertIn("account identity", result.stderr.lower())

    def test_realization_projection_rejects_conflicting_account_identity_with_same_legacy_scope(self):
        first = base_event("e1", identity("global-a"), timestamp="2026-09-17T08:00:00Z")
        first["realization_snapshot"] = {
            "snapshot_id": "r1",
            "captured_at": "2026-09-17T08:00:00Z",
            "realized_surfaces": ["shopping_results"],
            "coverage_status": "Complete",
        }
        second = base_event("e2", identity("global-b"), timestamp="2026-09-17T09:00:00Z")
        second["realization_snapshot"] = {
            "snapshot_id": "r2",
            "captured_at": "2026-09-17T09:00:00Z",
            "realized_surfaces": ["product_detail_page"],
            "coverage_status": "Complete",
        }

        result = invoke(REALIZATION_SCRIPT, [first, second])

        self.assertEqual(result.returncode, 2)
        self.assertIn("account identity", result.stderr.lower())

    def test_compatible_account_identity_is_preserved_by_both_projectors(self):
        account = identity("global-a", regional_id="regional-na-a")

        measurement_event = base_event("e1", account, timestamp="2026-09-17T08:00:00Z")
        measurement_event["evidence_snapshot"] = {
            "snapshot_id": "m1",
            "captured_at": "2026-09-17T08:00:00Z",
        }
        measurement = invoke(MEASUREMENT_SCRIPT, [measurement_event])
        self.assertEqual(measurement.returncode, 0, measurement.stderr)
        measurement_projection = json.loads(measurement.stdout)
        self.assertEqual(measurement_projection["account_identity"], account)

        realization_event = base_event("e2", account, timestamp="2026-09-17T09:00:00Z")
        realization_event["realization_snapshot"] = {
            "snapshot_id": "r1",
            "captured_at": "2026-09-17T09:00:00Z",
            "realized_surfaces": ["shopping_results"],
            "coverage_status": "Complete",
        }
        realization = invoke(REALIZATION_SCRIPT, [realization_event])
        self.assertEqual(realization.returncode, 0, realization.stderr)
        realization_projection = json.loads(realization.stdout)
        self.assertEqual(realization_projection["account_identity"], account)

    def test_measurement_expected_scope_rejects_wrong_advertiser_identity(self):
        event = base_event("e1", identity("global-b"), timestamp="2026-09-17T10:00:00Z")
        event["evidence_snapshot"] = {
            "snapshot_id": "m1",
            "captured_at": "2026-09-17T10:00:00Z",
        }

        result = invoke(MEASUREMENT_SCRIPT, [event], expected_scope("global-a"))

        self.assertEqual(result.returncode, 2)
        self.assertIn("account identity", result.stderr.lower())

    def test_realization_expected_scope_rejects_wrong_advertiser_identity(self):
        event = base_event("e1", identity("global-b"), timestamp="2026-09-17T10:00:00Z")
        event["realization_snapshot"] = {
            "snapshot_id": "r1",
            "captured_at": "2026-09-17T10:00:00Z",
            "realized_surfaces": ["shopping_results"],
            "coverage_status": "Complete",
        }

        result = invoke(REALIZATION_SCRIPT, [event], expected_scope("global-a"))

        self.assertEqual(result.returncode, 2)
        self.assertIn("account identity", result.stderr.lower())

    def test_expected_account_identity_rejects_missing_event_identity(self):
        measurement_event = base_event("e1", None, timestamp="2026-09-17T10:00:00Z")
        measurement_event["evidence_snapshot"] = {
            "snapshot_id": "m1",
            "captured_at": "2026-09-17T10:00:00Z",
        }
        measurement = invoke(
            MEASUREMENT_SCRIPT,
            [measurement_event],
            expected_scope("global-a"),
        )
        self.assertEqual(measurement.returncode, 2)
        self.assertIn("account identity", measurement.stderr.lower())

        realization_event = base_event("e2", None, timestamp="2026-09-17T11:00:00Z")
        realization_event["realization_snapshot"] = {
            "snapshot_id": "r1",
            "captured_at": "2026-09-17T11:00:00Z",
            "realized_surfaces": ["shopping_results"],
            "coverage_status": "Complete",
        }
        realization = invoke(
            REALIZATION_SCRIPT,
            [realization_event],
            expected_scope("global-a"),
        )
        self.assertEqual(realization.returncode, 2)
        self.assertIn("account identity", realization.stderr.lower())

    def test_matching_expected_account_identity_is_accepted(self):
        account = identity("global-a", regional_id="regional-na-a")
        measurement_event = base_event("e1", account, timestamp="2026-09-17T12:00:00Z")
        measurement_event["evidence_snapshot"] = {
            "snapshot_id": "m1",
            "captured_at": "2026-09-17T12:00:00Z",
        }

        result = invoke(
            MEASUREMENT_SCRIPT,
            [measurement_event],
            expected_scope("global-a"),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        projected = json.loads(result.stdout)
        self.assertEqual(projected["account_identity"]["global_advertiser_account_id"], "global-a")


if __name__ == "__main__":
    unittest.main()
