# Amazon Ads Skills

## v2.15.0 — Explicit empty account identity integrity

- Explicit empty or provenance-only `account_identity` objects now fail closed as incomplete claims in measurement and comparison projections.
- Missing identity remains distinct from an explicit incomplete claim; no Skill, schema, dependency or Ads write.


## v2.14.0 — Weak-only account identity claim integrity

- Explicit `account_identity` objects now require at least one advertiser or regional profile identifier; weak-only claims such as `country_code` fail closed instead of becoming missing identity.
- Missing identity remains missing; concrete opaque advertiser/profile identifiers remain supported.


- **Reject partial realization scope claims without entity identity (v2.13.0)** — realization events that supply marketplace/profile scope without a concrete entity identity now fail closed instead of being downgraded to legacy-unbound history. Missing scope remains distinct from partial/unresolved scope; no Skill, schema, dependency or Ads write.

- **Reject partial measurement/comparison scope claims (v2.12.0)** — a supplied marketplace/profile scope without a concrete entity identity now fails closed instead of silently downgrading to legacy-unbound history. Missing scope remains distinct from partial/unresolved scope; no Skill, schema, dependency or Ads write.

- **Reject unresolved account identity placeholders (v2.9.0)** — account identity fields now reject whole-label unresolved values and padded values in measurement and realization projections; concrete opaque IDs containing placeholder substrings remain valid. Read-only lineage guard only; no Skill or Ads write.

- **Reject unresolved observed realization scope without expected scope (v2.10.0)** — realization projections now validate any supplied marketplace/profile/entity scope even when expected_scope is omitted; legacy entity-only events remain distinct from supplied partial/unresolved scope.

- **Reject unresolved observed scope without expected scope (v2.9.0)** — when an event contains a scope object, every scope value is now validated even if no expected_scope was supplied. Whole-label unresolved placeholders and padded values are rejected; missing scope remains allowed when no scope is provided. Concrete opaque IDs remain compatible. Read-only lineage guard only; no Skill, schema, dependency or Ads write.

A portable **Amazon Ads decision library for AI agents**. It packages 15 focused Skills for audit, monitoring, diagnosis, growth, experiments, search terms, targeting, bids, budgets, placements, profitability and post-change learning without turning this repository into an autonomous write bot.

> 当前版本：`v2.15.0`  
> Default mode: `Suggest`  
> Live Amazon Ads writes: external Connector / Executor only

## What you can do

- **Reject unresolved measurement scope placeholders (v2.9.0)** — the read-only measurement-history projector now rejects whole-label `Unknown`/`Partial`/`Missing`/`Unsupported`/`Unavailable`/`N/A` and padded scope identities in expected or observed event scope. Concrete opaque IDs containing those words remain valid; missing/unknown scope is not promoted to a usable identity. No schema, Skill, dependency or Ads write.

- **Validate Skill-eval trigger observations and expose the rate denominator (v2.6.0)** — supplied non-null `triggered` values must be booleans, including on excluded trials; malformed strings/numbers/arrays/objects fail rather than silently disappearing. Missing/null remain unmeasured, not false/zero. Each comparable arm reports `trigger_observed_count`, `trigger_observation_coverage`, and `trigger_observation_status` beside `trigger_rate`; partial or unmeasured trigger coverage is explicit rather than inferred from the rate. Read-only synthetic verification; no harness authenticity or Ads write claim.

- **Reject unresolved single-run Skill-eval identities (v2.5.0)** — the paired read-only summarizer now rejects missing, malformed, padded or placeholder benchmark/fixture/model/runtime/evaluator identities and invalid evaluation modes before reporting `Measured`. Optional omitted/null hashes and explicit null rubric remain compatible; this does not authenticate real model runs, prove significance or authorize Ads writes.

- **Reject malformed Skill-evaluation token/latency measurements (v2.4.0)** — the paired read-only summarizer now rejects negative, non-finite or wrong-type resource values rather than averaging them or silently dropping supplied invalid values. Optional missing/null metrics remain unmeasured (not zero); valid zero tokens and fractional latency remain supported. Synthetic RED→GREEN regression coverage; no new Skill, schema, dependency, statistical-lift claim or Ads write.

- **Reject reused paired Skill-eval trial IDs (v2.3.0)** — the read-only effectiveness summarizer now refuses a repeated `trial_id` across pairs or variants, including excluded scorer/harness-error trials. One execution cannot inflate independent sample counts or a measured lift. Valid unique IDs, paired-arm accounting and null non-measured outcomes remain unchanged; no new Skill, schema, dependency or Ads write.

- **Fail closed on unresolved Skill-effectiveness measurement identity (v2.2.0)** — the read-only longitudinal comparator no longer treats repeated `Unknown`/`Partial`/`Missing`/`Unsupported`/`Not Applicable` labels, padded strings, or non-string model/fixture/evaluator/tool/evidence identities as `Comparable`. Real opaque labels and explicitly null `rubric_version` remain compatible. This does not certify agent effectiveness, Amazon Ads data, or any live write.

- **Stream v1/v2 explicit dataset identity parity (v2.1.0)** — supplied `stream_dataset` must be concrete and unpadded for either resolved generation; Unknown/Partial/Missing/Unsupported and malformed identities return `Unknown` despite otherwise Verified reconciliation. Fixes a regex escape error affecting `Missing` and `Unsupported`. Omitted optional dataset and concrete opaque labels remain compatible. No new Skill, schema, dependency or Ads write.

