---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

## Progressive loading

Load only what the case needs:

- detailed outcome/counterfactual/rollback logic: `references/post-change-evaluation.md`;
- source, semantic-version or backfill comparability: `../../references/data-lineage.md`;
- prior optimization state/history conflicts: `../../references/optimization-memory.md`.

Do not load data-lineage for a clean single-source comparison whose snapshots use the same maturity policy.

## Required inputs

Gather what is available and label missing fields:

- original action/proposal and reason;
- entity type and stable entity ID when available;
- before value/state and intended after value/state;
- action timestamp plus marketplace/profile/timezone;
- validation metric(s), expected mechanism, validation window and rollback condition;
- current trusted state or post-change export;
- comparable pre-change performance window;
- source/snapshot metadata when baseline and post windows differ in extraction, semantic version, completeness or backfill maturity;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first** — verify whether the intended change is actually present.
2. Classify application as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. **Measurement gate** — require completed, attribution-mature, definitionally comparable windows; when history can restate, verify baseline/post backfill parity before outcome attribution.
4. Compare the post-change metrics to the best available baseline and to the expected mechanism.
5. Separate delivery effects from downstream conversion/profit effects.
6. Check retail, market, concurrent-control and measurement confounders.
7. Classify the outcome using the detailed reference.
8. Recommend `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
9. Never execute rollback; any mutation remains external and explicitly authorized.

## Key rules

- `proposed != applied != readback confirmed != worked`.
- Never call an action failed merely because early attributed orders have not matured.
- Never call an action worked when baseline and post windows use materially different semantic definitions or asymmetric backfill maturity.
- Do not optimize on ACOS/ROAS alone; evaluate the mechanism the action was supposed to change.
- Treat promotion, price, stock, Buy Box/Featured Offer, listing, demand and competitor shocks as alternative explanations.
- If multiple material changes overlap the entity/window, downgrade single-action causal claims.
- If a previous winner deteriorates after a change, check entity history before proposing another aggressive edit.

## Output

Return:

1. readback/application status;
2. evaluation windows, attribution maturity and measurement comparability;
3. expected mechanism;
4. observed delivery, conversion, sales/profit and retail evidence;
5. confounders/concurrent changes;
6. outcome classification with confidence;
7. decision;
8. next check and evidence needed;
9. structured memory event when requested (`../../schemas/optimization-event.json`).

## Safety

Default mode is `Suggest`.

`Rollback Candidate` means evidence supports preparing a rollback proposal, not performing it. Any real account mutation requires explicit authorization plus an external Connector / Executor.
