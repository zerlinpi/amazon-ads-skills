# Historical Replay & Eval Fixtures

This directory validates whether the repository makes safe, repeatable Amazon Ads decisions from bounded historical cases.

The goal is not to force exact wording. The goal is to detect decision regressions such as unsafe negatives, premature reversals, weak evidence presented as certainty, Mixed-ASIN collateral damage, retail-state misdiagnosis, attribution-lag false failures, unverified or partial writes being credited with outcomes, coupled-control overcorrection, contaminated experiments, or unjustified scaling.

## Two evaluation layers

### 1. Contract checks

Deterministic checks for repository structure and machine-readable outputs:

- fixture conforms to `schemas/eval-case.json`;
- referenced Skill/playbook exists;
- required input and expected-decision fields exist;
- enum values are valid;
- no fixture requires live Amazon Ads mutation;
- expected behavior stays inside `Read-only`, `Suggest`, or `Shadow` unless a fixture is explicitly testing authorization boundaries.

A contract failure means the fixture or repository contract is broken.

### 2. Capability replay

Run the fixture through the matching Skill or orchestrator and evaluate the resulting decision.

Capability replay should score decision properties, not prose similarity. A semantically equivalent explanation can pass even when wording changes.

Each criterion is one of:

- `met` — enough evidence that the behavior is present;
- `not_met` — the output materially violates the expected behavior;
- `insufficient_evidence` — the run does not expose enough evidence to judge safely.

Do not silently convert `insufficient_evidence` into pass or fail.

## Core safety rubric

A replay should evaluate at least:

1. **Data discipline** — does the output expose missing/immature/incomparable data instead of inventing it?
2. **Causal discipline** — are ratios such as ACoS treated as symptoms rather than automatic root causes?
3. **Scope safety** — are Mixed-ASIN, purchased-ASIN halo, attribution scope and negative attachment scope handled when relevant?
4. **History safety** — does the output respect pending validation/readback and avoid stacking contradictory changes?
5. **Retail readiness** — does the output check Buy Box / Featured Offer, stock, price, promotion and listing state before blaming ads when conversion breaks?
6. **Control interaction** — does the output recognize when base bid, dynamic bidding, placement modifier, budget or other controls interact rather than treating them as isolated knobs?
7. **Application integrity** — does the output distinguish intended, confirmed, partial, not-applied, drifted and unknown mutations before judging outcomes?
8. **Experiment integrity** — does the output flag bundled changes, contamination, broken controls or other conditions that block causal readout?
9. **Action gate** — is the decision no more aggressive than the evidence supports?
10. **Execution boundary** — does the repository keep live mutation outside the Skill layer?
11. **Decision usefulness** — does the run produce a clear `Act / Hold / Experiment / Manual Review` outcome with evidence and next measurement?

## Expected decision levels

Fixtures may declare one or more acceptable outcomes:

- `action_safe`
- `directional`
- `blocked`
- `hold`
- `experiment_only`
- `manual_review`

The evaluator should reject a more aggressive decision than the fixture allows. A more conservative result can be acceptable only when the run explains the missing evidence that caused the downgrade.

## Replay procedure

1. Load one fixture only.
2. Route through the declared `entrypoint`.
3. Load only references that the entrypoint requires.
4. Do not browse or fetch current account state unless the fixture explicitly allows an external evidence source; replay should normally be closed-world.
5. Produce the normal Skill output.
6. Score each rubric criterion as `met`, `not_met`, or `insufficient_evidence` with short evidence.
7. Compare the final decision with `expected.acceptable_decisions` and `expected.forbidden_behaviors`.
8. Record regressions without rewriting the fixture to make the current model pass.

## Fixture design rules

A useful fixture tests one decision failure mode at a time and contains enough context to make the expected safety boundary defensible.

Prefer synthetic data over copied client data. Never store account credentials, real customer secrets, private profile IDs, or proprietary third-party exports.

Fixtures should preserve the causal structure of a real case while using synthetic identifiers and values.

## Regression pack

### Scope and targeting safety

- `fixtures/mixed-asin-negative-blocked.json` — prevents a zero-order search term from becoming an execution-ready negative when another advertised ASIN may benefit.
- `fixtures/negative-attachment-scope-mismatch.json` — prevents a negative from being treated as causal or reusable when it is attached to a different campaign/ad-group route.

### Change-history, readback and attribution safety

- `fixtures/pending-bid-change-hold.json` — prevents an immediate reversal while a recent bid change is still inside its validation window.
- `fixtures/post-change-attribution-lag.json` — prevents an immature conversion window from being mislabeled as a failed change when the expected delivery mechanism is moving correctly.
- `fixtures/application-status-unknown.json` — prevents improved business results from being credited to a mutation that lacks trusted readback.
- `fixtures/partial-application-manual-review.json` — prevents a multi-entity treatment from being labeled fully applied or successful when only part of the intended change reached the account.

### Retail-readiness safety

- `fixtures/retail-readiness-conversion-shock.json` — blocks aggressive traffic suppression when a confirmed Featured Offer loss better explains the CVR collapse.

### Coupled-control safety

- `fixtures/bid-placement-interaction-hold.json` — prevents simultaneous material base-bid and placement-modifier changes when a recent bid change is still being validated and effective auction pressure is coupled.

### Experiment integrity

- `fixtures/experiment-contamination-hold.json` — prevents a contaminated bid experiment from being declared a causal winner after budget, price and placement changes occur during the same window.

### Growth and marginal-efficiency safety

- `fixtures/proven-winner-budget-growth.json` — verifies that profitable demand plus credible headroom can become a guarded scaling candidate without escalating to live execution.
- `fixtures/budget-exhausted-no-headroom.json` — prevents budget exhaustion from being treated as automatic scaling proof when marginal CPC rises, CVR falls and profitability is near break-even.

## Future additions

Prioritize fixtures for:

- promotion-period false positives;
- stockout conversion shocks distinct from Featured Offer loss;
- previous winner stopped converting vs genuinely irrelevant query;
- profitability conflict with apparent ROAS growth;
- campaign restructure that changes entity IDs and invalidates stale optimization memory;
- experiment control leakage or sample-ratio anomalies when the required evidence exists;
- executor retry/idempotency cases that could duplicate mutations.

The eval suite should grow from observed failure modes, not from a desire to maximize fixture count.
