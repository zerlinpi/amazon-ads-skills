# Experiment interference and leakage reference

Load this only when treatment and comparison scopes may share auctions, queries, ASIN demand, budgets, routing, automation, platform-managed realization, or another constrained resource. It supplements `experiment-design.md`; ordinary low-overlap experiments do not need it.

The purpose is to stop an observed treatment lift from being mistaken for incrementality when the treatment changes what the control can receive.

## 1. Separate three failure modes

### Concurrent-change contamination

A third change affects the outcome during the experiment: price, promotion, budget, placement, listing state, inventory, automation, or another optimization.

### Treatment leakage

The control receives treatment-like exposure or the intended treatment boundary is not preserved.

Examples:

- the same bid/placement rule is accidentally applied to both cohorts;
- a harvested keyword or target appears in both treatment and control;
- routing/negative changes move supposedly held-out traffic into the treatment path;
- a shared automation edits both cohorts.

### Interference

The control is not directly treated, but treatment changes its opportunity set, resource capacity, or outcome.

Examples:

- treatment and control compete for the same query auction;
- both advertise the same ASIN or substitutable child ASINs and one cohort changes demand/halo captured by the other;
- campaigns draw from one fixed budget/pacing pool;
- treatment changes query routing, placement exposure, or auction pressure that changes control delivery.

Do not call these three mechanisms equivalent. They can require different redesigns.

## 2. Build an overlap map before launch

For treatment and comparison scopes, map when available:

- campaign/ad-group/keyword/target IDs;
- normalized search queries or target expressions;
- advertised ASINs and important purchased-ASIN/halo paths;
- parent/child variation-family relationships;
- match types and negative-routing boundaries;
- audience/optimization signals and the product-specific semantics of those controls;
- placement and bidding controls;
- shared portfolio, business budget, or external pacing pool;
- shared rules, bulk jobs, agents, or automations;
- parent entities that can change both cohorts.

The map should answer whether one cohort can directly or indirectly change the traffic, demand, or resource capacity available to the other.

## 3. Query and target overlap

Keyword/target identity alone is insufficient. Different targets can reach the same demand.

Check, where data supports it:

- exact search-term overlap;
- close-variant or broad/phrase routes that can enter both cohorts;
- product targets that reach the same product detail pages;
- automatic-targeting routes that overlap manual control scopes;
- negatives intended to isolate treatment/control traffic;
- branded or category demand that can substitute between campaigns.

Do not use a universal overlap-percentage threshold. The actionability depends on traffic concentration, business importance, and whether overlap can materially change the causal comparison.

## 4. Audience / optimization-signal boundary safety

In AI-managed campaigns, an advertiser-provided audience signal can be an **optimization signal** rather than a hard targeting constraint.

Current Amazon Ads Brand+ / Performance+ Audience Signals are an example of why this distinction matters: Amazon describes these audiences as inputs that guide AI optimization, and Brand+ Prospecting can retain broader reach discovery. Product documentation, not the field name alone, determines whether a given audience control is an eligibility boundary, an exclusion, or merely a model input.

Therefore:

```text
audience signal configured
!= delivery restricted to signal members
!= treatment cohort isolated from non-members
!= valid control/holdout boundary
```

An audience signal is **not a holdout boundary** unless the relevant control semantics or actual delivery evidence prove sufficient separation.

Before using an audience-defined experiment:

- classify each audience-related control as `hard include`, `hard exclude`, `optimization signal`, or `unknown`;
- verify whether the platform can expand beyond the provided signal;
- inspect actual delivery at the closest available audience/cohort/reporting scope;
- confirm exclusions or other isolation controls when causal separation depends on them;
- if realized delivery composition is unavailable, label cohort integrity `Unknown` rather than assuming the configured signal equals actual delivery.

Warning pattern:

```text
treatment = AI campaign + audience signal A
control = same AI campaign without signal A
assumption = only audience A can receive treatment
```

If the product can use the signal as an optimization input while retaining broader reach, that assumption is invalid. The test may still answer whether **providing the signal** changes performance, but it cannot automatically answer whether **audience A** itself caused the lift.

### Machine-readable holdout boundary

For a plan that will be marked `Ready` with `comparison.design_type = holdout`, record the actual isolation basis under `comparison.isolation_evidence` and keep `comparison.control_integrity = Clean` only while that boundary is verified.

