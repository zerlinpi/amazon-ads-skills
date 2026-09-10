import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_evals import validate_repository


class EvalValidatorTests(unittest.TestCase):
    def make_repo(self, fixture: dict, entrypoint: str = "skills/sample-skill/SKILL.md"):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        (root / "evals" / "fixtures").mkdir(parents=True)
        skill = root / entrypoint
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("---\nname: sample-skill\ndescription: sample\n---\n", encoding="utf-8")
        (root / "evals" / "fixtures" / "case.json").write_text(
            json.dumps(fixture), encoding="utf-8"
        )
        return root

    def valid_fixture(self):
        return {
            "id": "sample-case",
            "title": "Sample case",
            "entrypoint": "skills/sample-skill/SKILL.md",
            "mode": "Suggest",
            "scenario": "Synthetic decision case",
            "inputs": {},
            "allowed_external_evidence": [],
            "expected": {
                "acceptable_decisions": ["hold"],
                "forbidden_behaviors": ["Do not mutate live ads."],
                "required_observations": ["Evidence is incomplete."],
                "rubric": [
                    {"criterion": "action_gate", "requirement": "Hold safely."}
                ],
            },
        }

    def test_accepts_valid_fixture_with_existing_entrypoint(self):
        root = self.make_repo(self.valid_fixture())
        self.assertEqual([], validate_repository(root))

    def test_rejects_invalid_json(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        fixtures = root / "evals" / "fixtures"
        fixtures.mkdir(parents=True)
        (fixtures / "bad.json").write_text("{not-json", encoding="utf-8")
        errors = validate_repository(root)
        self.assertTrue(any("invalid JSON" in e for e in errors))

    def test_rejects_missing_required_top_level_field(self):
        fixture = self.valid_fixture()
        del fixture["scenario"]
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("missing required field 'scenario'" in e for e in errors))

    def test_rejects_unknown_top_level_field(self):
        fixture = self.valid_fixture()
        fixture["surprise"] = True
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("unexpected top-level field 'surprise'" in e for e in errors))

    def test_rejects_invalid_mode_or_decision_enum(self):
        fixture = self.valid_fixture()
        fixture["mode"] = "Execute"
        fixture["expected"]["acceptable_decisions"] = ["auto_execute"]
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("invalid mode 'Execute'" in e for e in errors))
        self.assertTrue(any("invalid acceptable decision 'auto_execute'" in e for e in errors))

    def test_rejects_missing_entrypoint(self):
        fixture = self.valid_fixture()
        fixture["entrypoint"] = "skills/missing/SKILL.md"
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("entrypoint does not exist" in e for e in errors))

    def test_rejects_fixture_id_filename_mismatch(self):
        fixture = self.valid_fixture()
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("id 'sample-case' must match filename 'case'" in e for e in errors))

    def test_rejects_execute_language_in_closed_world_fixture_contract(self):
        fixture = self.valid_fixture()
        fixture["id"] = "case"
        fixture["expected"]["acceptable_decisions"] = ["action_safe"]
        fixture["expected"]["rubric"] = [
            {"criterion": "execution_boundary", "requirement": "Execute the bid change live."}
        ]
        root = self.make_repo(fixture)
        errors = validate_repository(root)
        self.assertTrue(any("appears to require live mutation" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
