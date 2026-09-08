---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

Load `references/post-change-evaluation.md` when detailed classification, timing, counterfactual or rollback logic is needed.

## Required inputs

Gather what is available and label missing fields:

- original action/proposal and reason;
- entity type and stable entity ID when available;
- before value/state;
- approved or intended after value/state;
- action timestamp and marketplace/timezone;
- validation metric(s), expected mechanism, validation window and rollback condition;
- current live state or post-change export;
- comparable pre-change performance window;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first.** Confirm whether the intended change is actually present in current state before judging performance.
2. Classify implementation as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. Define observation windows using completed, attribution-mature periods; do not compare partial current-day data with complete historical days.
4. Compare the post-change metrics to the best available baseline and to the action's expected mechanism.
5. Separate delivery effects from business outcome effects. Example: a bid increase may restore impressions before orders mature.
6. Check confounders and concurrent changes. If multiple material controls changed together, reduce causal confidence.
7. Classify the outcome using the detailed reference.
8. Recommend one of: `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
9. Do not execute rollback. Return a guarded proposal for an external executor only when evidence supports it.

## Key rules

- Never call an action successful if readback shows it was not applied.
- Never call an action failed merely because early attributed orders have not matured.
- Do not optimize on ACOS/ROAS alone; evaluate the mechanism the action was supposed to change.
- Distinguish expected short-term movement from durable business impact.
- Treat promotion, price, stock, Buy Box/Featured Offer, listing, demand and competitor shocks as possible alternative explanations.
- If multiple changes overlap the same entity/window, downgrade single-action causal claims.
- If a previous winner deteriorates after a change, compare against entity history before recommending another aggressive edit.

## Output

Return:

1. **Readback status** — intended vs current state.
2. **Evaluation windows** — exact baseline/post-change dates and attribution maturity.
3. **Expected mechanism** — what the action was supposed to change first and downstream.
4. **Observed evidence** — delivery, conversion, sales/profit and retail context.
5. **Confounders / concurrent changes**.
6. **Outcome classification** — with confidence.
7. **Decision** — Keep / Monitor / Rollback Candidate / Follow-up Experiment / Fix Application / Manual Review.
8. **Next check** — metric, date/window, minimum evidence needed.
9. **Memory event** — when structured output is requested, emit a record compatible with `../../schemas/optimization-event.json`.

## Safety

Default mode is `Suggest`.

`Rollback Candidate` means “evidence supports preparing a rollback proposal,” not “perform rollback now.” Any real account mutation remains outside this repository and requires explicit authorization plus the external Connector / Executor layer.
