# Portfolio and budget-pool conflict reference

Load this only when multiple campaigns compete for the same business budget, portfolio cap, external pacing pool, or account-level spend constraint.

The goal is to avoid locally sensible campaign recommendations that are globally impossible, contradictory, or harmful.

## 1. Define the constrained pool first

Before recommending campaign budget changes, establish the actual constraint:

- fixed daily/weekly/monthly business budget;
- portfolio or product-line budget envelope;
- external pacing/automation pool;
- launch, defense, profitability, or inventory-specific reserve;
- no hard pool constraint, where campaigns can be evaluated more independently.

Do not assume every campaign can receive more budget simultaneously.

## 2. Separate campaign efficiency from allocation priority

A campaign can be efficient but still be a lower allocation priority than another campaign.

For each campaign, record when available:

- business role: defense, profit, launch, growth, discovery, rank support, clearance, experiment;
- contribution economics or the closest objective-aligned measure;
- current spend and budget utilization;
- evidence of marginal headroom;
- inventory/retail readiness;
- protected minimum spend or strategic floor;
- recent optimization/experiment status;
- whether another campaign serves the same ASIN/query demand.

Do not rank solely by historical ROAS/ACOS.

## 3. Detect budget-pool interference

Treat campaigns as interacting when one campaign's allocation can change another campaign's opportunity set.

Common mechanisms:

- a fixed pool means one increase requires a reduction elsewhere;
- an external allocator/pacer shifts spend among campaigns;
- campaigns overlap on query/ASIN demand and compete for the same auction opportunity;
- a protected defense or launch floor reduces genuinely movable budget;
- inventory constraints make nominal headroom unusable;
- concurrent reallocations contaminate post-change attribution.

When material interference exists, campaign-level recommendations must include the pool-level consequence.

## 4. Conflict-resolution order

Resolve competing proposals in this order:

1. **Safety and retail constraints** — avoid overspend, stock risk, loss of purchasability, suppression, or explicit stop conditions.
2. **Protected business roles** — preserve declared defense, launch, experiment, contractual, or minimum-volume commitments unless the user changes the objective.
3. **Objective alignment** — compare campaigns using the metric that matches the business objective; profit objectives should use contribution economics where available.
4. **Marginal headroom** — prefer destinations where additional spend has evidence of incremental value, not merely good average historical efficiency.
5. **Opportunity cost** — every transfer must identify what is sacrificed at the source.
6. **Reversibility and evidence quality** — prefer smaller, observable transfers when uncertainty is high.

If objectives conflict and no priority is declared, output `Manual Review` rather than inventing a business preference.

## 5. Reallocation packet

For a constrained pool, proposals should be expressed as a balanced transfer plan, not isolated budget edits.

Include:

- pool identifier/scope;
- pool budget before and after;
- source campaign(s) and destination campaign(s);
- protected floors/reserves;
- amount or bounded range moved;
- source opportunity cost;
- destination expected mechanism;
- marginal evidence and confidence;
- affected ASIN/query overlap;
- validation window;
- rollback/stop condition.

Unless the user explicitly changes the total pool, proposed transfers should reconcile to the same total budget.

## 6. Interaction with experiments and pending changes

Do not materially reallocate budget into or out of an active treatment/control cohort unless the experiment plan allows it.

If a campaign has a pending bid, placement, budget, or structure change:

- account for the pending validation window;
- avoid another large overlapping change that destroys interpretability;
- downgrade to `Hold`, `Experiment Only`, or `Manual Review` when attribution would become ambiguous.

## 7. Portfolio-level validation

After a reallocation, evaluate both:

- **destination effect** — did the recipient use incremental budget productively?
- **source cost** — what volume/profit/coverage was lost by removing budget?
- **pool outcome** — did total objective-aligned performance improve?

A destination campaign improving does not prove the reallocation was beneficial if the source lost more value.

## 8. Safety boundaries

- Do not optimize every campaign independently under a fixed total budget.
- Do not treat budget exhaustion as proof of marginal headroom.
- Do not pull protected spend without surfacing the business-role conflict.
- Do not infer that the campaign with the highest average ROAS deserves the next dollar.
- Do not claim a portfolio improvement from destination lift alone; include source opportunity cost.
- Do not introduce a live-account write path; this reference only shapes `Suggest`/`Shadow` decisions.
