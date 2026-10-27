---
name: post-change-review
description: Evaluate whether an Amazon Ads optimization change was actually applied and whether it worked. Use after bid, budget, placement, targeting, negative, structure or campaign changes to perform readback, compare expected vs observed outcomes, detect confounders, and decide monitor, validate, rollback or escalate. Default to Suggest/Shadow and never perform live mutations directly.
---

# Amazon Ads Post-change Review

## Non-rule event array completeness (v1.114.0)

The read-only comparator rejects unproven direct/deep routing arrays and nested audience-member arrays in positive mid-window SP `control_events` as `Unknown`, including empty lists. Flat audience and scalar routing changes remain compatible. An event cannot bypass endpoint collection completeness. This does not prove a complete event log or authorize Ads writes; default Read-only/Suggest/Shadow, external authorized Executor only.

## Optional nested rule-event JSON Pointer proof (v1.113.0)

For observed SP schedule/event/budget `control_events` containing nested rule-member arrays, the comparator accepts `rule_descendant_collection_evidence` only when both before/after maps exactly cover all state-relative RFC 6901 descendant list pointers, with independently Complete enumeration, Complete pagination and Supported capability. Also require valid paired outer `rule_collection_evidence`. Missing, extra, partial, malformed or one-sided proof is `Unknown`; legacy unproven nested arrays remain `Unknown`, and flat rule events retain prior behavior. This cannot establish authenticated complete event history or continuous execution. Default Read-only/Suggest/Shadow; external authorized Executor alone owns live Ads writes.

## Unproven nested rule collections in mid-window SP events (v1.112.0)

A positive Sponsored Products schedule/event/budget `control_events` transition cannot certify nested arrays inside rule members merely because its outer `schedule_rules`, `event_rules` or `active_budget_rules` list has a Complete declaration. Endpoint snapshots already require independent JSON-pointer evidence for nested arrays; the current event schema has no descendant-proof contract. Any descendant list (including an empty list) within an observed rule member returns `Unknown`, with or without optional outer proof. Flat scalar rule members, valid top-level empty collections and legacy non-nested events retain their existing classifications. This conservative repository-owned read-side rule does not authenticate Amazon Ads history or prove full-window coverage; only an authorized external Executor may write.

## Optional paired SP mid-window rule collection proof (v1.111.0)

For a positively observed Sponsored Products `control_events` schedule/event/budget-rule transition, `../../scripts/compare_control_state.py` accepts optional `rule_collection_evidence` only with both `before` and `after` maps. Each phase must independently declare Complete enumeration, Complete pagination and Supported capability for every relevant rule list; partial/truncated/one-sided/unmapped evidence returns `Unknown`, not a fabricated confounder. Legacy events without this optional proof remain compatible, **not** certified complete. This read-side metadata cannot authenticate source history or prove no other changes occurred; default Suggest/Shadow, external authorized Executor for all Ads writes.

## Unmapped Sponsored Products placement evidence (v1.110.0)

Before attributing a bid/budget result, use `../../scripts/compare_control_state.py` to reject extra unrecognized keys in the normalized Sponsored Products `placement_adjustment` state, both for endpoints and positive mid-window events. The three standard placement dimensions and optional Amazon Business modifier remain compatible; a new key requires verified adapter semantics, not a fabricated confounder. Return `Unknown` and retain missing/unsupported/partial as unknown, never zero. This does not prove full-window event completeness; Read-only/Suggest/Shadow default, live writes only through an external authorized Executor.

## Mid-window Sponsored Products rule activation parity (v1.109.0)

When positive `control_events` contain schedule/event bid-rule or active-budget rule transitions, use `../../scripts/compare_control_state.py` to reject one-sided optional `activation_status` or `activation_effective_at` for a shared `rule_id` as `Unknown`. Both-absent optional evidence and real status/time transitions remain compatible; a new rule ID does not imply a fabricated prior inactive state. Do not claim complete history or continuous execution from optional event rows. Read-only/Suggest/Shadow; live Ads writes belong to an authorized external Executor.