- **Stream v1 delta direct-sum proof (v2.0.0 breaking migration)** — deprecated Marketing Stream v1 delivers incremental changes, not complete window totals. The read-only aggregation gate now returns `Unknown` for additive/disjoint v1 data unless the external connector supplies Verified `idempotency_id_coverage`, `idempotency_id_deduplication`, and `delivery_window_coverage` under `stream_delta_reconciliation`. Previously unproven v1 rows could return `Allowed`; existing v1 callers must migrate their evidence envelope. Stream v2 retains separate highest-version-per-record proof. No Ads writes or connector retries are implemented here.

- **Reject unproven sibling arrays in observed SP rule events** — schedule/event/budget `control_events` now return `Unknown` when either before/after rule state contains an additional direct array not covered by the registered rule-list completeness proof, including empty arrays. Valid schedule/event/active-budget rule collections and scalar extra fields remain compatible. No new schema, Skill, dependency or live Ads write.

- **Reject unproven non-rule SP event collections** — routing events with direct or deep arrays, and audience events with nested member arrays, now return `Unknown` without independent collection evidence, even for empty lists. Valid scalar routing and flat audience events remain compatible. No new schema, Skill, dependency or Ads write.

- **Opt in to independent nested SP rule-event collection proof** — observed mid-window schedule/event/budget rule transitions may now include paired `rule_descendant_collection_evidence` with exact RFC 6901 state-relative pointers, Complete enumeration/pagination and Supported capability for every nested list. Requires independent outer `rule_collection_evidence`; missing, partial, extra or malformed pointers remain `Unknown`. Legacy unproven nested arrays remain `Unknown`; valid flat events remain compatible. This is an internal read-side evidence contract, not authenticated Amazon Ads event history or write authority.

- **Fail closed on unproven nested SP rule-event arrays** — a Complete top-level rule collection declaration cannot prove nested arrays within schedule/event/budget rule members. Such positive mid-window event evidence is `Unknown` until an independently verified descendant-proof contract exists; flat members and existing top-level rule proofs remain compatible. No Ads writes.

- **Accept paired SP event rule-collection completeness evidence** — optional `rule_collection_evidence` can now carry independent before/after Complete enumeration, Complete pagination and Supported capability declarations for observed schedule/event/budget rule transitions. Explicit partial, truncated, malformed or one-sided proof returns `Unknown`; both-absent legacy evidence remains compatible but **never** proves full-window capture. Read-only; no Ads writes.

- **Reject unmapped Sponsored Products placement dimensions** — normalized endpoint snapshots and positive mid-window placement events now fail closed as `Unknown` when an adapter supplies unknown placement keys, even if repeated. The three standard placement controls and optional Amazon Business modifier remain supported. This is a read-only evidence contract, not proof of complete event capture or live Ads write authority.

- **Reject one-sided activation metadata in mid-window SP rule events** — for a shared schedule/event/active-budget `rule_id`, optional `activation_status` and `activation_effective_at` must be present on both sides of a positively observed transition or neither. Missing-before/after metadata returns `Unknown`, not a fabricated confounder; valid activation changes and new rule identities remain compatible. This does not certify continuous execution, event-log completeness, or authorize Ads writes.

- **Reject co-observed routing/placement contradictions** — two positive mid-window Sponsored Products control events bound to the same concrete source readback cannot simultaneously certify `ACROSS_RETAILERS` routing and an Amazon Business placement modifier in the same before/after phase. Return `Unknown`, not an invented confounder. Distinct or missing readbacks are not assumed simultaneous; compatible Amazon Store states remain valid. No full-window capture or Ads write authority follows.

- **Detect contradictory mid-window event observations** — a reused concrete event `source.readback_id` cannot denote different UTC event times, and two events for the same control at the same instant cannot disagree on the before/after transition. Return `Unknown` for conflicts, preserving multi-control same-time observations, distinct event identities, nanosecond precision and non-exhaustive event-log compatibility. This does **not** prove complete event capture or authorize live Ads writes.

- **Reject nested null material-control evidence** — explicit JSON null inside an observed control-state object/list returns `Unknown`, not a fabricated isolated treatment or confounder. Measured zero/false, omitted optional dimensions and null provenance outside material state remain compatible; no live Ads writes.

- **Fail closed on one-sided mid-window budget evidence** — optional observed base/effective daily budget and policy fields must have before/after parity in Sponsored Products `control_events`. Preserve both-absent legacy bid surfaces and genuine Amazon Business placement additions as observed confounders. This is a read-only evidence check, not complete event-history proof.

- **Reject invalid mid-window Sponsored Products budget/routing events** — observed event before/after budget amounts, daily-budget policy and site/retailer routing must be usable before a competing change can be classified. Unmapped or contradictory site/retailer states and missing required budget-change fields return `Unknown`; valid observed transitions remain compatible. Event logs remain optional, non-exhaustive and read-only.

- **Validate intervening Sponsored Products event values** — positively observed mid-window bid, video, placement, audience and bidding-strategy transitions must carry usable, source-supported numeric/member/strategy states, not arbitrary strings, booleans, negative modifiers or incomplete placement surfaces. Invalid event values return `Unknown`, not a fabricated confounder or isolated treatment. This remains endpoint-only unless an authenticated, complete history is independently available; no live Ads writes.

