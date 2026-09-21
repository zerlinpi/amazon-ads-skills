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

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, identify the exact required capability IDs and run `../../scripts/evaluate_connector_capability_gate.py` **before metric interpretation**.

- `Pass` — continue with the Skill's normal evidence, sufficiency, lineage and safety checks.
- `Degraded` — do not make a high-confidence dependent recommendation; keep the result to `Directional`, `Hold`, `Alternate Source`, `Missing Data`, or `Manual Review`.
- `Blocked` — do not treat the dependent observation as action-safe until the capability is resolved or an allowed alternate source is verified.
- `missing_evidence_policy = never_zero` — `Partial`, `Unsupported`, `Unknown`, or absent connector capability is never a numeric zero, unchanged state, or proof that the platform lacks the feature.

This gate is read-only and does not authorize live Amazon Ads mutation.

## Progressive loading

Read this file first. Load only what is needed:

- Detailed causal workflow and Mixed-ASIN safety: `references/causal-drop-diagnosis.md`
- Platform-managed surface/product/creative realization: `../../references/realized-ad-identity.md`
- Cross-source, freshness, attribution-variant, or metric-version reconciliation: `../../references/data-lineage.md`
- Metric definitions: `../../references/amazon-ads-metrics.md`
- Shared decision boundaries: `../../references/decision-boundaries.md`
- General optimization logic: `../../references/optimization-framework.md`

Do not load `data-lineage.md` for a single stable measurement path whose source, completeness, attribution variant and metric definitions are already known to be comparable. Load `realized-ad-identity.md` only when the ad product can change delivery surface, product mix, creative/message realization, or another shopper-visible experience independently of ordinary manual campaign edits.

## Required context

Collect or explicitly mark missing:

- marketplace, profile/account scope, currency, timezone, date window, attribution maturity;
- attribution model/window/variant when conversion reporting can expose multiple methodologies such as standard/default vs `all views`;
- cross-ad-product activity when diagnosing attributed conversion movement: eligible Sponsored Products, Sponsored Brands, Sponsored Display and DSP activity can compete for conversion credit, so a product/campaign attribution drop can occur without an equivalent shopper-demand drop;
- primary KPI and business objective;
- daily or weekly account/campaign performance;
- source/metric metadata when windows use different reports, refresh paths, attribution variants, semantic versions, or unknown measurement definitions;
- advertised ASIN, purchased ASIN, parent/variation-family mapping where relevant;
- campaign/ad group/keyword/target/search-term/placement data;
- budget, bid, state, negative-targeting and structure-change history;
- platform-managed delivery-surface / ad-experience changes when the marketplace may auto-enroll existing campaigns into a new format or surface;
- realized product/creative/message mix when the selected ad format can dynamically choose among eligible products or shopper-facing realizations;
- retail context when available: stock, Featured Offer/Buy Box, price, coupon/deal, listing suppression, reviews, delivery promise, variation-family changes;
- timestamp/freshness for retail snapshots;
- total retail sales when making TACOS or organic-momentum claims.

## Workflow

1. **Reliability gate** — reconcile date windows, attribution model/variant, attribution lag, completeness and measurement comparability; a source, attribution-methodology or metric-definition cutover near the break is a competing cause.
2. **Find the break point** — identify the first sustained KPI change and classify it as abrupt, gradual, intermittent, or isolated.
3. **Size the loss** — compare matched windows; normalize unequal windows only after the data are comparable.
4. **Decompose the bridge** — impressions -> clicks -> CPC/spend -> orders/CVR -> sales/AOV -> ACOS/ROAS.
5. **Rank contributors** — prioritize ASINs, campaigns, targets, search terms and placements by lost business contribution, not noisy percentages.
6. **Check attribution competition** — when attributed purchases/sales fall while traffic is comparatively stable, check whether activity changed in other eligible Amazon ad products before treating the measured conversion drop as a shopper-conversion failure. Keep the observed credit shift separate from the hypothesis about why it shifted.
7. **Check retail/market confounders** — inventory, Buy Box, price, promotion, listing, reviews, delivery, demand, competitor and parent/variation-family changes.
8. **Audit controllable and platform-managed changes** — bids, budgets, placements, states, negatives, product-ad mapping, launches, pauses, automation or bulk edits, plus auto-enrolled delivery surfaces/ad experiences and dynamic product/creative realization that can change traffic or conversion mix without a manual campaign edit.
9. **Run Mixed-ASIN safety** — distinguish clean routes from halo-heavy or mixed-ASIN routes before target-level actions.
10. **Assign causality** — `Confirmed`, `Likely`, `Directional`, `Rejected`, or `Missing Data`.
11. **Propose recovery** — only actions that pass the actionability gate, with validation and rollback criteria.

## Output contract

Return:

1. data reliability, attribution/measurement comparability and actionability;
2. executive verdict and exact windows;
3. KPI bridge and primary driver;
4. ranked ASIN/campaign/target contribution;
5. attribution-competition, retail and control-change findings, including family-level and platform-managed realization effects when relevant;
6. Mixed-ASIN safety labels;
7. facts vs hypotheses vs missing data;
8. prioritized recovery proposals with confidence;
9. monitoring plan appropriate to attribution/sample maturity.

## Safety boundaries

- Do not infer causality from correlation alone.
- Same source/table/metric name does not prove comparability when attribution model/variant, completeness, filters, grain or metric semantic version changed.
- Standard/default conversion metrics and `all views` conversion metrics are not interchangeable merely because they share labels such as Purchases, Sales or ROAS.
- An attribution-methodology cutover near a performance break is a competing measurement cause until reconciled; do not generalize a documented view-attribution change to unaffected campaign/inventory scopes.
- A decline in attributed purchases/sales for one eligible ad product does not by itself prove shopper conversion propensity fell: cross-ad-product attribution competition can reassign credit after activity changes elsewhere in the account.
- Do not recommend aggressive bid cuts, pauses or traffic suppression solely from a product-level attributed-conversion drop until material cross-product attribution competition has been checked or explicitly marked unavailable.
- No manual control change does not prove that delivery conditions stayed constant when Amazon can auto-enroll existing campaigns into a platform-managed delivery surface or dynamically realize different products/creative experiences.
- Configured eligible products are not the same thing as the realized product mix when a format supports platform-managed selection.
- Missing realized product/creative/surface fields from the active connector are not evidence that realization was unchanged or zero.
- Do not recommend bid cuts, pauses or negatives solely because a row has poor ACOS.
- Do not call a target `waste` without sufficient evidence and compatible attribution maturity.
- If purchased-ASIN attribution or Mixed-ASIN scope is unclear, downgrade target-level actions to `Directional` or `Blocked`.
- A change made after the decline began is a possible fix, not a root cause.
- A stale retail snapshot cannot prove Buy Box, inventory, price or listing health during a later decline window.
- A child-ASIN conversion decline is not isolated ad inefficiency when parent/variation-family or sibling retail changes plausibly explain substitution.
- When missing/stale retail state, family-level retail shock, source-lineage drift, attribution-variant drift, metric-version drift, cross-ad-product attribution competition, or a platform-managed realization change can materially explain the break, downgrade aggressive traffic suppression until reconciled.
- Every recommendation must state evidence, confidence, expected effect, validation window and rollback trigger before it can ever reach an external executor.
