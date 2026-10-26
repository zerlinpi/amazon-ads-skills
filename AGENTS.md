# AGENTS.md

## Repository purpose

This repository contains reusable Amazon Ads Agent Skills. The canonical business logic lives under `skills/<skill-name>/SKILL.md` and must remain portable across Codex, Claude Code, WorkBuddy, and other Agent Skills-compatible runtimes.

## First-run / installation guidance

For a fresh runtime, repository URL, or manual checkout, read `docs/GETTING-STARTED.md` before inventing runtime-specific install paths. The stable default is repository-workspace mode: clone the whole repository, open the repository root, keep `AGENTS.md` plus the canonical `skills/` tree and shared references together, then progressively load only the Skill needed for the task.

A runtime manifest or cloned directory is not proof that Skill discovery succeeded. Verify a fresh setup with the bootstrap/smoke-test prompts in `docs/GETTING-STARTED.md`. If automatic discovery fails, explicitly load the matching `skills/<name>/SKILL.md`; for cross-domain work use `skills/amazon-ads-optimizer/SKILL.md`.

## Skill discovery

- Treat every `skills/*/SKILL.md` as an independently invocable skill.
- Read only the matching skill first; load shared files from `references/`, `playbooks/` and `schemas/` only when needed.
- For a custom host without native Skill discovery, use `scripts/resolve_skill_context.py`: expose only the metadata catalog at discovery time, preload exactly one selected `SKILL.md`, and treat returned resources as on-demand pointers. Do not preload all Skill bodies, `docs/research/`, or `evals/` merely because they exist.
- For cross-domain requests, use `skills/amazon-ads-optimizer/SKILL.md` as the orchestrator.
- For recurring weekly/Monday account reviews, start with `playbooks/weekly-review.md`, then load only specialist Skills required by material findings.
- When the task asks whether a previous optimization worked, route to `skills/post-change-review/SKILL.md` before proposing another edit on the same entity.
- When prior actions may overlap a new decision, load `references/optimization-memory.md` and retrieve only the bounded relevant entity history.
- When compared windows come from different APIs, MCPs, exports, warehouses or semantic/report versions, load `references/data-lineage.md` before making high-confidence trend or causal claims.
- When a decision depends on what the active MCP/connector can actually expose for the required profile, report, metric, dimension, history, pagination, freshness or semantic identity, load `references/connector-capability.md`; treat `Partial`, `Unsupported` and `Unknown` as acquisition-path evidence states, never as metric zero.
- Resolve decision-required connector capability IDs from `references/connector-capability-catalog.json` via `scripts/resolve_skill_capabilities.py`; do not invent new capability IDs ad hoc. When a causal review uses a registered `decision_surface`, pass that surface to the resolver so its versioned material-control set is attached to `entity-state-readback`; generic readback support must not substitute for exact `control_types_exposed` coverage. When a machine-readable connector capability snapshot is available, feed the resolved required IDs and merged data requirements into `scripts/evaluate_connector_capability_gate.py` before metric interpretation; `Degraded`/`Blocked` must cap the dependent decision to conservative classes instead of preserving high confidence.
- When a bid, budget, placement or other monetary-control Skill must turn a direction/raw estimate into a concrete magnitude, load `references/action-sizing.md`; do not invent a repository-global change percentage or damping constant.
- When a recommendation depends on a time-varying platform capability, exact platform limit, control eligibility, or console/API availability, load `references/platform-capability-lineage.md` and reconcile source date + capability scope before using the fact as action-safe.
- Historical replay fixtures under `evals/` are test inputs, not reusable operating instructions; do not load them during ordinary account analysis unless explicitly running an eval.
- Do not duplicate business logic into this file.

## Default operating mode

Default to `Suggest` mode. Analysis may propose actions, but no skill or playbook in this repository directly modifies a live Amazon Ads account.

Modes:
1. `Read-only` — inspect and explain data.
2. `Suggest` — generate recommended actions without applying them. **Default.**
3. `Shadow` — simulate actions for review/backtesting.
4. `Execute` — only after explicit authorization; hand validated actions to an external connector/executor.

## Safety rules

- For registered Sponsored Products bid/budget causal comparisons, complete, identity-verified `schedule_rules`, `event_rules`, and `active_budget_rules` are **sets keyed by unique concrete `rule_id`**, not ordered histories. The comparator may ignore member enumeration order only for these three validated collections when comparing control state; it must still detect changed member fields, additions/removals, activation changes, invalid/duplicate/one-sided evidence, and changes in other material arrays. Equal rule sets do **not** prove continuous execution, full-window trigger coverage, eligibility, raw source authenticity or causal lift. No Ads write authority is added.

