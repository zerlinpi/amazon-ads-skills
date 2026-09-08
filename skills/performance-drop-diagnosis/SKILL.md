---
name: performance-drop-diagnosis
description: Diagnose sudden or sustained Amazon Ads performance declines by tracing the break point from account to ASIN, campaign, target, search term, placement, retail readiness, and recent control changes. Use when sales, orders, ROAS, ACOS, TACOS, traffic, conversion, rank, or campaign performance dropped and the user wants a causal diagnosis rather than generic optimization advice.
description_zh: 诊断亚马逊广告销量、订单、ROAS、ACOS、TACOS、流量、转化、排名或 Campaign 表现突然或持续下降的根因。
description_en: Causal diagnosis for Amazon Ads performance declines with mixed-ASIN safety and actionability gates.
version: 0.1.0
author: zerlinpi
---

# Performance Drop Diagnosis

## Purpose

Find **what changed, when it changed, where the loss came from, and which causes are actually supported by evidence**. Do not treat ACOS/ROAS movement itself as a root cause.

Default mode: `Read-only` or `Suggest`. Never mutate a live account.

## Progressive loading

Read this file first. Load only what is needed:

- Detailed causal workflow and Mixed-ASIN safety: `references/causal-drop-diagnosis.md`
- Cross-source freshness/semantic reconciliation: `../../references/data-lineage.md`
- Metric definitions: `../../references/amazon-ads-metrics.md`
- Shared decision boundaries: `../../references/decision-boundaries.md`
- General optimization logic: `../../references/optimization-framework.md`

Do not load `data-lineage.md` for an ordinary single-source comparison with stable definitions.

## Required context

Collect or explicitly mark missing:

- marketplace, profile/account scope, currency, timezone, date window, attribution maturity;
- primary KPI and business objective;
- daily or weekly account/campaign performance;
- source metadata when baseline/comparison windows come from different reports or refresh paths;
- advertised ASIN, purchased ASIN, parent/variation-family mapping where relevant;
- campaign/ad group/keyword/target/search-term/placement data;
- budget, bid, state, negative-targeting and structure-change history;
- retail context when available: stock, Featured Offer/Buy Box, price, coupon/deal, listing suppression, reviews, delivery promise, variation-family changes;
- timestamp/freshness for every retail snapshot used as evidence;
- total retail sales when making TACOS or organic-momentum claims.

## Workflow

1. **Reliability gate** — reject incomplete current-day comparisons, reconcile date windows and attribution lag, verify source comparability when measurement paths differ, label missing data, and verify that retail snapshots are temporally relevant.
2. **Find the break point** — identify the first sustained KPI change and classify it as abrupt, gradual, intermittent, or isolated.
3. **Size the loss** — compare a matched baseline and decline window; normalize unequal windows to per-day values only after the underlying data are comparable.
4. **Decompose the bridge** — trace impressions -> clicks -> CPC/spend -> orders/CVR -> sales/AOV -> ACOS/ROAS.
5. **Rank contributors** — identify the ASINs, campaigns, targets, search terms and placements contributing most to lost sales/orders, not merely the noisiest percentage changes.
6. **Check retail and market confounders** — inventory, Buy Box, price, promotion, listing, reviews, delivery, demand, competitor and parent/variation-family changes. Mark stale snapshots as historical evidence, not current-state proof.
7. **Audit recent controls** — bids, budgets, placements, states, negatives, product-ad mapping, launches, pauses, automation or bulk edits around the break date.
8. **Run Mixed-ASIN safety** — distinguish clean single-ASIN routes from halo-heavy or mixed-ASIN routes before recommending target-level actions.
9. **Assign causality** — use `Confirmed`, `Likely`, `Directional`, `Rejected`, or `Missing Data`.
10. **Propose recovery** — only actions that pass the actionability gate; include observation window and rollback criteria for any future execution.

## Output contract

Return, in order:

1. data reliability, source comparability when relevant, and actionability;
2. executive verdict;
3. exact baseline and decline windows;
4. KPI bridge and primary driver;
5. ranked ASIN/campaign/target contribution;
6. retail and control-change findings, including retail snapshot freshness and family-level effects when relevant;
7. Mixed-ASIN safety labels;
8. facts vs hypotheses vs missing data;
9. prioritized recovery proposals with confidence;
10. 3-day / 7-day / 14-day monitoring plan when appropriate.

## Safety boundaries

- Do not infer causality from correlation alone.
- Do not compare cross-source windows as one clean trend when attribution, completeness, filters, grain, semantic version or available-through dates are materially unresolved.
- Do not recommend bid cuts, pauses or negatives solely because a row has poor ACOS.
- Do not call a target `waste` without enough clicks/spend and a compatible attribution window.
- If a campaign/ad group contains multiple advertised ASINs and purchased-ASIN attribution is unclear, downgrade target-level actions to `Directional` or `Blocked`.
- A change made after the decline began is a possible fix, not a root cause.
- A retail snapshot is valid only for the state/time it actually observed. A stale snapshot cannot prove Buy Box, inventory, price or listing health during a later decline window.
- A child-ASIN conversion decline should not be treated as isolated ad inefficiency when a dated parent/variation-family or sibling retail change can plausibly explain substitution or purchased-ASIN mix shift.
- When a conversion-led decline could materially be explained by missing/stale retail state, family-level retail shock, or unresolved source lineage, downgrade aggressive traffic-suppression actions until the competing explanation is resolved.
- Every recommendation must state evidence, confidence, expected effect, validation window and rollback trigger before it can ever reach an external executor.
