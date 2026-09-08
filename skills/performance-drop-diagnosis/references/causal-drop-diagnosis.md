# Causal performance-drop diagnosis

Use this reference only after `performance-drop-diagnosis/SKILL.md` routes here.

## 1. Window discipline

Prefer completed, equally mature periods. For recent daily reporting, anchor on the latest complete trusted day rather than partial current-day data. If windows differ in length, compare per-day rates as well as totals.

Record:

- baseline start/end;
- decline start/end;
- attribution maturity;
- known promotions or outages;
- marketplace, currency and timezone.

Do not hide window mismatches inside a percentage delta.

## 2. Driver bridge

Treat efficiency ratios as symptoms. Decompose sales loss through the observable chain:

- impressions and eligible traffic;
- CTR and clicks;
- CPC and spend;
- CVR and orders;
- AOV/ASP and attributed sales;
- placement/query mix;
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
- `budget-or-serving-constraint`
- `control-change`
- `retail-readiness`
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

## 4. Control-change timeline

For the period before and during the break, inspect changes to:

- campaign/ad-group/target/product-ad state;
- bids and bidding strategy;
- campaign and portfolio budgets;
- placement modifiers;
- negative keywords and negative product targets;
- keyword/target creation or removal;
- advertised-ASIN mapping;
- bulk edits, rules or external automation.

For each candidate change capture:

`timestamp -> entity -> previous value -> new value -> affected route -> timing relation -> plausible mechanism`

Timing relation:

- `preceded-break`
- `during-break`
- `after-break`
- `unknown`

Only changes that precede or overlap the decline can plausibly be root causes. Post-break changes belong in the recovery timeline.

## 5. Retail-readiness gate

Before blaming advertising, check whether the promoted product could still convert normally:

- in stock and purchasable;
- Featured Offer / Buy Box status;
- price and major price change;
- coupon, deal or promotion start/end;
- listing suppression or content disruption;
- delivery promise / Prime availability;
- review/rating shock;
- parent-child or variation changes.

A current snapshot is evidence about current state only. Historical causality requires dated observations or change history.

## 6. Mixed-ASIN safety

Target-level optimization becomes risky when a campaign or ad group advertises multiple ASINs or when purchased-ASIN halo is material.

Classify each action candidate:

### Action-safe

Use when the route is sufficiently attributable to the affected ASIN and the proposed action is unlikely to remove profitable demand for another ASIN.

### Directional

Use when evidence suggests a problem but mixed-ASIN, halo, low-volume, or attribution uncertainty could materially change the decision. Recommend further segmentation or observation rather than immediate mutation.

### Blocked

Use when the data cannot tell which ASIN benefits from the route, or when an action could plausibly damage another strategically important ASIN.

Never turn a `Directional` or `Blocked` row into an execution-ready negative, pause or large bid cut.

## 7. Causality ladder

Use explicit labels:

- `Confirmed` — timing, mechanism and scoped evidence align; material alternatives have been checked.
- `Likely` — evidence strongly supports the cause but one important verification remains.
- `Directional` — plausible pattern, insufficient for mutation.
- `Rejected` — evidence conflicts with the proposed cause.
- `Missing Data` — required evidence is unavailable.

Keep facts separate from hypotheses. A recommendation should never be more confident than the cause supporting it.

## 8. Negative-targeting protection

A high-spend zero-order query can be a new negative candidate, but it is not automatically the cause of a sales decline.

Before recommending a negative in a drop investigation:

- compare multiple windows when available;
- check prior conversion history;
- verify attachment scope;
- verify whether the search term served another ASIN profitably;
- distinguish `new waste` from `previous winner stopped converting`;
- consider attribution lag and promotion periods.

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

## 10. Monitoring cadence

Use short windows for serving-state recovery and longer windows for conversion and profitability confirmation:

- 3-day: delivery, impressions, clicks, obvious serving restoration;
- 7-day: conversion and order direction where attribution is sufficiently mature;
- 14-day: efficiency, profitability and secondary effects.

Adjust these windows when product velocity, attribution lag, seasonality or sample size makes them inappropriate.