- **Detect observed mid-window control confounders** — optional post-readback `control_events` records reveal positively observed schedule/event/budget/placement changes that revert before the final snapshot. A competing transition blocks `Treatment Isolated` as `Confounded`; missing, mismatched or contradictory event evidence is `Unknown`. Empty or omitted event lists do not prove complete event history or continuous rule execution. No Ads writes.


- **Reject N/A material-control evidence** — a repeated whole-label `N/A` or `Not Applicable` in a material state, nested state, rule ID or audience ID cannot certify stable competing controls even when collection coverage is Complete. Return `Unknown`; preserve real opaque IDs, zero/false, and actual confounders. No continuous rule-history proof or live Ads write authority is implied.


- **Reject conflicting transition provenance under one readback** — matching `source.readback_id` cannot certify contradictory transition actor, management mode, evidence status, reason or transition time. One-sided provenance returns `Unknown`; exact UTC timestamps preserve nanosecond differences and equivalent offsets. No source authentication, continuous control proof or live Ads write authority is implied.

- **Reject N/A scope/source identity placeholders** — repeated whole-label `N/A` or `Not Applicable` cannot certify marketplace, profile, campaign, entity, account, acquisition channel, source system or connector identity. Whitespace/hyphen/underscore variants return `Unknown` rather than false causal isolation. Concrete opaque IDs containing these words remain valid. No external source authentication, full-window control attestation or live Amazon Ads write is implied.


- **Reject contradictory control evidence within one readback** — identical concrete `source.readback_id` cannot certify different control `effective_at` instants or `evidence_status` values, even when `observed_at` and material state match. Exact UTC fractional timestamps are compared; omitted/null legacy IDs, distinct IDs and equivalent timezone spellings remain compatible. This does not authenticate external observations or prove full-window rule execution.

- **Reject unresolved or temporally contradictory control readback identities** — explicitly supplied non-null `source.readback_id` placeholders, blanks, padded or non-string values cannot prove independent observations. The same concrete ID cannot describe different `observed_at` instants, even when control values match. Omitted/null legacy IDs, valid distinct IDs and UTC-equivalent timestamps remain compatible. This is internal provenance consistency, not external API authentication or full-window control proof.

- **Reject conflicting control states under a reused readback ID** — when before/after snapshots claim the same explicit non-null `source.readback_id` but material states differ, the read-only comparator returns `Unknown`. Distinct observation IDs and legacy omissions remain compatible; a distinct label is not raw source authentication or full-window control proof.

- **Reject contradictory material-change re-verification evidence** — a Ready holdout cannot treat explicitly supplied null/Unknown or chronologically impossible `material_scope_changes[].reverified_at` as proof of a reverified boundary. Known-offset RFC3339 and exact UTC ordering require change ≤ re-verification ≤ latest clean check. Omitted legacy fields and exploratory plans remain compatible; this does not establish full-window external control stability or permit Ads writes.

- **Preserve nanosecond-scale Ready holdout chronology** — verified isolation, launch, latest boundary monitoring and material-change timestamps retain all RFC3339 fractional digits for UTC ordering instead of being truncated to Python microseconds. Valid high-precision timestamps, legacy omissions and exploratory plans remain compatible; this does not prove external control history or authorize Ads writes.

- **Reject internally stale Ready holdout monitoring** — a supplied latest clean boundary check cannot predate any valid positively verified isolation proof. UTC/offset chronology, omitted legacy fields and exploratory plans remain compatible. This does not establish continuous control coverage or raw source authenticity.

- **Reject whitespace-obfuscated unresolved Ready metric identities** — a combined readout cannot treat `Not  Applicable`, tab/newline/nonbreaking-space variants as real primary or guardrail metrics. The correction is a narrow whitespace normalization of the existing placeholder gate; concrete metric names, non-combined Ready and exploratory plans remain compatible. It does not authenticate reporting, recompute metrics or permit Ads writes.


- **Reject ambiguous Ready holdout verification times** — known-offset RFC3339 instants are required for supplied launch, monitoring, material-change and isolation evidence; -00:00, space separators and second-resolution offsets are not verification proof. Valid offsets, legacy omissions and exploratory plans remain compatible; no external source authentication or Ads writes.

- **Block additive Amazon benchmark rates and cost-per metrics** — standalone direct sums and Ready combined readouts reject additive claims for official purchase/add-to-cart/detail-page-view/branded-search rates, cost per purchase/detail-page view, and percent of purchases new to brand. This prevents incorrect cross-row rate summation while keeping actual counts additive. Metric labels are not proof of raw report identity or compatible denominators; no live Ads writes.

- **Require concrete metric identities for Ready combined readouts** — unresolved primary or decision-driving guardrail names (whole-label Unknown/Partial/Missing/Unsupported/Unavailable/N/A, blanks, non-strings) cannot pass solely on an additive or derived aggregation declaration. The standalone gate already protects its separate entrypoint; this release closes the Ready experiment parity gap. Concrete labels, non-combined Ready and exploratory plans remain compatible. This does not authenticate Amazon Ads source data or permit live writes.

- **Reject unresolved Ready combined-readout requirements** — an explicitly supplied `comparison.requires_combined_readout` must be a JSON boolean. Null, placeholder strings, numbers, lists and objects cannot silently bypass the combined ratio/derived KPI gate; omitted legacy fields and explicit false remain compatible. This is internal plan consistency, not proof of source comparability or Amazon Ads delivery.