- Feature-specific eligibility source independence covers capability-level `evidence[].reference` as well as binding IDs, surface IDs and binding-level probe references across **all** observed connector capabilities (including non-required/Unsupported). Reusing any of these normalized probe references cannot prove Eligible or Ineligible and degrades to Unknown. A distinct label is not external response authentication, advertiser entitlement, causality or write authority; 15 Skills and external Executor boundaries remain unchanged.

- Feature eligibility source independence applies across **all** observed connector capabilities in the same snapshot, not only the current decision's required IDs. A feature-specific `source_reference` colliding with any binding ID, surface ID or supporting probe reference (including unrequired, Unverified or Unsupported capability probes) cannot prove either Eligible or Ineligible; degrade to Unknown. Required-capability access checks remain unchanged. Different references are only a narrow consistency check, not raw HTTP authentication, entitlement verification or write authority.

- Feature eligibility source-reference independence must compare against **all** bindings on each required connector capability, including Unverified/Unknown/Unsupported probes, not only Verified read-side bindings. A reused binding ID, surface ID or supporting evidence reference is not independent entitlement proof even when another binding legitimately verifies connector access. Both Eligible and Ineligible self-references degrade to Unknown; distinct references remain only a narrow consistency check, not raw Amazon API authentication. This adds no write authority.

- For registered Sponsored Products bid/budget causal comparisons, both control-state snapshots must carry a concrete `scope.campaign_id` in addition to existing marketplace and account identity evidence. Two omitted/null campaign IDs cannot establish the same campaign, even if the profile and all observed controls match; classify as `Unknown`, not `Treatment Isolated` or `Comparable`. Other registered surfaces retain their existing scope contract. This is a read-only identity guard, not an Amazon-native schema, eligibility proof, continuous-rule-history proof or write permission.

- Feature-specific eligibility is not independently evidenced when its `source_reference` exactly repeats a Verified required connector binding's `binding_id`, `surface_id`, or supporting `evidence.reference`. This self-reference yields `feature_source_independence_effect=unknown` and degrades the feature decision (including a self-referential Ineligible claim); unrelated capability references are not compared. A distinct label only passes this narrow consistency check and never authenticates raw Amazon Ads HTTP, proves feature enrollment or grants write authority. Keep 15 Skills and external Executor boundary intact.

- When a named feature eligibility decision declares `as_of`, a connector capability snapshot captured **after** that decision instant cannot prove read-side coverage as of the earlier time. Missing/invalid/unknown-offset capture is also Unknown: `feature_snapshot_chronology_effect=unknown` degrades the final gate unless another independent block applies. Equal/earlier capture only passes chronology, not entitlement, freshness, or source authenticity. Do not reuse the eligibility evidence TTL as a connector TTL; explicit connector freshness and supporting binding timestamps remain independent. Calls without a feature requirement remain compatible. No Amazon Ads writes are authorized.

- Connector capability and exact advertiser/campaign scope do not establish feature enrollment. For a decision requiring a named feature, provide a concrete `feature_eligibility_requirement` matching the exact `expected_scope` advertiser/campaign/marketplace and a separately supplied feature-specific Verified eligibility record with concrete source/reference and valid observation time. Verified Eligible can pass the eligibility subgate only alongside all connector checks; Verified Ineligible blocks; missing, partial, unknown, stale, future, generic product-group, unverified or mismatched records degrade. Never equate Amazon Ads advertiser product-group eligibility with Amazon Business exclusive campaign enrollment, infer absent metrics as zero, or treat a normalized Verified label as authenticated raw API proof. No live Ads writes or external Executor behavior is introduced.


- An explicitly observed connector `access_mode=observe` may pass only when the required capability is declared `observe` by the canonical catalog and an independently Verified binding, concrete source/scope and all other data/freshness gates pass. Observation-only access cannot substantiate `read`/`report` capabilities or grant Amazon Ads write authority. Write-only stays Blocked; mixed/unknown stay Degraded. This is a repository-owned read-side evidence contract, not Amazon-native permission or proof of metric completeness.