Allowed evidence mechanisms are deliberately narrow:

- `platform_randomization` — a platform/assignment mechanism creates the treatment/control partition;
- `verified_hard_control` — a hard eligibility or exclusion control creates the relevant partition;
- `verified_routing_partition` — routing/negative/control logic is verified to keep the relevant traffic separated;
- `verified_delivery_partition` — realized delivery evidence verifies a distinct treatment/control partition when configured controls alone are insufficient.

Each item carries an evidence statement and a `verified` flag. These fields make the planner's claimed boundary auditable; they do **not** prove the external evidence is true by themselves.

`optimization_signal` is intentionally **not** an `isolation_evidence.mechanism`. An AI audience signal may coexist with a valid holdout when a separate verified boundary exists, but the signal itself cannot be promoted into holdout evidence merely because it is configured.

If the only proposed basis is an `optimization_signal`, or if the boundary evidence is missing/unverified, keep the plan in `Shadow Only`, `Redesign`, or `Hold` rather than `Ready`.

Load `../../../references/realized-ad-identity.md` when platform-managed audience/product/creative realization materially affects the interpretation.

## 5. Auction interference

In auction systems, increasing treatment bids, placement exposure, or budget can alter the control cohort even when control settings are unchanged.

Warning patterns include:

- treatment impressions/clicks rise while control falls on the same query family;
- treatment CPC rises or falls together with a control delivery shift;
- combined treatment+control volume is flat while one cohort appears to win;
- treatment receives traffic that previously served through control;
- a change in one campaign modifies the marginal opportunities available to another.

When these patterns are plausible, analyze combined demand and displaced control value before claiming incremental lift.

## 6. Shared-budget starvation

A control is not independent when treatment and control draw from the same fixed business budget, portfolio cap, or external pacing allocator.

A treatment that spends more can mechanically reduce the capacity available to control. This is **resource interference**, even if the control configuration itself never changed.

Before interpreting the result, compare:

- pool budget and whether the pool was truly fixed;
- treatment spend change;
- control spend/delivery change;
- whether treatment gained roughly the resource the control lost;
- combined orders, revenue, contribution profit, or other objective-aligned pool outcome;
- whether protected spend or pacing logic constrained control delivery.

Warning pattern:

```text
treatment spend ↑
control spend ↓
shared pool total unchanged
treatment orders ↑
control orders ↓
combined/pool outcome flat or worse
```

This pattern is compatible with **redistribution**, not necessarily incremental demand.

If the real business question is whether reallocating a fixed pool improves the portfolio, redesign the experiment around the **pool-level treatment** and evaluate source opportunity cost plus destination gain. If the question requires independent campaign exposure, isolate budget capacity before launch.

Load `../../budget-optimization/references/portfolio-budget-conflicts.md` only when detailed budget-pool reconciliation is needed.

## 7. ASIN substitution, variation families, and halo

Treat ASIN scopes as potentially interacting when:

- cohorts advertise the same ASIN;
- treatment/control advertise sibling child ASINs under one parent;
- child variations substitute strongly on size, color, pack, style, or availability;
- purchased-ASIN attribution crosses treatment/control boundaries;
- branded demand or defensive traffic can be captured by either cohort;
- one child becomes unavailable or loses Featured Offer and demand shifts to another child.

A child-level lift may represent a **mix shift** inside the variation family rather than incremental family demand.

When parent/child substitution is plausible, compare at least:

- treatment-child result;
- control/sibling-child result;
- parent/variation-family combined result;
- purchased-ASIN crossover where available;
- contribution economics at the level that matches the business objective.

Warning pattern:

```text
treatment child orders ↑
sibling/control child orders ↓
parent-family total flat
purchased-ASIN crossover present
```

Do not call the treatment child an incremental winner from its own lift alone. If ASIN-level incrementality is required but Purchased-ASIN, family mapping, or routing evidence is incomplete, downgrade the conclusion to `Directional`, `Redesign`, or `Hold`.

## 8. Control-boundary drift during long tests

A clean design at launch can become invalid later. Control integrity is a **time-varying property**, not a launch-time certificate.

Re-verify boundaries after material scope-changing events and at sensible checkpoints for long-running tests. Relevant events include:

