# Growth opportunity evaluation

Load this reference only when concrete Amazon Ads growth opportunities must be ranked, sized or converted into controlled action proposals.

## 1. Opportunity evidence model

A growth opportunity is stronger when multiple independent dimensions align:

- **Demand evidence** — repeatable orders/sales or high-quality leading indicators;
- **Economics** — compatible with product margin, target ACoS/CPA or explicit strategic objective;
- **Headroom** — evidence that more qualified traffic can actually be captured;
- **Retail readiness** — inventory, Featured Offer/Buy Box, price, reviews, delivery and listing support conversion;
- **Incrementality** — growth is not merely reallocating or cannibalizing demand already captured elsewhere;
- **Attribution quality** — campaign/target/search-term/ASIN relationships are sufficiently scoped;
- **Reversibility** — the proposed step can be measured and rolled back without large structural risk.

Low ACoS alone is never sufficient evidence of headroom or incrementality.

## 2. Headroom signals

Treat headroom as a hypothesis supported by one or more of the following:

- budget-limited delivery on an already validated route;
- proven search terms still living inside discovery campaigns without clean Exact coverage;
- profitable target or placement with low exposure relative to its validated demand;
- high-quality query/target adjacency that is not yet represented;
- strong retail conversion with limited paid coverage;
- sibling/variation performance suggesting an under-supported child ASIN;
- strategic generic or competitor demand where conversion and economics justify broader coverage.

Do not infer headroom simply because a campaign spends its full budget. A budget may be fully consumed by low-quality traffic.

## 3. Opportunity classes

### Proven scale

Use when demand, economics, readiness and attribution are all sufficiently credible. Appropriate next steps can include modest bid/budget/placement expansion, dedicated routing, or broader target coverage.

### Constrained winner

Use when evidence is strong but a specific serving constraint appears to limit delivery. Name the constraint explicitly: budget, bid, placement, match coverage, campaign state or other observable control.

### Harvest-and-isolate

Use when a converting search term or target is buried inside a broader discovery route. Separate it only when this improves control or measurement; do not create duplicate structures without a routing purpose.

### Retail-before-scale

Use when traffic quality appears adequate but conversion or offer readiness is the likely bottleneck. Additional spend should wait until the retail blocker is fixed or deliberately tested.

### Strategic defense

Use for brand, own-ASIN, rank-defense or launch support where pure efficiency is not the only objective. Require an explicit strategic rationale and distinguish defense from incremental acquisition.

### Experiment

Use when the opportunity is commercially plausible but not yet proven. An experiment should answer a specific uncertainty rather than merely “try more budget.”

### Hold / blocked

Use when missing data, weak samples, attribution ambiguity, inventory risk, structural losses or temporary promotional effects could materially reverse the decision.

## 4. Opportunity ranking without false precision

Do not invent a universal composite score. Rank opportunities using an explicit evidence table with these dimensions:

| Dimension | Questions |
|---|---|
| Expected impact | How much qualified demand or profit could plausibly be unlocked? |
| Evidence quality | Is the signal repeatable, mature and correctly scoped? |
| Headroom | Is there a credible reason additional investment can capture more demand? |
| Economics | Is the opportunity compatible with product contribution economics or strategic objective? |
| Retail readiness | Can the ASIN convert and fulfill additional traffic now? |
| Incrementality | Is the demand likely incremental rather than cannibalized/defensive? |
| Risk | Could the action damage another ASIN, rank, margin, budget stability or measurement clarity? |
| Reversibility | Can the action be tested and rolled back cleanly? |

Use qualitative labels such as `High / Medium / Low` or `Strong / Mixed / Weak` when the underlying data does not justify numeric precision.

## 5. Economics gate

When contribution economics are available, compare opportunity efficiency with the relevant break-even and target economics. Keep these concepts separate:

- platform-attributed sales;
- total retail sales;
- contribution margin before advertising;
- advertising cost;
- contribution profit after advertising;
- strategic spend intentionally accepted for launch/rank/defense.

If economics are missing, do not call an opportunity “profitable.” Use terms such as `efficient by platform proxy` and lower confidence.

## 6. Incrementality and cannibalization checks

Before scaling, ask:

- Is the traffic branded, generic, competitor, category, own-ASIN defense, remarketing or discovery?
- Is total sales growing with ad spend, or is paid share merely replacing organic share?
- Does TACoS move in a direction consistent with the stated objective?
- Are purchased-ASIN sales concentrated on the advertised ASIN or spread across siblings?
- Could a new exact/target campaign merely move conversions out of an existing route?
- Is the candidate protecting existing demand rather than creating incremental demand?

When incrementality cannot be established, label the opportunity `Directional` and define the evidence needed to test it.

## 7. Mixed-ASIN protection

For campaigns/ad groups with multiple advertised ASINs or material halo sales:

- preserve advertised and purchased ASIN joins where available;
- identify which ASIN receives the benefit;
- check whether a bid/budget/negative change could harm another ASIN;
- prefer ASIN-specific restructuring or measurement before aggressive scaling;
- downgrade ambiguous rows to `Directional` or `Blocked`.

## 8. Controlled scale design

A growth action should be decision-complete:

- entity and scope;
- current state;
- proposed change or experiment;
- growth hypothesis;
- supporting evidence;
- expected mechanism;
- primary success metric;
- guardrail metrics;
- validation window;
- rollback trigger;
- confidence;
- mode (`Suggest` or `Shadow` by default).

Avoid changing bid, budget, placement and structure simultaneously unless the user explicitly accepts the loss of causal clarity.

## 9. Experiment framing

When evidence is promising but uncertain, define:

- **Question** — what uncertainty are we resolving?
- **Hypothesis** — what should happen if the opportunity is real?
- **Change** — the smallest practical intervention;
- **Comparison** — baseline, holdout or matched historical window when feasible;
- **Success metric** — business outcome, not only delivery;
- **Guardrails** — spend, profit, inventory, CPC/CVR, rank or other downside protection;
- **Stopping condition** — enough evidence, unacceptable downside, or external event contamination;
- **Readback** — what is learned even if the hypothesis fails.

Do not call an uncontrolled budget increase an experiment.

## 10. Temporary winners and event contamination

Before scaling a recent winner, check for:

- coupon/deal/Prime event;
- temporary competitor stockout;
- price change;
- review/rating movement;
- inventory recovery;
- listing update;
- seasonality;
- campaign launch or recent control change.

A temporary event can create valid short-term growth, but the action should be labeled event-dependent instead of being treated as a permanent baseline.

## 11. Opportunity lifecycle

Use a simple lifecycle:

`Detected -> Qualified -> Proposed -> Shadow/Test -> Applied externally -> Observed -> Validated / Rolled back / Inconclusive`

Do not repeatedly rediscover the same opportunity without acknowledging prior actions or evaluations when change history is available.

## 12. Output table

Recommended columns:

- Priority
- Entity
- Opportunity type
- Growth objective
- Evidence
- Headroom
- Economics/readiness
- Incrementality risk
- Confidence
- Actionability
- Proposed next step
- Validation metric/window
- Rollback trigger

The top-ranked item should be the best commercial decision under current evidence, not simply the lowest ACoS row.