- When a decision depends on an exact advertiser account or campaign, set `expected_scope.advertiser_account_id` and/or `campaign_id` and require a concrete matching `scope.advertiser_account_ids` / `campaign_ids` on both the capability and an independently Verified binding. These opaque IDs compare case-sensitively; same marketplace/ad product does not prove same account/campaign. Missing scope never implies global coverage; Unknown/Partial membership is not zero or verified exclusion. Legacy requests without exact identity scope remain compatible. This is read-side provenance only, not advertiser/campaign feature eligibility, raw HTTP authentication, live delivery or write authority.

- For Global Sponsored Products campaign readback, an echoed placeholder or whitespace-padded global-account, campaign, explicit request, connector-source, or raw marketplace crosswalk identity cannot establish a verified post-write match. Return `Unknown`, not `Confirmed`, even when the request, 207 receipt, state and budget rows repeat the same unavailable label. Whole-label Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported are unusable; legitimate IDs containing those substrings remain valid. Legacy country-code-only and index-only receipts remain compatible. This is repository-owned evidence validation, not an Amazon-native ID grammar, proof of marketplace/advertiser eligibility, raw HTTP authentication or permission to execute.


- A reporting generation declared `active` or `sunset_scheduled` with a `sunset_at` earlier than the same connector snapshot's `captured_at` has unreconciled lifecycle evidence. When that generation is required, return `data_contract_effect=unknown` / `Degraded`, not high-confidence `Pass`. This does **not** assert that the report was retired, that Amazon's planned dates cannot change, or that unavailable metrics are zero. Future/equal sunsets, explicit retired blocking, and no-generation requirements retain their existing behavior. All dates are compared as offset-aware instants; actual Ads writes remain outside this repository.

- For an exact history-window requirement, an observed per-grain `available_through` more than one calendar day beyond the connector snapshot capture cannot prove already available history. Degrade to Unknown rather than high-confidence Pass, even if requested dates precede capture. The one-day allowance is only for date-only bounds without marketplace timezone, not an Amazon latency SLA or proof of data maturity. Never infer zero or authorize live Ads writes.

- A requested historical reporting `history_window.grain` must be concrete and unpadded; matching Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported labels do not prove historical availability. A padded connector-observed matching grain, including alongside a concrete match, is ambiguous and degrades rather than passing. Preserve valid case-insensitive grains and verified dates; do not infer metric zero, per-metric history, API entitlement or write authorization.


- A reporting-generation requirement must name a concrete, non-placeholder, unpadded identity. Repeating `Unknown` or `Unsupported` on both sides is not verified reporting-generation comparability. A connector-observed generation that is missing, placeholder, or whitespace-padded degrades to Unknown rather than asserting a real generation mismatch or matching it. Valid concrete generations still match case-insensitively; a concrete mismatch blocks. This is a repository-owned read-side provenance rule, not an Amazon API enum, permission to write, or proof of source authenticity.

- An observed, nonempty connector scope list with unmatched Unknown/Partial/malformed members yields `scope_effect=unknown` and a **Degraded**, not `Blocked`, final capability gate: unknown membership cannot prove exclusion. An omitted/empty/unbounded capability scope remains **Blocked** (no global assumption); a fully concrete unmatched scope also remains **Blocked**. A concrete match can pass the scope preflight subject to verified binding and all other gates. Do not infer marketplace/advertiser/campaign eligibility, actual delivery or write authorization from this distinction.


- A requested connector decision scope must be a concrete identity, not a repeated Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported label or whitespace-padded string. For a capability or verified binding scope, a matching concrete member proves only that bounded connector surface; an unmatched list containing an unavailable/malformed member is Unknown, not proof of marketplace, ad-product, region or account-type exclusion. A fully concrete unmatched list remains blocked. No scope list alone establishes Amazon Business advertiser/campaign eligibility, account entitlement, actual delivery, or authority to write.

- A `Supported`/`Verified` read capability must also have a concrete snapshot-level `connector_id`. A missing, blank, placeholder (`Unknown`/`Unsupported`/`Partial`/`Missing`/`Unavailable`/`Not Available`/`Not Supported`) or whitespace-padded connector identity degrades the entire decision, even with multiple valid bindings. Optional `source_system` and `acquisition_channel` may be omitted for legacy snapshots, but when explicitly provided they must be concrete identities, not null/placeholder/whitespace-padded values. This is a repository-owned read-side provenance check, not authentication of remote API responses, proof of account eligibility, or permission to write.

