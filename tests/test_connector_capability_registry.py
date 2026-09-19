import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "references/connector-capability-catalog.json"
RESOLVER = ROOT / "scripts/resolve_skill_capabilities.py"
SKILLS = sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))


class ConnectorCapabilityRegistryTests(unittest.TestCase):
    def load_catalog(self):
        return json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_catalog_exists_and_covers_every_discovered_skill(self):
        catalog = self.load_catalog()
        self.assertGreaterEqual(len(SKILLS), 15)
        self.assertEqual(set(catalog["skills"]), set(SKILLS))

    def test_capability_ids_are_unique_and_read_only(self):
        catalog = self.load_catalog()
        capabilities = catalog["capabilities"]
        ids = [item["capability_id"] for item in capabilities]
        self.assertEqual(len(ids), len(set(ids)))
        for item in capabilities:
            self.assertIn(item["access_mode"], {"read", "report", "observe", "stream"})
            self.assertNotIn("write", item["capability_id"].lower())

    def test_skill_profiles_only_reference_registered_capabilities(self):
        catalog = self.load_catalog()
        known = {item["capability_id"] for item in catalog["capabilities"]}
        for skill, profiles in catalog["skills"].items():
            self.assertIn("live-analysis", profiles, skill)
            for profile, spec in profiles.items():
                self.assertTrue(spec["required"] or spec["optional"], f"{skill}:{profile}")
                for capability_id in spec["required"] + spec["optional"]:
                    self.assertIn(capability_id, known, f"{skill}:{profile}:{capability_id}")

    def test_core_capabilities_have_stable_ids(self):
        catalog = self.load_catalog()
        known = {item["capability_id"] for item in catalog["capabilities"]}
        for capability_id in (
            "profile-identity-read",
            "campaign-performance-read",
            "report-completeness-observe",
            "metric-semantics-observe",
            "entity-state-readback",
            "change-history-read",
            "retail-readiness-read",
        ):
            self.assertIn(capability_id, known)

    def test_resolver_returns_registered_profile(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({"skill": "bid-optimization", "profile": "action-safe-proposal"}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["skill"], "bid-optimization")
        self.assertEqual(result["profile"], "action-safe-proposal")
        self.assertIn("entity-state-readback", result["required_capabilities"])
        self.assertTrue(result["catalog_version"])


    def test_outcome_review_requires_performance_and_historical_data(self):
        catalog = self.load_catalog()
        spec = catalog["skills"]["post-change-review"]["outcome-review"]
        self.assertIn("campaign-performance-read", spec["required"])
        self.assertIn("historical-availability-observe", spec["required"])
        self.assertEqual(
            spec["data_requirements"],
            {
                "campaign-performance-read": {
                    "requires_historical_data": True,
                }
            },
        )

    def test_profile_data_requirements_only_target_required_capabilities(self):
        catalog = self.load_catalog()
        allowed_fields = {
            "required_reporting_generation",
            "requires_historical_data",
        }
        for skill, profiles in catalog["skills"].items():
            for profile, spec in profiles.items():
                requirements = spec.get("data_requirements", {})
                self.assertIsInstance(requirements, dict, f"{skill}:{profile}")
                for capability_id, requirement in requirements.items():
                    self.assertIn(
                        capability_id,
                        spec["required"],
                        f"{skill}:{profile}:{capability_id}",
                    )
                    self.assertIsInstance(requirement, dict)
                    self.assertTrue(requirement)
                    self.assertTrue(
                        set(requirement).issubset(allowed_fields),
                        f"{skill}:{profile}:{capability_id}",
                    )

    def test_resolver_emits_profile_data_requirements(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "post-change-review",
                "profile": "outcome-review",
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertIn("campaign-performance-read", result["required_capabilities"])
        self.assertEqual(
            result["data_requirements"],
            {
                "campaign-performance-read": {
                    "requires_historical_data": True,
                }
            },
        )
        self.assertEqual(
            result["policy"]["use_with"],
            "scripts/evaluate_connector_capability_gate.py",
        )

    def test_resolver_emits_empty_data_requirements_for_unconstrained_profile(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "bid-optimization",
                "profile": "action-safe-proposal",
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["data_requirements"], {})


    def test_task_history_window_merges_without_relaxing_profile_requirement(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "post-change-review",
                "profile": "outcome-review",
                "task_data_requirements": {
                    "campaign-performance-read": {
                        "history_window": {
                            "start_date": "2026-08-01",
                            "end_date": "2026-09-15",
                            "grain": "daily",
                        }
                    }
                },
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(
            result["data_requirements"]["campaign-performance-read"],
            {
                "requires_historical_data": True,
                "history_window": {
                    "start_date": "2026-08-01",
                    "end_date": "2026-09-15",
                    "grain": "daily",
                },
            },
        )
        self.assertEqual(
            result["data_requirement_provenance"]["profile"],
            {
                "campaign-performance-read": {
                    "requires_historical_data": True,
                }
            },
        )
        self.assertEqual(
            result["data_requirement_provenance"]["task"],
            {
                "campaign-performance-read": {
                    "requires_historical_data": True,
                    "history_window": {
                        "start_date": "2026-08-01",
                        "end_date": "2026-09-15",
                        "grain": "daily",
                    },
                }
            },
        )

    def test_task_requirement_cannot_relax_profile_historical_requirement(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "post-change-review",
                "profile": "outcome-review",
                "task_data_requirements": {
                    "campaign-performance-read": {
                        "requires_historical_data": False,
                    }
                },
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("cannot relax", proc.stderr.lower())

    def test_task_requirement_must_target_required_capability(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "post-change-review",
                "profile": "outcome-review",
                "task_data_requirements": {
                    "change-history-read": {
                        "requires_historical_data": True,
                    }
                },
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("required", proc.stderr.lower())

    def test_task_can_strengthen_unconstrained_profile_with_explicit_generation(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({
                "skill": "bid-optimization",
                "profile": "action-safe-proposal",
                "task_data_requirements": {
                    "target-performance-read": {
                        "required_reporting_generation": "unified-reporting",
                    }
                },
            }),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(
            result["data_requirements"],
            {
                "target-performance-read": {
                    "required_reporting_generation": "unified-reporting",
                }
            },
        )

    def test_task_history_window_rejects_invalid_or_reversed_dates(self):
        for window in (
            {"start_date": "2026-09-20", "end_date": "2026-09-01", "grain": "daily"},
            {"start_date": "not-a-date", "end_date": "2026-09-01", "grain": "daily"},
        ):
            with self.subTest(window=window):
                proc = subprocess.run(
                    [sys.executable, str(RESOLVER)],
                    input=json.dumps({
                        "skill": "post-change-review",
                        "profile": "outcome-review",
                        "task_data_requirements": {
                            "campaign-performance-read": {
                                "history_window": window,
                            }
                        },
                    }),
                    text=True,
                    capture_output=True,
                    cwd=ROOT,
                    check=False,
                )
                self.assertEqual(proc.returncode, 2)
                self.assertIn("history_window", proc.stderr)

    def test_resolver_fails_closed_on_unknown_profile(self):
        proc = subprocess.run(
            [sys.executable, str(RESOLVER)],
            input=json.dumps({"skill": "bid-optimization", "profile": "invented-profile"}),
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown", proc.stderr.lower())


if __name__ == "__main__":
    unittest.main()
