# Portfolio and budget-pool conflict reference

Load this only when multiple campaigns compete for the same business budget, portfolio cap, external pacing pool, **Sponsored Products account-level daily budget cap**, or another account-level spend constraint.

The goal is to avoid locally sensible campaign recommendations that are globally impossible, contradictory, or harmful.

## 1. Define the constrained pool first

Before recommending campaign budget changes, establish the actual constraint hierarchy:

- campaign daily/lifetime budget;
- portfolio budget cap or product-line envelope;
- Sponsored Products account-level daily budget cap when configured;
- fixed daily/weekly/monthly business budget;
- external pacing/automation pool;
- launch, defense, profitability, or inventory-specific reserve;
- no hard upstream constraint, where campaigns can be evaluated more independently.

Do not assume every campaign can receive more budget simultaneously. A higher campaign budget is not additional account spend headroom when an upstream account/portfolio/business cap is already binding.

## 2. Separate campaign efficiency from allocation priority

A campaign can be efficient but still be a lower allocation priority than another campaign.

For each campaign, record when available:

- business role: defense, profit, launch, growth, discovery, rank support, clearance, experiment;
- contribution economics or the closest objective-aligned measure;
- current spend and budget utilization;
- average time in budget / budget-serving coverage when available;
- platform-estimated missed impressions/clicks/sales and recommended budget when available;
- evidence of marginal headroom;
- inventory/retail readiness;
- protected minimum spend or strategic floor;
- recent optimization/experiment status;
- whether another campaign serves the same ASIN/query demand.

Do not rank solely by historical ROAS/ACOS.

### Observed vs modeled budget evidence

Keep budget-serving observations separate from modeled opportunity estimates.

Examples of observed/current-state evidence:

- campaign spend;
- campaign budget;
- average time in budget / out-of-budget status;
- account/portfolio cap and current pool spend.

Examples of modeled or recommendation evidence:

- estimated missed impressions;
- estimated missed clicks;
- estimated missed sales;
- recommended campaign budget.

Modeled missed-opportunity metrics can support a directional headroom hypothesis. They are not guaranteed incremental outcomes and do not override profitability, inventory, overlap, or upstream-cap constraints.

## 3. Detect budget-pool interference

Treat campaigns as interacting when one campaign's allocation can change another campaign's opportunity set.

Common mechanisms:

- a fixed pool means one increase requires a reduction elsewhere;
- a Sponsored Products account-level daily budget cap constrains cumulative spend across campaigns;
- a portfolio cap blocks campaign-level delivery even when the campaign budget itself is raised;
- an external allocator/pacer shifts spend among campaigns;
- campaigns overlap on query/ASIN demand and compete for the same auction opportunity;
- a protected defense or launch floor reduces genuinely movable budget;
- inventory constraints make nominal headroom unusable;
- concurrent reallocations contaminate post-change attribution.

When material interference exists, campaign-level recommendations must include the pool-level consequence.

### Upstream-cap gate

Before treating a campaign-level budget increase as feasible, answer:

1. Is any account, portfolio, business, or external pacing cap active?
2. How much trusted headroom remains at each upstream level?
3. If upstream headroom is insufficient, which source campaign/pool allocation can move without violating protected floors?
4. If the upstream cap itself is proposed to change, is that a separate business-budget decision with explicit sizing basis and guardrails?

If these cannot be resolved, keep the campaign recommendation `Directional`, `Hold`, or `Manual Review` rather than presenting a precise increase as deliverable.

## 4. Conflict-resolution order

Resolve competing proposals in this order:

1. **Safety and retail constraints** — avoid overspend, stock risk, loss of purchasability, suppression, or explicit stop conditions.
2. **Upstream budget feasibility** — reconcile account/portfolio/business caps and remaining pool headroom.
3. **Protected business roles** — preserve declared defense, launch, experiment, contractual, or minimum-volume commitments unless the user changes the objective.
4. **Objective alignment** — compare campaigns using the metric that matches the business objective; profit objectives should use contribution economics where available.
5. **Marginal headroom** — prefer destinations where additional spend has evidence of incremental value, not merely good average historical efficiency or a platform missed-sales estimate.
6. **Opportunity cost** — every transfer must identify what is sacrificed at the source.
7. **Reversibility and evidence quality** — prefer smaller, observable transfers when uncertainty is high.

If objectives conflict and no priority is declared, output `Manual Review` rather than inventing a business preference.

## 5. Reallocation packet

For a constrained pool, proposals should be expressed as a balanced transfer plan, not isolated budget edits.

Include:

- pool identifier/scope and constraint type;
- active upstream caps and trusted remaining headroom;
- pool budget before and after;
- source campaign(s) and destination campaign(s);
- protected floors/reserves;
- amount or bounded range moved when supported;
- source opportunity cost;
- destination expected mechanism;
- observed serving evidence vs modeled missed-opportunity evidence;
- marginal evidence and confidence;
- affected ASIN/query overlap;
- validation window;
- rollback/stop condition.

Unless the user explicitly changes the total pool or upstream cap, proposed transfers should reconcile to the same total budget.

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
- **constraint realization** — did the intended account/portfolio/campaign budget state actually allow the extra delivery?

A destination campaign improving does not prove the reallocation was beneficial if the source lost more value. A campaign budget increase also does not prove increased serving if an upstream cap remained binding.

## 8. Safety boundaries

- Do not optimize every campaign independently under a fixed total budget.
- Do not treat budget exhaustion as proof of marginal headroom.
- Do not treat estimated missed sales/clicks/impressions as guaranteed incrementality.
- Do not treat a campaign-level recommendation as feasible without resolving a binding upstream account/portfolio cap.
- Do not pull protected spend without surfacing the business-role conflict.
- Do not infer that the campaign with the highest average ROAS deserves the next dollar.
- Do not claim a portfolio improvement from destination lift alone; include source opportunity cost.
- Do not introduce a live-account write path; this reference only shapes `Suggest`/`Shadow` decisions.
