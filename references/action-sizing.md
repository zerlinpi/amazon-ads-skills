# Contextual action sizing

Load this shared reference only when a Skill must turn a directional bid, budget, placement, or other monetary-control recommendation into a concrete proposed magnitude.

The goal is to make action size depend on evidence, business constraints, reversibility and downside exposure instead of a repository-wide percentage heuristic.

## 1. No universal default percentage

The repository does **not** define one default bid-change percentage, budget-change percentage, placement-change percentage, or damping factor that is safe for every account.

A percentage shown in a public guide, UI example, historical playbook, another seller's account, or third-party Skill is an example or local policy unless the current account has explicitly adopted it.

Therefore:

```text
no account policy + no calibrated response evidence
≠ permission to invent a universal ±X% action
```

When a numeric magnitude cannot be justified, keep the result directional, propose a bounded experiment, use the smallest reversible step allowed by an explicit caller policy, or return `Hold / Manual Review`.

## 2. Preconditions before sizing

Before calculating a final magnitude, resolve when material:

- marketplace/profile/entity identity and trusted current value;
- business objective and target economics;
- data window, attribution maturity and sample sufficiency;
- recent optimization history and any pending validation/readback;
- retail readiness, inventory and promotion/event context;
- bidding strategy, placement modifiers and other coupled controls;
- budget-pool, protected-spend or portfolio constraints;
- source comparability and material data-quality warnings.

If these inputs are missing in a way that could reverse the decision, do not compensate by choosing a smaller arbitrary percentage. Downgrade actionability instead.

## 3. Separate raw estimate from allowed action

A model or formula may produce a useful economic anchor without proving that the whole gap should be applied immediately.

For example, a Skill may derive a `raw_value` from target ACOS, expected CVR, marginal headroom, or another account-specific model. Preserve that raw estimate separately from the proposed control value.

Conceptually:

```text
raw_value
→ evidence/risk assessment
→ damping or bounded step only if justified
→ policy / business / platform constraints
→ proposed_value
```

If damping is used, its factor must come from an explicit account/caller policy, calibrated historical response, declared experiment design, or another documented constraint. Do not silently substitute a repository-global damping constant.

## 4. Evidence and risk dimensions

Use the following dimensions to decide whether a proposal can be larger, smaller, experimental, or held.

### Evidence strength

Stronger evidence can include:

- mature attribution and adequate repeat observations;
- stable relevance/retail state;
- consistent performance across comparable windows;
- trustworthy current-state readback;
- historical response for the same control/entity or a carefully justified comparable cohort;
- clear marginal headroom or response-curve evidence.

Weak or conflicting evidence should reduce actionability before it merely reduces percentage size.

### Downside exposure

Consider:

- expected incremental spend exposed before the next readout;
- business importance of the entity;
- brand-defense/protected role;
- inventory or margin risk;
- possibility of traffic collapse after a decrease;
- shared budget or auction effects on other campaigns.

### Reversibility and observability

A change is safer to probe when:

- trusted readback can confirm actual application;
- the prior state is known;
- rollback is operationally possible through the authorized external executor;
- the validation window is measurable;
- concurrent controls can remain stable enough to interpret the result.

Reversibility never authorizes the Skill itself to write to Amazon Ads.

### Coupling

Reduce actionability when bid, dynamic bidding, placement modifiers, budget, negatives, targeting, promotions or retail state are changing together. Prefer staged changes or an experiment if multiple controls would otherwise make attribution uninterpretable.

## 5. Action classes

Use qualitative classes before forcing a percentage:

- `Hold` — important evidence/state is missing, conflicting, immature, or another change is still being validated.
- `Probe` — direction is plausible but response is uncertain; use a caller-defined smallest reversible step or Shadow/Experiment design.
- `Bounded Adjust` — evidence supports a concrete change and an explicit account/business risk bound or calibrated response model defines the acceptable magnitude.
- `Scale Within Headroom` — strong evidence plus measurable marginal headroom and operational constraints support expansion; still validate post-change marginal efficiency.
- `Manual Review` — potential downside is large, constraints conflict, identity/current state is uncertain, or no safe numeric bound can be established.

Do not map these classes to hard-coded repository percentages.

## 6. Caller/account policy precedence

A caller may provide explicit control limits such as:

- max single-change percentage or absolute amount;
- minimum/maximum bid or budget;
- protected budget floors;
- maximum incremental spend-at-risk before review;
- allowed action class by confidence/risk tier;
- stricter limits for launch, defense, low-inventory or promotion states.

Treat these as **constraints**, not performance claims. The final proposal must be no more aggressive than the narrowest applicable trusted constraint.

If policies conflict, fail closed and expose the conflict.

## 7. Platform behavior is context, not a repository action rule

Amazon Ads exposes multiple bidding strategies, placement adjustments, schedule/event bid rules and performance/schedule budget rules. These platform capabilities show that control behavior depends on campaign configuration, performance goals and time/event context; they do not establish one universally correct manual adjustment percentage.

When platform-provided recommendations or suggested ranges are available in a trusted current source, they may be recorded as one evidence input. Do not treat them as an unconditional command or as transferable evidence across marketplaces/accounts.

## 8. Output contract

When a concrete monetary-control proposal is produced, include when available:

- `current_value`;
- `raw_value` or directional anchor and how it was derived;
- `proposed_value`;
- `action_class`;
- `sizing_basis` — account policy, calibrated history, marginal headroom, experiment design, etc.;
- `constraints_applied`;
- `evidence_strength` / confidence;
- material coupled-control and downside risks;
- validation window and next readout;
- rollback condition for an authorized external executor;
- `mode`, normally `Suggest` or `Shadow`.

If `proposed_value` cannot be justified, omit the false precision and return the missing constraint/evidence required to size it.

## 9. Safety boundary

This reference sizes proposals only. It does not authorize live Amazon Ads mutations. `Execute` remains an explicit external Connector/Executor concern under `references/decision-boundaries.md`.
