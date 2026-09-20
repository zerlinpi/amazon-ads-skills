import unittest
from pathlib import Path

from scripts.resolve_skill_context import build_skill_catalog, resolve_skill_context

ROOT = Path(__file__).resolve().parents[1]


class SkillContextResolverTests(unittest.TestCase):
    def test_catalog_is_metadata_only_for_all_canonical_skills(self):
        catalog = build_skill_catalog(ROOT)
        self.assertEqual(len(catalog), 15)
        self.assertEqual(len({item["name"] for item in catalog}), 15)
        for item in catalog:
            self.assertEqual(set(item), {"name", "description", "entrypoint"})
            self.assertTrue(item["name"])
            self.assertTrue(item["description"])
            self.assertEqual(item["entrypoint"], f'skills/{item["name"]}/SKILL.md')
            self.assertNotIn("content", item)
            self.assertNotIn("body", item)

    def test_resolve_preloads_only_selected_skill_and_defers_resources(self):
        result = resolve_skill_context(ROOT, "bid-optimization", "action-safe-proposal")
        self.assertEqual(result["skill"], "bid-optimization")
        self.assertEqual(result["preload_files"], ["skills/bid-optimization/SKILL.md"])
        self.assertTrue(result["context_policy"]["metadata_only_catalog"])
        self.assertTrue(result["context_policy"]["resources_on_demand"])
        self.assertEqual(result["context_policy"]["write_authority"], "none")
        self.assertNotIn("content", result)
        self.assertNotIn("body", result)
        self.assertFalse(any(path.startswith("docs/research/") for path in result["resource_candidates"]))
        self.assertFalse(any(path.startswith("evals/") for path in result["resource_candidates"]))
        self.assertFalse(any(
            path.startswith("skills/") and path != "skills/bid-optimization/SKILL.md"
            for path in result["preload_files"]
        ))

    def test_resolve_reuses_canonical_connector_capability_profile(self):
        result = resolve_skill_context(ROOT, "bid-optimization", "action-safe-proposal")
        connector = result["connector_profile"]
        self.assertEqual(connector["profile"], "action-safe-proposal")
        self.assertIn("bid-state-read", connector["required_capabilities"])
        self.assertIn("entity-state-readback", connector["required_capabilities"])
        self.assertEqual(connector["write_authority"], "none")

    def test_unknown_skill_fails_closed(self):
        with self.assertRaises(ValueError):
            resolve_skill_context(ROOT, "not-a-real-skill", "live-analysis")


if __name__ == "__main__":
    unittest.main()