## Co-observed Sponsored Products routing/placement evidence (v1.108.0)

Use `../../scripts/compare_control_state.py` to reject contradictory `ACROSS_RETAILERS` routing and Amazon Business placement modifier states when both positive mid-window events are bound to the same concrete event readback. Evaluate before and after phases independently; an equal event timestamp without a shared readback is not proof of co-observation. Return `Unknown` rather than manufacturing a confounder; preserve valid Amazon Store combinations and absent event history as unresolved coverage. Remain Read-only/Suggest/Shadow; only an authorized external Executor may write to Ads.

## Intervening event observation collisions (v1.107.0)

Use `../../scripts/compare_control_state.py` to reject reused concrete event readback IDs at conflicting UTC instants and incompatible same-control transitions at the exact same instant as `Unknown`. Multiple controls can legitimately share one readback/time; identical duplicate transitions and omitted optional event readback IDs remain compatible. Do not infer a contiguous event chain or full-window completeness from optional `control_events`. Remain Read-only/Suggest/Shadow; live Ads mutations belong to an external authorized Executor.

## Nested null material-state evidence (v1.106.0)

Use `../../scripts/compare_control_state.py` to reject explicit JSON null in any nested observed material-control state, including positive intervening events. Such unknown evidence cannot establish a stable competing control, isolated treatment or genuine confounder. Keep real zero/false and absent optional fields distinct; null metadata outside `state` remains optional. Read-only/Suggest/Shadow; no full-window coverage or live Ads write authority.

## Intervening SP optional budget evidence parity (v1.105.0)

For observed post-owned `control_events` on SP bid/budget causal reviews, use `../../scripts/compare_control_state.py` to reject a one-sided optional base/effective daily budget or average-daily-budget policy as `Unknown`. Both-absent optional bid-surface evidence stays compatible; a real Amazon Business placement addition remains a competing observed transition. Do not equate omitted fields with zero or claim full-window event coverage. Read-only/Suggest/Shadow; external authorized Executor for writes.

## Intervening Sponsored Products budget and routing state integrity (v1.104.0)

For optional post-owned `control_events` on SP bid/budget causal reviews, use `../../scripts/compare_control_state.py` to reject invalid explicit budget amounts/policy and unmapped or contradictory site/retailer routing. A budget-change event requires base/effective daily budgets, active rules and policy; bid-change events preserve partial budget-shape compatibility but cannot accept invalid supplied values. One-sided retailer scope is not a verified routing transition. Return `Unknown` rather than manufacturing a confounder or isolated treatment. These are repository-normalized read-side labels, not universal Amazon API enums or a complete history certificate. No live Ads writes.

## Intervening Sponsored Products event value integrity (v1.103.0)

When using optional post-owned `control_events` for a Sponsored Products bid/budget causal review, apply `../../scripts/compare_control_state.py` before classifying a confounder. A claimed observed transition with an invalid base/video bid, incomplete or nonnumeric placement, unusable audience member, or unsupported bidding-strategy state is `Unknown`, not an observed competing change. Valid positive observed transitions remain usable. This is a read-only normalized evidence guard; missing events do not become zero, event capture is not certified exhaustive, and only an external authorized Executor may write to Ads.

## Intervening material-control event evidence (v1.102.0)

When the connector exposes observed mid-window campaign control transitions, attach source/scope/time-bound `control_events` to the post snapshot before calling `../../scripts/compare_control_state.py`. A schedule/event/budget/placement change can confound a bid test even if it reverted and both endpoint readbacks match. Malformed or unverified event evidence is `Unknown`, not zero or unchanged; a competing observed event is `Confounded`. Omitted/empty event lists are **not** continuous-history proof. Keep causal confounders and incremental economics separate; external authorized Executor owns all writes.


## Material-control N/A evidence (v1.101.0)

