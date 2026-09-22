import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvidenceSnapshotLineagePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_optimization_event_evidence_snapshot_preserves_measurement_identity(self):
        text = self.read("schemas/optimization-event.json")
        self.assertIn('"source_system"', text)
        self.assertIn('"acquisition_channel"', text)
        self.assertIn('"reporting_generation"', text)
        self.assertIn('"date_attribution_semantics"', text)
        self.assertIn('"historical_availability_status"', text)
        self.assertIn('"comparability_status"', text)

    def test_memory_contract_names_measurement_identity_fields_for_replay(self):
        text = self.read("references/optimization-memory.md")
        self.assertIn("reporting_generation", text)
        self.assertIn("date_attribution_semantics", text)
        self.assertIn("historical_availability_status", text)
        self.assertIn("acquisition_channel", text)


class MarketingStreamDatasetCompletenessPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_stream_dataset_presence_does_not_imply_sibling_dataset_completeness(self):
        text = self.read("references/marketing-stream-dataset-coverage.md").lower()
        self.assertIn("dataset subscription", text)
        self.assertIn("traffic", text)
        self.assertIn("conversion", text)
        self.assertIn("sibling dataset", text)
        self.assertIn("not evidence", text)
        self.assertIn("zero", text)

    def test_stream_lineage_tracks_dataset_level_delivery_state(self):
        text = self.read("references/marketing-stream-dataset-coverage.md")
        self.assertIn("stream_dataset", text)
        self.assertIn("subscription_status", text)
        self.assertIn("delivery_status", text)

    def test_campaign_health_progressively_loads_stream_coverage_policy(self):
        text = self.read("skills/campaign-health-monitor/SKILL.md")
        self.assertIn("marketing-stream-dataset-coverage.md", text)


class ActionSizingPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_action_sizing_reference_exists(self):
        self.assertTrue((ROOT / "references/action-sizing.md").is_file())

    def test_decision_boundaries_do_not_define_universal_default_percentages(self):
        text = self.read("references/decision-boundaries.md")
        self.assertIn("action-sizing.md", text)
        self.assertNotIn("±20%", text)
        self.assertNotIn("±25%", text)

    def test_bid_skill_routes_change_magnitude_to_shared_policy(self):
        text = self.read("skills/bid-optimization/SKILL.md")
        self.assertIn("action-sizing.md", text)
        self.assertNotIn("默认单次建议通常限制在当前 bid 的 ±20%", text)
        self.assertNotIn("single_change_pct <= 20%", text)

    def test_budget_skill_routes_change_magnitude_to_shared_policy(self):
        self.assertIn("action-sizing.md", self.read("skills/budget-optimization/SKILL.md"))


class ReportCoveragePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_report_coverage_reference_exists(self):
        self.assertTrue((ROOT / "references/report-coverage.md").is_file())

    def test_search_term_skill_routes_coverage_sensitive_claims_to_shared_policy(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertIn("report-coverage.md", text)
        self.assertIn("row-inclusion", text)

    def test_data_lineage_treats_row_eligibility_as_measurement_identity(self):
        text = self.read("references/data-lineage.md")
        self.assertIn("row-inclusion", text)
        self.assertIn("report-coverage.md", text)


class AttributionVariantPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_data_lineage_distinguishes_standard_and_all_views_conversion_metrics(self):
        text = self.read("references/data-lineage.md")
        self.assertIn("all views", text.lower())
        self.assertIn("attribution_variant", text)
        self.assertIn("shopping-signal", text.lower())

    def test_attribution_variant_gap_does_not_become_business_performance_change(self):
        text = self.read("references/data-lineage.md")
        self.assertIn("same conversion metric family", text.lower())
        self.assertIn("not comparable", text.lower())
        self.assertIn("click-based attribution", text.lower())


class ReportingRetirementPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_unified_reporting_research_records_permanent_legacy_history_deletion(self):
        text = self.read("docs/research/unified-reporting-migration.md").lower()
        self.assertIn("permanently delete", text)
        self.assertIn("historical availability", text)
        self.assertIn("not coerced to zero", text)

    def test_data_lineage_treats_retired_source_history_as_unavailable_not_zero(self):
        text = self.read("references/data-lineage.md").lower()
        self.assertIn("retired", text)
        self.assertIn("historical availability", text)
        self.assertIn("historical metric value is zero", text)
        self.assertIn("do not backfill missing legacy history with zeros", text)


class BenchmarkPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_amazon_benchmark_policy_preserves_peer_group_semantics(self):
        text = self.read("references/benchmark-policy.md")
        self.assertIn("peer group", text.lower())
        self.assertIn("minimum of 5 brands", text.lower())
        self.assertIn("25th", text)
        self.assertIn("75th", text)

    def test_missing_amazon_benchmark_is_not_interpreted_as_zero_or_failure(self):
        text = self.read("references/benchmark-policy.md")
        self.assertIn("missing benchmark", text.lower())
        self.assertIn("not evidence", text.lower())
        self.assertIn("zero", text.lower())

    def test_campaign_health_routes_peer_comparisons_to_shared_benchmark_policy(self):
        text = self.read("skills/campaign-health-monitor/SKILL.md")
        self.assertIn("benchmark-policy.md", text)
        self.assertIn("peer", text.lower())
        self.assertIn("not", text.lower())


class SearchTermImpressionSharePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_impression_share_reference_exists(self):
        self.assertTrue((ROOT / "references/search-term-impression-share.md").is_file())

    def test_search_term_skill_routes_share_of_voice_analysis_to_shared_reference(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertIn("search-term-impression-share.md", text)
        self.assertIn("impression share", text.lower())

    def test_growth_skill_routes_query_headroom_to_impression_share_policy(self):
        self.assertIn("search-term-impression-share.md", self.read("skills/growth-opportunity-finder/SKILL.md"))

    def test_sis_policy_records_acquisition_channel_and_does_not_treat_missing_connector_field_as_zero(self):
        text = self.read("references/search-term-impression-share.md")
        self.assertIn("acquisition_channel", text)
        self.assertIn("missing from the active connector", text)
        self.assertIn("not evidence that SIS is zero", text)

    def test_data_lineage_distinguishes_source_system_from_acquisition_channel(self):
        text = self.read("references/data-lineage.md")
        self.assertIn("acquisition_channel", text)
        self.assertIn("available in the product", text)
        self.assertIn("available through the active connector", text)


class SearchTermOriginPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_search_term_skill_does_not_define_every_row_as_literal_user_query(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertNotIn("Search Term 是真实用户查询", text)
        self.assertIn("inferred", text.lower())
        self.assertIn("non-search", text.lower())

    def test_search_term_skill_guards_harvest_and_negative_actions_when_origin_is_uncertain(self):
        text = self.read("skills/search-term-analysis/SKILL.md")
        self.assertIn("term_origin", text)
        self.assertIn("literal shopper query", text.lower())
        self.assertIn("manual review", text.lower())

    def test_negative_targeting_requires_origin_check_for_search_term_rows(self):
        text = self.read("skills/negative-targeting/SKILL.md")
        self.assertIn("term_origin", text)
        self.assertIn("inferred", text.lower())


class PlatformManagedDeliverySurfacePolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_drop_skill_checks_platform_managed_delivery_surface_changes(self):
        text = self.read("skills/performance-drop-diagnosis/SKILL.md")
        self.assertIn("platform-managed", text.lower())
        self.assertIn("delivery surface", text.lower())

    def test_causal_reference_treats_auto_enrollment_as_competing_cause(self):
        text = self.read("skills/performance-drop-diagnosis/references/causal-drop-diagnosis.md")
        self.assertIn("auto-enrollment", text.lower())
        self.assertIn("traffic-mix", text.lower())
        self.assertIn("no manual control change", text.lower())
        self.assertIn("does not prove", text.lower())


class OptimizationSignalSemanticsPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_realized_identity_distinguishes_optimization_signal_from_hard_targeting_constraint(self):
        text = self.read("references/realized-ad-identity.md").lower()
        self.assertIn("optimization signal", text)
        self.assertIn("hard targeting constraint", text)
        self.assertIn("audience signal", text)

    def test_experiment_planner_routes_ai_signal_boundary_risk_to_realized_identity_policy(self):
        text = self.read("skills/experiment-planner/SKILL.md")
        self.assertIn("realized-ad-identity.md", text)
        self.assertIn("audience signal", text.lower())

    def test_interference_policy_does_not_treat_signal_membership_as_holdout_boundary(self):
        text = self.read("skills/experiment-planner/references/interference-and-leakage.md").lower()
        self.assertIn("audience signal", text)
        self.assertIn("not a holdout boundary", text)
        self.assertIn("actual delivery", text)

    def test_experiment_schema_can_encode_audience_control_semantics(self):
        text = self.read("schemas/experiment-plan.json")
        self.assertIn('"audience_control_semantics"', text)
        self.assertIn('"optimization_signal"', text)
        self.assertIn('"hard_exclude"', text)
        self.assertIn('"unknown"', text)


class RealizedAdIdentityPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_shared_realized_ad_identity_reference_exists(self):
        self.assertTrue((ROOT / "references/realized-ad-identity.md").is_file())

    def test_realized_ad_policy_separates_configured_controls_from_realized_product_mix(self):
        text = self.read("references/realized-ad-identity.md")
        self.assertIn("configured controls", text.lower())
        self.assertIn("realized product mix", text.lower())
        self.assertIn("unknown", text.lower())
        self.assertIn("not evidence", text.lower())

    def test_drop_skill_routes_platform_managed_realization_to_shared_policy(self):
        self.assertIn("realized-ad-identity.md", self.read("skills/performance-drop-diagnosis/SKILL.md"))

    def test_post_change_review_checks_realized_ad_identity_before_single_action_attribution(self):
        text = self.read("skills/post-change-review/SKILL.md")
        self.assertIn("realized-ad-identity.md", text)
        self.assertIn("realized", text.lower())


class RealizedAdMemoryPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_optimization_event_schema_has_canonical_realization_snapshot(self):
        text = self.read("schemas/optimization-event.json")
        self.assertIn('"realization_snapshot"', text)
        self.assertIn('"realization_mode"', text)
        self.assertIn('"comparability_status"', text)

    def test_entity_history_schema_exposes_latest_realization_state(self):
        text = self.read("schemas/entity-history.json")
        self.assertIn('"latest_realization"', text)
        self.assertIn('"comparability_status"', text)

    def test_memory_contract_requires_realization_context_when_it_affects_attribution(self):
        text = self.read("references/optimization-memory.md")
        self.assertIn("realization_snapshot", text)
        self.assertIn("realized-ad-identity.md", text)
        self.assertIn("control readback", text.lower())
        self.assertIn("realization", text.lower())


class SkillEffectivenessPolicyTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_skill_effectiveness_guide_exists(self):
        self.assertTrue((ROOT / "evals/SKILL-EFFECTIVENESS.md").is_file())

    def test_eval_index_distinguishes_capability_replay_from_effectiveness_measurement(self):
        text = self.read("evals/README.md")
        self.assertIn("with-skill", text)
        self.assertIn("without-skill", text)
        self.assertIn("negative control", text)
        self.assertIn("repeated", text)

    def test_effectiveness_guide_covers_discovery_and_forced_invocation(self):
        text = self.read("evals/SKILL-EFFECTIVENESS.md")
        self.assertIn("Discovery", text)
        self.assertIn("Forced invocation", text)
        self.assertIn("without-skill", text)
        self.assertIn("pass@k", text)


if __name__ == "__main__":
    unittest.main()
