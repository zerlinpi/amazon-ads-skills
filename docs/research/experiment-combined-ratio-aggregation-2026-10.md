# Ready combined ratio aggregation — 2026-10-26

## Baseline and nonduplicate gap

Fresh main HEAD: `fd2048fa96953efb46b9743fcd1257a3d2933e98` (v1.81.0), no open PR at initial read. Prior experiment changes covered conversion **attribution identity**, but `scripts/validate_experiment_plan.py` only required a non-unknown `aggregation_semantics` for `Ready` combined readouts. A named ROAS, ACOS, TACOS, CTR, CVR or CPC could declare `additive` or `non_additive_deduplicated` and still pass, although the existing `evaluate_metric_aggregation_gate.py` rejects direct sums of ratios.

Two older aggregation branches (`automation/metric-aggregation-gate-20260919`, `automation/experiment-aggregation-semantics-20260919`) were both fully behind main with no ahead commits. Reuse their existing taxonomy; do not resurrect duplicate branches.

## Deterministic RED → GREEN

- Initial RED commit `dc98d4bf06651d771850e44a8c7b2aa272e4f785` exposed 8 intended ratio failures plus one erroneous compatibility test fixture for additive Sales (9 total failures). This was a test-fixture mistake, not a production defect.
- Corrected fixture commit `40227502f362a635d3e54a4d33332010ec2c8ac6`, [RED Actions #40317709806](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40317709806): 1682 tests, **8 FAIL** for ratio misclassification, remaining 6 new compatibility cases passed.
- Minimal production fix `d714b9805a020ea21738e3e32e184b90c0d093e2`, [GREEN Actions #40317743385](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40317743385): **1682 PASS**, Skill validator PASS, Eval validator PASS.
- Added 14 synthetic tests in `tests/test_experiment_combined_ratio_aggregation.py`. They cover both primary and guardrail ratios, additive Sales/Impressions, correctly declared ratio metrics, exploratory status and non-combined legacy plans.

## Official source evidence and limits

- [Amazon Ads ACOS guide](https://advertising.amazon.com/library/guides/acos-advertising-cost-of-sales): ACOS is spend divided by ad revenue; ROAS is ad revenue divided by spend. Neither is directly additive across campaigns.
- [Amazon Ads metric definitions](https://advertising.amazon.com/help/G3HEFZYWZF84NPS9): CTR is clicks divided by impressions; CPC is spend divided by clicks.
- TACOS is treated as a distinct total-retail-sales-denominator ratio. It must not inherit the ad-attributed ACOS identity.
- The repository's narrow canonical-name guard is **not** an Amazon API enum, does not derive missing denominators, verify complete grain, or authenticate external connector data. Unknown/partial/unavailable values are never numeric zero.

## Open source review and copyright boundary

Previously reviewed candidates refreshed: [OpenEvals](https://github.com/langchain-ai/openevals) (~1.2k stars, MIT; sampled open PR #291/#283), [OpenLineage](https://github.com/OpenLineage/OpenLineage) (~2.7k stars, Apache-2.0; sampled PR #5107/#5105), [KuudoAI Amazon Ads MCP](https://github.com/KuudoAI/amazon_ads_mcp) (74 stars, MIT; sampled PR #104/#101). These are non-fork public upstreams in earlier research, with varying activity and CI. Stars are approximate public observations; the sampled metadata is not a complete code, CI, security, issue, or dependency-license audit. Reject all imports: local stdlib validation suffices; no external framework proves component-level completeness. No external source code, prompt, schema, workflow, or template copied. No license-uncertain content reused.

## Scope, safety, next gap

Keep 15 Skills and Read-only/Suggest/Shadow defaults. This change does not execute ads, retry writes, reconcile transactions, claim causal uplift or authorize any external Executor. Next gaps: authenticated external attribution and source evidence, full-window bid/budget rule execution continuity, and reliable component-level ratio recomputation under cross-campaign overlap, currency and grain constraints.