- **Reject explicit unresolved metric names in standalone sums** — explicit null, blank, placeholder or non-string `metric_name` cannot authorize an additive direct sum; omitted legacy names remain compatible. This does not authenticate metric provenance.

- **Distinguish absent from unresolved holdout monitoring** — when a `Ready` holdout explicitly supplies `boundary_monitoring`, a null/scalar/list cannot silently pass as if no monitoring were provided. Explicit null launch verification or malformed material-change collections are also unresolved. Omitted optional fields, exploratory plans and 15-Skill read-only boundaries remain compatible; this does not authenticate continuous delivery.

- **Block additional cost/return ratio roll-up errors** — CPA, CPM, vCPM and ROI now join the bounded ratio KPI checks in both the standalone direct-sum gate and `Ready` combined experiment readouts. An `additive` declaration cannot make these ratios summable. These name guards do not calculate ratios, prove denominator completeness, authenticate reporting, or authorize Amazon Ads writes.

- **Stream v2 dataset identity guard** — explicitly supplied unresolved/null/padded `stream_dataset` returns `Unknown` even with Verified record-key/version flags; omitted legacy metadata and concrete names remain compatible. This does not authenticate subscription/account filters or delivery completeness.
- **Prevent ratio KPI summation in the standalone gate** — when an explicit `metric_name` identifies ROAS, ACOS, TACOS, CVR, CTR or CPC, `scripts/evaluate_metric_aggregation_gate.py` rejects a contradictory `additive` declaration even for supposedly disjoint rows. This is a narrow optional name/semantics consistency check; unnamed legacy calls remain compatible, and the gate does not authenticate source rows or recompute ratios.

- **Keep retail outcomes separate from ad attribution** — a `Ready` experiment no longer mistakes exact Total Retail Sales, Retail Sales, Organic Sales or Sales Rank labels (or unrelated Wholesale Traffic) for ad-attributed conversions. Bare/attributed Sales, Purchases and explicit conversion-family claims retain strict attribution checks. This is a bounded name-classification correction, not proof of retail data provenance or incremental ad effects.

- **Prevent ratio KPI roll-up misclassification** — a `Ready` experiment requiring a combined readout cannot declare canonical ROAS, ACOS, TACOS, CTR, CVR or CPC as `additive` or `non_additive_deduplicated`; these require `ratio_or_derived` and a separate source/grain/completeness-safe recomputation. Raw Sales/Impressions remain additive when supported. Shadow and non-combined plans retain their prior contract; no live Ads writes.

- **Protect additional Ready conversion metric names** — ACOS, CVR, attributed orders/units and units sold cannot claim a traffic/Unknown family to bypass attribution/version evidence. Exact-name ACOS recognition does not conflate TACOS (total retail sales) with ad-attributed ACOS; genuine traffic and Shadow plans stay compatible. Internal checks do not authenticate external reports or execute Ads changes.


- **Fail closed on Ready conversion metric identity** — Purchases/Sales/ROAS cannot escape attribution requirements by declaring a traffic or Unknown metric family; conversion primary metrics and guardrails require a concrete attribution family and semantic version, not Missing/Partial/Unsupported placeholders. Non-conversion and exploratory plans remain compatible; no external attribution authentication or Ads writes.

- **Reject unsupported Ready holdout isolation proof** — a `verified: true` isolation record with placeholder/padded `evidence` is not a verified boundary. Optional `source` and `verified_at`, when supplied, must be concrete and timezone-aware. Valid narrative evidence and omitted optional fields remain compatible; this does not authenticate external delivery or authorize Ads writes.

- **Reject incomplete optional Ready holdout monitoring** — when a `Ready` holdout supplies `boundary_monitoring`, require `current_status: Clean` and a valid timezone-aware `latest_verified_at` even with no material changes. Optional `launch_verified_at` cannot be after the latest verification. Legacy absent-monitoring and exploratory plans remain compatible; no remote delivery authentication or Ads write authority.

- **Reject unknown post-change holdout re-verification** — a `Ready` experiment cannot rely on a later `boundary_monitoring.latest_verified_at` alone when any recorded material scope change lacks explicit boolean `reverified: true`. Missing/null/false/non-boolean flags fail closed; positive evidence and chronology both matter. Shadow/Hold remain exploratory, and this does not authenticate delivery or grant Ads write access.

- **Reject false Ready experiment scope** — unresolved or padded marketplace/profile/entity identifiers, duplicate treatment/control IDs and explicit arm overlap cannot masquerade as a verified experiment boundary; Shadow/Hold designs retain unresolved evidence without inventing IDs.

- **Avoid false SP rule confounding from enumeration order**: normalized, complete schedule/event/active-budget rule lists are compared by stable unique `rule_id` for the registered bid/budget causal surfaces. Different row order alone no longer counts as another control change; changed values/status/identities remain material, and incomplete evidence remains Unknown. This does not establish continuous rule execution or grant Ads write access.

- **Reject feature eligibility reuse of capability-level probes**: a feature-specific eligibility source reference cannot reuse a `capabilities[].evidence[].reference` from any observed connector capability, including non-required or Unsupported ones. This closes a separate provenance path from binding-level evidence. Eligible/Ineligible collisions degrade to Unknown; distinct references remain compatible but never authenticate external Amazon Ads responses or authorize writes.

- **Reject feature eligibility self-references across the entire connector snapshot**: a supposedly independent entitlement record cannot reuse any observed connector binding/probe reference, including on non-required or unverified capabilities. Both Eligible and Ineligible collisions degrade; actual capability requirements and valid distinct evidence remain unchanged. This does not authenticate remote API responses or permit writes.