- newly created or harvested keywords/targets;
- new, removed, or reattached negatives/routing rules;
- audience-signal / optimization-input changes whose delivery semantics can alter realized cohort composition;
- campaign/ad-group migrations or recreated entities;
- automation/rule scope changes;
- bulk edits that touch either cohort or a shared parent;
- budget-pool/portfolio membership changes;
- variation availability or parent/child structure changes;
- promotion, price, inventory, Buy Box / Featured Offer or listing-state changes that affect only one cohort.

Track this in the experiment-plan schema when available:

- `comparison.boundary_monitoring.launch_verified_at` — launch-time boundary check;
- `comparison.boundary_monitoring.latest_verified_at` — latest trustworthy boundary check;
- `comparison.boundary_monitoring.current_status` — current compact integrity state;
- `comparison.boundary_monitoring.material_scope_changes` — dated scope changes, each with `reverified` when known.

For a `Ready` holdout, a material change newer than `boundary_monitoring.latest_verified_at` means the boundary is stale. A change explicitly marked `reverified = false` also blocks `Ready`. Do not treat a stale launch check as evidence that later routing, audience, budget, entity, retail, or automation conditions remained clean.

If the latest trustworthy boundary check predates a material scope-changing event, do not claim the entire later window remained clean.

### Readout under drift

When drift begins mid-test:

1. keep the pre-drift interval separate from the affected interval;
2. do not silently pool both intervals into one clean causal estimate;
3. determine whether the affected interval can be excluded or separately interpreted without post-hoc cherry-picking;
4. if the design is no longer comparable, downgrade to `Hold`, `Redesign`, `Experiment Only`, or `Manual Review`;
5. prefer a clean rerun when the business decision requires strong causal evidence.

A successful launch audit does not override later evidence of changed routing, automation, entity lineage, budget membership, audience-signal semantics, or control exposure.

## 9. Integrity states

Use a compact interference state when useful:

- `Low` — boundaries are well isolated and no material shared opportunity set/resource is known;
- `Moderate` — some overlap exists but its causal impact appears bounded and measurable;
- `High` — treatment can materially change control exposure, demand, or resources;
- `Unknown` — the required overlap/routing/resource evidence is missing.

For control integrity, useful states are:

- `Clean` — currently verified against the relevant scope map;
- `At Risk` — a material scope change occurred and clean isolation is not yet re-verified;
- `Leaky` — control receives treatment-like exposure;
- `Interfering` — cohorts remain distinct but materially affect one another;
- `Unknown` — evidence is insufficient to verify current boundaries.

`High`, `At Risk`, `Leaky`, `Interfering`, or `Unknown` does not automatically mean the observed data are useless. It means causal winner claims and broad rollout require redesign, segmentation, additional evidence, or a clearly directional interpretation.

## 10. Redesign options

Prefer the least invasive design that restores a credible comparison:

- choose non-overlapping query/target scopes;
- use verified hard audience exclusions/eligibility controls instead of assuming optimization-signal membership creates isolation;
- isolate ASIN/product groups when business meaning remains valid;
- avoid sibling child-ASIN controls when strong substitution is expected;
- add explicit routing/negative boundaries and verify attachment;
- separate fixed budget/pacing pools when the experiment question requires independent capacity;
- redefine the treatment at portfolio/family level when the true intervention is reallocation or mix shift;
- use matched historical or phased evidence and label causal strength correctly when a clean concurrent control is impossible.

Do not create exclusions merely to improve experimental purity if they introduce unacceptable business risk. In that case prefer `Shadow`, `Hold`, or a weaker but honest design.

## 11. Readout rules

Before calling a treatment `Winner / Keep`:

1. confirm intended treatment actually applied;
2. verify allocation/delivery integrity;
3. verify control integrity across the relevant time window, not only at launch;
4. check leakage into control;
5. check audience-signal semantics when AI-managed delivery can expand beyond configured signal membership;
6. check shared-auction, ASIN-family, budget, routing, and automation interference;
7. compare combined/pool/family outcomes when displacement is possible;
8. account for attribution maturity and retail confounders;
9. state residual interference and boundary-drift risk.

A treatment can improve its own ROAS, orders, or contribution profit while producing no incremental account-level value if it mostly captures traffic, budget, or demand previously available to control.

## 12. Safety boundary

This reference only changes experiment design and interpretation. It never authorizes live Amazon Ads writes. Any routing, negative, bid, budget, audience, or structure change remains `Suggest`/`Shadow` until an authorized external executor is explicitly used.