- A `Supported` connector capability with a `Verified` binding still needs a concrete read-side `access_mode`. A `write`-only capability is `Blocked`; `mixed`, `unknown`, missing, malformed or unsupported modes are `Degraded`. Only explicit `read`, `report`, `export` or `stream` access can pass the access-mode preflight, subject to other evidence gates. A second binding or snapshot default mode cannot override write-only access. This repository-owned read-side check does not authenticate remote tool behavior, grant write permission, or replace an authorized external Executor.

- A `Verified` connector binding is not independently identified by an unavailable placeholder in its binding ID, surface ID or supporting evidence kind/reference. Reject whole-label Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported and whitespace-padded verification identifiers before high-confidence Pass. A separate valid binding can still qualify; this does not authenticate remote responses, establish advertiser eligibility, or grant write authority.

- A connector capability marked Supported and a binding marked Verified do not override impossible chronology. Independently validate snapshot capture, binding verification, and explicitly dated supporting evidence even when no freshness horizon was requested. A future/malformed/unknown-offset binding or evidence timestamp is not a verified surface and must not produce high-confidence Pass. This read-side rule does not authenticate raw HTTP, confer platform entitlement, or authorize writes.

- Never invent missing advertising data, source lineage, optimization history, or action-sizing precision.
- Repeated `Unknown`/`Unsupported`/`Partial`/`Missing`/`Unavailable`/`Not Available`/`Not Supported`, blank or whitespace-padded labels are not valid marketplace, profile, campaign, entity, advertiser-account, connector, source-system or acquisition-channel identities. Reject before claiming causal isolation; do not equate a shared placeholder with a shared account or data lineage. Real observed IDs and both-absent legacy optional connector IDs remain supported. This is read-side validation, not an Amazon-native ID format or account-entitlement check.
- For every material control, even a non-registry extra control, an explicitly observed state containing an exact missing/unknown/unsupported/partial/unavailable placeholder, a blank scalar string, or a non-finite numeric leaf cannot prove stability or treatment isolation. Reject such evidence recursively without turning it into zero, False or an absent control. Valid observed zero, boolean switches, descriptive values and verified complete collections remain usable; this is a repository-owned read-side check, not an Amazon API enum or a substitute for control-specific capability and eligibility proof.
- Do not recommend aggressive bid/budget changes when sample size is insufficient.
- A raw economic or directional estimate is not automatically an action-safe final magnitude; require an explicit account/caller policy, calibrated response, defensible marginal headroom, experiment design, or another auditable sizing basis for a concrete proposed value.
- Check marketplace, profile/account scope, currency, timezone, attribution window, date range, promotion context, data freshness and source comparability before high-confidence recommendations.
- Treat `extracted_at` and `available_through` as different concepts; a freshly fetched downstream table may still be incomplete for recent event dates.
- For registered Sponsored Products bid/budget causal comparisons, `bidding_strategy` must use a recognized source-supported normalized strategy. Simple `dynamic_down_only`, `dynamic_up_and_down` and `fixed` string labels (hyphen variants allowed) are supported. Rule-based bidding requires a structured state `{ "strategy": "rule_based", "roas_guardrail": 3 }` with a finite, strictly positive observed ROAS ratio; a bare `rule_based` label, unknown guardrail or unverified extra rule fields cannot prove treatment isolation. This rule-based ROAS guardrail is distinct from schedule/event bid-rule lists. These are repository-owned read-side labels, not Amazon-native API enums or proof of activation, eligibility or actual auction bids.
- For registered Sponsored Products bid/budget causal comparisons, a complete `audience_bid_adjustment` list must contain unique nonblank `audience_id` identities and finite nonnegative `bid_boost` values. Missing, duplicate, malformed, unknown or unsupported members cannot prove treatment isolation. This is a repository-normalized read-side contract, not an Amazon API payload.
- For registered Sponsored Products bid/budget causal comparisons, `base_bid` must be an observed finite nonnegative numeric value or plain decimal string; Unknown/Unsupported/Partial, booleans, negative/non-finite values, percentages and structured placeholders are not valid bid evidence. This is not a universal platform bid-minimum/maximum claim.
- For Sponsored Products bid/budget causal comparisons, `video_bid_adjustment` must be a source-supported finite nonnegative numeric observation (or plain decimal string), not Unknown/Unsupported/Partial, a boolean, a percent string, or a non-finite value. The comparator does not establish marketplace eligibility or an exact platform upper bound.
- For Sponsored Products causal comparisons, an explicitly supplied Amazon Business placement bid modifier is a distinct material placement value. Reject invalid/unknown/unsupported values and one-sided missing evidence; both-absent legacy snapshots do not prove B2B capability, ineligibility or zero. Verify account/marketplace/retailer scope independently before action-safe B2B conclusions.
- For registered Sponsored Products bid/budget causal comparisons, optional normalized `targeting_or_routing.state.retailer_scope` accepts only `AMAZON_STORE` or `ACROSS_RETAILERS` and must be present on both snapshots or neither. Across-retailers scope contradicts an explicitly supplied Amazon Business placement modifier (even numeric zero) or `AMAZON_BUSINESS`-exclusive site routing; return `Unknown`, not a stable/zero B2B control. Both-absent legacy scope remains compatible but does not prove retailer, marketplace, campaign or connector eligibility. These are repository-owned read-side labels, not Amazon-native API enums or verified delivery.
- For registered Sponsored Products bid/budget causal comparisons, `targeting_or_routing.state.site_restriction` must be a source-supported recognized normalized routing label (`ALL_ELIGIBLE` or `AMAZON_BUSINESS`). Missing, unknown, unsupported, partial, malformed or unmapped site restrictions cannot prove stable delivery even when repeated in both snapshots. These repository-owned labels do not prove account/marketplace eligibility, connector completeness or Amazon-native enum equivalence; new modes require explicit adapter mapping and dated capability verification.
- For Global SP readback, accept only country codes explicitly supported by the current dated Amazon Global Sponsored Products guide. An unsupported/new code is `Unknown` until official eligibility is reverified; do not silently substitute `UK` for `GB` or a raw marketplace ID for a country code.
- When Global SP query page response bodies are explicitly retained, require complete per-page `campaigns[]` and `nextToken` evidence and exact one-page native campaign membership; contradictory or partial response evidence is `Unknown`. Legacy traces without response bodies are not independently authenticated.
- For optional Global SP native query-request evidence, validate exact campaign/product/scope filters and per-page continuation requests against the pagination trace; an echoed query fingerprint is not independent authentication. Incomplete or contradictory explicit request evidence is `Unknown`, never an inferred empty/zero result.
- Treat a time-varying platform capability as lineage-bearing evidence: if current official/API/account evidence materially conflicts or scope/supersession is unresolved, fail closed on the exact numeric rule instead of silently choosing a convenient percentage, limit or formula.
- Treat Prime Day, Best Deal, Lightning Deal, Coupon, Prime-exclusive promotions, stockouts, listing suppression, major price changes, and parent/variation-family retail changes as potential confounders.
- Before reversing or stacking another action on the same entity, check whether a recent action is still inside its validation window when history is available.
- Distinguish `proposed`, `applied`, `readback confirmed`, and `worked`; none of these imply the next stage automatically.
- If history is unavailable or partial, expose that limitation instead of treating the ledger as complete.
- Prefer `Hold`, `Experiment Only`, or `Manual Review` when application is unknown/drifted, evaluation is still pending, source comparability is unresolved, action magnitude lacks a defensible sizing basis, or a new action would contaminate an active experiment unless a safety guardrail triggered.
- Weekly reviews must include a hold list; do not force every material entity into an action.
- Do not place credentials, refresh tokens, client secrets, profile IDs, account IDs, or customer secrets in generated files or logs.
- Any `Execute` plan must include evidence, confidence, guardrails, validation window, and rollback criteria.
- A `Rollback Candidate` is a proposal only; this repository does not perform the rollback itself.

