import json
import unittest
from pathlib import Path

from scripts.evaluate_connector_capability_gate import evaluate_connector_capability_gate
from scripts.resolve_skill_capabilities import resolve_skill_capabilities

ROOT = Path(__file__).resolve().parents[1]


def verified_readback(control_types=None):
    data_contract = {}
    if control_types is not None:
        data_contract["control_types_exposed"] = control_types
    return {
        "connector_id": "fixture",
        "connector_version": "1.0.0",
        "captured_at": "2026-09-21T00:00:00Z",
        "default_access_mode": "Read-only",
        "capabilities": [
            {
                "capability_id": "entity-state-readback",
                "status": "Supported",
                "access_mode": "read",
                "data_contract": data_contract,
                "bindings": [
                    {
                        "binding_id": "fixture:entity-state",
                        "surface_type": "endpoint",
                        "surface_id": "entity-state",
                        "verification_status": "Verified",
                        "observed_at": "2026-09-21T00:00:00Z",
                        "evidence": [
                            {
                                "kind": "contract-test",
                                "reference": "fixture",
                                "observed_at": "2026-09-21T00:00:00Z",
                            }
                        ],
                    }
                ],
            }
        ],
    }


class ControlCapabilityBindingTests(unittest.TestCase):
    def test_resolver_derives_exact_control_requirements_from_decision_surface(self):
        registry = json.loads((ROOT / "references/control-requirement-registry.json").read_text(encoding="utf-8"))
        expected = registry["decision_surfaces"]["sponsored_products_bid_change"]["required_control_types"]

        resolved = resolve_skill_capabilities({
            "skill": "post-change-review",
            "profile": "outcome-review",
            "decision_surface": "sponsored_products_bid_change",
        })

        self.assertEqual(
            resolved["data_requirements"]["entity-state-readback"]["required_control_types"],
            expected,
        )
        self.assertEqual(
            resolved["control_requirement_provenance"],
            {
                "decision_surface": "sponsored_products_bid_change",
                "requirement_registry_id": registry["registry_id"],
            },
        )

    def test_resolver_rejects_unknown_decision_surface(self):
        with self.assertRaisesRegex(ValueError, "unknown decision_surface"):
            resolve_skill_capabilities({
                "skill": "post-change-review",
                "profile": "outcome-review",
                "decision_surface": "invented_surface",
            })

    def test_gate_blocks_supported_readback_when_required_control_type_is_missing(self):
        required = [
            "base_bid",
            "bidding_strategy",
            "placement_adjustment",
            "audience_bid_adjustment",
            "schedule_or_event_rule",
            "budget_or_pacing",
            "targeting_or_routing",
        ]
        result = evaluate_connector_capability_gate({
            "snapshot": verified_readback(required[:-1]),
            "required_capabilities": ["entity-state-readback"],
            "data_requirements": {
                "entity-state-readback": {
                    "required_control_types": required,
                }
            },
        })
        self.assertEqual(result["gate_status"], "Blocked")
        self.assertFalse(result["high_confidence_allowed"])
        requirement = result["requirements"][0]
        self.assertEqual(requirement["data_contract_effect"], "blocked")
        self.assertTrue(any("targeting_or_routing" in warning for warning in requirement["warnings"]))

    def test_gate_blocks_unproven_control_type_coverage(self):
        required = ["base_bid", "targeting_or_routing"]
        result = evaluate_connector_capability_gate({
            "snapshot": verified_readback(),
            "required_capabilities": ["entity-state-readback"],
            "data_requirements": {
                "entity-state-readback": {
                    "required_control_types": required,
                }
            },
        })
        self.assertEqual(result["gate_status"], "Blocked")
        self.assertFalse(result["high_confidence_allowed"])

    def test_gate_passes_exact_or_superset_control_type_coverage(self):
        required = ["base_bid", "targeting_or_routing"]
        result = evaluate_connector_capability_gate({
            "snapshot": verified_readback([
                "base_bid",
                "bidding_strategy",
                "targeting_or_routing",
            ]),
            "required_capabilities": ["entity-state-readback"],
            "data_requirements": {
                "entity-state-readback": {
                    "required_control_types": required,
                }
            },
        })
        self.assertEqual(result["gate_status"], "Pass")
        self.assertTrue(result["high_confidence_allowed"])

    def test_connector_schema_exposes_control_type_coverage(self):
        schema = json.loads((ROOT / "schemas/connector-capability-snapshot.json").read_text(encoding="utf-8"))
        data_contract = schema["properties"]["capabilities"]["items"]["properties"]["data_contract"]["properties"]
        self.assertIn("control_types_exposed", data_contract)
        field = data_contract["control_types_exposed"]
        self.assertEqual(field["type"], "array")
        self.assertTrue(field["uniqueItems"])


if __name__ == "__main__":
    unittest.main()
