"""RED-first: Ready combined metric identity rejects whitespace-obfuscated N/A labels.

Synthetic plans only. No Amazon Ads access or live writes.
"""
import unittest

from scripts.validate_experiment_plan import validate_experiment_plan
from test_ready_combined_unresolved_metric_identity import ready_combined


class ReadyCombinedNotApplicableWhitespaceTests(unittest.TestCase):
    def assert_unresolved(self, name, *, guardrail=False, aggregation="additive"):
        errors = validate_experiment_plan(ready_combined(
            name, guardrail=guardrail, aggregation=aggregation
        ))
        self.assertTrue(
            any("metric" in error and "identity" in error for error in errors),
            f"{name!r}, guardrail={guardrail}: {errors}",
        )

    def test_double_space_primary(self):
        self.assert_unresolved("Not  Applicable")

    def test_tab_primary(self):
        self.assert_unresolved("Not\tApplicable")

    def test_newline_primary(self):
        self.assert_unresolved("Not\nApplicable")

    def test_nonbreaking_space_primary(self):
        self.assert_unresolved("Not\u00a0Applicable")

    def test_double_space_guardrail(self):
        self.assert_unresolved("Not  Applicable", guardrail=True)

    def test_tab_guardrail_ratio(self):
        self.assert_unresolved(
            "not\tapplicable", guardrail=True, aggregation="ratio_or_derived"
        )

    def test_multiple_spaces_guardrail(self):
        self.assert_unresolved("NOT   APPLICABLE", guardrail=True)

    def test_single_space_placeholder_stays_blocked(self):
        self.assert_unresolved("Not Applicable")

    def test_hyphen_placeholder_stays_blocked(self):
        self.assert_unresolved("Not-Applicable", guardrail=True)

    def test_concrete_name_containing_phrase_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(
            ready_combined("Not Applicable customer segment clicks")
        ))

    def test_concrete_impressions_remains_ready(self):
        self.assertEqual([], validate_experiment_plan(ready_combined("Impressions")))

    def test_noncombined_ready_keeps_legacy_contract(self):
        plan = ready_combined("Not  Applicable")
        plan["comparison"]["requires_combined_readout"] = False
        self.assertEqual([], validate_experiment_plan(plan))

    def test_shadow_combined_preserves_unresolved_label(self):
        self.assertEqual([], validate_experiment_plan(
            ready_combined("Not\tApplicable", status="Shadow Only")
        ))


if __name__ == "__main__":
    unittest.main()
