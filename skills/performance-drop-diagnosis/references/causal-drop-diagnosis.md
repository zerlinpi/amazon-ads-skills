# Causal performance-drop diagnosis

Use this reference only after `performance-drop-diagnosis/SKILL.md` routes here.

## 1. Window discipline

Prefer completed, equally mature periods. For recent daily reporting, anchor on the latest complete trusted day rather than partial current-day data. If windows differ in length, compare per-day rates as well as totals.

Record:

- baseline start/end;
- decline start/end;
- attribution maturity;
- known promotions or outages;
- marketplace, profile/account scope, currency and timezone;
- source system and `available_through` when the measurement path differs between windows.

Do not hide window mismatches or source-definition mismatches inside a percentage delta.

When baseline and decline come from different reports, APIs, MCPs, warehouses or semantic versions, load `../../../references/data-lineage.md` before sizing the loss. A source/reporting switch near the apparent break point is a competing cause until reconciled.

## 2. Driver bridge

Treat efficiency ratios as symptoms. Decompose sales loss through the observable chain:

- impressions and eligible traffic;
- CTR and clicks;
- CPC and spend;
- orders/CVR;
- AOV/ASP and attributed sales;
- placement/query/ad-experience mix;
- budget or serving constraints.

For each step, report baseline, decline-window value, absolute delta, relative delta, contribution and confidence.

Primary driver labels:

- `traffic-loss`
- `ctr-loss`
- `cpc-inflation`
- `conversion-loss`
- `aov-loss`
- `query-mix-shift`
- `placement-mix-shift`
- `delivery-surface-mix-shift`
- `budget-or-serving-constraint`
- `control-change`
- `retail-readiness`
- `variation-family-shift`
- `source-lineage-drift`
- `market-or-seasonality`
- `mixed`
- `unknown`

## 3. Contribution before optimization

Start from business loss, not from bad-looking ratios. Rank entities by:

1. lost sales/day;
2. lost orders/day;
3. share of total account or ASIN decline;
4. strategic importance;
5. actionability and attribution quality.

A tiny target with extreme ACOS should not outrank a large previous winner that lost substantial qualified traffic.

Do not rank contribution from disputed cross-source deltas as high-confidence until source comparability is established.

## 4. Control and delivery-surface timeline

For the period before and during the break, inspect changes to:

- campaign/ad-group/target/product-ad state;
- bids and bidding strategy;
- campaign and portfolio budgets;
- placement modifiers;
- negative keywords and negative product targets;
- keyword/target creation or removal;
- advertised-ASIN mapping;
- bulk edits, rules or external automation;
- platform-managed ad experiences, delivery surfaces, or auto-enrollment that can alter where/how an existing campaign serves without an advertiser-initiated campaign edit.

For each candidate change capture:

`timestamp -> source of change -> entity/surface -> previous state -> new state -> affected route -> timing relation -> plausible mechanism`

Use `source of change` values such as `advertiser`, `external automation`, `platform-managed`, or `unknown` when the distinction matters.

Timing relation:

- `preceded-break`
- `during-break`
- `after-break`
- `unknown`

Only changes that precede or overlap the decline can plausibly be root causes. Post-break changes belong in the recovery timeline.

### Platform-managed delivery surfaces

Do not make this inference:

```text
no manual control change
→ campaign delivery conditions were unchanged
```

No manual control change **does not prove** unchanged delivery conditions when Amazon introduces or auto-enrolls existing campaigns into a new platform-managed ad experience or delivery surface.

Current public Amazon Ads documentation provides one concrete example: Sponsored Products prompts and Sponsored Brands prompts became generally available in the U.S. in March 2026, with eligible existing campaigns automatically enrolled. Amazon states that prompts use existing campaign parameters, can appear in shopping results and product detail pages, participate in CPC bidding/billing, and expose prompt-level performance reporting. Treat those facts as an example of the generic confounder, not as a permanent assumption about every marketplace, ad product, or future feature.

When such a rollout overlaps an apparent performance break:

1. identify rollout/eligibility dates and marketplace/ad-product scope;
2. check whether the affected campaign was eligible or actually received traffic from the new surface;
3. obtain surface/format-level impressions, clicks, spend, orders/sales when available;
4. compare the pre/post traffic mix before attributing the break to bid, budget, keyword, target, placement, or retail changes;
5. keep the cause `Directional` / `Missing Data` if the new surface plausibly changed mix but surface-level evidence is unavailable;
6. do not assume that pausing/suppressing another control fixes a platform-surface problem.

A platform feature announcement alone is not proof that a specific account was affected. Evidence must connect rollout eligibility and actual delivery to the scoped campaign/account.