- **Reject eligibility self-references to unverified connector probes**: a feature-specific source reference cannot reuse a required connector capability's binding ID, surface ID or supporting probe reference even if that binding is Unverified. A separate Verified read-side binding cannot make the reused probe independent entitlement evidence. Eligible and Ineligible self-references degrade; distinct sources retain legacy behavior. This is not raw Amazon API authentication or write authorization.

- **Require exact campaign identity for Sponsored Products causal reviews**: bid/budget comparisons with both `scope.campaign_id` values absent or null now return `Unknown`, not `Treatment Isolated`. A shared profile and marketplace do not identify the same campaign; valid, concrete campaign IDs retain existing behavior. This is read-only control comparability, not proof of delivery, continuous rule activation, or API authenticity.

- **Reject self-referential feature eligibility source evidence**: a Verified feature-specific record cannot reuse a required connector binding's ID, surface ID or supporting evidence reference as its supposedly independent source. Such Eligible or Ineligible claims degrade to Unknown, not Pass or verified exclusion. Distinct reference identity is necessary but does not authenticate raw Amazon Ads responses or prove enrollment; no live writes.

- **Keep feature-specific decision time separate from connector capture time**: a connector snapshot taken after the feature requirement's `as_of` cannot prove earlier capability coverage. A future/missing/invalid capture degrades; equal/earlier capture passes only chronology. Explicit connector freshness remains separate; Verified Ineligible still blocks. No Amazon Ads entitlement lookup or write authority is implied.

- **Join feature-specific eligibility evidence to exact connector scope when required**: an optional read-side eligibility subgate binds a named feature, marketplace, advertiser account, campaign, source identity, and observation time to the requested decision. A Verified feature-specific Eligible record may pass only alongside existing connector capability checks; verified Ineligible blocks, while unknown/partial/stale/mismatched/generic product-group evidence degrades. This is not an Amazon entitlement query or permission to execute.

- **Reconcile canonical observation-only connector capabilities**: a Verified `access_mode=observe` surface can substantiate only a catalog-declared `*-observe` requirement, subject to all existing identity, scope, freshness and data-contract checks. It cannot prove campaign report access, advertiser eligibility or write permission; `write`, `mixed`, and unknown access remain guarded. Snapshot schema now recognizes `observe`.

- **Bind connector capability to exact advertiser/campaign identity when required**: optional `expected_scope.advertiser_account_id` and `campaign_id` require matching concrete, case-sensitive opaque IDs on both the observed capability and a Verified binding. A shared marketplace alone is insufficient; missing/unknown membership cannot prove coverage or become zero. Existing calls omitting exact IDs remain compatible. This does not establish feature eligibility, delivery, source authentication or permission to write.

- **Fail closed on repeated Global SP identity placeholders**: a matching `Unknown`/unavailable account, campaign, explicit request ID, connector source or raw marketplace crosswalk cannot confirm an externally executed campaign update. Require concrete, unpadded identities; retain legitimate IDs containing placeholder substrings and legacy index-only/country-code-only readbacks. This read-only gate does not authenticate raw API responses or establish advertiser eligibility.


- **Degrade overdue reporting sunset evidence**: when a connector snapshot claims a required reporting generation is still active or awaiting sunset after its own declared `sunset_at`, require refreshed source evidence rather than high-confidence Pass. Do not infer actual retirement or zero metrics; future sunset, explicitly retired, and no-generation cases remain compatible.


- **Reject future-dated historical availability claims**: a per-grain `available_through` more than one calendar day after snapshot capture cannot prove history was already retrievable. Degrade rather than high-confidence Pass; preserve valid earlier ranges and no-history decisions. This does not establish an Amazon API SLA, completeness, eligibility or causal effect.

- Require **concrete historical reporting grain evidence** before accepting a dated availability window. Requested unavailable/padded grain identities are invalid; observed padded apparent matches degrade even alongside valid matches. Concrete case-insensitive grains remain compatible. This does not prove per-metric history, source authenticity or account eligibility.


- Require **concrete reporting-generation identity** before high-confidence report interpretation: repeated Unknown/Unsupported/Partial/Missing/Unavailable/Not Available/Not Supported cannot prove a matching reporting generation. Invalid requested generation labels are configuration errors; explicitly unavailable or whitespace-padded observed generation degrades to Unknown, not zero or a verified mismatch. Concrete matching/mismatching generations remain compatible. This read-side guard does not authenticate Amazon API responses or prove advertiser eligibility.

- Preserve connector scope uncertainty at the **final decision gate**: when a present bounded scope list has unmatched Unknown/Partial/malformed members, report `scope_effect=unknown` and `gate_status=Degraded`, not a definitive exclusion. Missing scope evidence still blocks rather than assuming global coverage; a fully concrete mismatch remains `Blocked`. This read-side distinction is not advertiser/campaign entitlement, a metric zero, or permission to execute.


- Fail closed on placeholder connector decision scope: a repeated `Unknown` requested marketplace/ad-product/region/account type is not an identity; an observed scope list containing unknown/malformed members cannot prove an unmatched scope absent. Preserve concrete matches and fully concrete mismatches. This is a read-side connector scope-evidence rule, not advertiser/campaign entitlement or Amazon-native schema.