Before causal isolation, use `../../scripts/compare_control_state.py` to reject whole-label `N/A` / `Not Applicable` in material control state, nested values, Sponsored Products schedule/event/budget rule IDs and audience IDs. A Complete inventory and `observed` status cannot turn a placeholder into a known stable competing control; return `Unknown`. Concrete opaque IDs containing these substrings, observed zero/false and real confounders remain valid. This is not continuous rule-history authentication or live Ads write authority.


## Reused readback transition provenance (v1.100.0)

Run `../../scripts/compare_control_state.py` before causal review. A reused concrete `source.readback_id` must not carry contradictory per-control `transition_provenance` (management mode, actor, actor-evidence status, reason, or transition-observed instant). One-sided provenance is unresolved. Compare supplied known-offset RFC3339 instants in exact UTC time, including nanoseconds. Return `Unknown`, not `Comparable`. Distinct readbacks, both-absent/null legacy provenance and offset-equivalent times remain compatible. This read-only consistency gate does not prove external actor identity, full-window rule execution, or authorize Ads writes.



## Scope/source placeholder safety (v1.99.0)

Before claiming `Comparable` or `Treatment Isolated`, run the read-only control-state comparator on concrete source and decision-scope identities. Repeated `N/A` / `Not Applicable` labels in marketplace, account, campaign, entity, source system, acquisition channel or connector fields are unresolved, even when both snapshots match; they return `Unknown`. Valid opaque IDs containing these words are not placeholders. This does not prove continuous rule execution or permit live Amazon Ads writes.

## Readback control-evidence consistency (v1.98.0)

For post-change readback, the same concrete `source.readback_id` cannot justify different per-control `effective_at` or `evidence_status`, even if observed time and control state match. Use the read-only `scripts/compare_control_state.py` gate; contradictions return `Unknown`. Equivalent UTC instants, distinct IDs and legacy optional omissions remain compatible. This does not prove continuous control execution, authenticate source payloads or authorize Ads writes.

