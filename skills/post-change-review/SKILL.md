---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, resolve the selected decision profile with `../../scripts/resolve_skill_capabilities.py`, pass both its `required_capabilities` and any returned `data_requirements` into `../../scripts/evaluate_connector_capability_gate.py`, and run the gate **before metric interpretation**. For the `outcome-review` profile, live performance evidence requires historical campaign performance rather than history metadata alone. When the pre/post windows and grain are known, pass them to the resolver through `task_data_requirements.campaign-performance-read.history_window`; use the resolver's merged `data_requirements` as the gate input so the task cannot accidentally drop the profile-owned historical-data requirement. When causal attribution uses a registered control-state decision surface such as `sponsored_products_bid_change` or `sponsored_products_budget_change`, also pass that exact `decision_surface` to the resolver. The resolver derives the registry-required control types onto `entity-state-readback`; the connector gate must prove `control_types_exposed` covers every required type before high-confidence causal review can proceed. Overall history availability cannot stand in for exact range coverage, and generic readback support cannot stand in for exact material-control observability.

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
- prior optimization state/history conflicts: `../../references/optimization-memory.md`;
- action-time/current campaign objective semantics: `../../references/campaign-objective.md`.

Do not load data-lineage for a clean single-source comparison whose snapshots use the same maturity policy. Load `control-state-comparability.md` when the baseline and post-change windows can differ in bidding strategy, placement/audience adjustments, bid rules, budget/pacing, targeting/routing, or another material advertiser control. Load `realized-ad-identity.md` when the ad format can change the shopper-visible surface, product mix, creative/message, prompt, or other realization independently of the advertiser control under review. When conversion metrics can include modeled attribution or lower-grain `Unallocated` rows, compare baseline/post `measurement_composition` from the decision-time evidence snapshot instead of assuming the same report name implies the same allocation coverage.

## Campaign objective lineage gate

When the original action carried a campaign objective, preserve that **action-time campaign objective** and its declared primary/guardrail metrics before judging the outcome. Also resolve the **current campaign objective** when available.

If they differ, label **objective drift**. Evaluate whether the historical action achieved the mechanism and guardrails it was designed for, then separately decide whether the current objective changes what should happen next. **Do not retroactively** judge a Growth, Discovery, Defense, Control, Profit, or Experiment action by a later objective's KPI, and do not carry an old objective forward as current truth.

If the action-time objective is missing or `Unknown`, do not infer it from later ACOS/TACOS, campaign name, spend, rank movement, or the current objective. Keep the historical decision context uncertain and lower confidence when that uncertainty is material.

## Measurement composition gate

When conversion evidence can mix directly measured and modeled conversions, compare baseline and post-change **measurement composition** before causal outcome classification. Use the persisted `measurement_composition` evidence when available. When two machine-readable measurement states exist, run `../../scripts/compare_measurement_composition.py <baseline.json> <post.json>` as the deterministic first-pass gate, then inspect:

- modeled-conversion inclusion state;
- whether a direct/modeled split is available;
- lower-grain **allocation coverage**;
- presence of `Unallocated` rows;
- allocation grain.

Interpret the comparator fail-closed: `Comparable` means only that the composition gate passes; all other measurement, control, realization and retail gates still apply. `Directional` means lower-grain split/allocation evidence drifted and affected causal conclusions must remain directional or `Inconclusive`. `Not Comparable` means modeled-inclusion semantics or allocation grain changed and the affected metric comparison must not support `Worked` / `Failed`. `Unknown` means required composition evidence is missing, invalid or explicitly unknown; it is not unchanged state.

If these dimensions differ materially, label **composition drift**. A disappearance, appearance, or material change in `Unallocated` coverage can move conversion credit between dimension rows without proving shopper-demand or action-effect change. Do not redistribute `Unallocated` conversions to targets, placements, queries, or other dimensions without supported allocation evidence.

When composition drift is material and unreconciled, do not classify the action as causally `Worked`, `Likely Worked`, `Likely Failed`, or `Failed` from the affected conversion/ROAS movement alone. Keep the outcome `Inconclusive` or otherwise directional/manual-review until comparable composition is restored, a parent-level metric avoids the allocation ambiguity, or a stronger counterfactual supports the conclusion.

When an `evaluated` or `corrected` structured optimization event is emitted after running the machine comparator, persist the returned `measurement_comparison` audit evidence: `comparator_id`, `classification`, `changed_fields`, `reasons`, `baseline_snapshot_id`, and `post_snapshot_id`. Preserve null snapshot IDs when the source evidence lacks them; do not invent identities. The raw baseline/post evidence snapshots remain authoritative.

Missing composition evidence is not evidence of direct-only measurement, zero modeled conversions, complete allocation, or unchanged composition.

## Required inputs

Gather what is available and label missing fields:

- original action/proposal and reason;
- entity type and stable entity ID when available;
- before value/state and intended after value/state;
- action timestamp plus marketplace/profile/timezone;
- validation metric(s), expected mechanism, validation window and rollback condition;
- action-time campaign objective, objective source/confidence, primary metric and guardrail metrics when recorded;
- current campaign objective when available, kept separate from the action-time objective;
- current trusted state or post-change export;
- comparable pre-change performance window;
- source/snapshot metadata when baseline and post windows differ in extraction, semantic version, completeness or backfill maturity;
- baseline/post measurement composition when conversion metrics may include modeled attribution, including modeled/direct split availability, allocation coverage, Unallocated-row presence and allocation grain;
- material control state/timestamps for baseline and post-change windows when causal attribution matters;
- realized surface/product/creative identity when the ad product can vary it during the evaluation window;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first** — verify whether the intended advertiser control is actually present.
2. Classify application as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. **Objective-lineage gate** — preserve the action-time campaign objective and compare it with the current campaign objective. If they differ, record objective drift; do not retroactively replace the historical success metric or guardrails with the current objective.
4. **Measurement gate** — require completed, attribution-mature, definitionally comparable windows; when history can restate, verify baseline/post backfill parity before outcome attribution. When modeled conversion or lower-grain allocation can matter, compare baseline/post measurement composition with `compare_measurement_composition.py` when machine-readable states exist. Treat `Directional`, `Not Comparable`, or `Unknown` as unresolved measurement comparability rather than action effect.
5. **Control-state comparability gate when causal attribution matters** — reconstruct material advertiser-control state across baseline and post-change windows. If overlapping changes can explain the effect, cap the single-control conclusion at `Directional` / `Confounded` / `Unknown` rather than calling the intended action causal.
6. **Realization gate when relevant** — verify whether platform-managed surface/product/creative realization stayed sufficiently comparable. A confirmed control readback does not prove stable realized ad identity.
7. Compare the post-change metrics to the best available baseline and to the expected mechanism.
8. Separate delivery effects from downstream conversion/profit effects.
9. Check retail, market, concurrent-control, platform-managed-realization and measurement confounders.
10. Classify the outcome using the detailed reference.
11. Recommend `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
12. Never execute rollback; any mutation remains external and explicitly authorized.

## Key rules

- `proposed != applied != readback confirmed != worked`.
- `measurement comparable != control-state comparable`; a clean metric series does not isolate the intended action when another material control changed.
- `readback confirmed != stable realized ad identity` when Amazon can dynamically select surfaces, products, creative/message, or another shopper-visible realization.
- `current campaign objective != action-time campaign objective` after objective drift; historical outcome review and future optimization intent are separate questions.
- Do not retroactively re-score a prior action under a later campaign objective or infer a missing action-time objective from current performance.
- Never call an action failed merely because early attributed orders have not matured.
- Never call an action worked when baseline and post windows use materially different semantic definitions, asymmetric backfill maturity, or material unresolved measurement composition / allocation coverage.
- Never treat disappearance of `Unallocated` rows as proof that a target/query/placement improved; lower-grain allocation movement is not shopper-demand evidence.
- If composition drift is material, cap affected causal outcome classification at `Inconclusive` / directional review until reconciled.
- Never call an action worked/failed causally when overlapping material control changes remain `Confounded` or `Unknown`.
- Do not optimize on ACOS/ROAS alone; evaluate the mechanism the action was supposed to change.
- Treat promotion, price, stock, Buy Box/Featured Offer, listing, demand and competitor shocks as alternative explanations.
- If multiple material advertiser or platform-managed changes overlap the entity/window, downgrade single-action causal claims.
- Missing control state or realized product/creative/surface fields from the active connector are not evidence of unchanged state, zero exposure, or unchanged realization.
- If a previous winner deteriorates after a change, check entity history before proposing another aggressive edit.

## Output

Return:

1. readback/application status;
2. action-time campaign objective, current campaign objective, and objective-drift status when available;
3. evaluation windows, attribution maturity, measurement comparability, and measurement-composition / allocation-coverage comparability when relevant;
4. control-state comparability when causal attribution matters;
5. realized-ad-identity comparability when relevant;
6. expected mechanism;
7. observed delivery, conversion, sales/profit and retail evidence;
8. confounders/concurrent changes;
9. outcome classification with confidence;
10. decision;
11. next check and evidence needed;
12. structured memory event when requested (`../../schemas/optimization-event.json`), preserving the decision-driving outcome metric semantics and per-metric evidence semantics when known rather than inferring them from display names; for `evaluated` / `corrected` events after composition comparison, also persist `measurement_comparison` with comparator identity, classification, changed fields, reasons, and baseline/post snapshot identities.

## Safety

Default mode is `Suggest`.

`Rollback Candidate` means evidence supports preparing a rollback proposal, not performing it. Any real account mutation requires explicit authorization plus an external Connector / Executor.