- A `Supported`/`Verified` read capability must also have a concrete snapshot-level `connector_id`. A missing, blank, placeholder (`Unknown`/`Unsupported`/`Partial`/`Missing`/`Unavailable`/`Not Available`/`Not Supported`) or whitespace-padded connector identity degrades the entire decision, even with multiple valid bindings. Optional `source_system` and `acquisition_channel` may be omitted for legacy snapshots, but when explicitly provided they must be concrete identities, not null/placeholder/whitespace-padded values. This is a repository-owned read-side provenance check, not authentication of remote API responses, proof of account eligibility, or permission to write.


- A `Supported` connector capability with a `Verified` binding still needs a concrete read-side `access_mode`. A `write`-only capability is `Blocked`; `mixed`, `unknown`, missing, malformed or unsupported modes are `Degraded`. Only explicit `read`, `report`, `export` or `stream` access can pass the access-mode preflight, subject to other evidence gates. A second binding or snapshot default mode cannot override write-only access. This repository-owned read-side check does not authenticate remote tool behavior, grant write permission, or replace an authorized external Executor.

- Fail closed on placeholder `Verified` connector binding identity: a binding/surface ID or supporting evidence kind/reference equal to `Unknown`, `Unsupported`, `Partial`, `Missing`, `Unavailable`, `Not Available` or `Not Supported` is not concrete provenance. Preserve valid alternate bindings and real identifiers; this is read-side validation, not raw HTTP authentication.

- Fail closed on invalid connector freshness horizons: a caller-supplied `max_age_seconds` must be a finite non-negative numeric duration. NaN, infinity and numeric overflow are rejected before freshness evaluation; an invalid horizon cannot make stale connector evidence appear current. Valid zero/finite horizons remain supported. This is a repository-owned evidence rule, not an Amazon API TTL.

- Reject temporally impossible connector capability verification: a Verified binding cannot postdate its snapshot, and explicitly dated supporting evidence cannot postdate binding verification. This chronology gate applies even without a caller-supplied freshness horizon; legacy undated evidence remains compatible but does not prove freshness or source authenticity.

- Reject repeated unavailable labels as marketplace, profile, campaign, entity, advertiser-account, connector, source or acquisition identity. Shared `Unknown` is not verified shared identity or provenance; valid IDs and both-absent optional legacy connector IDs remain compatible. Read-side only, not authentication.

- Fail closed on explicitly unavailable material-control state values, even inside a nested object or complete list and even when both snapshots repeat the same placeholder. Generic Unknown/Unsupported/Partial/Missing/Unavailable, blank scalar strings and non-finite numbers are not observed stable controls. Verified numeric zero, boolean switches and valid descriptive values remain distinct; this is read-only evidence validation, not Amazon-native schema or eligibility proof.

