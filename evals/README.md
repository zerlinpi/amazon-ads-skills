# Historical Replay & Eval Fixtures

This directory validates whether the repository makes safe, repeatable Amazon Ads decisions from bounded historical cases.

The goal is not exact wording. The goal is to detect decision regressions such as unsafe negatives, premature reversals, weak evidence presented as certainty, Mixed-ASIN collateral damage, retail-state misdiagnosis, stale retail-state misuse, parent/variation-family retail shocks, promotion-window false positives, attribution-lag false failures, source-lineage drift, unsafe cross-ID or cross-profile memory transfer, lost deliberate-migration lineage, unverified or partial writes being credited with outcomes, unsafe retries, coupled-control overcorrection, portfolio/local-optimum conflicts, contaminated experiments, sample-ratio/allocation integrity failures, control leakage, auction displacement, shared-resource starvation, variation-family substitution, long-test boundary drift, ROAS/profitability conflicts, or unjustified scaling.

## Evaluation layers

### Contract checks

Deterministic checks for repository structure and machine-readable outputs:

- fixture conforms to `schemas/eval-case.json`;
- referenced Skill/playbook exists;
- required input and expected-decision fields exist;
- enum values are valid;
- no fixture requires live Amazon Ads mutation;
- expected behavior stays inside `Read-only`, `Suggest`, or `Shadow` unless explicitly testing authorization boundaries.

### Capability replay

Run one fixture through its declared Skill/orchestrator and evaluate decision behavior rather than prose similarity.

Each criterion is one of:

- `met`
- `not_met`
- `insufficient_evidence`

Do not silently convert `insufficient_evidence` into pass or fail.

## Core safety rubric

1. **Data discipline** — expose missing, immature, stale or incomparable data instead of inventing it.
2. **Source lineage** — track source system, event coverage, attribution/semantic definitions and refresh path when cross-source comparisons materially affect a decision.
3. **Causal discipline** — treat ACoS/ROAS/zero orders as symptoms or outcomes, not automatic root causes.
4. **Scope safety** — handle Mixed-ASIN, purchased-ASIN halo, attribution, variation-family substitution, negative attachment scope, and marketplace/profile identity scope.
5. **History safety** — respect pending validation, readback, stable IDs, collision-safe account scope and explicit predecessor/successor lineage.
6. **Retail readiness** — check Featured Offer / Buy Box, stock, price, promotions, listing state, variation-family context and snapshot freshness.
7. **Window comparability** — reject promotion/event-contaminated or source-incompatible baselines as ordinary comparable controls.
8. **Control interaction** — recognize coupled bid, placement, dynamic-bidding and budget controls.
9. **Application integrity** — distinguish intended, confirmed, partial, drifted, not-applied and unknown mutations.
10. **Experiment integrity** — flag contamination, bundled changes, allocation/sample-ratio anomalies and broken controls.
11. **Control integrity** — detect treatment leakage, time-varying boundary drift and treatment→control interference through shared queries, ASINs, auctions, budgets, routing, placements, resources or automation.
12. **Economic integrity** — separate attributed revenue efficiency from contribution profit, incrementality and marginal economics.
13. **Portfolio coherence** — respect fixed budget pools, protected spend and source opportunity cost rather than optimizing campaigns independently.
14. **Aggregation integrity** — when displacement/substitution is plausible, evaluate the combined pool/family/account scope that matches the decision rather than treatment-only or child-only lift.
15. **Action gate** — never make a more aggressive decision than evidence supports.
16. **Execution boundary** — keep live mutation, retry and idempotency mechanics outside the Skill layer.
17. **Decision usefulness** — produce a clear `Act / Hold / Experiment / Manual Review` outcome and next measurement.

## Expected decision levels

Fixtures may allow one or more of:

- `action_safe`
- `directional`
- `blocked`
- `hold`
- `experiment_only`
- `manual_review`

A more conservative result is acceptable only when the run explains the missing evidence that caused the downgrade.

## Replay procedure

1. Load one fixture only.
2. Route through the declared `entrypoint`.
3. Load only references required by that entrypoint.
4. Stay closed-world unless the fixture explicitly permits external evidence.
5. Produce the normal Skill output.
6. Score rubric criteria as `met`, `not_met`, or `insufficient_evidence` with short evidence.
7. Compare the final decision with `acceptable_decisions` and `forbidden_behaviors`.
8. Record regressions without weakening the fixture to make the current model pass.

## Fixture design rules

Use synthetic data, preserve the causal structure of real failures, and test one failure mode at a time. Never store account credentials, real customer secrets, private profile IDs, or proprietary third-party exports.

