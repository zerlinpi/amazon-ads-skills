import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryNavigationTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_readme_is_a_user_entrypoint_not_a_deep_technical_dump(self):
        readme = self.read("README.md")
        required_headings = [
            "## What you can do",
            "## Start here",
            "## How it works",
            "## Capability map",
            "## Safety boundaries",
            "## Documentation",
        ]
        positions = [readme.index(heading) for heading in required_headings]
        self.assertEqual(positions, sorted(positions))

        for link in (
            "docs/CAPABILITIES.md",
            "docs/ARCHITECTURE.md",
            "docs/README.md",
            "CHANGELOG.md",
        ):
            self.assertIn(link, readme)

        deep_dive_headings = (
            "## MCP / Connector capability layer",
            "## Data reliability",
            "## Optimization memory",
            "## Experiments",
            "## Evaluation",
            "## Runtime compatibility",
        )
        for heading in deep_dive_headings:
            self.assertNotIn(heading, readme)

    def test_documentation_has_clear_active_navigation_layers(self):
        for path in (
            "docs/README.md",
            "docs/CAPABILITIES.md",
            "docs/ARCHITECTURE.md",
            "docs/research/README.md",
            "docs/archive/README.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_legacy_superpowers_design_is_archived_out_of_active_docs(self):
        self.assertFalse((ROOT / "docs/superpowers").exists())
        self.assertTrue(
            (ROOT / "docs/archive/legacy-design/2026-09-07-amazon-ads-agent-skills.md").is_file()
        )
        self.assertTrue(
            (ROOT / "docs/archive/legacy-design/2026-09-07-amazon-ads-agent-skills-design.md").is_file()
        )


if __name__ == "__main__":
    unittest.main()
