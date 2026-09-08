# Experiment interference and leakage reference

Load this only when treatment and comparison scopes may share auctions, queries, ASIN demand, budgets, routing, or automation. It supplements `experiment-design.md`; ordinary low-overlap experiments do not need it.

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

The control is not directly treated, but treatment changes its opportunity set or outcome.

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
- match types and negative-routing boundaries;
- placement and bidding controls;
- shared portfolio, business budget, or external pacing pool;
- shared rules, bulk jobs, agents, or automations;
- parent entities that can change both cohorts.

The map should answer whether one cohort can directly or indirectly change the traffic available to the other.

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

## 5. Shared-budget and pacing interference

If treatment and control share a fixed business budget, portfolio cap, or external pacing allocator, they are not independent resource consumers.

A treatment that spends more can mechanically starve control. In that case:

- treatment lift alone is not sufficient evidence;
- report source/control opportunity cost;
- evaluate the pool-level objective;
- redesign when the experiment question requires independent exposure.

Load `../../budget-optimization/references/portfolio-budget-conflicts.md` only when detailed budget-pool reconciliation is needed.

## 6. ASIN substitution and halo

Treat ASIN scopes as potentially interacting when:

- cohorts advertise the same ASIN;
- child variations substitute strongly;
- purchased-ASIN attribution crosses treatment/control boundaries;
- branded demand or defensive traffic can be captured by either cohort.

If ASIN-level incrementality is required but Purchased-ASIN or routing evidence is incomplete, downgrade the conclusion to `Directional`, `Redesign`, or `Hold`.

## 7. Integrity states

Use a compact interference state when useful:

- `Low` — boundaries are well isolated and no material shared opportunity set is known;
- `Moderate` — some overlap exists but its causal impact appears bounded and measurable;
- `High` — treatment can materially change control exposure, demand, or resources;
- `Unknown` — the required overlap/routing evidence is missing.

`High` or `Unknown` does not automatically mean the observed data are useless. It means causal winner claims and broad rollout require redesign, additional evidence, or a clearly directional interpretation.

## 8. Redesign options

Prefer the least invasive design that restores a credible comparison:

- choose non-overlapping query/target scopes;
- isolate ASIN/product groups when business meaning remains valid;
- add explicit routing/negative boundaries and verify attachment;
- separate fixed budget/pacing pools when the experiment question requires independent capacity;
- use matched historical or phased evidence and label the causal strength correctly when a clean concurrent control is impossible;
- use a portfolio-level outcome if the real treatment is reallocation across interacting campaigns.

Do not create exclusions merely to improve experimental purity if they would introduce unacceptable business risk. In that case prefer `Shadow`, `Hold`, or a weaker but honest design.

## 9. Readout rules

Before calling a treatment `Winner / Keep`:

1. confirm intended treatment actually applied;
2. verify allocation/delivery integrity;
3. check leakage into control;
4. check shared-auction, ASIN, budget, routing, and automation interference;
5. compare combined/pool outcomes when displacement is possible;
6. account for attribution maturity and retail confounders;
7. state residual interference risk.

A treatment can improve its own ROAS, orders, or contribution profit while producing no incremental account-level value if it mostly captures traffic previously served by control.

## 10. Safety boundary

This reference only changes experiment design and interpretation. It never authorizes live Amazon Ads writes. Any routing, negative, bid, budget, or structure change remains `Suggest`/`Shadow` until an authorized external executor is explicitly used.