- Audit an Amazon Ads account without treating missing connector/report data as zero.
- Diagnose sustained performance drops and separate observations, hypotheses, causes, actions and outcomes.
- Analyze search terms, keyword/target structure, bids, budgets and placements with report-coverage and control-state gates.
- For Sponsored Products bid/budget causal reviews, explicit normalized rule activation_status (active/inactive/scheduled) must be valid and present on both snapshots for a common rule identity; Unknown/Unsupported or one-sided status evidence fails closed. This optional status is not proof of continuous execution or Amazon-native API fields.
- If an SP rule member explicitly includes optional `activation_effective_at`, it must be a valid timezone-aware transition instant no later than snapshot observation, paired with an observed status and symmetrically present for the same rule ID. Malformed/future/one-sided time evidence returns Unknown; this does not prove uninterrupted rule execution.
- For Sponsored Products bid/budget causal reviews, complete schedule/event bid-rule and active budget-rule lists also require individually observed, uniquely identified rule members and valid nonnegative modifiers. Missing, duplicated, Unknown or unsupported rule members cannot establish treatment isolation; this is read-side normalization, not proof of activation or Amazon-native API fields.
- For Sponsored Products causal reviews, distinguish observed site routing (`ALL_ELIGIBLE` versus Amazon Business-exclusive) from unknown/unsupported routing; a complete control inventory alone does not prove site eligibility or unchanged delivery.
- Evaluate break-even ACOS, contribution economics and TACOS without confusing historical efficiency with marginal headroom.
- Find guarded growth opportunities only after retail readiness, economics, incrementality and binding-control checks.
- Design experiments when evidence is not strong enough for a direct recommendation.
- Review previous changes using readback, validation windows, confounders and append-first optimization memory.
- Sponsored Products bid/budget causal reviews require recognized bidding-strategy evidence: simple dynamic-down-only, dynamic-up-and-down and fixed labels remain valid; rule-based bidding additionally requires a structured positive, observed ROAS guardrail (`{"strategy":"rule_based","roas_guardrail":3}`). A bare `rule_based` label is Unknown rather than proof of unchanged control. These are normalized read-side labels, not Amazon API enums, activation proof or universal eligibility.
- Sponsored Products bid/budget causal reviews now validate every member of a fully enumerated audience bid-adjustment collection: unique nonblank audience identity and finite nonnegative bid boost are required. A verified empty list and observed zero remain valid; missing, duplicate or invalid members yield Unknown. This is a repository-normalized readback contract, not an Amazon-native schema.
- Sponsored Products bid/budget causal reviews now reject invalid base-bid evidence (Unknown/Unsupported/Partial, boolean, negative, non-finite, percentage strings or structured placeholders) before claiming treatment isolation. Valid observed numeric and plain decimal-string values remain supported; bid eligibility/limits require separate dated evidence.
- Sponsored Products bid/budget causal reviews reject unknown, unsupported, boolean, negative, non-finite, percentage-formatted or structured video bid-adjustment evidence before claiming an isolated treatment. Explicit numeric zero remains valid; platform-specific limits and eligibility require separate dated evidence.
- For Sponsored Products causal comparisons, an explicitly supplied normalized retailer scope must be recognized and symmetric across snapshots. Across-retailers scope cannot coexist with an Amazon Business placement modifier (even observed zero) or Business-exclusive site routing. Legacy both-absent retailer scope remains compatible but does not prove eligibility, connector capability or actual delivery.
- Explicit Amazon Business placement modifier evidence is now checked separately from the three standard Sponsored Products placements: invalid or one-sided missing B2B values yield Unknown, while legacy omission remains compatible but does not prove B2B eligibility or zero.
- Sponsored Products bid/budget causal reviews now reject unknown, unsupported, boolean, negative and non-finite placement modifiers for Top of Search, Rest of Search and Product Pages; an explicitly observed numeric zero remains valid. Platform-specific upper bounds require separately dated capability evidence.
- Sponsored Products budget-change causal reviews now reject Unknown/Unsupported placeholders, booleans, negative/non-finite amounts and missing average-daily-budget policy; only observed finite budget values can support Treatment Isolated. Explicit numeric zero remains distinct from missing evidence.
- For Global SP campaign, ad-group and target readback, reject unsupported or malformed marketplace country codes before an otherwise matching receipt/query can be classified `Confirmed`; eligibility follows the dated official Global SP country-code list, not arbitrary ISO codes or raw marketplace IDs.
- When a trusted adapter explicitly retains query page `response_body` evidence, require every page's `campaigns[]` and `nextToken` to match the declared trace, and require the complete native campaign to appear exactly once on the claimed provenance page; missing, duplicated, displaced or contradictory response members are `Unknown`. Legacy traces without retained response bodies remain compatible.
- When both native Global SP campaign configuration and its paginated query trace are supplied, require an explicit source/time/filter/identity binding to one enumerated query page before confirming; contradictory or missing page provenance is `Unknown`. Native-only or trace-only legacy evidence remains compatible.
- For a Global SP single-campaign query, optional adapter-retained native request filters and every page's request body must select exactly the same Sponsored Products / GLOBAL / campaign ID scope, with page continuation tokens matching the trace. Explicit contradictory or incomplete request evidence is `Unknown`; an opaque query fingerprint alone does not authenticate HTTP filters.
- For Global SP campaign queries, an optional source-attributed pagination trace must have a complete terminating nextToken chain, stable campaign/account/filter identity, consistent source, and post-write page timestamps; contradictory traces cannot be marked `Confirmed`. An explicitly supplied query-level source must also match the envelope/page source; missing or contradictory explicit lineage cannot confirm.
- For Global SP campaign updates, reject explicitly contradictory campaign/account/request identities in the HTTP 207 receipt before independently verifying per-marketplace configured-state readback; optional daily monetary-budget changes additionally require per-marketplace currency, amount, recurrence and independently complete budget readback. Explicitly supplied per-budget-row source, observation time, and account/campaign identity must also agree with the enclosing readback; a successful receipt is not a confirmed application.
- When a Global SP campaign configured-state or daily-budget readback includes raw marketplace IDs, require a complete, uniquely sourced raw-ID-to-country-code crosswalk and exact row binding; missing, duplicate or contradictory identity evidence returns `Unknown`. Country-code-only legacy evidence remains supported; this is not independent adapter authentication.
- When a trusted adapter retains a complete native Global SP campaign query resource in `readback.raw_campaign`, independently recompute marketplace configured states from top-level `state` and `marketplaceConfigurations` overrides; reject contradictions as `Unknown`. When a monetary-budget update is being verified and that native resource explicitly includes `budgets`, cross-check its per-marketplace daily monetary amounts, currencies and recurrence against the normalized budget rows; contradictions are `Unknown`, not false `Confirmed`. The adapter must preserve exact native budget numeric lexemes as decimal strings. Never derive configured state from `deliveryStatus`. Legacy normalized envelopes remain supported; raw query authenticity remains an external adapter responsibility.
- Do not interpret a Global SP campaign-state/budget `Confirmed` as verification of separate ad-group/target bid or placement changes: unsupported `expected_*` intent now returns `Unknown`, not false confirmation.
- Independently verify a **single Global SP ad-group** 207 update against complete native-currency marketplace **default-bid** query readback using `scripts/evaluate_global_sp_adgroup_bid_readback.py`; this is separate from campaign/target verification and never writes Ads.
- Independently verify a **single-call Global SP multi-ad-group batch** with `scripts/evaluate_global_sp_adgroup_batch_readback.py`: correlate every 207 index with one distinct ad-group request and independently complete native-currency marketplace default-bid readback for each success; Unknown/Partial/Drifted never become a blanket Confirmed. No Ads writes.
- Independently verify a **single positive Global SP keyword/product target** bid update with `scripts/evaluate_global_sp_target_bid_readback.py`: one marketplace, target-specific identity, native-currency bid, a bound 207 receipt and complete post-write query evidence. Never substitute ad-group default bid, campaign status, or an auction bid.
- Independently verify a **single-call Global SP positive-target batch** using `scripts/evaluate_global_sp_target_batch_readback.py`: bind every 207 index to its ordered target request, require unique target/request identities and exactly one independently complete query readback for each successful item; a mixed or incomplete batch never becomes Confirmed.
- Independently classify a **mixed-resource Global SP optimization plan** with `scripts/evaluate_global_sp_mixed_plan_readback.py`: a trusted complete plan manifest must bind every declared campaign, ad-group, target, or homogeneous batch component to its own readback verifier. Partial, drifted, unsupported or missing evidence cannot become a whole-plan `Confirmed`. The manifest is an external assertion, not an Amazon-native response or Executor reconciliation.
- Run recurring weekly reviews that preserve campaign mission instead of applying one universal ACOS rule to every campaign.

