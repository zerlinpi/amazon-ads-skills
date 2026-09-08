---
name: amazon-ads-optimizer
description: Orchestrate Amazon Ads audit, monitoring, diagnosis, search-term, keyword, bid, budget, placement, negative-targeting, profitability and anomaly skills into one guarded action plan. Use for whole-account optimization, multi-domain analysis, or when the user does not know which Amazon Ads skill to choose.
---

# Amazon Ads Optimizer

Use this as the routing layer. Keep detailed business logic in the selected child Skill and its references instead of loading the whole repository.

## Default mode

`Suggest`.

Never claim a live Amazon Ads change succeeded unless an external connector/executor actually performed it and returned success.

## Route by intent

| Intent | Skill |
|---|---|
| Whole-account audit / account takeover | `amazon-ads-audit` |
| Routine campaign health / alerts | `campaign-health-monitor` |
| Sudden sales, orders, ROAS, ACOS or traffic decline; “what dropped and why?” | `performance-drop-diagnosis` |
| Search-term winners / harvesting / query quality | `search-term-analysis` |
| Keyword/target structure and lifecycle | `keyword-optimization` |
| Bid/CPC adjustment | `bid-optimization` |
| Budget, pacing, reallocation | `budget-optimization` |
| Top of Search / Product Pages / Rest of Search | `placement-optimization` |
| Negative keywords / negative product targeting | `negative-targeting` |
| Break-even ACOS / contribution profit / TACOS | `profitability-analysis` |
| Unexplained metric anomaly / monitoring signal | `anomaly-detection` |

## Routing rules

- For a sustained decline with a business impact, prefer `performance-drop-diagnosis` over a generic anomaly review.
- For an alert without a confirmed sustained decline, start with `anomaly-detection` or `campaign-health-monitor`.
- For “lower ACOS”, first diagnose whether the driver is traffic quality, CPC, CVR, placement, budget allocation, retail readiness, or economics. Do not route directly to bid reduction by default.
- For growth, identify proven winners and profitability/stock constraints before increasing bids or budgets.
- Load only the minimum child Skills needed for the question.

## Shared checks

Before high-confidence recommendations confirm when relevant:

- marketplace, currency and timezone;
- exact date windows and attribution maturity;
- ad type and entity scope;
- business objective / target economics;
- promotion, price, inventory, Buy Box / Featured Offer and listing state;
- data freshness and sample sufficiency.

Use `../../references/benchmark-policy.md` when external benchmarks affect a decision.
Use `../../references/decision-boundaries.md` for action permissions.

## Conflict resolution

If multiple Skills propose incompatible actions on the same entity:

1. prefer data-quality and retail-readiness fixes before bid/budget tuning;
2. respect explicit business/profitability constraints;
3. prefer protective and reversible actions over aggressive growth actions;
4. prefer higher-confidence, better-scoped evidence;
5. if uncertainty remains, output `manual_review` / hold instead of forcing a mutation.

Examples of invalid unresolved conflicts:

- increase bid + decrease bid;
- increase budget + decrease budget;
- harvest a search term + negate the same term;
- scale a campaign while profitability analysis says it is structurally loss-making without an explicit strategic exception.

## Action priority

Default ordering:

1. **P0** data, serving, inventory, Buy Box / Featured Offer, listing or attribution failures;
2. **P1** material waste or dangerous control errors;
3. **P2** efficiency repairs: search terms, bids, placements, budget reallocation;
4. **P3** proven growth opportunities;
5. **P4** larger structural redesigns and experiments.

## Output

Return:

1. Executive summary.
2. Data confidence and important missing inputs.
3. Routed diagnoses with supporting evidence.
4. Deduplicated prioritized action plan.
5. Conflicts resolved or unresolved.
6. Hold/observe list.
7. Validation window and next measurement.

Every actionable proposal should include entity, reason, evidence, confidence, mode, guardrails, validation window and rollback condition. Default to `Suggest`; use `Shadow` for simulation/backtesting when useful.
