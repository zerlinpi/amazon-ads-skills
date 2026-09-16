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
6. Check whether treatment/control can interfere through shared queries, ASIN demand, budgets, routing, placements, auctions, automation, or platform-managed realization.
7. If an AI-managed campaign uses an audience signal or another optimization signal, verify whether it is a hard eligibility/exclusion control or merely a model input before treating it as a cohort/holdout boundary.
8. For long-running tests, re-verify control boundaries after material keyword/target/negative, audience-signal, automation, migration, budget-pool, variation-family or retail-scope changes; launch-time cleanliness is not permanent proof.
9. Estimate the minimum decision-useful effect or practical business threshold when the economics support it; do not invent statistical precision from missing inputs.
10. Define pre-test state, test window, observation window, stop conditions and rollback triggers before any mutation.
11. Output a machine-readable experiment plan when needed using `../../schemas/experiment-plan.json`. A plan marked `Ready` must resolve collision-safe scope: marketplace, profile/account scope, entity type and non-empty entity IDs. When repository scripts are available, validate this readiness gate with `../../scripts/validate_experiment_plan.py`; unresolved identity belongs in `Shadow Only`, `Redesign`, or `Hold` rather than fabricated scope.
12. After an externally applied test, route outcome evaluation to `post-change-review` rather than judging success inside this planner.

## Progressive loading

- Detailed design, control selection, windows and general contamination: `references/experiment-design.md`
- Shared query/ASIN/budget/auction/control leakage, interference, or long-test boundary drift: `references/interference-and-leakage.md`
- AI-managed surface/product/creative realization or optimization-signal semantics: `../../references/realized-ad-identity.md`

Load only the reference required by the experiment. Ordinary short, low-overlap tests should not load the interference or realization references.

## Experiment validity gates

Do not call an experiment decision-ready when any material issue remains unresolved:

- marketplace/profile scope or the actual experiment entity identity is unresolved for a plan that would otherwise be marked `Ready`;
- the hypothesis changes multiple independent controls without a way to separate effects;
- baseline and treatment periods differ materially in promotion, stock, price, listing state or attribution maturity;
- treatment and control share traffic or resources in a way that causes substantial leakage, displacement, or interference;
- the proposed cohort boundary relies on an audience signal / optimization signal whose product semantics do not prove hard targeting or exclusion;
- a material scope-changing event occurred after the latest trustworthy control-boundary verification;
- realized treatment/control allocation materially departs from the declared design without an explanation;
- the test entity is mixed-ASIN and the proposed conclusion requires ASIN-level attribution that is not reliable;
- the primary metric can improve while profitability or a critical guardrail deteriorates;
- sample size or traffic is too small to distinguish a useful business effect;
- another recent optimization on the same entity is still inside its validation window.

When blocked, return `Redesign`, `Hold`, or `Directional only` instead of forcing a test.

## Status semantics

- `Ready` — the experiment is decision-ready for **external execution review**, with collision-safe entity scope resolved. It is not permission to mutate Amazon Ads.
- `Shadow Only` — the design is useful for simulation/replay, but one or more action-safety or identity prerequisites are not resolved.
- `Redesign` — the current comparison/treatment structure cannot answer the declared question credibly without changing the design.
- `Hold` — required evidence, retail/data state, validation maturity, or another prerequisite is not yet available.

A plan must never upgrade itself from `Shadow Only`/`Redesign`/`Hold` to `Ready` by inventing marketplace, profile/account scope, entity IDs, audience semantics, sample sufficiency, or control integrity.

## Design principles

- Change the fewest controls needed to test the hypothesis.
- Prefer reversible treatments.
- Predeclare the primary metric and decision rule; do not select the winner after seeing whichever KPI improved.
- Keep efficiency and volume together. A lower ACOS with collapsed qualified demand is not automatically a win.
- Separate platform-attributed outcomes from business profitability and incrementality claims.
- When cohorts interact, inspect combined/pool outcomes before calling a treatment incremental.
- Treat control integrity as time-varying during long tests; revalidate after material scope changes.
- Treat configured audience/model signals as optimization inputs unless the relevant Amazon Ads product contract proves they are hard eligibility or exclusion boundaries.
- Use account-specific economics and comparable history before generic benchmarks.
- Never treat a fixed click/order count as a universal Amazon requirement.

## Output

Return:

1. **Decision question** — what uncertainty this test should resolve.
2. **Hypothesis** — treatment → mechanism → expected outcome.
3. **Scope** — marketplace, profile/account scope, ad type, entity IDs/ASINs, audience/optimization-signal semantics, and exclusions.
4. **Design** — treatment, comparison method, baseline/control, allocation integrity, boundary freshness and interference risk.
5. **Metrics** — one primary metric, diagnostics and guardrails.
6. **Readiness** — data quality, sample sufficiency, attribution maturity, overlap/interference and confounders.
7. **Windows** — pre-test baseline, treatment period, conversion-lag/observation period and next review point.
8. **Decision rules** — Keep/Test winner, Extend, Inconclusive, Stop, Rollback Candidate or Redesign.
9. **Execution boundary** — `Suggest`/`Shadow`; external executor required for any live write.

Every experiment should preserve enough before/after state to support later `post-change-review` and `optimization-event` history.
