---
name: amazon-ads-audit
display_name: 亚马逊广告账户体检
display_name_en: Amazon Ads Audit
description: 对 Amazon Ads 账户、广告活动与投放结构进行系统体检，识别数据质量、浪费、预算、转化、结构和增长机会。适用于广告体检、账户诊断、周/月复盘、接手新账户等场景。
description_zh: 系统审计亚马逊广告账户，输出问题、证据、优先级和优化建议。
description_en: Audit Amazon Ads accounts for data quality, structure, efficiency, waste, budget constraints, conversion issues and growth opportunities.
version: 0.1.0
author: zerlinpi
---

# Amazon Ads Audit

Use for account audits, account handovers, broad health reviews, or when the user wants the most important paid-media risks and opportunities across several domains.

Default mode: `Suggest`. Never mutate a live account.

## Progressive loading

Read this file first, then load only what is needed:

- full audit workflow and aggregation safety: `references/account-audit-framework.md`;
- metric definitions: `../../references/amazon-ads-metrics.md`;
- cross-source/semantic/backfill comparability: `../../references/data-lineage.md`;
- decision/execution boundaries: `../../references/decision-boundaries.md`.

Do not load specialist Skills unless a material finding needs their decision logic.

## Required context

Collect or mark missing:

- marketplace and profile/account scope;
- currency, timezone, exact date/comparison windows and attribution maturity;
- source freshness/completeness and truncation/coverage warnings;
- profile/account and campaign base metrics;
- keyword/target, search term and placement views when available;
- budget/bid/state/structure context;
- stated objective or target economics;
- retail/product context when conversion or scaling is material.

## Workflow

1. **Reliability gate** — validate scope, dates, attribution, freshness and source comparability.
2. **Canonical totals** — choose one additive account grain and reconcile it to a complete campaign view when possible.
3. **Metric integrity** — sum compatible base metrics, then recompute ratios; never add overlapping entity grains or simple-average ratio KPIs.
4. **Account result** — establish spend, attributed sales/orders, efficiency and business-objective fit.
5. **Driver analysis** — rank material contributors by absolute impact, then decompose through campaign/product/target/query/placement views.
6. **Structure and routing** — identify conflicting intents, Mixed-ASIN risk, unclear query routing, duplication, fragmentation or budget interdependence.
7. **Waste/protection** — identify evidence-backed waste without turning zero orders/high ACOS into automatic negatives or pauses.
8. **Growth/headroom** — identify qualified opportunities only after economics, retail readiness and marginal headroom checks.
9. **Prioritize** — blockers/risks first, then efficiency, growth and longer-term structure.
10. Route specialized findings to matching Skills instead of duplicating their rules.

## Output contract

Return:

1. scope and data confidence;
2. executive verdict;
3. canonical account scorecard;
4. largest driver/contribution findings;
5. structure/routing and retail/economic findings;
6. prioritized issues/opportunities with evidence and confidence;
7. specialist action proposals when justified;
8. Hold / Need more data;
9. next review/measurement.

## Safety boundaries

- Missing rows are not automatically zero.
- Profile/campaign/keyword/search-term/placement totals are not additive when they describe overlapping traffic.
- Account ratios must be recomputed from compatible aggregate components rather than averaged across rows.
- TACOS requires compatible total retail sales; profit claims require sufficient cost/economic inputs.
- Do not make high-confidence optimization decisions from unresolved marketplace/currency/date/attribution/source mismatches.
- Conversion-led issues must consider stock, Featured Offer / Buy Box, price, promotions, listing and variation-family changes.
- Default to `Hold`, `Directional` or specialist review when evidence is insufficient.
- Any real mutation requires explicit authorization and an external Connector / Executor.
