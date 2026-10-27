# Unproven non-rule SP intervening arrays (v1.114.0)

A positive mid-window SP routing event with direct list fields or deeper list descendants, or an audience event with lists nested inside audience members, cannot certify collection completeness merely because `evidence_status=observed`. These arrays (including empty lists) return `Unknown` without independent proof; the current non-rule event contract has no such proof. Existing endpoint completeness helpers enforce the same conservative boundary. Scalar routing, flat audience and valid placement transitions remain compatible. This does not certify raw source identity, complete window capture or permission to write Ads.

# Optional paired SP rule-event descendant JSON Pointer evidence (v1.113.0)

Observed SP schedule/event/budget rule `control_events` may optionally supply `rule_descendant_collection_evidence` with `before` and `after` maps of RFC 6901 JSON Pointers rooted at the corresponding event-side state (for example `/schedule_rules/0/conditions`). Every list below the direct outer rule collection requires an independent Complete enumeration, Complete pagination and Supported capability declaration, including empty lists. The set of proof pointers must match the actual descendant lists exactly; missing, extra, malformed or one-sided proof is `Unknown`. An outer `rule_collection_evidence` declaration is required separately and cannot substitute for descendant evidence. Array indices and escaping follow JSON Pointer semantics per phase; a re-enumerated member order requires a corresponding independently verified pointer map.

Omitting descendant proof preserves the previous conservative `Unknown` for nested arrays, not an assumption that arrays were absent or complete. Flat rule events remain compatible. This repository-normalized read-only contract cannot authenticate an Ads API response, prove full-window capture, certify rule trigger execution or authorize live writes; any connector must independently establish the claimed source/pagination coverage.

# Unproven nested SP rule-event collections (v1.112.0)

A positive Sponsored Products schedule/event/budget `control_events` transition cannot certify nested arrays inside rule members merely because its outer `schedule_rules`, `event_rules` or `active_budget_rules` list has a Complete declaration. Endpoint snapshots already require independent JSON-pointer evidence for nested arrays; the current event schema has no descendant-proof contract. Any descendant list (including an empty list) within an observed rule member returns `Unknown`, with or without optional outer proof. Flat scalar rule members, valid top-level empty collections and legacy non-nested events retain their existing classifications. This conservative repository-owned read-side rule does not authenticate Amazon Ads history or prove full-window coverage; only an authorized external Executor may write.

# Optional paired mid-window SP rule collection completeness evidence (v1.111.0)

An observed `control_events` rule transition can optionally include `rule_collection_evidence` with independent `before` and `after` maps. For `schedule_or_event_rule`, both maps must cover `schedule_rules` and `event_rules`; for `budget_or_pacing`, both must cover `active_budget_rules`. Each collection requires `enumeration_status=Complete`, `pagination_status=Complete`, and `capability_status=Supported`, with no extra unmapped collection names. Explicit Partial/Truncated/Unsupported/Unknown, malformed, missing or one-sided proof returns `Unknown` rather than a confirmed confounder. A valid opt-in declaration allows the already validated observed transition; omitted proof retains legacy event compatibility but does **not** prove that the collection or the event history was exhaustive. The connector must independently authenticate underlying source records, pagination, revisions and time-window coverage. This is a repository-normalized read-side contract, not an Amazon Ads API field or permission to mutate accounts.

# Unmapped Sponsored Products placement dimension evidence (v1.110.0)

The repository-normalized SP placement state for a registered bid/budget causal review currently recognizes `top_of_search`, `rest_of_search`, `product_pages` and optional `amazon_business`. In both endpoint snapshots and positively observed mid-window `control_events`, an extra adapter field is not verified as a placement dimension, even when it repeats on both sides. Classify `Unknown`, not an observed confounder or isolated treatment. Preserve legitimate zero values, the optional Amazon Business boost and other material control types. This is a conservative repository-owned adapter contract, **not** a claim that Amazon can never introduce a new placement. Add dated source/adapter validation before extending the recognized set.

The check cannot authenticate the underlying Ads API response, certify a complete event history, prove continuous control stability or authorize writes. Keep source, metric, date, grain, identity, connector capability, competing controls and marginal economics distinct; only an external authorized Executor may mutate Ads accounts.

# Mid-window Sponsored Products rule activation evidence parity (v1.109.0)

A positive post-owned `control_events` transition can only compare optional rule activation metadata when the same `rule_id` is present in both its `before_state` and `after_state`. For `schedule_rules`, `event_rules` and `active_budget_rules`, require symmetric presence of `activation_status` and `activation_effective_at` on common rule IDs. A field present on only one side is unresolved evidence (`Unknown`), not proof of an activation transition or inactive/zero state. Reuse the endpoint parity helper; both-absent optional metadata, observed status/time changes and added/removed rule identities remain compatible. The latter do not by themselves establish full collection capture.

These are repository-normalized read-only fields, not Amazon API-native enums or an authenticated continuous event history. A positive event can expose a confounder, but empty/omitted event lists cannot prove that no competing control changed. Preserve source, metric, date, grain, identity, connector capability, causal confounders and marginal economics; only an external authorized Executor may write to Ads.

# Intervening event observation identity and same-instant transition consistency (v1.107.0)

When an adapter supplies optional positively observed post-owned `control_events`, each concrete `source.readback_id` denotes one observation instant across those event rows. Reusing that ID for different `event_at` instants, including a one-nanosecond difference, is contradictory evidence and returns `Unknown`. Compare known-offset RFC3339 instants in exact UTC time; offset-equivalent representations are compatible.

Within one decision scope, two rows with the same material `control_type` and exact `event_at` cannot assert different `before_state` or `after_state` transitions. For Sponsored Products rule/budget member lists, compare normalized identity-keyed members rather than row order. Conflicting simultaneous transitions return `Unknown`; identical duplicate rows with distinct event IDs and simultaneous transitions for *different* controls remain compatible. Do not require adjacent events to form a complete state chain: the event list is explicitly optional and non-exhaustive, so missing intermediate transitions cannot be inferred or ruled out. This is internal read-side consistency, not authenticated source history, continuous-control proof, an Amazon API event schema or live-write authority.

