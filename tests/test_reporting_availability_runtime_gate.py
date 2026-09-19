import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/evaluate_connector_capability_gate.py"


def base_snapshot():
    return {
        "connector_id": "fixture",
        "connector_version": "1.0.0",
        "captured_at": "2026-09-19T00:00:00Z",
        "default_access_mode": "Read-only",
        "capabilities": [
            {
                "capability_id": "campaign-performance-read",
                "status": "Supported",
                "access_mode": "report",
                "scope": {"marketplaces": ["US"]},
                "data_contract": {
                    "reporting_generation": "unified-reporting",
                    "reporting_generation_status": "active",
                    "historical_availability_exposed": True,
                    "historical_availability_status": "available",
                },
                "bindings": [
                    {
                        "binding_id": "fixture:campaign-report",
                        "surface_type": "report",
                        "surface_id": "campaign-performance",
                        "surface_version": "1",
                        "verification_status": "Verified",
                        "observed_at": "2026-09-19T00:00:00Z",
                        "scope": {"marketplaces": ["US"]},
                        "evidence": [
                            {
                                "kind": "contract-test",
                                "reference": "fixture",
                                "observed_at": "2026-09-19T00:00:00Z",
                            }
                        ],
                    }
                ],
            }
        ],
    }


def run_gate(snapshot, requirement=None):
    payload = {
        "snapshot": snapshot,
        "required_capabilities": ["campaign-performance-read"],
        "expected_scope": {"marketplace": "US"},
    }
    if requirement is not None:
        payload["data_requirements"] = {
            "campaign-performance-read": requirement
        }
    return subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


class ReportingAvailabilityRuntimeGateTests(unittest.TestCase):
    def test_matching_active_generation_with_available_history_passes(self):
        proc = run_gate(
            base_snapshot(),
            {
                "required_reporting_generation": "unified-reporting",
                "requires_historical_data": True,
            },
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "pass")

    def test_required_reporting_generation_mismatch_blocks(self):
        snapshot = base_snapshot()
        snapshot["capabilities"][0]["data_contract"]["reporting_generation"] = "legacy-sponsored-ads"
        proc = run_gate(
            snapshot,
            {"required_reporting_generation": "unified-reporting"},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "blocked")

    def test_retired_reporting_generation_blocks_even_with_verified_binding(self):
        snapshot = base_snapshot()
        snapshot["capabilities"][0]["data_contract"]["reporting_generation_status"] = "retired"
        proc = run_gate(
            snapshot,
            {"required_reporting_generation": "unified-reporting"},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Blocked")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "blocked")

    def test_unavailable_or_retired_history_blocks_history_dependent_decision(self):
        for status in ("unavailable", "retired"):
            with self.subTest(status=status):
                snapshot = base_snapshot()
                snapshot["capabilities"][0]["data_contract"]["historical_availability_status"] = status
                proc = run_gate(snapshot, {"requires_historical_data": True})
                self.assertEqual(proc.returncode, 0, proc.stderr)
                out = json.loads(proc.stdout)
                self.assertEqual(out["gate_status"], "Blocked")
                self.assertEqual(out["requirements"][0]["data_contract_effect"], "blocked")
                self.assertEqual(out["missing_evidence_policy"], "never_zero")

    def test_partial_history_degrades_instead_of_inventing_completeness(self):
        snapshot = base_snapshot()
        snapshot["capabilities"][0]["data_contract"]["historical_availability_status"] = "partial"
        proc = run_gate(snapshot, {"requires_historical_data": True})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "degraded")

    def test_unknown_history_state_degrades_not_zero(self):
        snapshot = base_snapshot()
        snapshot["capabilities"][0]["data_contract"]["historical_availability_status"] = "unknown"
        proc = run_gate(snapshot, {"requires_historical_data": True})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Degraded")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "unknown")
        self.assertFalse(out["high_confidence_allowed"])

    def test_sunset_scheduled_generation_is_currently_usable_but_warned(self):
        snapshot = base_snapshot()
        contract = snapshot["capabilities"][0]["data_contract"]
        contract["reporting_generation_status"] = "sunset_scheduled"
        contract["sunset_at"] = "2026-12-31T23:59:59Z"
        proc = run_gate(
            snapshot,
            {"required_reporting_generation": "unified-reporting"},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "pass")
        warnings = " ".join(out["requirements"][0]["warnings"]).lower()
        self.assertIn("sunset", warnings)

    def test_no_data_requirement_preserves_existing_capability_behavior(self):
        proc = run_gate(base_snapshot())
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["gate_status"], "Pass")
        self.assertEqual(out["requirements"][0]["data_contract_effect"], "not_evaluated")

    def test_data_requirement_for_non_required_capability_is_configuration_error(self):
        proc = subprocess.run(
            [sys.executable, str(GATE)],
            input=json.dumps({
                "snapshot": base_snapshot(),
                "required_capabilities": ["campaign-performance-read"],
                "data_requirements": {
                    "historical-availability-observe": {
                        "requires_historical_data": True
                    }
                },
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("required_capabilities", proc.stderr)


if __name__ == "__main__":
    unittest.main()