## Start here

Clone the repository, open the repository root in Codex, Claude Code, WorkBuddy or another file-capable agent, then run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

For setup, read [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md). For a broad account task start with `skills/amazon-ads-optimizer/SKILL.md`; for a narrow task select the matching Skill directly.

A useful bootstrap instruction is:

```text
Read the repository instructions first. Select the minimum Skill needed.
State the operating mode and missing evidence. Default to Suggest.
Do not infer missing data as zero and do not perform live Amazon Ads writes.
```

## How it works

```text
evidence
→ identity / lineage / coverage / connector checks
→ campaign objective + retail/economic context
→ observation
→ hypothesis
→ supported cause or unresolved uncertainty
→ guarded action / experiment / hold
→ external execution only when separately authorized
→ readback
→ outcome review + memory
```

The repository uses progressive loading: one selected `SKILL.md`, then only the references, schemas, playbooks and read-only helpers required by that decision.

## Capability map

| Need | Primary capability |
|---|---|
| Whole-account review | `amazon-ads-audit` |
| Multi-domain orchestration | `amazon-ads-optimizer` |
| Routine health / anomaly | `campaign-health-monitor`, `anomaly-detection` |
| Sustained decline diagnosis | `performance-drop-diagnosis` |
| Qualified growth headroom | `growth-opportunity-finder` |
| Controlled validation | `experiment-planner` |
| Post-change learning | `post-change-review` |
| Search terms / targeting | `search-term-analysis`, `keyword-optimization`, `negative-targeting` |
| Bid / budget / placement | `bid-optimization`, `budget-optimization`, `placement-optimization` |
| Profitability | `profitability-analysis` |

The catalog intentionally stays at 15 Skills. Composite operating procedures belong in `playbooks/`; shared decision contracts belong in `references/` and `schemas/`.

See [docs/CAPABILITIES.md](docs/CAPABILITIES.md) for the full capability and routing map.

## Safety boundaries

Core invariants:

```text
missing data ≠ 0
unsupported connector capability ≠ 0
unsupported report request ≠ metric zero
returned rows ≠ complete logical population
same metric label ≠ same measurement definition
configured control ≠ effective control
proposed ≠ applied ≠ readback confirmed ≠ worked
historical profitability ≠ marginal profitability
campaign role/objective ≠ inferable from one ACOS snapshot
```

Operating modes are `Read-only`, `Suggest`, `Shadow`, and externally authorized `Execute`. Credentials, OAuth/LWA, live writes, retry/idempotency and reconciliation stay outside this repository. See `AGENTS.md` and `references/decision-boundaries.md`.

## Documentation

- [docs/README.md](docs/README.md) — documentation index and audience map.
- [docs/CAPABILITIES.md](docs/CAPABILITIES.md) — what the 15 Skills can do and how they route.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — connector, lineage, memory, experiment, evaluation and runtime architecture.
- [docs/SOURCES.md](docs/SOURCES.md) — reviewed sources, licenses and adoption boundaries.
- [docs/research/](docs/research/) — dated research notes, including operator/community evidence.
- [evals/README.md](evals/README.md) — deterministic replay and effectiveness evaluation.
- `scripts/project_measurement_history.py` — bounded measurement-history projection.
- `scripts/evaluate_global_sp_readback.py` and `references/global-sp-readback-evidence.md` — read-only Global SP 207/per-marketplace readback gate (single-item campaign updates).
- `scripts/summarize_skill_effectiveness.py` and `schemas/skill-effectiveness-benchmark.json` — paired Skill-effectiveness measurement.
- [CHANGELOG.md](CHANGELOG.md) — release history.

## Contributing

Use pull requests and RED→GREEN for behavioral changes: prove the gap with a deterministic test/eval, implement the smallest useful change, run unit/Skill/eval validators, and inspect GitHub Actions. Popular repositories and community posts are discovery evidence, not authority; license, engineering quality, Amazon official semantics, duplication and action safety control adoption.

## License

Repository-owned code and Skills are distributed under [MIT](LICENSE). Amazon documentation and third-party projects retain their own copyrights and licenses.

## v2.12.0 — Partial scope claim integrity

- Measurement and comparison history now reject marketplace/profile scope claims without a concrete entity type/id.
- Missing scope remains missing; supplied partial/unresolved scope is not promoted to a usable identity.
- No live Amazon Ads writes, retries, idempotency, or reconciliation are introduced.

## v2.11.0 — Realization expected-scope placeholder integrity

- Realization history now rejects unresolved or padded `expected_scope` values before projection.
- Missing, unknown, partial, and unsupported scope values remain non-evidence and are never converted to zero or a usable identity.
- No live Amazon Ads writes, retries, idempotency, or reconciliation are introduced.
