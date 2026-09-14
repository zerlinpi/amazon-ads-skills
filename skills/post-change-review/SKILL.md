---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

## Progressive loading

Load only what the case needs:

- detailed outcome/counterfactual/rollback logic: `references/post-change-evaluation.md`;
- platform-managed surface/product/creative realization: `../../references/realized-ad-identity.md`;
- source, semantic-version or backfill comparability: `../../references/data-lineage.md`;
- prior optimization state/history conflicts: `../../references/optimization-memory.md`.

Do not load data-lineage for a clean single-source comparison whose snapshots use the same maturity policy. Load `realized-ad-identity.md` when the ad format can change the shopper-visible surface, product mix, creative/message, prompt, or other realization independently of the advertiser control under review.

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
- realized surface/product/creative identity when the ad product can vary it during the evaluation window;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first** — verify whether the intended advertiser control is actually present.
2. Classify application as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. **Measurement gate** — require completed, attribution-mature, definitionally comparable windows; when history can restate, verify baseline/post backfill parity before outcome attribution.
4. **Realization gate when relevant** — verify whether platform-managed surface/product/creative realization stayed sufficiently comparable. A confirmed control readback does not prove stable realized ad identity.
5. Compare the post-change metrics to the best available baseline and to the expected mechanism.
6. Separate delivery effects from downstream conversion/profit effects.
7. Check retail, market, concurrent-control, platform-managed-realization and measurement confounders.
8. Classify the outcome using the detailed reference.
9. Recommend `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
10. Never execute rollback; any mutation remains external and explicitly authorized.

## Key rules

- `proposed != applied != readback confirmed != worked`.
- `readback confirmed != stable realized ad identity` when Amazon can dynamically select surfaces, products, creative/message, or another shopper-visible realization.
- Never call an action failed merely because early attributed orders have not matured.
- Never call an action worked when baseline and post windows use materially different semantic definitions or asymmetric backfill maturity.
- Do not optimize on ACOS/ROAS alone; evaluate the mechanism the action was supposed to change.
- Treat promotion, price, stock, Buy Box/Featured Offer, listing, demand and competitor shocks as alternative explanations.
- If multiple material advertiser or platform-managed changes overlap the entity/window, downgrade single-action causal claims.
- Missing realized product/creative/surface fields from the active connector are not evidence of zero exposure or unchanged realization.
- If a previous winner deteriorates after a change, check entity history before proposing another aggressive edit.

## Output

Return:

1. readback/application status;
2. evaluation windows, attribution maturity and measurement comparability;
3. realized-ad-identity comparability when relevant;
4. expected mechanism;
5. observed delivery, conversion, sales/profit and retail evidence;
6. confounders/concurrent changes;
7. outcome classification with confidence;
8. decision;
9. next check and evidence needed;
10. structured memory event when requested (`../../schemas/optimization-event.json`).

## Safety

Default mode is `Suggest`.

`Rollback Candidate` means evidence supports preparing a rollback proposal, not performing it. Any real account mutation requires explicit authorization plus an external Connector / Executor.
