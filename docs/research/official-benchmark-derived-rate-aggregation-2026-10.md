# Official Amazon Ads benchmark derived-rate aggregation safety — 2026-10-27

## Verified baseline and actual gap

Fresh main HEAD: `3bc3a09329550feeba263060a8dfd66ef05bbc4f` (v1.89.0); latest main push Actions #40380600070 SUCCESS, no open PR at start. Existing aggregation branch `automation/metric-aggregation-gate-20260919` had 0 commits ahead and 1179 behind; no duplicate branch work. Repository tree, 15 canonical Skills, supporting references, scripts, tests, eval fixtures, schemas, research and runtime manifests were inventoried. Related validator/test/source documents were read; inventory does not imply exhaustive deep review of every file.

Amazon Ads official [Benchmark reporting](https://advertising.amazon.com/help/GXRC3X4EEPXH8NVE), updated October 6, 2026, defines purchase rate, add-to-cart rate, detail-page-view rate, branded-search rate, cost per purchase, cost per detail-page view and percent of purchases new to brand as numerator/denominator measures. Its denominators and attribution/variant definitions differ by metric. [Amazon Attribution](https://advertising.amazon.com/en-us/solutions/products/amazon-attribution/) separately lists purchase and add-to-cart rates. These are *not additive*. Both `scripts/evaluate_metric_aggregation_gate.py` and `scripts/validate_experiment_plan.py` previously only recognized bounded acronym ratios (ROAS/ACOS/CTR/CVR/CPA/CPM/etc.), so explicit additive claims for official benchmark-derived labels could pass.

## RED → GREEN and implementation

- RED commit `5aa792219be0fad06f9dc6e9b6226abf7c4682ad`; [Actions #40390201710](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40390201710): **1816 tests, 14 FAIL** (new synthetic cases), demonstrating the old false Allowed/Ready results. No live account data.
- Minimal two-entrypoint fix: bounded case-insensitive detection of explicit purchase/add-to-cart/detail-page-view/branded-search **rate** labels, cost-per-purchase/detail-page-view labels and percent-of-purchases-new-to-brand; do not infer a generic platform schema or trust an arbitrary metric name as source authentication.
- GREEN [Actions #40390377095](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40390377095): **1816/1816 PASS**, Skill and Eval validators PASS. An intermediate CI run failed because of raw-regex escape syntax; fixed before release.
- Additive Purchases/Impressions, valid ratio-derived Ready plans, non-combined Ready, Shadow Only, omitted standalone metric name and unrelated `Rate limit adjustment count` remain compatible. No extra Skill, schema, third-party runtime dependency, Amazon Ads API write or executor authority.

## Source review, reuse rights and limitations

- Primary official definitions: [Amazon Ads benchmark reporting](https://advertising.amazon.com/help/GXRC3X4EEPXH8NVE) (updated 2026-10-06), [Amazon Attribution](https://advertising.amazon.com/en-us/solutions/products/amazon-attribution/), [Unified reporting GA](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) (2026-06-08), and [View attribution changes](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/) (2026-01-01). These establish metric definitions and potential attribution/coverage differences, **not** this repository's internal validation policy or raw-source authenticity.
- Rechecked GitHub public metadata 2026-10-27: `dbt-labs/metricflow` 1848 stars, Apache-2.0, nonfork, pushed 2026-10-13, sampled latest Actions action_required; `OpenLineage/OpenLineage` 2725 stars, Apache-2.0, nonfork, pushed 2026-10-25, sampled Actions success; `langchain-ai/openevals` 1232 stars, MIT, nonfork, pushed 2026-10-22, sampled Actions success; `KuudoAI/amazon_ads_mcp` 74 stars, MIT, nonfork, pushed 2026-10-14, sampled Actions success; `modelcontextprotocol/servers` 91592 stars, GitHub SPDX NOASSERTION, nonfork, pushed 2026-10-25. Open issue counts are mixed issue/PR counters, not an independent issue audit. Stars, metadata, partial CI/PR checks are not comprehensive code, dependency, security or license audits.
- **Reject imports**: a small deterministic local metric contract needs no external semantic engine, eval framework or MCP. NOASSERTION is not blanket permission. No third-party code, prompts, schemas, workflows, templates or licensed prose copied. Public Reddit/advertiser case studies are hypothesis sources, not platform rules or causal evidence.

## Next verified gaps

1. Source-authenticated numerator/denominator identity, compatible metric/event/attribution family, currency, date, grain, record overlap and completeness for recomputation; the current change only blocks obvious metadata contradictions.
2. Full-window schedule/event/budget rule activation and control-interaction evidence, not endpoint snapshots.
3. Marginal contribution profit and causal confounder checks across bid/budget/placement/retail interactions.

Preserve missing/unsupported/partial/unknown ≠ zero; Observation/Hypothesis/Cause/Action/Outcome; Read-only/Suggest/Shadow default and external authorized Executor for all writes/retries/idempotency/reconciliation.
