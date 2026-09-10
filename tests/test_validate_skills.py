import tempfile
import unittest
from pathlib import Path

from scripts.validate_skills import validate_repository


class SkillValidatorTests(unittest.TestCase):
    def make_repo(self, skill_body: str, extra_files=None):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        skill = root / "skills" / "sample-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(skill_body, encoding="utf-8")
        for rel, content in (extra_files or {}).items():
            path = skill / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        self.addCleanup(td.cleanup)
        return root

    def test_accepts_spec_frontmatter_and_existing_local_reference(self):
        root = self.make_repo(
            """---\nname: sample-skill\ndescription: Sample workflow\nlicense: MIT\nmetadata:\n  maturity: stable\n---\n\nRead [details](references/details.md).\n""",
            {"references/details.md": "# Details\n"},
        )
        self.assertEqual([], validate_repository(root))

    def test_rejects_unexpected_top_level_frontmatter_field(self):
        root = self.make_repo(
            """---\nname: sample-skill\ndescription: Sample workflow\nversion: 1.0.0\n---\n"""
        )
        errors = validate_repository(root)
        self.assertTrue(any("unexpected frontmatter field 'version'" in e for e in errors))

    def test_rejects_folder_name_mismatch(self):
        root = self.make_repo(
            """---\nname: other-name\ndescription: Sample workflow\n---\n"""
        )
        errors = validate_repository(root)
        self.assertTrue(any("must match folder name 'sample-skill'" in e for e in errors))

    def test_rejects_broken_relative_markdown_link(self):
        root = self.make_repo(
            """---\nname: sample-skill\ndescription: Sample workflow\n---\n\nRead [missing](references/missing.md).\n"""
        )
        errors = validate_repository(root)
        self.assertTrue(any("broken local reference" in e for e in errors))

    def test_allows_repository_local_shared_reference(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        skill = root / "skills" / "sample-skill"
        skill.mkdir(parents=True)
        shared = root / "references" / "shared.md"
        shared.parent.mkdir()
        shared.write_text("# Shared\n", encoding="utf-8")
        (skill / "SKILL.md").write_text(
            "---\nname: sample-skill\ndescription: Sample workflow\n---\n\nRead [shared](../../references/shared.md).\n",
            encoding="utf-8",
        )
        self.assertEqual([], validate_repository(root))

    def test_rejects_nested_skill(self):
        root = self.make_repo(
            """---\nname: sample-skill\ndescription: Sample workflow\n---\n""",
            {"references/nested/SKILL.md": "---\nname: nested\ndescription: bad\n---\n"},
        )
        errors = validate_repository(root)
        self.assertTrue(any("nested SKILL.md" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