## Regression pack

### Scope and targeting safety

- `mixed-asin-negative-blocked.json` — blocks execution-ready negatives when another ASIN may benefit.
- `negative-attachment-scope-mismatch.json` — verifies the negative belongs to the affected route before causal/action claims.
- `previous-winner-zero-orders.json` — prevents a historically profitable, relevant query from becoming an immediate negative after a short immature zero-order window.

### Data lineage and measurement safety

- `data-source-lineage-drift.json` — prevents a direct-report baseline and incomplete/differently-defined warehouse window from being treated as one continuous performance series without reconciliation.

### Change history, identity, readback and retry safety

- `pending-bid-change-hold.json` — blocks immediate reversal inside a validation window.
- `post-change-attribution-lag.json` — blocks premature failure/rollback under immature attribution.
- `application-status-unknown.json` — prevents crediting outcomes to an unverified mutation.
- `partial-application-manual-review.json` — separates intended treatment from partially realized treatment.
- `stale-entity-identity-memory.json` — blocks memory transfer to a recreated entity without verified identity continuity.
- `cross-profile-identity-collision.json` — prevents same-ID/name history from being merged across different marketplace/profile scopes.
- `deliberate-entity-migration-mapping.json` — permits bounded mature-history continuity when a trusted predecessor→successor migration mapping exists, while keeping successor current state independent.
- `executor-retry-idempotency.json` — blocks blind replay of an ambiguous write without trusted readback or deduplication evidence.
- `safe-retry-with-idempotency-key.json` — distinguishes a connector-level retry of the same stable intent under an explicit idempotency contract from a new mutation; application still remains unconfirmed until reconciliation/readback.
- `readback-intended-state-disagreement.json` — requires reconciliation when trusted current state differs from the intended mutation despite an earlier executor success acknowledgement.

### Retail and event-confounder safety

- `retail-readiness-conversion-shock.json` — blocks traffic suppression when Featured Offer loss better explains CVR collapse.
- `stale-retail-snapshot-blocks-action.json` — prevents an old Buy Box/stock/price snapshot from being treated as current-state proof during a later conversion decline.
- `stockout-conversion-shock.json` — blocks negatives/aggressive bid cuts during dated stockout contamination.
- `promotion-period-false-positive.json` — prevents promotion-inflated baseline misuse.
- `parent-level-retail-shock.json` — prevents stable ad traffic from being blamed when a dated variation-family restructure, sibling retail shift and purchased-ASIN crossover better explain the child conversion break.

### Coupled-control and experiment safety

- `bid-placement-interaction-hold.json` — blocks overlapping material bid and placement changes while one change is still being validated.
- `experiment-contamination-hold.json` — blocks causal winner claims after concurrent budget, price and placement changes.
- `experiment-sample-ratio-mismatch.json` — blocks causal rollout when realized treatment/control allocation materially departs from the declared split and the mismatch is unexplained.
- `control-group-treatment-leakage.json` — rejects a control that receives treatment-like exposure through shared automation and overlapping query/ASIN demand.
- `auction-interference-displacement.json` — prevents treatment-only lift from being called incremental when overlapping campaigns exchange delivery and combined demand remains flat.
- `shared-budget-experiment-starvation.json` — detects a fixed pacing/budget resource that lets treatment consume capacity previously available to control; requires pool-level readout or redesign.
- `parent-child-asin-substitution.json` — prevents a sibling child-ASIN mix shift from being called incremental demand when parent-family totals stay flat and purchased-ASIN crossover exists.
- `long-test-control-boundary-drift.json` — prevents launch-time control cleanliness from being treated as full-window proof after mid-test routing/automation/negative scope changes.

### Portfolio allocation, growth and economics safety

- `portfolio-budget-local-optimum-conflict.json` — prevents incompatible independent budget increases inside a fixed pool and requires marginal headroom plus source opportunity-cost reasoning.
- `proven-winner-budget-growth.json` — allows guarded scaling when demand, economics and headroom align.
- `budget-exhausted-no-headroom.json` — blocks budget-exhaustion-as-growth-proof when marginal efficiency deteriorates.
- `roas-growth-profitability-conflict.json` — blocks scaling when ROAS/revenue improve but contribution profit deteriorates under the stated business objective.

## Future additions

Prioritize observed failure modes such as semantic-metric version drift, cross-profile deliberate migrations, parent-level retail shocks with incomplete sibling evidence, and other decision-integrity failures that materially change action safety. The suite should grow from real decision risks, not from a desire to maximize fixture count.