# Explicit nested null material-control evidence (v1.106.0)

A Complete/observed endpoint control or positively observed mid-window `control_events` cannot treat explicitly supplied JSON null inside a material-state object/list as a known value. Return `Unknown`, not `Treatment Isolated` or `Confounded`. Preserve measured zero/false, omitted optional dimensions, and optional null metadata outside `state`. This repository-owned conservative rule is not an Amazon API schema, full-window event capture proof, external authentication, or Ads write authority.

# Control-state comparability

## One-sided optional SP intervening budget evidence (v1.105.0)

For registered Sponsored Products bid/budget reviews, a positively observed mid-window `control_events` budget transition cannot compare an optional base/effective daily budget or average-daily-budget policy present on only one event side. Return `Unknown` rather than manufacturing a `Confounded` or `Treatment Isolated` judgment. On bid surfaces, both-absent optional fields remain legacy-compatible; budget-change surfaces still require the full budget state. Preserve the existing positively observed Amazon Business placement addition/removal as a confounder rather than misclassifying it as unknown. No full-window event coverage, API authentication or Ads write permission follows. A positive rule-change event may still be a confounder, but a record with one-sided budget amount or policy evidence is not a verified paired state. No source authentication, rule activation continuity or Ads write authority is implied.

## Intervening SP budget and routing state semantics (v1.104.0)

Positive mid-window `control_events` must carry usable budget and routing states before a change can support `Confounded` or `Treatment Isolated`. For SP budget-change decisions, each event-side `budget_or_pacing` state requires finite nonnegative base/effective daily budgets, a source-supported active-budget-rule list and a concrete policy label. SP bid-change decisions preserve legacy partial budget state shapes but reject any explicitly invalid budget amount/policy. `targeting_or_routing` events require the existing normalized site restrictions (`ALL_ELIGIBLE` or `AMAZON_BUSINESS`); optional retailer scope must be `AMAZON_STORE` or `ACROSS_RETAILERS`, present on both sides when used, and must not contradict Business-exclusive routing. Non-scalar labels are unresolved, not parser exceptions. This does not independently prove Amazon API eligibility, event stream completeness, actor identity or causal incrementality.

## Intervening Sponsored Products event state values (v1.103.0)

The optional post-owned `control_events` contract describes positively observed transitions, not arbitrary value changes. For registered Sponsored Products bid/budget causal surfaces, the comparator now checks event before/after base and video bid values for finite nonnegative numeric evidence, placement events for all three standard surfaces with usable modifiers (and usable Amazon Business modifier if present), audience events for stable unique IDs and nonnegative boosts, and bidding-strategy events for supported fixed/dynamic or rule-based guardrail states. Invalid event-only values return `Unknown` rather than manufacturing a `Confounded` or `Treatment Isolated` conclusion. Preserve valid decimal strings, zero, and rule-based strategy aliases. This does not prove source authenticity, continuous rule execution, complete event capture, or causal impact.

## Co-observed routing/placement event consistency (v1.108.0)

For registered Sponsored Products bid/budget reviews, an event `source.readback_id` shared by positive `targeting_or_routing` and `placement_adjustment` transitions binds their before/after states as one source observation. The same phase cannot claim `retailer_scope=ACROSS_RETAILERS` and an `amazon_business` placement modifier. Return `Unknown` for that internal contradiction rather than `Confounded`. Do not infer co-observation from coincident timestamps or separate/missing readback IDs. These are normalized repository control labels, not native Amazon API event schemas; neither an event list nor a readback ID authenticates complete control history.

## Observed intervening control events (v1.102.0)

Use optional post-owned `control_events` in `schemas/control-state-snapshot.json` only when the adapter has positively observed a material transition between the baseline and post readbacks. Each record must bind the same concrete campaign/account scope and source lineage, unique event identity, exact known-offset RFC3339 event time, registered material control type, and distinct source-supported before/after states. For registered SP rule controls, rule-member identity and modifiers must be usable. An observed competing event is `Confounded` even when it reverted before the post snapshot; unresolved evidence is `Unknown`. An event involving only the intended treatment does not substitute for an observed endpoint treatment change. An omitted or empty event list remains endpoint-only compatibility, **never** evidence of exhaustive capture or uninterrupted budget/rule/placement activation. The connector must independently authenticate its raw event stream, deduplicate/reconcile restatements and establish coverage before anyone claims full-window stability. No live Ads writes.


## N/A material state and member identity (v1.101.0)

A Complete, observed material-control snapshot still cannot certify a whole-label `N/A` or `Not Applicable` in a scalar, nested or list state. This includes normalized Sponsored Products `rule_id` and `audience_id` members: a repeated unavailable member label cannot prove stable competing controls. Return `Unknown` instead of `Comparable` or `Treatment Isolated`. Normalize whitespace, hyphen and underscore variants only for exact reserved labels; do not reject opaque IDs containing these substrings. Preserve genuine observed zero/false, valid control changes, and legacy optional fields. This is read-only internal consistency, not authenticated rule execution history or Ads write permission.


## Transition provenance under one readback (v1.100.0)

A reused concrete `source.readback_id` must not carry contradictory per-control `transition_provenance` (management mode, actor, actor-evidence status, reason, or transition-observed instant). One-sided provenance is unresolved. Compare supplied known-offset RFC3339 instants in exact UTC time, including nanoseconds. Return `Unknown`, not `Comparable`. Distinct readbacks, both-absent/null legacy provenance and offset-equivalent times remain compatible. This read-only consistency gate does not prove external actor identity, full-window rule execution, or authorize Ads writes.



## N/A and Not Applicable scope/source identity evidence (v1.99.0)

Whole-label `N/A` and `Not Applicable` are not observed marketplace/profile/campaign/entity/account/source/acquisition/connector identifiers. Normalize whitespace, underscores and hyphens only to recognize these reserved placeholders; do not reject real opaque identifiers merely because they contain those substrings. Repeated placeholders on both sides remain `Unknown`, never proof of unchanged scope or isolated treatment. Existing Unknown/Missing/Partial/Unsupported guards and valid IDs remain intact. This is a repository-owned read-only identity contract, not an Amazon API enum or external response authentication.