- For registered Sponsored Products bid/budget causal comparisons, a Complete schedule/event bid-rule or active budget-rule collection must also have usable member evidence: unique nonblank normalized `rule_id` and finite nonnegative observed `bid_increase` (schedule/event) or `increase_percent` (active budget). Missing, duplicate, unknown, unsupported, boolean, negative and non-finite member values are `Unknown`, not zero or unchanged. This is a read-side evidence contract, not an Amazon API payload, activation proof or bid-composition formula.

- For registered Sponsored Products bid/budget causal comparisons, an optional normalized schedule/event/active-budget rule member `activation_status` is accepted only as `active`, `inactive`, or `scheduled`; repeated Unknown/Unsupported, malformed or one-sided activation status on a shared `rule_id` is `Unknown`, not an unchanged control. Absence on both legacy snapshots remains backward-compatible but does not prove activation or continuous rule execution. This field is repository-owned read-side evidence, not an Amazon-native enum or a substitute for time-window proof.
- For the same SP rule members, an explicitly supplied optional `activation_effective_at` must be a timezone-aware RFC3339 transition instant no later than its snapshot's `observed_at`, paired with an explicit valid `activation_status`, and present on both snapshots for the same `rule_id`. Invalid, future, status-less or one-sided transition-time evidence is `Unknown`. A changed valid transition time is a competing control. Both-absent legacy evidence is accepted without claiming full-window execution, event-trigger or timezone coverage.

