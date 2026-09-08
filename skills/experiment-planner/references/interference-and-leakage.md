# Experiment interference and leakage reference

Load this only when treatment and comparison scopes may share auctions, queries, ASIN demand, budgets, routing, automation, or another constrained resource. It supplements `experiment-design.md`; ordinary low-overlap experiments do not need it.

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

## 4. Auction interference

In auction systems, increasing treatment bids, placement exposure, or budget can alter the control cohort even when control settings are unchanged.

Warning patterns include:

- treatment impressions/clicks rise while control falls on the same query family;
- treatment CPC rises or falls together with a control delivery shift;
- combined treatment+control volume is flat while one cohort appears to win;
- treatment receives traffic that previously served through control;
- a change in one campaign modifies the marginal opportunities available to another.

When these patterns are plausible, analyze combined demand and displaced control value before claiming incremental lift.

## 5. Shared-budget starvation

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

## 6. ASIN substitution, variation families, and halo

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

## 7. Control-boundary drift during long tests

A clean design at launch can become invalid later.

Re-check during the test when practical:

- newly created keywords/targets;
- new negatives or routing rules;
- campaign migrations or renamed/recreated entities;
- automation scope changes;
- budget-pool membership changes;
- variation availability or parent/child structure changes;
- promotion or retail events that affect only one cohort.

Do not assume launch-time isolation persisted through the full readout window.

## 8. Integrity states

Use a compact interference state when useful:

- `Low` — boundaries are well isolated and no material shared opportunity set/resource is known;
- `Moderate` — some overlap exists but its causal impact appears bounded and measurable;
- `High` — treatment can materially change control exposure, demand, or resources;
- `Unknown` — the required overlap/routing/resource evidence is missing.

`High` or `Unknown` does not automatically mean the observed data are useless. It means causal winner claims and broad rollout require redesign, additional evidence, or a clearly directional interpretation.

## 9. Redesign options

Prefer the least invasive design that restores a credible comparison:

- choose non-overlapping query/target scopes;
- isolate ASIN/product groups when business meaning remains valid;
- avoid sibling child-ASIN controls when strong substitution is expected;
- add explicit routing/negative boundaries and verify attachment;
- separate fixed budget/pacing pools when the experiment question requires independent capacity;
- redefine the treatment at portfolio/family level when the true intervention is reallocation or mix shift;
- use matched historical or phased evidence and label causal strength correctly when a clean concurrent control is impossible.

Do not create exclusions merely to improve experimental purity if they introduce unacceptable business risk. In that case prefer `Shadow`, `Hold`, or a weaker but honest design.

## 10. Readout rules

Before calling a treatment `Winner / Keep`:

1. confirm intended treatment actually applied;
2. verify allocation/delivery integrity;
3. check leakage into control;
4. check shared-auction, ASIN-family, budget, routing, and automation interference;
5. compare combined/pool/family outcomes when displacement is possible;
6. account for attribution maturity and retail confounders;
7. state residual interference risk.

A treatment can improve its own ROAS, orders, or contribution profit while producing no incremental account-level value if it mostly captures traffic, budget, or demand previously available to control.

## 11. Safety boundary

This reference only changes experiment design and interpretation. It never authorizes live Amazon Ads writes. Any routing, negative, bid, budget, or structure change remains `Suggest`/`Shadow` until an authorized external executor is explicitly used.
