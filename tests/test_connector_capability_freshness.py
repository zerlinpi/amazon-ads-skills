import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_connector_capability_gate.py"


def run_gate(payload):
    return subprocess.run([sys.executable, str(GATE)], input=json.dumps(payload), text=True, capture_output=True, check=False)


def supported_snapshot(observed_at="2026-09-18T00:00:00Z", captured_at=None, evidence_observed_at=None):
    captured_at = observed_at if captured_at is None else captured_at
    evidence_observed_at = observed_at if evidence_observed_at is None else evidence_observed_at
    return {"connector_id": "fixture", "connector_version": "1.0.0", "captured_at": captured_at, "default_access_mode": "Read-only", "capabilities": [{"capability_id": "campaign-performance-read", "status": "Supported", "access_mode": "report", "bindings": [{"binding_id": "fixture:campaign-report", "surface_type": "report", "surface_id": "campaign-performance-v3", "verification_status": "Verified", "observed_at": observed_at, "evidence": [{"kind": "contract-test", "reference": "fixture", "observed_at": evidence_observed_at}]}]}]}


class ConnectorCapabilityFreshnessTests(unittest.TestCase):
    def test_stale_verified_binding_cannot_preserve_high_confidence(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-01T00:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "stale")
        self.assertEqual(out["missing_evidence_policy"], "never_zero")

    def test_recent_verified_binding_passes_same_explicit_horizon(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T12:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertTrue(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "pass")

    def test_stale_snapshot_with_newer_binding_claim_remains_degraded(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T12:00:00Z", captured_at="2026-09-01T00:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["snapshot_freshness_effect"], "stale")
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "unknown")

    def test_recent_snapshot_cannot_rescue_stale_binding(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-01T00:00:00Z", captured_at="2026-09-17T12:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["snapshot_freshness_effect"], "pass")
        self.assertEqual(out["requirements"][0]["freshness_effect"], "stale")
        self.assertEqual(out["gate_status"], "Degraded")

    def test_recent_binding_cannot_launder_stale_supporting_evidence(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T12:00:00Z", evidence_observed_at="2026-09-01T00:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "stale")

    def test_recent_supporting_evidence_preserves_recent_verified_binding(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T12:00:00Z", evidence_observed_at="2026-09-17T11:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertTrue(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "pass")

    def test_evidence_after_binding_verification_is_not_causal_support(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T10:00:00Z", captured_at="2026-09-17T12:00:00Z", evidence_observed_at="2026-09-17T11:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "unknown")

    def test_binding_after_snapshot_capture_is_not_part_of_that_snapshot(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-09-17T12:00:00Z", captured_at="2026-09-17T10:00:00Z", evidence_observed_at="2026-09-17T09:00:00Z"), "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "unknown")

    def test_timestamp_only_evidence_cannot_prove_verified_binding(self):
        snapshot = supported_snapshot("2026-09-17T12:00:00Z")
        evidence = snapshot["capabilities"][0]["bindings"][0]["evidence"][0]
        evidence["kind"] = None
        evidence["reference"] = None
        proc = run_gate({"snapshot": snapshot, "required_capabilities": ["campaign-performance-read"], "freshness_requirement": {"as_of": "2026-09-18T00:00:00Z", "max_age_seconds": 86400}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertFalse(out["high_confidence_allowed"])
        self.assertEqual(out["requirements"][0]["freshness_effect"], "unknown")

    def test_no_freshness_requirement_does_not_invent_global_ttl(self):
        proc = run_gate({"snapshot": supported_snapshot("2026-01-01T00:00:00Z"), "required_capabilities": ["campaign-performance-read"]})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertEqual(out["snapshot_freshness_effect"], "not_evaluated")
        self.assertEqual(out["requirements"][0]["freshness_effect"], "not_evaluated")


if __name__ == "__main__":
    unittest.main()
