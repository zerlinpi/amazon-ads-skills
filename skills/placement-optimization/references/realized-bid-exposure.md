# Realized Bid Exposure Framework

Load this reference when a placement recommendation depends on the interaction among base/target bid, placement adjustments, campaign bidding strategy, scheduled/event bid rules, or other bid modifiers.

The goal is to avoid treating a placement modifier as an isolated control when the auction exposure observed in reports is produced by several controls plus Amazon's real-time auction logic.

## 1. Separate configured controls from realized exposure

Track the configured controls that were active for the observation window:

- target/default/base bid;
- placement adjustments for Top of Search, Rest of Search, and Product Pages when applicable;
- campaign bidding strategy (`fixed`, `dynamic-down-only`, `dynamic-up-and-down`, or unknown);
- schedule/event bid rules and their active windows when present;
- audience or other supported bid modifiers when relevant;
- effective timestamps for each material control change.

Then track realized evidence by placement:

- impressions and impression share when available;
- clicks and click share;
- spend and spend share;
- CPC;
- orders, sales, CVR, ACOS/ROAS;
- traffic/query/target mix where a mix shift could explain the placement result.

Configured controls are intent. Placement reports are realized outcomes. Do not substitute one for the other.

## 2. Do not invent a single exact effective-bid formula

Amazon Ads publicly documents that Sponsored Products placement adjustments can coexist with fixed and dynamic bidding strategies, and that dynamic bidding may adjust bids in real time based on conversion likelihood. Schedule/event rules can also change bids during declared windows.

Without a source that proves the exact composition/order for every active control in the specific campaign/runtime, do not claim an exact auction-level effective bid from configuration alone.

Use a bounded statement instead:

```text
base/target bid
+ configured placement/control modifiers
+ dynamic auction-time adjustment when enabled
→ realized auction exposure observed indirectly through placement delivery/CPC
```

The diagnostic object is the coupled control system, not a fabricated deterministic bid value.

## 3. Build a control timeline before causal claims

For any material placement change, reconstruct when possible:

```text
t0: base bid state
t1: placement modifier change
t2: bidding-strategy change
t3: schedule/event rule active window
t4: budget or retail-state change
```

If multiple material controls changed inside the same attribution/measurement window, downgrade attribution. A later placement ROAS improvement does not prove the placement modifier caused it when base bid, bidding strategy, traffic mix, budget, promotion, or retail state changed concurrently.

## 4. Distinguish control opportunity from performance correlation

A placement can show strong historical CVR/ROAS because it received a selected subset of auction opportunities. That does not prove a larger modifier will preserve the same mix or marginal efficiency.

Before increasing a modifier, ask:

- Is the placement efficient at meaningful volume?
- Is it underexposed relative to the stated objective, or already dominant?
- Did its query/target/product mix remain comparable?
- Is base bid itself the better control to change?
- Is dynamic bidding already amplifying or suppressing auction exposure?
- Are there active bid rules that will overlap the proposed change?
- Is the recommendation based on average historical efficiency or evidence of marginal headroom?

Treat historical placement efficiency as evidence for a hypothesis, not guaranteed marginal return.

## 5. Coupled-control action gate

Prefer one interpretable change at a time when feasible.

If a placement modifier, base bid, bidding strategy, or schedule/event rule is already pending evaluation on the same traffic route:

- `Hold` another overlapping material change unless a guardrail requires intervention;
- or use a bounded `Shadow/Experiment` plan that explicitly models the interaction;
- preserve the prior control state and exact active windows for post-change review.

If the current state of any material control is unknown or stale, do not issue a precise placement modifier as action-safe.

## 6. Output contract

When this reference materially affects the recommendation, include:

- `control_state`: base/target bid, placement modifier, bidding strategy, active rule/modifier state;
- `control_state_as_of` and material change timestamps;
- `realized_placement_evidence`: delivery, CPC, conversion/efficiency, and mix notes;
- `interaction_risk`: Low / Medium / High / Unknown;
- `causal_attribution`: Supported / Directional / Confounded / Unknown;
- `recommended_control`: placement modifier / base bid / rule / hold / experiment;
- `sizing_basis` if a numeric modifier is proposed;
- guardrails, validation window, and rollback condition.

Load `../../../references/action-sizing.md` when a directional placement conclusion is converted into a specific numeric change.

## 7. Safety boundary

This framework is decision support only. It does not authorize live Amazon Ads writes. Mutation, retry, idempotency, and authoritative readback remain external Connector/Executor responsibilities.