## 5. Retail-readiness gate

Before blaming advertising, check whether the promoted product could still convert normally:

- in stock and purchasable;
- Featured Offer / Buy Box status;
- price and major price change;
- coupon, deal or promotion start/end;
- listing suppression or content disruption;
- delivery promise / Prime availability;
- review/rating shock;
- parent-child or variation-family changes.

A current snapshot is evidence about current state only. Historical causality requires dated observations or change history.

### Variation-family / parent-level shock

A child-ASIN campaign can look worse even when its ad controls and qualified traffic are stable if the surrounding variation family changed.

Check, when relevant:

- parent/child mapping additions, removals, splits or merges;
- sibling price/promotion differences;
- sibling inventory or purchasability changes;
- Featured Offer / retail-status shifts across sibling children;
- purchased-ASIN crossover toward another child;
- family-level orders/sales vs the advertised child's orders/sales;
- whether a family-level retail event begins at the same time as the child conversion break.

Warning pattern:

```text
child clicks/CPC stable
child CVR/orders ↓
sibling orders or purchased-ASIN share ↑
family total approximately stable
family/retail change precedes or overlaps break
```

This is compatible with substitution or retail mix shift, not automatically advertising waste.

Do not assume the parent entity itself has the same purchasability mechanics as a child ASIN. Use the family relationship as causal context and evaluate dated child/sibling retail observations at the scope where they are actually measured.

## 6. Mixed-ASIN safety

Target-level optimization becomes risky when a campaign or ad group advertises multiple ASINs or when purchased-ASIN halo is material.

Classify each action candidate:

### Action-safe

Use when the route is sufficiently attributable to the affected ASIN and the proposed action is unlikely to remove profitable demand for another ASIN.

### Directional

Use when evidence suggests a problem but mixed-ASIN, halo, low-volume, attribution uncertainty, family substitution, source-lineage uncertainty, or platform-managed delivery-surface changes could materially change the decision. Recommend further segmentation or observation rather than immediate mutation.

### Blocked

Use when the data cannot tell which ASIN benefits from the route, when a source disagreement makes the underlying delta unreliable, or when an action could plausibly damage another strategically important ASIN.

Never turn a `Directional` or `Blocked` row into an execution-ready negative, pause or large bid cut.

## 7. Causality ladder

Use explicit labels:

- `Confirmed` — timing, mechanism and scoped evidence align; material alternatives have been checked.
- `Likely` — evidence strongly supports the cause but one important verification remains.
- `Directional` — plausible pattern, insufficient for mutation.
- `Rejected` — evidence conflicts with the proposed cause.
- `Missing Data` — required evidence is unavailable.

Keep facts separate from hypotheses. A recommendation should never be more confident than the cause supporting it.

Unresolved source lineage, stale retail state, family-level substitution evidence, or a plausible but unmeasured platform-managed delivery-surface shift can cap an otherwise strong-looking ad diagnosis at `Directional` or `Missing Data`.

## 8. Negative-targeting protection

A high-spend zero-order query can be a new negative candidate, but it is not automatically the cause of a sales decline.

Before recommending a negative in a drop investigation:

- compare multiple compatible windows when available;
- check prior conversion history;
- verify attachment scope;
- verify whether the search term served another ASIN profitably;
- distinguish `new waste` from `previous winner stopped converting`;
- consider attribution lag, promotion periods, variation-family retail shifts, and delivery-surface/traffic-mix changes.

## 9. Recovery design

Prefer recovery actions that restore qualified demand and conversion before cosmetic ratio improvements.

Every proposal should carry:

- entity and scope;
- action;
- evidence;
- confidence;
- expected mechanism;
- risk;
- validation metric;
- validation window;
- rollback trigger;
- mode: `Suggest` or `Shadow` unless explicitly authorized externally.

When source lineage is unresolved, the recovery action may simply be `same-source replay / reconcile data`. When a family-level retail shock is more plausible than ad inefficiency, prioritize retail/family investigation before suppressing traffic. When a platform-managed surface plausibly changed traffic mix, prefer surface-level reconciliation before changing unrelated campaign controls.

## 10. Monitoring cadence

Use short windows for serving-state recovery and longer windows for conversion and profitability confirmation:

- 3-day: delivery, impressions, clicks, obvious serving restoration;
- 7-day: conversion and order direction where attribution is sufficiently mature;
- 14-day: efficiency, profitability and secondary effects.

Adjust these windows when product velocity, attribution lag, seasonality, sample size, data refresh lag, or retail changes make them inappropriate.