Use this Skill after a proposed or externally executed optimization action. It closes the loop between `action -> observe -> evaluate -> rollback/keep`.

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, resolve the selected decision profile with `../../scripts/resolve_skill_capabilities.py`, pass both its `required_capabilities` and any returned `data_requirements` into `../../scripts/evaluate_connector_capability_gate.py`, and run the gate **before metric interpretation**. For the `outcome-review` profile, live performance evidence requires historical campaign performance rather than history metadata alone. When the pre/post windows and grain are known, pass them to the resolver through `task_data_requirements.campaign-performance-read.history_window`; use the resolver's merged `data_requirements` as the gate input so the task cannot accidentally drop the profile-owned historical-data requirement. When causal attribution uses a registered control-state decision surface such as `sponsored_products_bid_change` or `sponsored_products_budget_change`, also pass that exact `decision_surface` to the resolver. The resolver derives the registry-required control types onto `entity-state-readback`; the connector gate must prove `control_types_exposed` covers every required type before high-confidence causal review can proceed. Overall history availability cannot stand in for exact range coverage, and generic readback support cannot stand in for exact material-control observability. When a causal claim depends on **who changed a control**, add `task_data_requirements.entity-state-readback.required_transition_provenance_fields` (at minimum `management_mode`, `last_transition_actor`, `actor_evidence_status`) to the resolver, then pass the merged requirements unchanged to the gate. For a reason-dependent claim additionally require `transition_reason`. `entity-state-readback Supported` alone does not prove change actor/history access. Connector preflight is necessary but not sufficient: still verify source-supported event-time actor evidence and historical coverage before attributing authorship.

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
- overlapping advertiser-control history and causal isolation: `../../references/control-state-comparability.md`; an explicit non-null `source.readback_id` must be concrete and unpadded; the same ID cannot prove different material states **or different exact UTC observation instants**. Treat invalid/reused provenance as `Unknown`, not independent causal evidence;
- prior optimization state/history conflicts: `../../references/optimization-memory.md`;
- For all Global SP campaign, ad-group and target readback, use only marketplace country codes currently supported by the dated official Global SP API guide (`GB`, not `UK`); unsupported/new codes remain `Unknown` until officially verified. Raw marketplace IDs are not country codes.
- Global Sponsored Products 207 campaign-update receipts and marketplace configured-state readback: `../../references/global-sp-readback-evidence.md`. When both native campaign configuration and a paginated query trace are supplied, require explicit source/time/filter binding to one query page; unbound native evidence is `Unknown`, never `Confirmed`. For a monetary-budget change, an explicitly retained native campaign `budgets` array must also agree with normalized native-currency budget rows; contradictory source evidence is `Unknown`.
- When a Global SP campaign pagination trace explicitly retains query page response bodies, require all page responses and exact one-page membership of the native campaign under the bound provenance index; missing or contradictory page evidence is `Unknown`, not an applied update. This does not independently authenticate HTTP.
- When a Global SP campaign pagination trace explicitly includes native query filters or page request bodies, use the request-binding contract in `../../references/global-sp-readback-evidence.md`; reject filter/continuation contradictions as `Unknown`, even when an opaque query fingerprint agrees. The adapter still authenticates raw HTTP evidence externally.
- Independent Global Sponsored Products **ad-group default-bid** 207 receipts and native-currency marketplace bid query evidence: `../../references/global-sp-adgroup-bid-readback.md`.
- Homogeneous Global SP multi-ad-group 207 default-bid updates with complete indexed receipts and independent native-currency marketplace query readback: `../../references/global-sp-adgroup-batch-readback.md`. Never interpret partial batch success as a blanket confirmation.
- Independent Global Sponsored Products **positive single-marketplace target bid** 207 receipts and target-specific native-currency query evidence: `../../references/global-sp-target-bid-readback.md`.
- Mixed-resource Global SP plans spanning campaign, ad-group and target changes: `../../references/global-sp-mixed-plan-readback.md`. Require an externally authenticated, complete plan manifest and independent per-component readback before calling the whole plan `Confirmed`; a local resource success is not an overall plan outcome.
- Homogeneous multi-target Global SP HTTP 207 updates with index-bound per-target query readbacks: `../../references/global-sp-target-batch-readback.md`. Only use this read-only batch gate when the trusted adapter can prove the ordered request list and complete indexed receipt; do not promote any partial/unknown item to batch Confirmed.
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
- when an outcome metric contains modeled/projected future value (for example Long-Term Sales), its `evidence_type`, estimate horizon, `estimate_as_of`, model identity/version when exposed, and a separate realized-outcome `realized_through` / maturity state when available;
- baseline/post measurement composition when conversion metrics may include modeled attribution, including modeled/direct split availability, allocation coverage, Unallocated-row presence and allocation grain;
- material control state/timestamps for baseline and post-change windows when causal attribution matters;
- realized surface/product/creative identity when the ad product can vary it during the evaluation window;
- promotions, price, inventory, Featured Offer/Buy Box, listing and competitor context that could confound the result.

## Workflow

