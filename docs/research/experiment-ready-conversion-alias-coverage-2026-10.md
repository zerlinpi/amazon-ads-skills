# Ready experiment conversion alias coverage — 2026-10-26

## Fresh evidence and ranked gaps

Main HEAD `491cfb65c7a54a405cf1dbd2a07f3fdf7bc69f43`; main Actions #40302312600 SUCCESS; zero open PR. Prior experiment branches sampled were 0 ahead. Inspected repository tree, README, AGENTS, CLAUDE, SOURCES, relevant research, schemas, validators/tests, runtime manifests and all 15 canonical Skill files. 55 eval fixtures; no `knowledge/` folder. Directory inventory is not a line-by-line audit of every file.

- **P0 confirmed:** `_is_conversion_metric` recognized Purchases/Sales/ROAS but not ACOS, CVR, Attributed Orders/Units or Units Sold when `metric_family` was falsely declared `traffic`. The `Ready` primary or guardrail then bypassed the attribution family/semantic version gate.
- **P1 external evidence:** a concrete attribution label is not a verified original Amazon Ads response or permission to query/modify an account.
- **P2 causal continuity:** full-window rules, traffic overlap, retail state and incremental contribution-profit still require independent evidence.

## RED → GREEN

New synthetic test file: `tests/test_experiment_ready_conversion_alias_coverage.py` (15 tests). RED `81fb26b7dceddf1afbc42f91c8effd5e6a02bbd8`, [Actions #40310486694](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40310486694): 1668 tests, 10 FAIL. Positive compatibility tests passed. Minimal fix `c7ba5a903a5a74cf1f06b4da4d147d889224135f`, [Actions #40310592404](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40310592404): 1668/1668 PASS; 15 Skills, 55 evals PASS.

The patch extends the existing Ready conversion display-name guard with bounded ACOS/CVR tokens and specific attributed-order/unit and units-sold phrases. `TACOS` is not matched by `ACOS` because total retail sales are not equivalent to ad-attributed sales. Valid conversion identity, genuine nonconversion metrics and Shadow plans remain compatible. No schema, dependency, Skill count or live Ads write changed.

## Source, license and practice review

Official [Amazon ACOS guide](https://advertising.amazon.com/library/guides/acos-advertising-cost-of-sales) establishes the derived attributed-sales denominator; [Amazon Attribution](https://advertising.amazon.com/en-us/solutions/products/amazon-attribution/) lists units sold and purchase-rate conversions; [DSP conversion metrics](https://advertising.amazon.com/resources/whats-new/amazon-dsp-updated-names-for-conversion-metrics) describes CVR as conversion rate; [2026 Store view-attribution change](https://advertising.amazon.com/resources/whats-new/view-attribution-updates-for-amazon-store-ads/) is inventory-specific, not a universal conversion definition.

GitHub samples: KuudoAI/amazon_ads_mcp (74 stars/MIT), langchain-ai/openevals (1231/MIT), OpenLineage/OpenLineage (2723/Apache-2.0), agentskills/agentskills (26639/Apache-2.0), modelcontextprotocol/servers (91575/NOASSERTION). Checked non-fork status, activity, license and sampled Actions/PRs on three candidates; no full source/security/dependency audit. Reject code import: local deterministic stdlib validation is narrower and no framework authenticates caller-supplied attribution. No third-party code, prompts, schemas, templates or workflows copied. Unlicensed/restricted content is principles-only.

Reddit PPC anecdotes about ACOS/CPC/orders are competing-cause hypotheses, not platform specifications, sample sufficiency rules or causal proof. Maintain missing/unknown/partial/unsupported as evidence states (never zero), source/metric/date/grain/identity/capability lineage, Observation/Hypothesis/Cause/Action/Outcome, marginal economics, confounders, control interaction and Read-only/Suggest/Shadow; any real Ads write/retry/idempotency/reconciliation remains with an explicitly authorized external Executor.
