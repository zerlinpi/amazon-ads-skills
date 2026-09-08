---
name: experiment-planner
description: Design guarded Amazon Ads experiments when an optimization hypothesis is promising but not yet action-safe. Use for bid, budget, placement, targeting, search-term, campaign-structure, launch, retail-readiness or growth tests that need a clear hypothesis, comparable baseline/control, primary metric, guardrails, validation window and stop/rollback criteria before external execution.
---

# Amazon Ads Experiment Planner

Use this Skill when evidence is insufficient for a confident direct optimization but strong enough to justify a controlled test.

Default mode: `Shadow` for design/simulation, otherwise `Suggest`. This Skill never executes live Amazon Ads mutations.

## Core workflow

1. State the decision the experiment is meant to resolve.
2. Write one falsifiable hypothesis with an expected mechanism.
3. Define treatment scope and the cleanest feasible comparison: holdout/control, matched historical baseline, phased rollout, or switchback.
4. Choose one primary success metric and a small set of diagnostic/guardrail metrics.
5. Check sample sufficiency, attribution maturity, seasonality, promotions, stock, price, Buy Box / Featured Offer, mixed-ASIN and concurrent-change risk.
6. Check whether treatment/control can interfere through shared queries, ASIN demand, budgets, routing, placements, auctions, or automation.
7. For long-running tests, re-verify control boundaries after material keyword/target/negative, automation, migration, budget-pool, variation-family or retail-scope changes; launch-time cleanliness is not permanent proof.
8. Estimate the minimum decision-useful effect or practical business threshold when the economics support it; do not invent statistical precision from missing inputs.
9. Define pre-test state, test window, observation window, stop conditions and rollback triggers before any mutation.
10. Output a machine-readable experiment plan when needed using `../../schemas/experiment-plan.json`.
11. After an externally applied test, route outcome evaluation to `post-change-review` rather than judging success inside this planner.

## Progressive loading

- Detailed design, control selection, windows and general contamination: `references/experiment-design.md`
- Shared query/ASIN/budget/auction/control leakage, interference, or long-test boundary drift: `references/interference-and-leakage.md`

Load only the reference required by the experiment. Ordinary short, low-overlap tests should not load the interference reference.

## Experiment validity gates

Do not call an experiment decision-ready when any material issue remains unresolved:

- the hypothesis changes multiple independent controls without a way to separate effects;
- baseline and treatment periods differ materially in promotion, stock, price, listing state or attribution maturity;
- treatment and control share traffic or resources in a way that causes substantial leakage, displacement, or interference;
- a material scope-changing event occurred after the latest trustworthy control-boundary verification;
- realized treatment/control allocation materially departs from the declared design without an explanation;
- the test entity is mixed-ASIN and the proposed conclusion requires ASIN-level attribution that is not reliable;
- the primary metric can improve while profitability or a critical guardrail deteriorates;
- sample size or traffic is too small to distinguish a useful business effect;
- another recent optimization on the same entity is still inside its validation window.

When blocked, return `Redesign`, `Hold`, or `Directional only` instead of forcing a test.

## Design principles

- Change the fewest controls needed to test the hypothesis.
- Prefer reversible treatments.
- Predeclare the primary metric and decision rule; do not select the winner after seeing whichever KPI improved.
- Keep efficiency and volume together. A lower ACOS with collapsed qualified demand is not automatically a win.
- Separate platform-attributed outcomes from business profitability and incrementality claims.
- When cohorts interact, inspect combined/pool outcomes before calling a treatment incremental.
- Treat control integrity as time-varying during long tests; revalidate after material scope changes.
- Use account-specific economics and comparable history before generic benchmarks.
- Never treat a fixed click/order count as a universal Amazon requirement.

## Output

Return:

1. **Decision question** — what uncertainty this test should resolve.
2. **Hypothesis** — treatment → mechanism → expected outcome.
3. **Scope** — marketplace, ad type, entity IDs/ASINs and exclusions.
4. **Design** — treatment, comparison method, baseline/control, allocation integrity, boundary freshness and interference risk.
5. **Metrics** — one primary metric, diagnostics and guardrails.
6. **Readiness** — data quality, sample sufficiency, attribution maturity, overlap/interference and confounders.
7. **Windows** — pre-test baseline, treatment period, conversion-lag/observation period and next review point.
8. **Decision rules** — Keep/Test winner, Extend, Inconclusive, Stop, Rollback Candidate or Redesign.
9. **Execution boundary** — `Suggest`/`Shadow`; external executor required for any live write.

Every experiment should preserve enough before/after state to support later `post-change-review` and `optimization-event` history.