1. **Readback first** — verify whether the intended advertiser control is actually present. For Global SP campaign updates, a 207 receipt alone is insufficient: when a trusted normalized single-item receipt and complete query readback are available, use `../../scripts/evaluate_global_sp_readback.py`; otherwise preserve Partial/Unknown rather than claiming application. If the intended update included a marketplace monetary budget, pass the optional `expected_marketplace_budgets` with complete independently evidenced per-marketplace budget/currency readback; **never omit budget expectations to obtain a state-only `Confirmed`**. The helper only supports daily monetary budgets and never performs FX conversion or verifies delivery. For a separately executed Global SP **ad-group default-bid** update, use `../../scripts/evaluate_global_sp_adgroup_bid_readback.py` with an ad-group-bound 207 receipt and complete per-marketplace query readback; do not reuse a campaign receipt, infer target bids, or combine independent resource confirmations into a blanket multi-resource success. For a separately executed positive Global SP **KEYWORD/PRODUCT target** bid update, use `../../scripts/evaluate_global_sp_target_bid_readback.py` with the exact target ID and one-marketplace query evidence; an ad-group default-bid readback never confirms a target bid.
2. Classify application as `Confirmed`, `Partial`, `Not Applied`, `Drifted`, or `Unknown`.
3. **Objective-lineage gate** — preserve the action-time campaign objective and compare it with the current campaign objective. If they differ, record objective drift; do not retroactively replace the historical success metric or guardrails with the current objective.
4. **Measurement gate** — require completed, attribution-mature, definitionally comparable windows; when history can restate, verify baseline/post backfill parity before outcome attribution. Keep modeled/projected future-value evidence separate from realized outcomes: a Long-Term Sales estimate may support directional learning, but it is not sales already realized through the review date. If the realized/Accumulated Sales counterpart is immature, unavailable, unsupported, or unknown, preserve that state rather than imputing zero or promoting the action to `Worked` from the estimate alone. When modeled conversion or lower-grain allocation can matter, compare baseline/post measurement composition with `compare_measurement_composition.py` when machine-readable states exist. Treat `Directional`, `Not Comparable`, or `Unknown` as unresolved measurement comparability rather than action effect.
5. **Control-state comparability gate when causal attribution matters** — reconstruct material advertiser-control state across baseline and post-change windows. If overlapping changes can explain the effect, cap the single-control conclusion at `Directional` / `Confounded` / `Unknown` rather than calling the intended action causal.
6. **Mutation-provenance gate when platform-managed state changes are possible** — keep the observed control state separate from who caused its latest transition. A complete local/external Executor ledger proves only that Executor's history. If platform-management mode, transition actor, or transition reason is unavailable/unsupported/unknown, do not attribute the state change to the advertiser or Executor; cap authorship-dependent causal claims at directional/manual review until source-supported provenance or change history resolves it.
7. **Realization gate when relevant** — verify whether platform-managed surface/product/creative realization stayed sufficiently comparable. A confirmed control readback does not prove stable realized ad identity.
8. Compare the post-change metrics to the best available baseline and to the expected mechanism.
9. Separate delivery effects from downstream conversion/profit effects.
10. Check retail, market, concurrent-control, platform-managed-realization and measurement confounders.
11. Classify the outcome using the detailed reference.
12. Recommend `Keep`, `Keep Monitoring`, `Rollback Candidate`, `Follow-up Experiment`, `Fix Application`, or `Manual Review`.
13. Never execute rollback; any mutation remains external and explicitly authorized.

## Key rules

- `proposed != applied != readback confirmed != worked`.
- `measurement comparable != control-state comparable`; a clean metric series does not isolate the intended action when another material control changed.
- `current control state != transition provenance`; observing a state change does not identify whether the advertiser, an external Executor, Amazon automation, or another authorized actor caused it.
- `readback confirmed != stable realized ad identity` when Amazon can dynamically select surfaces, products, creative/message, or another shopper-visible realization.
- `current campaign objective != action-time campaign objective` after objective drift; historical outcome review and future optimization intent are separate questions.
- Do not retroactively re-score a prior action under a later campaign objective or infer a missing action-time objective from current performance.
- Never call an action failed merely because early attributed orders have not matured.
- Never treat modeled/projected long-horizon sales as already-realized sales. Do not splice Long-Term Sales estimates and realized/Accumulated Sales into one continuous metric series unless the source contract explicitly establishes comparable semantics.
- A high modeled long-term estimate alone does not justify `Worked` / `Likely Worked` or another scale-up. Until realized evidence is sufficiently mature and comparable, keep the conclusion directional, hold, or manual-review as appropriate.
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

## Observed SP rule-event extra direct arrays (v1.115.0)

For mid-window Sponsored Products schedule/event/budget rule `control_events`, the paired `rule_collection_evidence` only proves the registered rule-list fields. Any additional direct array on either event side (even empty or unchanged) is unproven and the comparator returns `Unknown`. Do not interpret that result as zero, an isolated treatment or a verified competing control. Valid flat/scalar evidence stays compatible; source authenticity and full-window coverage remain separate. This is read-only; external authorized Executor owns all live changes.