## Reused readback control evidence integrity (v1.98.0)

When baseline and post explicitly reuse the same concrete `source.readback_id`, require not only the same exact UTC `observed_at` and material state but also the same per-control `effective_at` instant and `evidence_status`. Compare effective times as known-offset RFC3339 UTC instants, preserving every fractional digit; a null/omitted effective time on only one side is unresolved. A changed effective time alone under **different** observation IDs does not prove a material state change. Legacy omitted/null readback IDs and equivalent timezone-offset representations retain compatibility. This is an internal consistency gate; no raw API authentication, full-window rule trace or live Ads write authority follows.

## Explicit readback identity and observation-time integrity (v1.97.0)

A supplied non-null `source.readback_id` must be a concrete unpadded observation identifier. Whole-label Unknown/Partial/Missing/Unsupported/Unavailable/Not Available/Not Supported/Not Applicable/N/A, blanks and non-string values cannot certify a control readback. If two snapshots reuse the same concrete ID, their `observed_at` must denote the same exact UTC instant, including submicrosecond fractions; different offset spellings of the same instant are compatible. Distinct valid IDs, omitted/null legacy IDs and unchanged same-instant snapshots remain compatible. This check is not external API response authentication, continuous rule-history evidence or permission to write Amazon Ads.

## Conflicting material states cannot share one readback identity (v1.96.0)

`source.readback_id` is an individual observation identifier, not a campaign, profile, connector or reporting-generation label. If baseline/post reuse one explicit non-null readback ID but report different material states, the comparator returns `Unknown` rather than claiming independent observations. Distinct IDs, omitted legacy IDs and unchanged states remain compatible. Different labels do not authenticate external source responses, time-window coverage or causal isolation.

## Normalized Sponsored Products rule-member order (v1.75.0)

In the registered Sponsored Products bid/budget causal comparator, `schedule_rules`, `event_rules`, and `active_budget_rules` are source-observed collections of unique concrete `rule_id` members. Once completeness and member validity are verified, an adapter's enumeration order does not itself represent a material control change. Compare those three lists as identity-keyed sets, preserving all member fields, activation status/effective timestamps, and added/removed identities. Do **not** apply this normalization to unrelated material lists or infer rule execution continuity, actual bid composition, feature entitlement or causal lift. An observed change in a rule's amount/status/time remains a competing control; malformed or incomplete evidence stays `Unknown`. See `docs/research/sp-rule-member-order-invariance-2026-10.md`.

Load this shared reference when a baseline/post-change, period-over-period, experiment, placement, bid, or budget conclusion depends on causal interpretation rather than descriptive movement alone.

Measurement comparability is necessary but not sufficient for causal comparability. Two windows can use the same source, reporting generation, metric definitions, attribution semantics, grain, and mature data while the active advertiser controls differ materially.

## Scope and source identity placeholders (2026-10-25)

