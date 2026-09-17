import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RuntimeOnboardingTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_getting_started_covers_clone_runtime_routes_and_verification(self):
        guide_path = ROOT / "docs/GETTING-STARTED.md"
        self.assertTrue(guide_path.is_file())
        guide = guide_path.read_text(encoding="utf-8")

        required = (
            "git clone https://github.com/zerlinpi/amazon-ads-skills.git",
            "## Codex",
            "## Claude Code",
            "## WorkBuddy",
            "## Manual / explicit Skill loading",
            "AGENTS.md",
            "CLAUDE.md",
            "skills/amazon-ads-optimizer/SKILL.md",
            "python -m unittest discover -s tests -v",
            "python scripts/validate_skills.py .",
            "python scripts/validate_evals.py .",
            "Suggest",
            "External Connector / Executor",
        )
        for text in required:
            self.assertIn(text, guide)

    def test_public_entrypoints_link_to_getting_started(self):
        for path in ("README.md", "AGENTS.md", "CLAUDE.md"):
            self.assertIn("docs/GETTING-STARTED.md", self.read(path), path)

    def test_bootstrap_prompts_are_copyable_and_fail_closed(self):
        guide_lower = self.read("docs/GETTING-STARTED.md").lower()
        required = (
            "bootstrap prompt",
            "read the repository instructions",
            "do not perform live amazon ads writes",
            "state which skill you selected",
            "list missing inputs instead of guessing",
        )
        for text in required:
            self.assertIn(text, guide_lower)

    def test_examples_do_not_reintroduce_global_percent_guardrail(self):
        examples = self.read("examples/README.md")
        self.assertNotIn('"single bid change <= 20%"', examples)
        self.assertIn("contextual action sizing", examples.lower())

    def test_ci_covers_runtime_facing_onboarding_contracts(self):
        workflow = self.read(".github/workflows/validate-skills.yml")
        required_paths = (
            '"README.md"',
            '"AGENTS.md"',
            '"CLAUDE.md"',
            '"docs/**"',
            '"examples/**"',
            '".codex-plugin/**"',
            '".claude-plugin/**"',
            '".workbuddy-plugin/**"',
        )
        for path in required_paths:
            self.assertIn(path, workflow)


if __name__ == "__main__":
    unittest.main()
