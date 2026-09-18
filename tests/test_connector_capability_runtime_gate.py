import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_connector_capability_gate.py"
REFERENCE = ROOT / "references/connector-capability.md"
SKILLS = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))


def run_gate(payload):
    proc = subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    return proc


class ConnectorCapabilityRuntimeGateTests(unittest.TestCase):
    def test_all_skill_entrypoints_route_through_connector_capability_gate(self):
        self.assertGreaterEqual(len(SKILLS), 15, "expected the repository Skill catalog to be discoverable")
        for name in SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(
                "../../references/connector-capability.md",
                text,
                msg=f"{name} must load the shared connector capability gate when connector evidence matters",
            )
            self.assertIn(
                "evaluate_connector_capability_gate.py",
                text,
                msg=f"{name} must point to the deterministic gate helper",
            )

    def test_supported_capability_without_verified_binding_is_degraded(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "connector_version": "1.0.0",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {
                        "capability_id": "campaign-performance-read",
                        "status": "Supported",
                        "access_mode": "report",
                    }
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["binding_effect"], "unknown")

    def test_supported_capability_with_verified_binding_passes(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "connector_version": "1.0.0",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {
                        "capability_id": "campaign-performance-read",
                        "status": "Supported",
                        "access_mode": "report",
                        "bindings": [
                            {
                                "binding_id": "fixture:campaign-report",
                                "surface_type": "report",
                                "surface_id": "campaign-performance-v3",
                                "surface_version": "3",
                                "verification_status": "Verified",
                                "observed_at": "2026-09-18T00:00:00Z",
                                "scope": {
                                    "marketplaces": ["US"],
                                    "ad_products": ["Sponsored Products"],
                                },
                                "evidence": [
                                    {
                                        "kind": "contract-test",
                                        "reference": "fixture",
                                        "observed_at": "2026-09-18T00:00:00Z",
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
            "expected_scope": {
                "marketplace": "US",
                "ad_product": "Sponsored Products",
            },
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertTrue(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["binding_effect"], "pass")
        self.assertEqual(
            out["requirements"][0]["verified_binding_ids"],
            ["fixture:campaign-report"],
        )

    def test_unverified_binding_cannot_preserve_high_confidence(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "connector_version": "1.0.0",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {
                        "capability_id": "campaign-performance-read",
                        "status": "Supported",
                        "access_mode": "report",
                        "bindings": [
                            {
                                "binding_id": "fixture:guessed-tool",
                                "surface_type": "tool",
                                "surface_id": "campaign_report",
                                "verification_status": "Unverified",
                                "observed_at": "2026-09-18T00:00:00Z",
                                "evidence": [],
                            }
                        ],
                    }
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["binding_effect"], "unverified")

    def test_supported_requirement_passes(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {"capability_id": "campaign-performance-read", "status": "Supported", "access_mode": "read"}
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertTrue(out["high_confidence_allowed"])

    def test_supported_capability_outside_requested_marketplace_is_blocked(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {
                        "capability_id": "campaign-performance-read",
                        "status": "Supported",
                        "access_mode": "report",
                        "scope": {"marketplaces": ["US"], "ad_products": ["Sponsored Products"]},
                    }
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
            "expected_scope": {"marketplace": "JP", "ad_product": "Sponsored Products"},
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["scope_effect"], "blocked")
        self.assertIn("marketplace", " ".join(out["requirements"][0]["warnings"]).lower())

    def test_supported_capability_with_matching_scope_passes(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {
                        "capability_id": "campaign-performance-read",
                        "status": "Supported",
                        "access_mode": "report",
                        "scope": {"marketplaces": ["JP", "US"], "ad_products": ["Sponsored Products"]},
                    }
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
            "expected_scope": {"marketplace": "JP", "ad_product": "Sponsored Products"},
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertEqual(out["requirements"][0]["scope_effect"], "pass")

    def test_expected_scope_without_connector_scope_is_blocked_not_assumed_global(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {"capability_id": "campaign-performance-read", "status": "Supported", "access_mode": "report"}
                ],
            },
            "required_capabilities": ["campaign-performance-read"],
            "expected_scope": {"marketplace": "JP"},
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertEqual(out["requirements"][0]["scope_effect"], "unknown")
        self.assertEqual(out["missing_evidence_policy"], "never_zero")

    def test_partial_requirement_forces_directional_or_hold(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {"capability_id": "search-term-origin-read", "status": "Partial", "access_mode": "report"}
                ],
            },
            "required_capabilities": ["search-term-origin-read"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertIn("Directional", out["allowed_decision_classes"])
        self.assertIn("Hold", out["allowed_decision_classes"])
        self.assertEqual(out["missing_evidence_policy"], "never_zero")

    def test_unsupported_requirement_blocks_high_confidence_action(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {"capability_id": "entity-state-readback", "status": "Unsupported", "access_mode": "read"}
                ],
            },
            "required_capabilities": ["entity-state-readback"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["missing_evidence_policy"], "never_zero")
        self.assertIn("Alternate Source", out["allowed_decision_classes"])
        self.assertIn("Missing Data", out["allowed_decision_classes"])

    def test_unregistered_required_capability_is_configuration_error(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [],
            },
            "required_capabilities": ["invented-current-bid-capability"],
        })
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unregistered capability", proc.stderr.lower())

    def test_missing_or_unknown_capability_is_blocked_not_zero(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [],
            },
            "required_capabilities": ["inventory-read"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertEqual(out["requirements"][0]["status"], "Unknown")
        self.assertNotEqual(out["requirements"][0].get("value"), 0)
        self.assertEqual(out["missing_evidence_policy"], "never_zero")

    def test_reference_defines_runtime_gate_before_metric_interpretation(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("evaluate_connector_capability_gate.py", text)
        self.assertIn("before metric interpretation", text.lower())
        self.assertIn("never_zero", text)


if __name__ == "__main__":
    unittest.main()
