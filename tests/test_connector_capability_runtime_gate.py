import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_connector_capability_gate.py"
REFERENCE = ROOT / "references/connector-capability.md"
SKILLS = ["amazon-ads-audit","amazon-ads-optimizer","anomaly-detection","bid-optimization","budget-optimization","campaign-health-monitor","experiment-planner","growth-opportunity-finder","keyword-optimization","negative-targeting","performance-drop-diagnosis","placement-optimization","post-change-review","profitability-analysis","search-term-analysis"]


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

    def test_partial_requirement_forces_directional_or_hold(self):
        proc = run_gate({
            "snapshot": {
                "connector_id": "fixture",
                "captured_at": "2026-09-18T00:00:00Z",
                "default_access_mode": "Read-only",
                "capabilities": [
                    {"capability_id": "search-term-origin", "status": "Partial", "access_mode": "report"}
                ],
            },
            "required_capabilities": ["search-term-origin"],
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
                    {"capability_id": "current-bid-readback", "status": "Unsupported", "access_mode": "read"}
                ],
            },
            "required_capabilities": ["current-bid-readback"],
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["missing_evidence_policy"], "never_zero")
        self.assertIn("Alternate Source", out["allowed_decision_classes"])
        self.assertIn("Missing Data", out["allowed_decision_classes"])

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
