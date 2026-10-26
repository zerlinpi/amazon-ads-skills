# Standalone direct-sum ratio KPI contradiction — 2026-10-26

## Baseline and independently verified gap

Initial main HEAD `a41ab6ae6600ed14d2adbb69636ff96f66bdb1f1`, version 1.83.0, main CI #40327932718 SUCCESS, no open PR. Historical aggregation branches `automation/aggregation-semantics-projection-20260919`, `automation/metric-aggregation-gate-20260919`, `automation/experiment-aggregation-semantics-20260919` each had zero commits ahead of main. All 15 Skills retained.

The Ready experiment validator already rejects canonical ROAS/ACOS/TACOS/CVR/CTR/CPC names with `additive` aggregation semantics, but the separate `scripts/evaluate_metric_aggregation_gate.py` would return `Allowed` for those same explicitly named ratio KPIs whenever the caller declared `metric_semantics.aggregation_semantics=additive` and `source_relation=disjoint`. This is an independent cross-entrypoint safety inconsistency, not a duplicate change to the experiment validator.

## RED → GREEN

- RED test commit `df175e0065e9c4fa7999860aca51bd9c87835e44`: [Actions #40339525064](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40339525064), 1711 tests, 8 FAIL for contradictory additive ratio names. Seven other new tests preserved additive/unknown/overlap/legacy behavior.
- Minimal production fix `f656e102e21e5217ed7ee0969248a733ace7f497`: [GREEN Actions #40339653449](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40339653449) SUCCESS. Optional `metric_name` enables a bounded canonical ratio contradiction check before disjoint-row approval. No metric-name inference of source provenance or data values. No schema migration, new Skill, dependency, or Ads write.

## Official platform facts and inference boundary

- [Amazon Ads ACOS guide](https://advertising.amazon.com/library/guides/acos-advertising-cost-of-sales): ACOS = ad spend / attributed ad revenue, ROAS = attributed ad revenue / ad spend. Adding campaign-level ratios is not a combined ratio calculation.
- [Amazon Ads ROAS guide](https://advertising.amazon.com/library/guides/return-on-ad-spend-roas): campaign ROAS measures revenue per unit of ad spend.
- These public definitions justify rejecting a direct-sum contradiction; they do not define the repository field `metric_name`, authenticate external Ads/retail responses, guarantee denominator coverage, solve cross-profile currency/attribution/grain comparability, or prove causal lift.

## Open-source review and copyright

Rechecked public GitHub metadata on 2026-10-26: [langchain-ai/openevals](https://github.com/langchain-ai/openevals) (1,232 stars, MIT, non-fork, pushed 2026-10-22), [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) (2,724 stars, Apache-2.0, non-fork, pushed 2026-10-25), [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) (74 stars, MIT, non-fork, pushed 2026-10-14). SOURCES already reviewed these candidates. No full new security/issue/dependency/license audit; no third-party code, prompts, schemas, workflows, or templates copied. Reject framework imports: this narrow deterministic safety contradiction is solved with Python stdlib. Public practitioner anecdotes remain hypotheses, not Amazon specifications.

## Next genuine gaps

1. Verify independently sourced ratio components, attribution family/version, date, grain, currency, denominator nonzero, completeness, and overlapping rows before safe recomputation. This standalone gate still does not aggregate.
2. Full-window schedule/event/budget-rule execution history, rather than only endpoint snapshots.
3. Cross-campaign control interference and marginal contribution-profit causality; do not turn missing/unsupported/partial/unknown into zero.

Default Suggest/Shadow/Read-only. Actual Ads writes/retries/idempotency/reconciliation remain with the authorized external Executor.
