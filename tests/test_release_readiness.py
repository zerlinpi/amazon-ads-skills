import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_ci_uses_current_node24_generation_github_actions(self):
        workflow = self.read(".github/workflows/validate-skills.yml")
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v7", workflow)
        self.assertNotIn("actions/checkout@v4", workflow)
        self.assertNotIn("actions/setup-python@v5", workflow)

    def test_runtime_manifests_and_readme_publish_v1(self):
        for path in (
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            ".workbuddy-plugin/plugin.json",
        ):
            manifest = json.loads(self.read(path))
            self.assertEqual(manifest["version"], "1.0.0", path)

        self.assertIn("当前版本：`v1.0.0`", self.read("README.md"))

    def test_public_docs_route_to_new_measurement_and_effectiveness_tools(self):
        readme = self.read("README.md")
        agents = self.read("AGENTS.md")
        required_paths = (
            "scripts/project_measurement_history.py",
            "scripts/summarize_skill_effectiveness.py",
            "schemas/skill-effectiveness-benchmark.json",
        )
        for path in required_paths:
            self.assertIn(path, readme)
            self.assertIn(path, agents)


if __name__ == "__main__":
    unittest.main()