- Connector freshness requirements must use finite non-negative `max_age_seconds`; NaN, infinity or overflowing numeric horizons are invalid and must never bypass stale-evidence checks. This is an internal read-side invariant, not an Amazon Ads API TTL or permission to execute writes.

## Shared references, playbooks and evals

- Weekly operating cadence: `playbooks/weekly-review.md`
- Metrics: `references/amazon-ads-metrics.md`
- Optimization framework: `references/optimization-framework.md`
- Decision boundaries: `references/decision-boundaries.md`
- Contextual action sizing: `references/action-sizing.md`
- Platform capability version/scope lineage: `references/platform-capability-lineage.md`
- Benchmark policy: `references/benchmark-policy.md`
- Optimization memory: `references/optimization-memory.md`
- Canonical data model: `references/data-schema.md`
- Source lineage and cross-source comparability: `references/data-lineage.md`
- Active MCP/connector capability evidence: `references/connector-capability.md` and `schemas/connector-capability-snapshot.json`
- Canonical connector capability IDs / Skill decision profiles: `references/connector-capability-catalog.json`
- Action proposal schema: `schemas/optimization-action.json`
- Action/readback/evaluation event schema: `schemas/optimization-event.json`
- Derived entity-history schema: `schemas/entity-history.json`
- Experiment plan schema: `schemas/experiment-plan.json`
- Historical replay framework: `evals/README.md`
- Eval-case schema: `schemas/eval-case.json`
- Paired Skill-effectiveness result schema: `schemas/skill-effectiveness-benchmark.json`
- Decision-time measurement-state projector: `scripts/project_measurement_history.py`
- Paired with/without-Skill benchmark summarizer: `scripts/summarize_skill_effectiveness.py`

## Evaluation rules

When adding or changing decision logic, prefer adding a focused synthetic replay fixture for material failure modes.

- Keep deterministic contract checks separate from capability evals.
- Every fixture must remain valid under `scripts/validate_evals.py`: valid JSON, allowed contract fields/enums, collision-free ID, filename/ID alignment, and an existing repository-local entrypoint.
- Score decision behavior rather than exact prose.
- Use `met`, `not_met`, or `insufficient_evidence`; do not coerce missing evidence into pass/fail.
- A fixture may allow multiple conservative outcomes, but must list forbidden unsafe behaviors explicitly.
- Do not weaken a fixture merely because a current model fails it; change the Skill only when the fixture represents the intended behavior.
- Prefer synthetic identifiers and values. Never commit client/account secrets or proprietary exports as fixtures.
- Eval fixtures must remain closed-world by default and must not trigger live Amazon Ads writes.
- For important with-Skill / without-Skill comparisons, keep pair identity and harness/model/tool/evidence configuration aligned. `scripts/summarize_skill_effectiveness.py` fails closed on missing/duplicate pair variants and reports measured deltas only; it does not claim statistical significance.

## Read-only repository utilities

The repository includes deterministic helpers for derived memory and evaluation summaries. These are not Amazon Ads executors.

