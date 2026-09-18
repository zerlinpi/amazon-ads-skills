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
