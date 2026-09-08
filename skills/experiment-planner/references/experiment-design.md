# Experiment design reference

Use this only when `experiment-planner` needs detailed design logic.

## 1. Start with a decision, not a metric

An experiment exists to reduce a specific decision uncertainty.

Good structure:

`If we change X for scope Y, mechanism Z should improve primary outcome M without violating guardrails G.`

Examples of valid questions:

- Does increasing Top of Search exposure for already-profitable exact targets create incremental orders at acceptable contribution economics?
- Does separating a mixed campaign into cleaner ASIN scopes improve controllability without sacrificing profitable halo?
- Does harvesting a proven query into Exact preserve/increase qualified volume versus leaving discovery traffic unchanged?

Avoid hypotheses such as “improve ACOS” that do not identify a treatment or mechanism.

## 2. Select the cleanest feasible comparison

Preferred order depends on the account and available traffic:

1. concurrent randomized or clean holdout/control when feasible;
2. matched entities with similar objective, maturity and economics;
3. phased rollout where comparable untreated entities remain available;
4. switchback/time-sliced treatment when auction/traffic conditions support it;
5. matched historical baseline using complete attribution-mature periods;
6. pre/post only, clearly labeled as weaker causal evidence.

Do not present a historical comparison as equivalent to a randomized control.

## 3. Unit of treatment

Define what receives the treatment:

- campaign;
- ad group;
- keyword/target;
- search-term routing;
- advertised ASIN;
- placement modifier;
- budget allocation;
- portfolio or grouped cohort.

The measurement unit should match the causal question where possible. If a campaign contains multiple ASINs but the decision concerns one ASIN, either redesign the experiment or mark ASIN-level conclusions as directional.

## 4. Primary metric contract

Choose one primary success metric before observing the result. It should connect directly to the business decision.

Possible primary metrics include:

- contribution profit or profit after ads;
- incremental orders/revenue when a credible control exists;
- attributed orders or sales;
- ROAS/ACOS when efficiency is genuinely the objective;
- qualified traffic or impression share when the test is explicitly a delivery/visibility experiment.

Supporting diagnostics may include impressions, CTR, CPC, clicks, CVR, AOV/ASP, placement mix and search-term composition.

Guardrails may include:

- maximum acceptable spend loss;
- minimum order/revenue retention;
- contribution-margin floor;
- inventory cover;
- Buy Box / Featured Offer stability;
- branded/defense coverage;
- no material deterioration in another protected ASIN or campaign.

A diagnostic KPI improving does not override a failed primary metric or breached safety guardrail.

## 5. Minimum decision-useful effect

When business economics are available, define the smallest effect that would change the operating decision.

Examples:

- minimum extra contribution profit required to justify more spend;
- minimum order lift worth accepting higher CPC;
- maximum efficiency loss acceptable for a strategic rank/defense objective.

This is a practical decision threshold, not automatically a statistical minimum detectable effect.

If sufficient data and a valid statistical design exist, a power/MDE calculation may be used. If variance, sample, allocation or baseline rate is missing, do not fabricate a power result.

## 6. Sample and duration logic

Do not use fixed universal click/order counts.

Duration should account for:

- normal daily/weekly traffic variation;
- conversion lag / attribution maturity;
- expected effect size;
- baseline variance;
- sales velocity;
- promotional calendar;
- stock horizon;
- auction volatility.

A low-volume experiment can remain `Directional` or `Inconclusive` rather than being forced into a winner/loser classification.

## 7. Allocation integrity and sample-ratio checks

When an experiment declares an expected traffic or entity split, compare that design with realized eligible allocation before trusting the outcome.

An unexplained mismatch can indicate:

- assignment/routing errors;
- eligibility filters applied differently across arms;
- logging or data-loss problems;
- serving constraints;
- external automation changing one cohort;
- interference or contamination;
- an implementation that differs from the declared experiment.

Do not treat a nominal 50/50 design as proof that realized treatment/control exposure was valid.

If sufficient counts and a valid probabilistic assignment model exist, a formal sample-ratio mismatch test may be used. If the expected allocation, assignment process, or eligible population is unclear, do not fabricate a p-value; classify allocation integrity as unresolved and downgrade causal confidence.

A strong observed lift under unexplained allocation mismatch is still an observation, not an action-safe causal result. Prefer `Hold`, `Redesign`, `Experiment Only`, or `Manual Review` until the mismatch is explained or a clean rerun succeeds.

## 8. Contamination and interference

Check whether treatment can affect the comparison group through:

- the same query auction;
- overlapping keywords/targets;
- shared budget constraints;
- portfolio budget rules;
- parent/child ASIN substitution;
- cross-ASIN halo;
- branded cannibalization;
- concurrent promotions or price changes;
- external automation editing either cohort.

Record contamination risk as `Low`, `Moderate`, `High`, or `Unknown`. High/Unknown risk should reduce causal confidence or trigger redesign.

## 9. Pre-test freeze and lineage

Before external execution, capture:

- entity IDs and serving states;
- bids, budgets, placement modifiers and negatives relevant to the test;
- advertised-ASIN mapping;
- primary/guardrail metric baseline;
- inventory, price, promotion and Featured Offer/Buy Box state;
- recent optimization events on the same entities;
- exact source/date lineage.

Avoid changing unrelated controls during the test unless a guardrail/safety issue requires intervention. If another change occurs, record it as a confounder.

## 10. Early stopping

Early stopping is allowed for safety, not for opportunistic winner selection.

Valid safety stops include:

- spending/risk limit breached;
- inventory or Buy Box/Featured Offer failure;
- obvious serving/application failure;
- structural data-quality problem;
- protected profitability/volume guardrail breached beyond the declared tolerance.

Do not repeatedly peek at noisy short-term conversion data and stop as soon as the preferred variant looks ahead. Sequential-testing methods require an explicit method and compatible data; otherwise wait for the declared observation window.

## 11. Result states

Use explicit states:

- `Ready` — design is executable through an authorized external layer.
- `Shadow Only` — useful for simulation/backtest but not live testing yet.
- `Redesign` — hypothesis/design has allocation, contamination or identification problems.
- `Hold` — data/economics/readiness are insufficient.

After execution, evaluation should use `post-change-review` with the experiment plan as context. Recommended outcome labels:

- `Winner / Keep`;
- `Likely Winner / Monitor`;
- `Inconclusive / Extend or Repeat`;
- `Loser / Rollback Candidate`;
- `Application Failure`;
- `Invalidated by Confounder`;
- `Invalidated by Allocation Integrity`.

## 12. Multi-arm and multi-factor caution

Do not introduce multiple independent changes just because they are all plausible improvements. Multi-factor experiments need enough traffic and a design that can identify effects/interactions. In normal Amazon PPC operations, sequential small tests are usually easier to interpret and reverse.

## 13. Handoff contract

The planner should hand off:

- experiment ID;
- hypothesis;
- treatment and comparison scopes;
- declared allocation and realized-allocation check when applicable;
- exact planned changes;
- primary metric;
- diagnostic metrics;
- guardrails;
- baseline and test windows;
- contamination/confounder assumptions;
- stop/rollback rules;
- expected mechanism;
- mode and authorization boundary.

This context should be retained for readback, evaluation and future optimization memory.