- `scripts/project_measurement_history.py` reads an optimization-event slice from stdin and projects only the newest traceable `evidence_snapshot` into `latest_measurement_state`. It fails closed on requested scope mismatch, preserves `unknown`, `retired_or_deleted` and `Not Comparable`, and never converts unavailable history to zero.
- `scripts/resolve_skill_capabilities.py` resolves canonical required/optional connector capability IDs plus profile-owned `data_requirements` for a registered Skill decision profile and can merge explicit task-level constraints such as an exact `history_window`. Task requirements may only strengthen profile policy, must target a required capability, and retain profile/task provenance. Pass the merged requirements unchanged to the connector capability gate. It never calls a connector or grants write authority.
- `scripts/evaluate_connector_capability_gate.py` reads a connector capability snapshot plus required capability IDs from stdin and returns `Pass`, `Degraded`, or `Blocked`. It is read-only, never calls a connector, and enforces `missing_evidence_policy = never_zero` for Partial/Unsupported/Unknown/absent capability evidence. Optional per-capability `data_requirements` additionally gate exact reporting generation and history availability: retired/mismatched generations or unavailable/retired required history block; partial/unknown required history degrades rather than becoming zero. A task-level `history_window` checks exact start/end dates against the matching observed grain; no cross-grain coverage inference is allowed.
- `scripts/evaluate_global_sp_readback.py` classifies a single Global SP campaign-update 207 receipt against complete post-write per-marketplace configured-state readback. It is read-only; partialSuccess/error, incomplete pagination, missing marketplace/account/source evidence or ambiguous batches never become Confirmed. If the adapter explicitly retains native campaign monetary budgets, contradictory currency/amount/recurrence/marketplace evidence cannot confirm a requested daily monetary-budget update. See `references/global-sp-readback-evidence.md`.
- `scripts/evaluate_global_sp_target_batch_readback.py` conservatively classifies a single-call, homogeneous Global SP positive-target batch: full 207 index coverage, unique request/target identity and per-success independent query evidence are mandatory. Each item reuses the single-target readback gate. Only all-Confirmed items yield batch Confirmed; unknown evidence takes precedence over partial/drifted. No Ads calls, retries or Executor reconciliation. See `references/global-sp-target-batch-readback.md`.
- `scripts/evaluate_global_sp_adgroup_bid_readback.py` independently classifies one external Global SP **ad-group** update receipt against source-supported, complete per-marketplace native-currency **default-bid** query evidence. It requires explicit external request/receipt binding, account/campaign/ad-group identity, query capability, pagination, and freshness; it never performs Ads writes, retries, or target-bid verification. See `references/global-sp-adgroup-bid-readback.md`.
- `scripts/evaluate_global_sp_adgroup_batch_readback.py` verifies one homogeneous Global SP multi-ad-group update call with complete 207 index coverage, unique ad-group/request identities and independently complete per-marketplace native-currency default-bid readback for each successful item. Any ambiguous evidence returns Unknown, and no Ads write/retry/executor action occurs. See `references/global-sp-adgroup-batch-readback.md`.
- `scripts/evaluate_global_sp_mixed_plan_readback.py` classifies an externally asserted complete, single-account Global SP optimization plan across campaign/ad-group/target or homogeneous batch readback gates. It binds each manifest component and ordered request IDs, rejects repeated entities, forged component verdicts and unsupported plan intent, and never upgrades partial/unknown child evidence to whole-plan confirmation. The manifest's completeness/authenticity must be guaranteed by the external authorized Executor; this helper does not verify a plan ledger or perform writes/retries/reconciliation. See `references/global-sp-mixed-plan-readback.md`.
- `scripts/evaluate_global_sp_target_bid_readback.py` independently verifies one **positive KEYWORD/PRODUCT target** bid update in one Global SP marketplace, requiring target-specific identity, native-currency Decimal bid, bound 207 receipt, query freshness, completeness and connector evidence. It does not verify ad-group defaults, negative/THEME targets, auction outcomes, or batch writes. See `references/global-sp-target-bid-readback.md`.
- `scripts/evaluate_metric_aggregation_gate.py` is a read-only policy gate for direct summation. It permits a sum only when metric aggregation semantics are explicitly additive and source rows are explicitly disjoint; unknown semantics never default to additive, and non-additive de-duplicated or ratio/derived metrics are blocked from direct summation. When source identity resolves to Marketing Stream v2 (including a coherent generic Stream channel with `stream_generation=v2`), the same gate also requires independently verified full record-key coverage and highest `streamBatch.version` selection before aggregation; Stream v2 totals are not v1 deltas.
- `scripts/evaluate_skill_effectiveness_comparability.py` compares two benchmark measurement identities before longitudinal interpretation. Fixture/evaluator/rubric/model/runtime/config/tool/evidence mismatches return `Not Comparable`; missing identity returns `Unknown`, never implicit comparability. It is read-only.
- `scripts/summarize_skill_effectiveness.py` reads benchmark trial records that conform to `schemas/skill-effectiveness-benchmark.json`. It validates paired `with_skill` / `without_skill` trials and reports counts/rates/deltas only from pairs where both arms were actually measured. Scorer/harness errors and insufficient-evidence arms exclude the whole pair rather than being imputed as zero quality. It does not call a model, invoke a live agent runtime, or mutate an advertiser account.

