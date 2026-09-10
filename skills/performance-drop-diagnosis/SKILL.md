---
name: performance-drop-diagnosis
description: Diagnose sudden or sustained Amazon Ads performance declines by tracing the break point from account to ASIN, campaign, target, search term, placement, retail readiness, measurement lineage, and recent control changes. Use when sales, orders, ROAS, ACOS, TACOS, traffic, conversion, rank, or campaign performance dropped and the user wants a causal diagnosis rather than generic optimization advice.
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  description_zh: "诊断亚马逊广告销量、订单、ROAS、ACOS、TACOS、流量、转化、排名或 Campaign 表现突然或持续下降的根因。"
  description_en: "Causal diagnosis for Amazon Ads performance declines with mixed-ASIN, data-lineage, and actionability gates."
---

# Performance Drop Diagnosis

Find **what changed, when it changed, where the loss came from, and which causes are supported by evidence**. ACOS/ROAS movement is an outcome, not a root cause.

Default mode: `Read-only` or `Suggest`. Never mutate a live account.

## Progressive loading

Read this file first. Load only what is needed:

- Detailed causal workflow and Mixed-ASIN safety: `references/causal-drop-diagnosis.md`
- Cross-source, freshness, or metric-version reconciliation: `../../references/data-lineage.md`
- Metric definitions: `../../references/amazon-ads-metrics.md`
- Shared decision boundaries: `../../references/decision-boundaries.md`
- General optimization logic: `../../references/optimization-framework.md`

Do not load `data-lineage.md` for a single stable measurement path whose source, completeness and metric definitions are already known to be comparable.

## Required context

Collect or explicitly mark missing:

- marketplace, profile/account scope, currency, timezone, date window, attribution maturity;
- primary KPI and business objective;
- daily or weekly account/campaign performance;
- source/metric metadata when windows use different reports, refresh paths, semantic versions, or unknown measurement definitions;
- advertised ASIN, purchased ASIN, parent/variation-family mapping where relevant;
- campaign/ad group/keyword/target/search-term/placement data;
- budget, bid, state, negative-targeting and structure-change history;
- retail context when available: stock, Featured Offer/Buy Box, price, coupon/deal, listing suppression, reviews, delivery promise, variation-family changes;
- timestamp/freshness for retail snapshots;
- total retail sales when making TACOS or organic-momentum claims.

## Workflow

1. **Reliability gate** — reconcile date windows, attribution lag, completeness and measurement comparability; a source or metric-definition cutover near the break is a competing cause.
2. **Find the break point** — identify the first sustained KPI change and classify it as abrupt, gradual, intermittent, or isolated.
3. **Size the loss** — compare matched windows; normalize unequal windows only after the data are comparable.
4. **Decompose the bridge** — impressions -> clicks -> CPC/spend -> orders/CVR -> sales/AOV -> ACOS/ROAS.
5. **Rank contributors** — prioritize ASINs, campaigns, targets, search terms and placements by lost business contribution, not noisy percentages.
6. **Check retail/market confounders** — inventory, Buy Box, price, promotion, listing, reviews, delivery, demand, competitor and parent/variation-family changes.
7. **Audit recent controls** — bids, budgets, placements, states, negatives, product-ad mapping, launches, pauses, automation or bulk edits.
8. **Run Mixed-ASIN safety** — distinguish clean routes from halo-heavy or mixed-ASIN routes before target-level actions.
9. **Assign causality** — `Confirmed`, `Likely`, `Directional`, `Rejected`, or `Missing Data`.
10. **Propose recovery** — only actions that pass the actionability gate, with validation and rollback criteria.

## Output contract

Return:

1. data reliability, measurement comparability and actionability;
2. executive verdict and exact windows;
3. KPI bridge and primary driver;
4. ranked ASIN/campaign/target contribution;
5. retail and control-change findings, including family-level effects when relevant;
6. Mixed-ASIN safety labels;
7. facts vs hypotheses vs missing data;
8. prioritized recovery proposals with confidence;
9. monitoring plan appropriate to attribution/sample maturity.

## Safety boundaries

- Do not infer causality from correlation alone.
- Same source/table/metric name does not prove comparability when attribution, completeness, filters, grain or metric semantic version changed.
- Do not recommend bid cuts, pauses or negatives solely because a row has poor ACOS.
- Do not call a target `waste` without sufficient evidence and compatible attribution maturity.
- If purchased-ASIN attribution or Mixed-ASIN scope is unclear, downgrade target-level actions to `Directional` or `Blocked`.
- A change made after the decline began is a possible fix, not a root cause.
- A stale retail snapshot cannot prove Buy Box, inventory, price or listing health during a later decline window.
- A child-ASIN conversion decline is not isolated ad inefficiency when parent/variation-family or sibling retail changes plausibly explain substitution.
- When missing/stale retail state, family-level retail shock, source-lineage drift, or metric-version drift can materially explain the break, downgrade aggressive traffic suppression until reconciled.
- Every recommendation must state evidence, confidence, expected effect, validation window and rollback trigger before it can ever reach an external executor.