Repeated unavailable labels in `marketplace_id`, profile/campaign/ad-group/entity identity, `entity_type`, explicit advertiser-account context or source/acquisition/connector identity cannot establish shared scope or lineage. Explicit blank or whitespace-padded IDs also fail closed. Both-absent optional legacy connector IDs remain compatible, but do not authenticate the source. Valid IDs remain usable. Amazon Ads MCP documents dynamic/fixed account context and explicit profile/advertiser/manager IDs (https://advertising.amazon.com/API/docs/en-us/mcp/get-started); Global Sponsored Products uses Global Account ID and per-marketplace scope (https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns). These are platform facts, not an Amazon API schema, eligibility proof or independent raw-response authentication.

## Campaign-bound Sponsored Products causal scope (v1.71.0)

For the registered `sponsored_products_bid_change` and `sponsored_products_budget_change` decision surfaces, a baseline/post pair must identify the same concrete `scope.campaign_id` as well as passing marketplace, profile/global-advertiser and source-lineage checks. A repeated missing or null campaign ID is not a verified shared campaign. Even a complete material-control inventory with an intended base-bid/budget change must return `Unknown` when both campaign IDs are omitted; one-sided/mismatched/unavailable IDs remain guarded. Real opaque IDs (including those containing words such as `unknown`) remain valid. This requirement is scoped to these two campaign-specific causal surfaces, not a blanket rule for all repository comparisons.

Amazon's [Global Sponsored Products campaign guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) distinguishes campaign IDs, ad groups, marketplace-specific configurations and account scope. It does not define this repository's normalized snapshot fields. A shared campaign identity still does not authenticate raw responses, prove rule execution throughout the window, isolate all economic confounders or authorize Amazon Ads writes.

## Explicit generic material-state placeholders

For every material control (including a registry-required control and any extra control), `coverage_status=Complete` and `evidence_status=observed` cannot turn a repeated explicit `Unknown`, `Unsupported`, `Partial`, `Missing`, `Unavailable`, `Not Available` or blank scalar string into a stable observation. The deterministic comparator rejects these reserved placeholders and non-finite numeric values even inside nested objects or independently complete lists, returning `Unknown` before claiming treatment isolation or comparability. It does not impute zero, False, absence or an ineligible capability. Genuine observed numeric zero, boolean switches, valid descriptive states and fully verified collections remain compatible. This narrow repository-owned guard is not an Amazon-native field schema, a connector authenticity proof, a complete validator for arbitrary domain-specific values, or a proof of continuous control activation.

## Control-state comparability gate

For each decision-relevant window, capture when supported and relevant: base/default/target bid state; campaign bidding strategy; placement bid adjustments; audience bid adjustment state; Sponsored Products video bid adjustment state when applicable; schedule/event bid rules; campaign/portfolio/account budget and pacing controls; targeting/negative/routing state; experiment/treatment assignment; and effective timestamps for material control changes.

When control evidence is exchanged between a Skill, connector, replay fixture, or reviewer, use `schemas/control-state-snapshot.json` as the machine-readable evidence envelope. A missing, unsupported, or stale control remains `unknown`; it must not be synthesized as zero, false, absent, or unchanged.

The snapshot must declare the decision-material control types expected and a coverage status. `Complete` is allowed only when every required control is represented by source-supported evidence. `Partial` or `Unknown` coverage is not evidence that omitted controls were absent.

### Control-state source provenance

A source envelope is required for each read-only snapshot. The comparator requires nonempty `source.source_system` and `source.acquisition_channel` on both sides and does not assume cross-source or cross-acquisition equivalence without an explicit, verified lineage-mapping contract (which this snapshot schema does not currently carry). If `source.connector_id` is supplied on either side, both sides must provide the same nonempty connector identity. Absent connector IDs on both sides remain compatible with legacy snapshots. `source.readback_id` identifies a particular readback and may differ between baseline and post; it is not a source identity. Missing or mismatched source provenance yields `Unknown`, never a fabricated zero or a claim of treatment isolation.

### Global Sponsored Products account identity

Amazon's Global Sponsored Products campaign-management APIs use a Global Account ID in the `Amazon-Ads-AccountId` header rather than the legacy profile-scope header. A profile ID must therefore not be fabricated merely to populate a control-state snapshot. The optional `scope.account_identity` envelope permits a profile-less snapshot only when an explicit `global_advertiser_account_id` and the decision marketplace are present. Legacy profile-scoped snapshots remain valid.

For read-side comparisons, matching `marketplace_id` and matching control values are insufficient when explicit advertiser identities disagree. Compare any provided global, regional, legacy, advertiser, regional-profile, manager and country identity fields; missing or conflicting values fail closed to `Unknown`. An account-identity envelope on only one side is not proof of equivalence. If an envelope is present, require a shared, nonempty, matching strong advertiser/profile identifier. Identity mapping provenance may be retained, but does not automatically establish equivalence between distinct identifier generations. Profile-less Global SP evidence requires the same explicit Global Account ID on both sides. Do not compare one profile-scoped snapshot with one profile-less snapshot by inference.

This is a read-only evidence envelope, not an Amazon API payload, eligibility assertion or connector capability claim. It does not prove that a global campaign's marketplace-specific budget, bid, state, reporting or currency settings are identical. Preserve those dimensions and verify the active acquisition path separately. No Ads write, retry or reconciliation is performed by this comparator.

Source: Amazon Ads Global Campaigns API guide (reviewed 2026-10-23): https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns . Platform facts are independently paraphrased; no Amazon source code, examples, prompts or schemas are reused.

### Collection-valued control evidence

When a registry-required control is represented as a top-level list, the list contents alone do not prove that the control state is complete. This applies to both empty and non-empty lists: one returned row/page is still partial evidence when additional rows may exist.

A list-valued required control is decision-complete only when its machine-readable `collection_evidence` establishes all three conditions:

- `enumeration_status=Complete` — the source/connector completed the decision-relevant enumeration;
- `pagination_status=Complete` — no unresolved continuation, row cap, or truncation remains;
- `capability_status=Supported` — the active acquisition path supports that control collection at the required scope.

`Partial`, `Truncated`, `Unsupported`, `Unknown`, or missing collection evidence fails closed to `Unknown`, even when the returned list is non-empty. A verified empty list is therefore distinct from an unknown empty list, and a non-empty partial list is distinct from a complete collection.

Every material control explicitly present in a snapshot participates in the comparison, including controls beyond the registry-required minimum. A present extra control with null/missing state is not evidence of an unchanged value. A present extra list-valued control needs the same independently verified enumeration, pagination and capability completeness as a required list; otherwise the comparison is `Unknown`. A complete, observed extra control remains compatible with normal comparisons. This prevents extra material evidence from being silently laundered into comparability.

This generic gate applies to every material control, whether required by the registry or additionally observed. For any object-valued `state`, each direct list-valued field requires matching `nested_collection_evidence` with independently Complete enumeration, Complete pagination and Supported capability, even for empty lists. This includes `budget_or_pacing.state.active_budget_rules` during Sponsored Products **bid** reviews as well as budget reviews; the registry requirement and a complete parent object do not prove the child list was fully observed.

For every material control, list-valued descendants at any depth of a structured `state` (including lists inside objects or array elements) require independent completeness evidence. Keep the existing direct-field evidence key for first-level lists (for example `rules`); use an RFC 6901 JSON Pointer rooted at `state` for deeper lists (for example `/policy/rules` or `/policies/0/overrides`). Escape `~` as `~0` and `/` as `~1` in object keys. Each list, including an empty one, needs its own `nested_collection_evidence` entry with Complete enumeration, Complete pagination and Supported capability. Parent completeness never proves a child list complete. This also applies when the control's **top-level `state` is itself a list**: `collection_evidence` proves only that root list, while every list inside its elements needs separate `nested_collection_evidence` under a pointer such as `/0/rules` or `/0` for a nested array. Flat root lists remain valid with root completeness alone. The same rule now applies to **registry-required object controls** (for example routing and placement state), not only extra material controls or registry-required top-level lists. Unknown evidence yields `Unknown`, not zero or unchanged.

For structured controls that contain decision-material nested lists, completeness is recorded separately in `nested_collection_evidence`, keyed by the nested state field. Sponsored Products causal comparisons currently require this for:

- `schedule_or_event_rule.state.schedule_rules`;
- `schedule_or_event_rule.state.event_rules`;
- `budget_or_pacing.state.active_budget_rules` in Sponsored Products bid or budget causal reviews.

Each required nested list must independently prove `enumeration_status=Complete`, `pagination_status=Complete`, and `capability_status=Supported`. One nested surface cannot launder another: complete event-rule evidence does not prove schedule-rule completeness, and a non-empty budget-rule list does not prove that all active rules were observed. Missing, partial, truncated, unsupported, or unknown nested evidence fails closed to `Unknown`.

### Versioned requirement provenance

`references/control-requirement-registry.json` is the repository-owned, versioned authority for `decision_surface -> required_control_types`. A snapshot with `derivation_status=Verified` must name its `requirement_registry_id`, and that identity plus the decision surface must resolve to the exact required set in the registry. An unknown/stale registry identity, an unregistered decision surface, or a snapshot-required set that differs from the registry fails closed to `Unknown`.

Connector capability is deliberately separate. Capability evidence answers whether a required control can be observed; it never decides whether the control is required. Connector non-support therefore reduces coverage rather than shrinking the registry-derived requirement set. This prevents a connector or agent from manufacturing `Complete` by omitting a control it cannot read.

The registry should remain narrow and evidence-backed. Add production decision surfaces only when Amazon official semantics or equivalent high-confidence evidence show that the listed controls are decision-material. Unknown surfaces remain `Unknown`; do not infer a nearest surface. Registry changes require regression evidence because they alter the causal proof boundary.

The schema is an evidence contract, not an Amazon API response schema and not an execution payload. It does not require a connector to expose controls it cannot read; unsupported controls instead prevent a false completeness claim.

Optimization identity is type-bound as well as ID-bound. When `scope.entity_id` is populated, `scope.entity_type` must identify the semantic namespace/kind represented by that ID. This matters when reporting surfaces normalize distinct targeting entities into a shared identifier field; the same identifier value without its entity type is not sufficient evidence of the same optimization entity. Baseline/post snapshots with a missing or changed entity type must fail closed to `Unknown`.

When two schema-valid snapshots are available, `scripts/compare_control_state.py` provides a deterministic, read-only first-pass classification. It fails closed to `Unknown` for marketplace/profile mismatch, incomplete/unknown material-control coverage, unverified requirement provenance, missing/unknown/stale registry identity, unregistered decision surface, registry mismatch, required controls absent from either snapshot, changed expected-control sets or decision surfaces, stale/unsupported/unknown evidence, or changed controls without effective timestamps. With an explicitly named intended treatment, it returns `Treatment Isolated` only when that treatment changed inside a complete, registry-verified material-control set and no other evidenced material control changed; overlapping evidenced changes are `Confounded`. Without an intended treatment, stable evidenced controls are `Comparable` and changed controls are only `Directional`.

Control timestamps are decision-time evidence, not arbitrary labels. The comparator requires parseable timezone-aware RFC3339 `observed_at` and rejects any supplied malformed/ambiguous-offset `effective_at` or an effective instant later than the snapshot observation. UTC offsets and fractional seconds beyond microseconds are compared as actual instants. A missing `effective_at` on an unchanged control remains distinct from a fabricated timestamp; an evidenced change still requires effective timestamps. These checks do not by themselves prove who initiated a change or establish marketplace-wide Global SP control equivalence. A post-change snapshot observed before its baseline is not a forward causal comparison, even when control values are identical; compare their UTC instants including offsets and submicrosecond fractions and return `Unknown` on reversal. Equal observation instants remain permitted for synthetic/same-time evidence but do not themselves establish a causal elapsed interval.

Do not invent an auction-level composition formula from configured controls. Treat them as a control graph whose realized effect is observed through delivery, CPC, traffic mix, placement/audience/video mix, conversion, and economic outcomes.

## Sponsored Products Amazon Business placement evidence

Amazon Ads help updated 2026-09-28 lists **Amazon Business placements** as a distinct Sponsored Products bid-adjustment surface in addition to Top of Search, Rest of Search, and Product Pages. It also notes that Sponsored Products across-retailers campaigns cannot adjust bids for Amazon Business placements. Preserve this as a separate configured control dimension; do not add it to ordinary placement reporting totals or infer a universal account/marketplace eligibility rule.

For the existing read-only SP bid/budget causal comparator, an explicitly supplied `placement_adjustment.state.amazon_business` is validated as a finite nonnegative numeric value (or plain decimal string). Unknown/Unsupported/Partial, booleans, non-finite/negative values, percent strings and structured placeholders cannot prove stability. If only one snapshot provides the field, the comparison is `Unknown`; a genuine numeric change is a placement-control confounder. Both snapshots omitting the field remain **legacy-compatible**, but this does **not** prove Amazon Business capability, absence, or a zero modifier. A source/connector-supported capability-and-eligibility contract is still required before claiming B2B-complete causal coverage. Keep Amazon Business exclusive-campaign site routing under `targeting_or_routing`, not under this bid modifier.

Sources: Amazon Ads, *Adjust Sponsored Products bids*, updated 2026-09-28, https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5 ; Amazon Ads, *Advertising on Amazon Business*, https://advertising.amazon.com/channels/amazon-business . Repository-authored guard only; no copied API schema or platform formula.

### Optional retailer-scope consistency for Amazon Business controls (v1.53.0)

When an adapter explicitly supplies `targeting_or_routing.state.retailer_scope` in a registered Sponsored Products bid/budget causal comparison, accept only repository-normalized `AMAZON_STORE` or `ACROSS_RETAILERS`. The field must be present in both snapshots or neither; one-sided presence is `Unknown`, not a proven retailer transition. A complete inventory and identical strings do not make an unmapped retailer label valid.

A snapshot with `ACROSS_RETAILERS` cannot simultaneously substantiate `placement_adjustment.state.amazon_business` (even observed numeric `0`) or Amazon Business-exclusive `site_restriction=AMAZON_BUSINESS`; such internally contradictory evidence is `Unknown`. A real, consistently observed change between supported retailer scopes remains a competing routing control (`Confounded`). Both-absent legacy retailer scope remains compatible **without** proving B2B eligibility or an absent modifier. A valid `AMAZON_STORE` label is not proof of marketplace/account/campaign eligibility, connector coverage, native API enum mapping or actual delivery. Mixed retailer/ad-group contexts need a separately verified adapter contract, not a guessed label.

Amazon Ads references: https://advertising.amazon.com/solutions/products/sponsored-products-across-retailers ; https://advertising.amazon.com/en-us/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product/ ; https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5 (prior dated platform review). No native API schema or third-party code reused.

## Sponsored Products video bid adjustment

For the registered Sponsored Products bid/budget causal surfaces, the read-only comparator requires `video_bid_adjustment.state` to be a finite, nonnegative observed number or plain decimal string. Explicit zero is valid; missing/Unknown/Unsupported/Partial, booleans, negative/non-finite numbers, percentage-formatted strings and structured placeholders are not valid observed video-boost values. Repeating an unknown value on both sides cannot prove an unchanged control. This is a local evidence guard, not an Amazon-native API field definition, marketplace eligibility proof, or universal platform bid-boost ceiling. Amazon's Sponsored Products video guide states that video-specific bid boosts can stack on top of other placement adjustments; preserve them as separate controls.


Amazon currently exposes a distinct Sponsored Products video bid adjustment that can combine with other bid modifiers. For registered Sponsored Products bid/budget causal surfaces, preserve `video_bid_adjustment` as a separate material control rather than folding it into placement or creative metadata.

- A source-supported zero/no-boost state is different from missing or unsupported evidence.
- Connector non-support, ineligible scope, or unknown availability must remain `Unknown`/partial coverage rather than being coerced to zero.
- If video bid adjustment changes in the same comparison window as base bid, placement, audience, budget, or another intended treatment, treat the causal review as confounded unless an explicit design separates the effects.
- Verify current marketplace/category/control availability through platform-capability lineage; the control registry records materiality, not universal eligibility.

## Sponsored Products budget-change state

For `decision_surface=sponsored_products_budget_change`, generic evidence that a campaign has a budget is not enough. The repository-owned `budget_or_pacing.state` must preserve at least:

- `base_average_daily_budget` — the source-supported configured average daily budget;
- `effective_daily_budget` — the budget actually in force for the decision window after applicable automated budget rules;
- `active_budget_rules` — source-supported rule evidence for that window. An empty list means the source positively observed no active rules; connector non-support or missing rule evidence remains unknown and must not be encoded as `[]`.

Amazon currently documents schedule-based and performance-based Sponsored Ads budget rules that can automatically raise daily budgets, with multiple applicable rules able to combine. Amazon also documents Sponsored Ads daily budgets as average daily budgets whose day-level spend can vary under the account policy. Therefore configured budget, effective budget, observed spend, and rule state are distinct evidence. A day where spend exceeds the configured average daily budget is not by itself proof of a manual budget edit, policy breach, or executor action.

The deterministic comparator applies this stronger structured-state check only to the registered Sponsored Products budget-change surface. If base/effective budget or active-rule evidence is missing, the comparison fails closed to `Unknown`. This does not model Amazon's budget-rule implementation and does not authorize any write.

## States

- `Comparable` — no decision-material control difference outside the intended treatment/change.
- `Treatment Isolated` — intended control changed and other registry-required controls are sufficiently stable.
- `Directional` — material controls changed without an identified isolated treatment.
- `Confounded` — overlapping material controls can plausibly explain the observed effect.
- `Unknown` — required state, coverage, requirement provenance, registry resolution, or timestamps are unavailable, stale, unverified, or unsupported.

`Unknown` is not unchanged state. Missing connector support is not evidence that a control was absent.

### JSON state type identity

The read-only comparator compares material-control `state` as JSON values, not Python's coercive boolean/number equality. In JSON, `false` is not numeric `0`, and `true` is not numeric `1`; the same distinction applies inside objects and complete collections. Such differences are material observed changes, not proof of unchanged controls or isolated treatment. Equivalent numeric representations such as `0` and `0.0` remain compatible when their numeric values match. Missing, stale, unsupported, or unverified control evidence is still `Unknown` under the existing gates; this comparison never fabricates a state or performs Ads writes.

## Control state is not transition provenance

A source-supported current control value proves the observed state, not who caused the latest transition. This distinction is material when Amazon can manage, curate, pause, add, remove, or otherwise change a decision-relevant state without a matching advertiser or external-Executor write.

When the source exposes it, preserve the optional `transition_provenance` block from `schemas/control-state-snapshot.json`:

- `management_mode` — `advertiser_managed`, `platform_managed`, `hybrid`, or safe `unknown`;
- `last_transition_actor` — source-supported advertiser, external Executor, Amazon platform, other authorized actor, or `unknown`;
- `transition_reason` and `transition_observed_at` when explicitly exposed;
- `actor_evidence_status` — observed/derived/unsupported/unknown.

Do not infer missing provenance from the final state, an empty local change ledger, a successful prior readback, or the absence of a connector-visible write. A complete Executor ledger proves only the writes represented by that Executor; it is not proof of complete platform-wide mutation history.

Amazon currently provides a concrete provenance precedent in automatic deal selection: platform-managed inventory groups can be identified with `curationSourceType=AMAZON_CURATED_AGENT`. Amazon also documents product surfaces whose eligibility can automatically alter lifecycle state, including Review Requests auto-pausing at its review threshold. These are product-specific examples of the generic rule; do not assume the same field or behavior exists for every Amazon Ads product.

When a source-supported connector is involved, require `entity-state-readback` to prove the decision-needed `required_transition_provenance_fields` via the shared capability gate before claiming an actor or reason. The gate does not substitute for event-time provenance: its supported status and exposed-field list are not proof of who actually changed this instance.

If a causal conclusion depends on who changed a control and actor/reason provenance is unavailable, keep authorship `Unknown` and downgrade the dependent single-action claim to Directional/Hold/Manual Review as appropriate. State comparability and transition authorship are separate questions: two snapshots can prove that state changed while still failing to prove who changed it.

## Causal rule

A post-change or experiment conclusion must not be more causal than the weaker of measurement comparability and control-state comparability. If baseline and post-change windows differ in placement adjustment, audience bid adjustment, video bid adjustment, bidding strategy, schedule/event rule, budget/pacing state, or traffic-routing controls beyond the intended treatment, downgrade a single-control causal claim unless a valid design or reconciliation separates the effects.

## Unified reporting boundary

Amazon Ads Unified Reporting can combine dimensions such as campaign, placement, and audience and standardize metrics across ad products. That improves measurement access; it does not prove that advertiser control state was stable between compared windows.

## Decision use

Before `Worked`, `Failed`, aggressive scale, rollback, or precise marginal-effect claims: verify intended change/readback; verify measurement comparability; resolve the decision surface against `references/control-requirement-registry.json`; use connector capability only to determine observability; reconstruct material control timelines with source/effective timestamps; run `scripts/compare_control_state.py` when two snapshots exist; identify binding/overlapping controls; inspect traffic and economic outcomes; downgrade causal language when isolation is unsupported; and prefer a clean validation window when confounding remains material.

This reference is read-only. It does not authorize Amazon Ads writes; execution, retry, idempotency, and reconciliation remain external Connector/Executor concerns.

## Sponsored Products budget value evidence (v1.46.1)

For sponsored_products_budget_change, base_average_daily_budget and effective_daily_budget must be source-supported, finite, nonnegative monetary observations (JSON numbers or plain decimal strings). Booleans, negative/non-finite amounts, structured placeholders, and Unknown/Unsupported strings are not observed budget values. The average_daily_budget_policy must be a nonempty, source-supported policy label, not Unknown, Unsupported, Partial, Missing or Unavailable. An arbitrary structured policy object requires a separately verified contract and is not accepted as policy proof. Invalid values yield Unknown before causal isolation, including when both snapshots repeat the same placeholder. Explicit numeric zero is distinct from missing evidence, and is never inferred from it. This is a local read-only evidence rule, not an Amazon API schema or account write permission.

## Sponsored Products placement value evidence (v1.46.2)

For the registered Sponsored Products bid-change and budget-change causal surfaces, each required `placement_adjustment.state` value (`top_of_search`, `rest_of_search`, `product_pages`) must be a finite nonnegative numeric observation (JSON number or plain decimal string). `Unknown`, `Unsupported`, `Partial`, missing/empty, boolean, negative, non-finite and structured placeholders are not stable modifiers, even when repeated on both sides of a comparison. An explicit observed numeric `0` is valid and is never inferred from missing capability. This numeric evidence gate is not a claim that a particular modifier is eligible, within the current marketplace-specific maximum, or that the resulting auction bid can be calculated from configuration alone; those are separate platform-capability and control-interaction checks. The comparator remains read-only.

## Sponsored Products base-bid numeric evidence

For `sponsored_products_bid_change` and `sponsored_products_budget_change`, the read-only comparator requires `base_bid.state` to contain source-supported finite, nonnegative numeric evidence or a plain decimal string. Status placeholders (Unknown, Unsupported, Partial), booleans, negative/non-finite numbers, percentage strings, arrays and structured placeholders fail closed to `Unknown`, including when repeated unchanged across windows. This is a data-validity boundary, not proof that a particular zero or bid meets marketplace/account limits. Platform eligibility, currency/units, realized auction exposure and causal outcomes remain separately evidenced. No live Ads writes are performed.

Sources: Amazon Ads, *Best practices for your Sponsored Products ads*, https://advertising.amazon.com/en-ca/library/guides/sponsored-products-best-practices (checked 2026-10-25); *A guide to targeting with Sponsored Products*, https://advertising.amazon.com/en-gb/library/guides/targeting-with-sponsored-products (checked 2026-10-25). Only platform concepts paraphrased; guard implementation independently authored.


### Sponsored Products audience-member evidence (2026-10-25)

For registered SP bid/budget causal surfaces, audience_bid_adjustment.state is a source-supported fully enumerated list. A verified empty list is valid only with Complete enumeration, pagination and Supported connector capability. A nonempty list also requires each repository-normalized member to have a unique, nonblank string audience_id and a finite nonnegative observed numeric bid_boost (JSON number or plain decimal string). Duplicate IDs, missing IDs or boosts, booleans, status placeholders, percentages, negative/non-finite values and malformed members return Unknown, even when repeated in both snapshots. Valid member/boost changes remain audience-control confounders, not evidence of improved outcomes.

This is a repository-owned normalized readback contract, not a copied Amazon Ads API schema. Official Sponsored Products guidance supports distinct per-audience bid boosts, but does not authenticate adapter data or establish universal marketplace eligibility or exact bid limits. Preserve source, identity, observation time and connector capability; never infer zero from an absent audience row.


### Sponsored Products bidding-strategy evidence (2026-10-25)

For registered Sponsored Products bid/budget causal comparisons, `bidding_strategy.state` must be a source-supported repository-normalized string naming a known strategy family: `dynamic_down_only`, `dynamic_up_and_down`, `fixed`, or `rule_based` (hyphen spelling also accepted). Unknown, Unsupported, Partial, Missing, empty, numeric, boolean, structured and unrecognized values return `Unknown` even when repeated across snapshots. A verified change between known strategy families remains a competing control (`Confounded` when another control is the intended treatment). These are **local evidence labels, not asserted Amazon-native API enum tokens**; a new strategy requires official verification and an explicit adapter mapping rather than silent acceptance. This check does not prove marketplace eligibility, rule configuration, realized auction exposure or causal outcomes.

Source: Amazon Ads, *Bidding strategies for Sponsored Products*, updated 2026-09-28, https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7 . Independently authored read-only evidence guard; no vendor schema or example copied.

## Sponsored Products rule-based bidding guardrail evidence

Amazon Ads distinguishes rule-based bidding with a campaign ROAS guardrail from schedule/event bid rules. In the registered Sponsored Products bid/budget causal comparison, the three simple normalized bidding strategy families (`dynamic_down_only`, `dynamic_up_and_down`, `fixed`) remain source-supported string labels. A rule-based strategy requires an object-valued `bidding_strategy.state` with exactly `{"strategy":"rule_based","roas_guardrail":3}` (example), where `roas_guardrail` is a finite strictly positive observed ROAS ratio, represented by a JSON number or plain decimal string. The hyphenated `rule-based` strategy alias is also accepted inside this object. A bare `rule_based` string, missing/Unknown/Unsupported guardrail, boolean, zero, negative, non-finite, percent-formatted or structured placeholder, or additional unverified rule fields returns `Unknown`, never inferred zero or unchanged. When two complete snapshots have different guardrails, `bidding_strategy` is a competing changed control (`Confounded` for another intended treatment).

This is a repository-owned normalized read-side contract, **not** an Amazon API enum, a write schema, or proof of campaign rule activation, eligibility, historical rule execution or realized auction bids. The existing `schedule_or_event_rule` collections cannot stand in for a rule-based ROAS guardrail. If the connector cannot expose the guardrail, retain Unknown and hold a causal-isolation claim. Official basis: https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7 (updated 2026-09-28), https://advertising.amazon.com/library/guides/budget-rules/ (reviewed 2026-10-25).

## Sponsored Products site-routing evidence (v1.48.1)

A complete material-control inventory is not proof that the campaign's site restriction was actually observed. For registered Sponsored Products base-bid and budget causal comparisons, the repository-normalized `targeting_or_routing.state` must be an object with a source-supported `site_restriction` mapped to either `ALL_ELIGIBLE` (eligible-site routing as reported by the adapter) or `AMAZON_BUSINESS` (Amazon Business-exclusive routing). Missing, Unknown, Unsupported, Partial, null, booleans, numeric placeholders, whitespace-padded and unmapped strings fail closed to `Unknown`, even if repeated in both windows. A verified routing change is a separate confounder. Other routing collections still require independent completeness proof; this check does not override those gates.

Amazon Ads documents Amazon Business-exclusive Sponsored Products campaigns with a distinct site restriction and advertiser/marketplace eligibility (launch 2025-10-31): https://advertising.amazon.com/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product . These two labels are independently authored **read-side normalization**, not a copied API schema, not exhaustive native site enums and not evidence that the adapter actually observed the campaign. A new retail/site mode requires an explicit verified adapter mapping rather than a guessed default. Site routing, B2B placement bid boost, marketplace/campaign eligibility, connector capability, platform-managed delivery and realized traffic mix remain distinct evidence. No Ads writes or external Executor operations.

## Sponsored Products schedule/event/budget rule member evidence

For registered SP bid/budget causal reviews, Complete enumeration, pagination and Supported capability prove only the **rule collection**, not each member. The repository-normalized read-side contract requires each nonempty `schedule_or_event_rule.state.schedule_rules` and `.event_rules` member to have a unique nonblank `rule_id` and a finite nonnegative observed `bid_increase`. Each nonempty `budget_or_pacing.state.active_budget_rules` member needs a unique nonblank `rule_id` and finite nonnegative observed `increase_percent`; this member check applies even when the intended treatment is a **base-bid** change. Plain decimal strings and explicit numeric zero are accepted as observations; Unknown, Unsupported, Partial, missing IDs/modifiers, booleans, negative/non-finite numbers, percentages-as-strings and malformed members yield `Unknown`. Complete, source-supported empty lists remain valid, and genuine member changes remain confounders.

These are independently authored normalized evidence keys, **not** Amazon Advertising API field names or a claim that every rule type is expressible by these two numeric fields. A connector unable to map its rule variant must return incomplete/Unknown evidence rather than fabricate a rule or zero. Validating member identity/modifier does not prove activation, effective schedule, trigger state, exact bid composition, marketplace eligibility, API authenticity or incremental performance. Official basis: [Amazon schedule-based bid rules (2023-11-06)](https://advertising.amazon.com/en-us/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products/), [event-based bid rules (2025-01-02)](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers). No Ads writes or Executor behavior.


## Optional Sponsored Products rule activation status evidence (2026-10-25)

The normalized read-side schedule/event bid-rule and active budget-rule member may include `activation_status`. When explicitly supplied it must be exactly `active`, `inactive`, or `scheduled`, based on a documented adapter mapping. A repeated `Unknown`/`Unsupported`, boolean, null, numeric or unrecognized status is not a stable competing control. For a shared `rule_id` present in both snapshots, one-sided presence of this optional status returns `Unknown` rather than treating absence as `inactive`. A verified status transition remains a competing changed control; verified empty collections retain their prior meaning.

Both-absent legacy fields remain accepted for compatibility, **not** as evidence that the rule was inactive or that its schedule was fully observed. A status observed at two instants does not prove continuous execution, event eligibility, time-zone alignment, or absence of intervening triggers across the comparison window. Those claims require separately source-supported temporal/connector evidence. This is repository-owned normalization, not an Amazon Ads API enum or a write contract.

Official factual background: https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products (2023-11-06); https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers (2025-01-02). No official API schema or vendor implementation was copied.


## Optional Sponsored Products rule activation transition-time evidence (2026-10-25)

A normalized schedule/event/active-budget rule member may additionally carry `activation_effective_at`, an optional source-supported transition instant paired with `activation_status`. If supplied, it must be a timezone-aware RFC3339 timestamp at or before that snapshot's `observed_at`; a future, malformed, null, Unknown/Unsupported or status-less value is `Unknown`. A common `rule_id` cannot have this field on only one side. A real transition-time change remains a material competing-control change, even if the two status labels are the same.

Both-absent legacy timestamps remain compatible and do **not** establish that rules were inactive or continuously active between observations. A valid last-transition timestamp is not proof of complete schedule windows, time zones, event triggers, eligibility or actual execution. The field is repository-owned read-side normalization, not an Amazon-native API schema, an execution instruction or independent connector authentication. See official [schedule-based bid rules](https://advertising.amazon.com/en-us/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products/) (2023-11-06) and [event-based bid rules](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) (2025-01-02).

## Unproven extra direct arrays in SP rule events (v1.115.0)

An observed mid-window SP schedule/event/budget rule event may have a paired `rule_collection_evidence` envelope. That envelope covers only the registered outer lists: `schedule_rules` and `event_rules` for bid rules, or `active_budget_rules` for budget rules. It does not cover an additional sibling array in the same `before_state` or `after_state`, including an empty array or one repeated unchanged on both sides. The existing descendant JSON Pointer contract covers lists *inside* rule members, not extra sibling collections. Such unproven extra direct lists now yield `Unknown`, not a verified confounder. Valid rule lists, scalar additional evidence and legacy flat events remain compatible. No event-log completeness, raw Amazon Ads provenance or write authority is implied. See `docs/research/intervening-sp-rule-extra-direct-list-2026-10.md`.
