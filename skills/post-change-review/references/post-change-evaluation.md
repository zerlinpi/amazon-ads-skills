# Post-change evaluation framework

Load this only when `post-change-review` needs detailed evaluation logic.

## 1. Separate application from outcome

A change has two independent questions:

1. Was the intended state applied?
2. Did the business outcome improve for the intended reason?

Application states:

- `Confirmed` — current state matches the intended after-state.
- `Partial` — only part of the intended mutation is present.
- `Not Applied` — current state still matches the before-state or otherwise shows no intended change.
- `Drifted` — the change was applied but later moved again.
- `Unknown` — live state cannot be verified.

Never evaluate performance success until the application state is understood.

## 2. Expected mechanism chain

Every optimization action should declare its mechanism. Examples:

- bid increase -> auction competitiveness -> impressions/placement -> clicks -> orders -> sales/profit;
- budget increase -> fewer budget-constrained hours -> incremental qualified traffic -> orders/sales;
- negative keyword -> reduced irrelevant traffic/waste -> mix shift -> efficiency;
- placement modifier -> placement mix -> CPC/CVR mix -> sales/profit;
- exact harvest -> query routing -> controlled delivery -> conversion efficiency;
- pause/reduction -> reduced low-quality spend while preserving strategically important traffic.

Judge upstream indicators before downstream indicators when the downstream outcome has attribution lag.

## 3. Evaluation windows

Use exact dates and completed periods.

Prefer:

- a comparable pre-change baseline;
- a post-change readback window for serving-state checks;
- an attribution-mature performance window for conversion/profit evaluation.

Do not prescribe universal day counts. The right window depends on traffic volume, conversion lag, seasonality, promotion periods, and the action's mechanism.

When a 3/7/14-day cadence is operationally useful, treat it as a review schedule rather than proof thresholds:

- early: application/delivery;
- middle: directional conversion evidence;
- later: efficiency/profit and secondary effects.

## 4. Counterfactual hierarchy

Use the strongest available comparison:

1. same-entity holdout or controlled experiment;
2. matched control entity unaffected by the change;
3. same entity, comparable historical period;
4. account/category trend adjusted comparison;
5. simple before/after, explicitly labeled weak.

Do not claim incremental lift from a plain before/after comparison when market, promotion, price or seasonality changed materially.

## 5. Concurrent-change contamination

Build a short timeline around the evaluated action and list any other material changes to:

- bids;
- budgets;
- placements;
- targeting or negatives;
- campaign/ad-group/product-ad states;
- price, coupon, deal or promotion;
- inventory/availability;
- listing/variation structure;
- external automation.

If multiple changes plausibly affect the same KPI, classify the result as multi-change or lower causal confidence instead of assigning all movement to one action.

## 6. Outcome classification

Use these labels:

- `Worked` — intended state confirmed, mechanism-consistent improvement observed, and material alternative explanations are weak.
- `Likely Worked` — evidence supports success but counterfactual or attribution remains imperfect.
- `Monitoring` — action is applied but the performance window is not mature enough.
- `Inconclusive` — enough time passed but signal is weak/noisy or confounded.
- `Likely Failed` — application confirmed and mechanism-consistent deterioration or lack of expected effect is reasonably supported.
- `Failed` — strong evidence shows the action did not achieve the intended objective or violated a rollback guardrail.
- `Application Failure` — intended state was not correctly applied; performance outcome should not be attributed to the proposal.
- `Drifted` — later changes invalidate a clean evaluation.

The outcome confidence must never exceed the evidence quality.

## 7. Decision mapping

| Outcome | Default decision |
|---|---|
| Worked | Keep |
| Likely Worked | Keep / continue monitoring |
| Monitoring | Keep Monitoring |
| Inconclusive | Follow-up Experiment or Manual Review |
| Likely Failed | Rollback Candidate or controlled adjustment |
| Failed | Rollback Candidate |
| Application Failure | Fix Application |
| Drifted | Re-baseline / Manual Review |

These are recommendations, not live-write authorization.

## 8. Rollback gate

Prepare a rollback candidate only when:

- the current applied state is known;
- the original before-state is known or safely reconstructable;
- the observed failure is material relative to the stated objective;
- attribution maturity is sufficient for the decision;
- product/retail changes do not better explain the result;
- rollback does not create a new known safety risk;
- entity IDs and before/after values are exact when a future executor would need them.

If the original before-state is unknown, prefer `Manual Review` over inventing a rollback value.

## 9. Memory event fields

When writing a structured optimization event, capture enough context for a later Agent to avoid repeating or misreading the action:

- unique event ID;
- parent/proposal ID when available;
- event type;
- timestamp;
- marketplace/profile scope;
- entity type/id;
- action type;
- before/intended/current values;
- objective and expected mechanism;
- evidence summary;
- application status;
- outcome status;
- confidence;
- baseline/post windows;
- confounders;
- decision;
- next evaluation time/window;
- rollback condition or rollback candidate;
- source lineage.

Do not store credentials, tokens, customer secrets or unnecessary personal data.
