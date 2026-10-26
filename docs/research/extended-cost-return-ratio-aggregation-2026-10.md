# Cost/return ratio KPI aggregation boundary — 2026-10-26

## Fresh baseline and independently reproduced gap

main HEAD `adbde886739c06f492d2b72b57fbfdfd26646598`, v1.84.0, main push CI #40340031934 SUCCESS, no open PR. All 15 canonical Skills were read and existing research, SOURCES, schemas, references, evals, tests, scripts and runtime manifests were inventoried. Historical aggregation branches had no commits ahead of main.

Both `scripts/evaluate_metric_aggregation_gate.py` and `scripts/validate_experiment_plan.py` already blocked additive ROAS/ACOS/TACOS/CVR/CTR/CPC, but accepted CPA, CPM, vCPM and ROI as additive when explicitly named. CPA is a cost per qualifying event, CPM a cost per thousand impressions, vCPM a cost per thousand *viewable* impressions, and ROI a return divided by cost. None can be summed as a ratio across rows, even when rows are disjoint. This is a concrete nonduplicate hole in the bounded name contradiction guard, not a claim that metric names authenticate source data.

## RED → GREEN

- RED synthetic test commit `28513208d2081202873f64c7fec3ecfd34d096b2`, [Actions #40343010591](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40343010591): 1730 tests, 10 FAIL; 9 compatibility tests passed.
- Minimal fixes: `78ce6aa01cfae11516d5b139a40595f1e470b6b0` (standalone), `a0c638891937fa784e1a37a82de90bf3ededd752` (Ready combined); [GREEN Actions #40343137676](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40343137676): 1730 PASS, Skill and Eval validators PASS.
- The two read-only gates now share the same expanded bounded KPI token set. Real additive Spend/Impressions, exploratory plans, non-combined Ready plans, legacy unnamed standalone callers and unknown aggregation semantics retain compatibility. No additional Skill, schema, dependency, API write, retry, idempotency or Executor changes.

## Source and license boundaries

- [Amazon Ads fundamentals](https://advertising.amazon.com/en-us/library/guides/basics-of-success-understanding-amazon-advertising): CPM and ROI definitions.
- [Amazon Ads measurement guide](https://advertising.amazon.com/library/guides/measure-improve-campaigns): cost of acquisition and conversion KPIs.
- [Amazon Sponsored Brands](https://advertising.amazon.com/library/guides/sponsored-brands-what-to-know): vCPM pricing.
- Public project metadata rechecked: dbt-labs/metricflow (Apache-2.0), OpenLineage/OpenLineage (Apache-2.0), langchain-ai/openevals (MIT), KuudoAI/amazon_ads_mcp (MIT), agentskills/agentskills (Apache-2.0), modelcontextprotocol/servers (GitHub NOASSERTION). Existing SOURCES already discussed these families. No third-party code, prompts, schemas, workflow, templates or licensed prose reused. Rejected imports because the defect is a small deterministic metadata invariant; full security/transitive-license audit was not performed.
- Practitioner discussions are not official Amazon definitions, denominator contracts, experiments, or evidence of causality.

## Residual gaps

1. External source authenticity and complete compatible numerator/denominator evidence: currency, timezone, date, grain, event definition, attribution family/version, nonzero denominator, deduplication and row coverage.
2. Full-window schedule/event/budget rule activation evidence rather than two endpoint snapshots.
3. Cross-campaign bid/budget/placement/retail interference and incremental contribution-profit validation.

Default Read-only/Suggest/Shadow; Amazon Ads execution remains with a separately authorized external Executor.
