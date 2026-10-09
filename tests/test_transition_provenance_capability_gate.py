import json
import unittest
from pathlib import Path

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from scripts.resolve_skill_capabilities import resolve_skill_capabilities

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = ["management_mode", "last_transition_actor"]


def verified_connector(exposed=None):
    contract = {"control_types_exposed": ["base_bid"]}
    if exposed is not None:
        contract["transition_provenance_fields_exposed"] = exposed
    return {
        "connector_id": "bounded-fixture", "captured_at": "2026-10-09T00:00:00Z",
        "default_access_mode": "Read-only",
        "capabilities": [{
            "capability_id": "entity-state-readback", "status": "Supported",
            "access_mode": "read", "data_contract": contract,
            "bindings": [{
                "binding_id": "verified-state-only", "surface_type": "endpoint",
                "surface_id": "state-read", "verification_status": "Verified",
                "observed_at": "2026-10-09T00:00:00Z",
                "evidence": [{"kind": "contract-test", "reference": "synthetic"}],
            }],
        }],
    }


class TransitionProvenanceCapabilityGateTests(unittest.TestCase):
    def test_required_actor_fields_not_proven_by_supported_state_readback(self):
        req = {"entity-state-readback": {"required_transition_provenance_fields": REQUIRED_FIELDS}}
        result = evaluate_connector_capability_gate({
            "snapshot": verified_connector(), "required_capabilities": ["entity-state-readback"],
            "data_requirements": req,
        })
        self.assertEqual(result["gate_status"], "Blocked")
        self.assertFalse(result["high_confidence_allowed"])

    def test_partial_provenance_field_coverage_blocks_actor_attribution(self):
        result = evaluate_connector_capability_gate({
            "snapshot": verified_connector(["management_mode"]),
            "required_capabilities": ["entity-state-readback"],
            "data_requirements": {"entity-state-readback": {"required_transition_provenance_fields": REQUIRED_FIELDS}},
        })
        self.assertEqual(result["gate_status"], "Blocked")

    def test_full_verified_provenance_observability_allows_capability_gate(self):
        result = evaluate_connector_capability_gate({
            "snapshot": verified_connector(REQUIRED_FIELDS + ["transition_reason"]),
            "required_capabilities": ["entity-state-readback"],
            "data_requirements": {"entity-state-readback": {"required_transition_provenance_fields": REQUIRED_FIELDS}},
        })
        self.assertEqual(result["gate_status"], "Pass")
        self.assertTrue(result["high_confidence_allowed"])

    def test_resolver_preserves_task_provenance_fields(self):
        resolved = resolve_skill_capabilities({
            "skill": "post-change-review", "profile": "outcome-review",
            "task_data_requirements": {"entity-state-readback": {
                "required_transition_provenance_fields": REQUIRED_FIELDS,
            }},
        })
        self.assertEqual(
            resolved["data_requirements"]["entity-state-readback"]["required_transition_provenance_fields"],
            REQUIRED_FIELDS,
        )

    def test_provenance_requirement_cannot_be_redirected_to_metric_report(self):
        with self.assertRaises(ValueError):
            resolve_skill_capabilities({
                "skill": "post-change-review", "profile": "outcome-review",
                "task_data_requirements": {"campaign-performance-read": {
                    "required_transition_provenance_fields": REQUIRED_FIELDS,
                }},
            })

    def test_schema_exposes_observed_provenance_fields(self):
        schema = json.loads((ROOT / "schemas/connector-capability-snapshot.json").read_text(encoding="utf-8"))
        props = schema["properties"]["capabilities"]["items"]["properties"]["data_contract"]["properties"]
        self.assertIn("transition_provenance_fields_exposed", props)
        self.assertTrue(props["transition_provenance_fields_exposed"]["uniqueItems"])


if __name__ == "__main__":
    unittest.main()
