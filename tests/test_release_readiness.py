import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def release_version(self) -> str:
        return self.read("VERSION").strip()

    def test_ci_uses_current_node24_generation_github_actions(self):
        workflow = self.read(".github/workflows/validate-skills.yml")
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v7", workflow)
        self.assertNotIn("actions/checkout@v4", workflow)
        self.assertNotIn("actions/setup-python@v5", workflow)

    def test_release_version_is_semver_and_all_public_surfaces_match(self):
        version = self.release_version()
        self.assertRegex(version, r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")

        for path in (
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            ".workbuddy-plugin/plugin.json",
        ):
            manifest = json.loads(self.read(path))
            self.assertEqual(manifest["version"], version, path)

        expected_readme_label = "当前版本：" + chr(96) + f"v{version}" + chr(96)
        self.assertIn(expected_readme_label, self.read("README.md"))

        changelog = self.read("CHANGELOG.md")
        self.assertRegex(
            changelog,
            rf"(?m)^## v{re.escape(version)}(?:\s|$)",
            "CHANGELOG.md must contain an entry for VERSION",
        )

    def test_version_governance_is_documented_for_future_release_worthy_changes(self):
        agents = self.read("AGENTS.md")
        contributing = self.read("CONTRIBUTING.md")
        pull_request_template = self.read(".github/pull_request_template.md")

        for text in (agents, contributing):
            self.assertIn("VERSION", text)
            self.assertIn("PATCH", text)
            self.assertIn("MINOR", text)
            self.assertIn("MAJOR", text)

        self.assertIn("Version impact", pull_request_template)
        self.assertIn("CHANGELOG.md", pull_request_template)

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