Actual model/harness execution remains an external evaluation-runner concern. Raw transcripts and provider credentials should stay outside normal Skill loading paths and outside committed fixtures unless explicitly synthetic and safe.

## Agent Skills frontmatter compatibility

`SKILL.md` frontmatter must stay compatible with the Agent Skills specification and strict reference validators.

Allowed top-level fields are:

- `name` — required and must match the parent directory name;
- `description` — required and should state both capability and trigger/use case;
- `license` — optional; repository-owned Skills should normally use `MIT`;
- `compatibility` — optional, only when environment requirements are material;
- `metadata` — optional string-to-string map for repository-specific metadata;
- `allowed-tools` — optional/experimental and should not be used to broaden execution authority.

Do **not** add custom top-level fields such as `display_name`, `display_name_en`, `description_zh`, `description_en`, `version` or `author`. Put repository-specific values under `metadata` instead.

Keep `name` within the Agent Skills naming constraints and `description` within the specification limit. Metadata compatibility is part of multi-agent portability; a Skill that works in one permissive runtime but fails strict validation is not considered portable.

## Versioning and releases

`VERSION` is the canonical repository release version. Keep the README version label and all runtime manifests (`.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.workbuddy-plugin/plugin.json`) synchronized with it, and add the release entry to `CHANGELOG.md`.

Use semantic versioning for release-worthy changes:

- **PATCH** — backward-compatible bug fixes, documentation corrections, research/source maintenance, or internal changes that do not materially expand a public decision/runtime contract.
- **MINOR** — backward-compatible new capability, materially stronger decision/safety/data/runtime behavior, new optional schema surface, or another substantial improvement users should be able to identify as a new release.
- **MAJOR** — breaking changes to public schemas, CLI/output contracts, canonical Skill/capability identity, runtime integration contracts, or changes that require downstream migration.

A material MINOR/MAJOR change must not merge while the repository continues to advertise the previous release indefinitely. Classify version impact in the pull request; when a bump is required, update `VERSION`, README, all runtime manifests, and `CHANGELOG.md` in the same PR. Do not add repository release versions to individual `SKILL.md` top-level frontmatter.

## Deterministic repository validation

After changing a Skill, its supporting references, shared references, schemas, playbooks, eval fixtures, validators, projector/summarizer utilities, or runtime manifests, run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

The validators are intentionally dependency-free and check repository invariants that should fail before a runtime or eval harness discovers them interactively. Unit tests additionally cover measurement-state projection, realized-ad projection, experiment-plan semantics, paired effectiveness aggregation and release/runtime compatibility.

Skill/package validation checks:

- every direct child of `skills/` contains `SKILL.md`;
- required `name` / `description` frontmatter exists;
- top-level frontmatter stays within the Agent Skills allowed field set;
- Skill `name` matches its folder name;
- nested `SKILL.md` files are rejected;
- relative Markdown references from `SKILL.md` stay inside the repository and resolve to existing paths.

Eval-contract validation checks:

- every `evals/fixtures/*.json` file parses as JSON;
- required/allowed fixture and expected-result fields are respected;
- mode and acceptable-decision values stay within the closed-world schema contract;
- fixture ID matches filename and does not collide;
- entrypoint stays inside the repository and exists;
- rubric/required-observation contracts do not positively require live mutation.

`.github/workflows/validate-skills.yml` runs unit tests plus both validators for relevant pushes and pull requests when GitHub Actions is enabled. Do not treat a local or CI pass as proof of Amazon Ads decision quality; deterministic structure/contract checks complement, rather than replace, capability replay behavior checks.

## Contribution rules

New skills must:
- use kebab-case directory names;
- include Agent Skills-compatible YAML frontmatter with at least `name` and `description`;
- keep custom metadata under the `metadata` map rather than inventing top-level fields;
- keep the core `SKILL.md` concise and progressively load shared references;
- state required inputs, workflow, output contract, safety checks, and stop conditions;
- output proposals rather than performing live account mutation.

Add a playbook instead of a new Skill when the new material is primarily a recurring operating rhythm that composes existing Skills rather than a distinct decision capability.

Shared memory/history features should prefer append-first events plus derived compact summaries rather than mutable prose logs.

When a change materially affects source comparability, negatives, bid/budget reversals or sizing, retail causality, Mixed-ASIN safety, growth qualification, experiments, readback, or rollback decisions, add or update a replay fixture when practical.