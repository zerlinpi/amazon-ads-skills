---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, resolve the selected decision profile with `../../scripts/resolve_skill_capabilities.py`, pass both its `required_capabilities` and any returned `data_requirements` into `../../scripts/evaluate_connector_capability_gate.py`, and run the gate **before metric interpretation**. For the `outcome-review` profile, live performance evidence requires historical campaign performance rather than history metadata alone.

- `Pass` — continue with the Skill's normal evidence, sufficiency, lineage and safety checks.
- `Degraded` — do not make a high-confidence dependent recommendation; keep the result to `Directional`, `Hold`, `Alternate Source`, `Missing Data`, or `Manual Review`.
- `Blocked` — do not treat the dependent observation as action-safe until the capability is resolved or an allowed alternate source is verified.
- `missing_evidence_policy = never_zero` — `Partial`, `Unsupported`, `Unknown`, or absent connector capability is never a numeric zero, unchanged state, or proof that the platform lacks the feature.

This gate is read-only and does not authorize live Amazon Ads mutation.

## Progressive loading

Load only what the case needs:

- detailed outcome/counterfactual/rollback logic: `references/post-change-evaluation.md`;
- platform-managed surface/product/creative realization: `../../references/realized-ad-identity.md`;
- source, semantic-version or backfill comparability: `../../references/data-lineage.md`;
- overlapping advertiser-control history and causal isolation: `../../references/control-state-comparability.md`;
- prior optimization state/history conflicts: `../../references/optimization-memory.md`.

Do not load data-lineage for a clean single-source comparison whose snapshots use the same maturity policy. Load `control-state-comparability.md` when the baseline and post-change windows can differ in bidding strategy, placement/audience adjustments, bid rules, budget/pacing, targeting/routing, or another material advertiser control. Load `realized-ad-identity.md` when the ad format can change the shopper-visible surface, product mix, creative/message, prompt, or other realization independently of the advertiser control under review.

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
- material control state/timestamps for baseline and post-change windows when causal attribution matters;
- realized surface/product/creative identity when the ad product can vary it during the evaluation window;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first** — verify whether the intended advertiser control is actually present.
2. Classify application as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. **Measurement gate** — require completed, attribution-mature, definitionally comparable windows; when history can restate, verify baseline/post backfill parity before outcome attribution.
4. **Control-state comparability gate when causal attribution matters** — reconstruct material advertiser-control state across baseline and post-change windows. If overlapping changes can explain the effect, cap the single-control conclusion at `Directional` / `Confounded` / `Unknown` rather than calling the intended action causal.
5. **Realization gate when relevant** — verify whether platform-managed surface/product/creative realization stayed sufficiently comparable. A confirmed control readback does not prove stable realized ad identity.
6. Compare the post-change metrics to the best available baseline and to the expected mechanism.
7. Separate delivery effects from downstream conversion/profit effects.
8. Check retail, market, concurrent-control, platform-managed-realization and measurement confounders.
9. Classify the outcome using the detailed reference.
10. Recommend `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
11. Never execute rollback; any mutation remains external and explicitly authorized.

## Key rules

- `proposed != applied != readback confirmed != worked`.
- `measurement comparable != control-state comparable`; a clean metric series does not isolate the intended action when another material control changed.
- `readback confirmed != stable realized ad identity` when Amazon can dynamically select surfaces, products, creative/message, or another shopper-visible realization.
- Never call an action failed merely because early attributed orders have not matured.
- Never call an action worked when baseline and post windows use materially different semantic definitions or asymmetric backfill maturity.
- Never call an action worked/failed causally when overlapping material control changes remain `Confounded` or `Unknown`.
- Do not optimize on ACOS/ROAS alone; evaluate the mechanism the action was supposed to change.
- Treat promotion, price, stock, Buy Box/Featured Offer, listing, demand and competitor shocks as alternative explanations.
- If multiple material advertiser or platform-managed changes overlap the entity/window, downgrade single-action causal claims.
- Missing control state or realized product/creative/surface fields from the active connector are not evidence of unchanged state, zero exposure, or unchanged realization.
- If a previous winner deteriorates after a change, check entity history before proposing another aggressive edit.

## Output

Return:

1. readback/application status;
2. evaluation windows, attribution maturity and measurement comparability;
3. control-state comparability when causal attribution matters;
4. realized-ad-identity comparability when relevant;
5. expected mechanism;
6. observed delivery, conversion, sales/profit and retail evidence;
7. confounders/concurrent changes;
8. outcome classification with confidence;
9. decision;
10. next check and evidence needed;
11. structured memory event when requested (`../../schemas/optimization-event.json`), preserving the decision-driving outcome metric semantics and per-metric evidence semantics when known rather than inferring them from display names.

## Safety

Default mode is `Suggest`.

`Rollback Candidate` means evidence supports preparing a rollback proposal, not performing it. Any real account mutation requires explicit authorization plus an external Connector / Executor.
