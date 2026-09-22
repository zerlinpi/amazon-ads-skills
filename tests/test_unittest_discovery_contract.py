import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"


class UnittestDiscoveryContractTests(unittest.TestCase):
    def test_no_top_level_test_functions_are_silently_ignored_by_unittest_discover(self):
        offenders = []
        for path in sorted(TESTS_DIR.glob("test_*.py")):
            if path.name == Path(__file__).name:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                    offenders.append(f"{path.relative_to(ROOT)}::{node.name}")

        self.assertEqual(
            offenders,
            [],
            "python -m unittest discover does not collect top-level pytest-style test functions; "
            "convert these tests to unittest.TestCase methods or change the CI runner explicitly: "
            + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
