# Changelog

This file records user-visible repository releases. The canonical current version is stored in `VERSION`.

## v1.26.0 — 2026-10-24

### Safety

- Fail closed on descendant lists inside a top-level list-valued extra material control. Root `collection_evidence` alone cannot prove completeness of `state[0].rules`, `state[0]` when it is a list, or any deeper list. Require independent RFC 6901 `nested_collection_evidence` per descendant, with Complete enumeration, Complete pagination, and Supported connector capability.
- Preserve flat complete root lists, object-root legacy direct-list keys, complete descendants, isolated/confounded treatment classification, and all 15 Skills. The comparator remains read-only; no Amazon Ads execution, retry, credential, or connector mutation capability is introduced.

### Verification

- RED: commit `cee188266af0c3f3898f8b0c5c0b3fee99d2e461` failed 6 of 530 deterministic unit tests in GitHub Actions `39989044504` (old code incorrectly returned Comparable for unverified root-list descendants).
- GREEN: commit `58b22c6c25fdd75db314e30c2709f6d2de392228` passed 530 unit tests and both Skill/Eval validators in GitHub Actions `39989177279`. Release PR HEAD and merged main require their own latest required-check verification.

### Sources and copyright

- Independently derived from this repository's existing control-state completeness contract and synthetic regressions. Official Amazon Ads platform documentation remains contextual; no third-party code, prompts, schemas, workflows or templates were copied. No duplicate SOURCES entry or new dependency was added.

## v1.25.0 — 2026-10-23

### Safety

- Fail closed on deep list-valued descendants of an extra material control, including lists inside nested objects or elements of already-verified parent lists. Require per-list source-supported Complete enumeration, Complete pagination and Supported connector capability. Direct list keys remain backward compatible; deep paths use RFC 6901 JSON Pointer.
- Preserve complete nested evidence, JSON Pointer key escaping, isolated/confounded treatment classifications and all 15 Skills. No live Amazon Ads write, retry, executor or credential capability was introduced.

### Verification

- RED: commit `cab5df09651e07ceb149bea130cc552fd0d905e2` failed 7 of 517 unit tests in Actions `39980796062` (old comparator incorrectly returned Comparable for incomplete deep lists).
- GREEN: commit `642b771d88ed518969ee7497f1f28ed3e210cf58` passed all 517 unit tests plus Skill and Eval validators in Actions `39980927430`. Latest release PR HEAD and merged main require independent required-check verification.

### Sources and copyright

- The behavior is independently derived from this repository's existing snapshot evidence contract and deterministic failure cases. Official Amazon Global SP documentation is platform context only; no third-party code, prompts, schemas, workflows or templates were copied. Existing source reviews were not duplicated.

## v1.24.0 — 2026-10-23

### Safety

- Fail closed when a material control beyond the versioned required set carries a direct nested list-valued state field without its own verified enumeration, pagination and connector-capability evidence. An empty or nonempty returned list does not establish complete readback.
- Preserve complete nested lists, scalar extra controls, and isolated/confounded treatment distinctions. This only changes read-only control-state evidence classification; it does not add Amazon Ads write, retry, or executor authority.

### Verification

- RED: commit `12bafb677810a8347006f59220efa95cdf703ce7` failed 7 of 504 deterministic unit tests in GitHub Actions `39972265204` (old behavior incorrectly returned Comparable).
- GREEN: commit `1414ac95e419d0b96a9c035b75b20a89c3ec1c4f` passed all 504 unit tests, 15-Skill validator and 55-eval validator in GitHub Actions `39972418888`. Release PR HEAD and merged main require separate green checks.

### Sources and copyright

- Independently derived from this repository's existing snapshot schema, nested-collection evidence contract and comparator. No third-party code, prompts, schemas, workflows, or templates copied. Amazon Ads official documentation remains platform context, not an assumed connector capability.

## v1.23.0 — 2026-10-23

### Safety

- Compare material-control JSON state without Python's boolean/numeric equality collision: `false` is distinct from `0`, and `true` is distinct from `1`, including inside nested objects and verified-complete collections.
- Prevent an unobserved boolean-to-numeric state change from being labeled `Comparable` or incorrectly isolating another treatment. Preserve identical booleans and equal numeric representations such as `0` and `0.0`. Missing/unsupported evidence still fails closed; the helper remains read-only.

### Verification

- RED: commit `a2044ff53f83a06119a8a913a191a01741eeb796` failed 5 of 493 unit tests in GitHub Actions `39963602838`, including a false `Treatment Isolated` classification.
- GREEN: commit `546c36c55ccd0063d14bbe30539b75b7ba48d23f` passed all 493 unit tests, Skill Validator and Eval Validator in GitHub Actions `39963714085`. The release PR HEAD and merged main must pass required validation again.

### Sources and copyright

- Independently implemented from this repository's own JSON control-state schema and deterministic comparator; no third-party code, prompts, schemas, workflows, or templates copied. Public Amazon Ads guidance informs future placement/control coverage, not a universal bid rule.

## v1.22.0 — 2026-10-23

### Safety

- Fail closed when an extra observed material control outside the registry-required minimum has a null/missing state or unverified list enumeration/pagination/capability completeness. Such evidence cannot be treated as unchanged merely because the control was not required by the decision-surface registry.
- Preserve compatible observed scalar extras and verified-complete list extras. The registry still defines the mandatory minimum; connector limitations never become zero, and the read-only comparator never performs Ads writes.

### Verification

- RED: PR #124 commit `310e7e7d24f32c7375d7ac8fe388059cdd05b504` failed 5 of 486 unit tests in GitHub Actions `39956202534`.
- GREEN: commit `c5bf3d9ab3dffb2eb73e8cb74d4251bb1a776567` passed 486 unit tests, 15-Skill validator and 55-eval validator in GitHub Actions `39956278773`. Final release PR HEAD must pass required checks again before merge.

### Sources and copyright

- Based on this repository's existing control-state snapshot schema, versioned registry and comparator; no third-party code, prompts, schemas or workflows copied. Amazon Ads official documentation is platform context, not a numeric bid rule.

## v1.21.0 — 2026-10-23

### Safety

- Fail closed when a control-state comparison lacks the required source envelope, source system, or acquisition channel, or when those identities differ without a verified cross-source mapping contract.
- Preserve connector identity when supplied: a mismatched or one-sided connector ID cannot silently establish Comparable or Treatment Isolated. Different per-observation readback IDs remain valid; legacy snapshots without connector IDs on both sides remain compatible.
- This is a read-only source-provenance gate. It does not equate missing source information with zero, assert cross-source semantic equivalence, or grant Ads write permission.

### Verification

- Deterministic RED: PR #123 commit 3bba9996ed5487c05828d1bd059af8b81e98248e failed 8 of 479 unit tests in GitHub Actions 39948565519.
- GREEN: source-lineage guard commit a157440cc2c38d6af157a618b37c3bf4c6fb955e passed repository unit tests, Skill validator and Eval validator in GitHub Actions 39948651042. Final release PR HEAD must pass required validate again before merge.

### Sources and copyright

- Independently implemented from this repository's own schema-required source fields and data-lineage safety contract. No external code, prompts, schemas, workflows, or templates copied. Amazon Ads documentation remains platform context.

## v1.20.0 — 2026-10-23

### Safety

- Fail closed when a post-change control-state snapshot was observed before its baseline, preventing reversed evidence windows from being labeled Comparable or Treatment Isolated.
- Compare actual UTC instants across explicit offsets and preserve submicrosecond fractional precision; same-instant fixture comparisons and forward-ordered observations remain valid.
- This is a read-only causal-evidence gate. It does not infer Ads account state, change controls, or grant execution permission.

### Verification

- Deterministic RED: PR #122 commit 6082db48220931d31bc62aed85013a1dbf25b6c2 produced 4 failures among 468 unit tests (GitHub Actions 39941157426).
- GREEN: comparator fix 9a30c84230ca862b5f153a3e06014be6a8e0195e passed unit tests, Skill validator and Eval validator (GitHub Actions 39941273340). The final PR HEAD must pass required validate again before merge.

### Sources and copyright

- Repository-owned observation-order and measurement-lineage invariant; no third-party code, prompt, schema, workflow or template copied. Official Amazon Ads materials are platform context, not a claimed API change.

## v1.19.0 — 2026-10-23

### Safety

- Reject malformed or ambiguous-offset RFC3339 control-state observation/effective timestamps and controls whose effective instant occurs after their snapshot observation. This prevents future-dated control evidence from being misclassified as Comparable or Treatment Isolated.
- Compare UTC instants with their full fractional-second precision, including offsets and digits beyond microseconds; preserve valid historical controls, legacy profile/global identity semantics and read-only behavior.
- An absent effective timestamp for an unchanged control retains the prior comparator contract; changed controls still require effective timestamp evidence.

### Verification

- Deterministic RED: PR #121 commit d2a027a89f56f3f63c893e2359f57e9cac53250a failed 8 of 462 repository unit tests in GitHub Actions 39933928276.
- GREEN: comparator fix at 0f0aef29ac97bbb01fa2c82513555ee063531e40 passed repository unit tests, Skill validator and Eval validator in GitHub Actions 39934023587. Final release commit must pass the same required validate check before merge.

### Source and copyright

- Independent safety invariant derived from the repository's existing event-time/measurement lineage contract; no external code, prompts, schemas or workflows reused. Amazon Ads product documentation remains platform context, not a claim about a new API field.


## v1.18.0 — 2026-10-23

### Added

- Read-only Global Sponsored Products control-state comparison supports profile-less snapshots when a source-supported Global Account ID and marketplace scope are explicit. Legacy profile-scoped snapshots remain supported.
- Optional account-identity envelope preserves global, regional, legacy and profile identifiers without assuming cross-generation mappings.

### Safety

- Reject conflicting or one-sided advertiser identity, country context, missing strong identifiers and profile/global identity mismatches as Unknown, even if control values are identical.
- The comparator does not infer marketplace-wide control equivalence, connector capability, account mappings or Ads write authorization.

### Verification

- Deterministic RED on PR #120 commit 912dee834bc78571e1bd309646ac4891247632ca: five failures in 452 repository unit tests (GitHub Actions 39927421372).
- GREEN requires repository unit tests, Skill validator and Eval validator to pass on the final PR HEAD before merge.

### Source and copyright

- Amazon Ads Global Campaigns API guide (reviewed 2026-10-23; publication date not established): https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns
- Only publicly documented identity/header semantics were used; no Amazon API examples, code, schemas or third-party workflows were copied.

## v1.17.0 — 2026-10-23

### Fixed

- Fail closed on duplicate or malformed material control identities before constructing control-state maps, preventing silent evidence overwrites.
- Accept only observed/derived evidence statuses for comparability; missing, invalid, stale, unsupported, and unknown evidence remain Unknown rather than being interpreted as stable controls.
- Preserve existing read-only decision boundaries, required-control registry checks, and 15 canonical Skills.

### Verification

- Deterministic RED on PR #119 commit 21f3db4a00841cb5e59d89d31bb7141e56018ea0: five failed assertions and one missing-key error; GREEN on 7f1f6eeb1f77f7f589ea952f7147144cce54d648: repository unit tests, Skill validator and Eval validator passed in GitHub Actions 39920200834.

## v1.16.0 — 2026-10-15

### Fixed

- Reject competing correction events that supersede the same in-slice measurement-comparison audit event. Ambiguous audit forks must not silently resolve to a seemingly available comparison.
- Preserve linear correction chains, distinct independent correction targets, and bounded histories with missing predecessors.
- Reject missing or duplicate audit event IDs and in-slice supersession cycles in the measurement-comparison history projector; preserve bounded missing-predecessor semantics.
- Bind measurement-comparison projections to an optional caller-requested entity and advertiser identity, rejecting mismatched or missing identities even for a single-event slice; preserve legacy unbound calls.
- Reject in-slice corrections targeting a different or unverified parent action; preserve bounded missing-predecessor compatibility.

### Verification

- Four deterministic correction-fork regressions: 2 failures before the fix, 4 passes after the minimal fix. Full repository unit tests and Skill/eval validators must pass in PR CI before merge.
- Seven caller-bound comparison regressions, including wrong/missing account, missing requested regional ID, wrong entity, valid binding and legacy compatibility.

## v1.15.0 — 2026-10-09

### Fixed

- Fail-closed Marketing Stream source/generation lineage in the read-only metric aggregation gate; generic and readable v2 identifiers now enforce highest-version reconciliation, while conflicting/unknown source identities cannot authorize direct summation.
- Preserve explicit Stream v1 delta and ordinary Reporting API paths without introducing a live Ads mutation surface.

### Verification

- Deterministic RED regression committed before the fix; full repository unit tests and Skill/eval validators are required before merge.

### Research

- Re-validated Amazon's Stream v2 total-value and record-version rules; reviewed pre-existing MIT/MIT-0 connector/sample references without copying external implementations.

## v1.14.0 — 2026-10-09

### Added

- RED→GREEN deterministic regression for Amazon Marketing Stream v2 total-valued restatement records and out-of-order highest-version selection.
- Stream v2-specific, read-only reconciliation evidence gate in the existing metric aggregation helper; direct additive/disjoint summation is not permitted unless the full record identity and highest `streamBatch.version` selection are verified.

### Changed

- Shared Stream coverage reference now distinguishes v1 per-hour delta / independent subscriptions from v2 unified performance datasets and per-window totals, with v1/v2 migration and version-reconciliation boundaries.
- Existing campaign health and performance-drop Skills load Stream generation/reconciliation guidance only when Stream is used; absence of verified v2 reconciliation becomes Unknown, not zero or unchanged.

### Research

- Re-reviewed current Amazon Ads Stream v2 overview and v1→v2 migration guidance, plus Amazon-owned sample repositories (MIT-0), OpenLineage (Apache-2.0) and an already-reviewed Amazon Ads MCP (MIT). No third-party code, schema, prompts, or ingestion workflows imported.

## v1.13.0 — 2026-10-09

### Added
- Task-scoped, canonical `required_transition_provenance_fields` on the existing entity-state-readback capability. The capability gate now blocks actor-dependent claims when the active connector cannot prove source-supported coverage for every required transition provenance dimension.
- Deterministic RED→GREEN unit tests for missing, partial, and verified provenance capability evidence, plus resolver preservation and invalid-scope rejection.

### Changed
- Post-change review and shared connector/control-state references distinguish source-observability preflight from event-time actor proof. Empty local change history and a Supported current-state readback are no longer considered sufficient to assign mutation authorship.

### Research
- Reviewed Amazon official automatic deal selection and the Amazon-owned MIT-0 advanced-tools repository; distinguished maintainer change-history guidance from an unresolved user-reported missing-event issue. No third-party code, schemas, prompts or workflows reused.

## v1.12.0 — 2026-10-06

### Added

- Optional control-state `transition_provenance` evidence for management mode, last transition actor/reason/time and provenance evidence status.
- Deterministic regression covering platform-managed control-state changes when the local Executor ledger is empty but transition actor/reason is unavailable.

### Changed

- Post-change review now separates current control state from mutation authorship and caps advertiser/Executor causal claims when Amazon/platform-managed mutation is possible but provenance is unknown.
- Control-state and optimization-memory guidance now treats a complete local/external Executor ledger as bounded history rather than proof of complete platform-wide mutation history.

### Research

- Re-verified Amazon automatic deal selection, Review Requests and Sponsored Ads auto-optimization documentation for platform-managed mutation/provenance semantics. Re-ran multi-query Amazon Ads/MCP, agent audit/provenance, evaluation and lineage discovery; previously reviewed high-value projects were de-duplicated and a newly surfaced unlicensed/low-evidence event-sourcing project was rejected for implementation reuse.

## v1.11.0 — 2026-10-05

### Added

- Deterministic Long-Term Sales maturity regression covering modeled/projected estimate evidence versus realized/Accumulated Sales outcome evidence.
- Contract test locking the estimate-vs-realized evidence boundary across the post-change Skill, replay fixture and shared lineage guidance.

### Changed

- Post-change review now keeps Long-Term Sales projections separate from realized sales and forbids promoting an action to `Worked` / `Likely Worked` or scaling again from the long-horizon estimate alone when realized evidence is immature, unavailable, unsupported or unknown.
- Shared data-lineage guidance now preserves evidence type, estimate horizon/as-of, model identity/version when exposed, realized-through/maturity and revision/backfill state for modeled/projected outcomes.

### Research

- Re-verified Amazon official Long-Term Sales, campaign reporting and 2026-09-30 AI-measurement guidance. Amazon vendor documentation informed only factual metric semantics and the independently rewritten decision-safety boundary; no Amazon code, schema, prompt, workflow or proprietary implementation was copied.

## v1.10.0 — 2026-09-29

### Added

- Canonical `video_bid_adjustment` material-control type for Sponsored Products causal review.
- Deterministic regression proving that a concurrent Sponsored Products video boost change confounds a base-bid treatment rather than remaining `Treatment Isolated`.

### Changed

- Sponsored Products bid and budget control requirement sets now include source-supported video bid-adjustment state when applicable.
- The versioned material-control registry advances to `control-requirements@2026-09-29`; older registry identities remain stale rather than silently inheriting the enlarged requirement set.
- Bid, placement, and budget Skills now treat missing/changed Sponsored Products video bid state as part of the coupled-control causal gate.

### Research

- Re-verified Amazon Ads help updated 2026-09-23 and the Sponsored Products video guide. Both independently document video-specific bid adjustment and combination with other bid modifiers. Re-ran Amazon Ads/MCP/Agent Skills searches; already-reviewed projects were de-duplicated and no third-party implementation was imported.

## v1.9.0 — 2026-09-22

### Added

- Shared report-request compatibility gate that separates an unsupported `reportTypeId × groupBy × columns × timeUnit × filters` configuration from advertiser metric zero.
- Regression coverage for Reporting API v3 daily/summary date-column semantics and multi-`groupBy` filter compatibility.

### Changed

- Report coverage now validates request compatibility before metric interpretation while keeping generation, extraction completeness and population coverage as separate evidence states.
- Unsupported, partial or unknown request compatibility fails closed to missing/alternate-source/hold/manual-review behavior rather than silently substituting a nearby metric or grain.

### Research

- Re-verified current Amazon Sponsored Ads Reporting API v3 request semantics and Unified Reporting context. Re-discovered Amazon Ads MCP/downloader projects and high-adoption Agent Skills/evaluation projects; forks, archived projects and already-reviewed runtime ideas were de-duplicated. No external code, schema, prompt, workflow or request template was imported.

## v1.8.0 — 2026-09-22

### Added

- Bounded `measurement_comparison` audit evidence on optimization events, preserving comparator identity, classification, changed fields, deterministic reasons, and baseline/post evidence snapshot IDs.
- Stable `measurement-composition@1` comparator identity plus snapshot-lineage passthrough in `compare_measurement_composition.py`.

### Changed

- `post-change-review` now preserves the machine comparison result on `evaluated` / `corrected` structured events when that comparison materially gates the outcome.
- Optimization-memory guidance now treats comparator output as append-first audit lineage rather than a transient LLM judgment; missing snapshot identities remain unknown and are never reconstructed.

### Research

- Re-verified Amazon Ads conversion-attribution, modeled-conversion and Unified Reporting semantics and reviewed OpenLIT and Arize Phoenix for agent-evaluation/trace auditability. Langfuse was de-duplicated from prior review. No external trace schema, observability backend, evaluator or runtime was imported.

## v1.7.0 — 2026-09-22

### Added

- Dependency-free `scripts/compare_measurement_composition.py` for deterministic baseline/post comparison of modeled/direct inclusion, split availability, allocation coverage, `Unallocated` state and allocation grain.
- Regression coverage for fail-closed unknown evidence, hard semantic/grain incompatibility and lower-grain directional allocation drift.

### Changed

- `post-change-review` now routes machine-readable baseline/post composition states through the comparator before affected conversion outcomes can be promoted to causal `Worked` / `Failed`.
- Shared data-lineage guidance now defines the machine classifications `Comparable`, `Directional`, `Not Comparable` and `Unknown` for the bounded composition contract.

### Research

- Re-verified Amazon official modeled-conversion reporting semantics and reviewed Great Expectations and Soda Core as data-quality/data-contract references. No third-party validator, framework, contract syntax, workflow or implementation was imported.

## v1.6.0 — 2026-09-22

### Added

- Post-change measurement-composition comparability gate covering modeled/direct inclusion, lower-grain allocation coverage, `Unallocated` rows and allocation grain.
- A replay fixture for a confirmed bid action whose apparent conversion/ROAS improvement coincides with changed lower-grain allocation coverage.

### Changed

- Post-change outcome review now treats material unreconciled measurement-composition drift as a measurement confounder and caps affected conclusions at `Inconclusive` / directional / Hold / Manual Review rather than promoting them directly to causal `Worked` or `Failed`.
- Weekly change-memory review now checks measurement-composition drift before attributing recent conversion movement to a prior optimization action.

### Research

- Re-verified Amazon official modeled-conversion/`Unallocated` reporting semantics and reviewed OpenLineage, OpenMetadata and DataHub as high-adoption lineage/context projects. No external lineage framework, schema, client, workflow or runtime was imported.

## v1.5.0 — 2026-09-22

### Added

- Optional `measurement_composition` schema parity at both optimization-event evidence and derived entity-history measurement boundaries, matching the existing read-only projector.
- A deterministic unittest-discovery guard that prevents top-level pytest-style tests from being silently skipped by the repository's `unittest discover` CI runner.

### Changed

- Measurement-composition persistence now explicitly keeps modeled/direct inclusion, split availability, allocation coverage, unallocated-row presence and allocation grain nullable/unknown when evidence is absent.
- The schema-parity regression is now a real `unittest.TestCase`, so CI exercises the contract instead of returning a false green.

### Research

- Re-verified Amazon official modeled-conversion reporting semantics and reviewed `microsoft/skills`, `alibaba/skill-up`, and `SalesforceAIResearch/MCPEval` for evaluation/test-harness practices. No external runtime, harness, schema, prompt or workflow was imported.

## v1.4.0 — 2026-09-21

### Added

- Campaign-objective decision lineage across optimization memory and post-change review, including explicit action-time objective preservation and objective-drift handling.
- Regression/eval coverage for a Growth action reviewed after the campaign later switches to a Profit objective.

### Changed

- Derived `entity-history.latest_action` can preserve the source action's `campaign_objective` without treating it as current truth.
- Post-change review now separates historical outcome evaluation from the current campaign objective and forbids retroactive KPI/guardrail substitution.
- Weekly review now checks action-time objective vs current objective before classifying prior actions.

### Research

- Re-reviewed Amazon official goal/KPI guidance and high-adoption agent/evaluation projects including `mozilla-ai/any-agent`, `google/adk-go`, and `mlflow/mlflow`; no external runtime or implementation was imported.

## v1.3.0 — 2026-09-21

### Changed

- Bid and placement optimization now load the shared campaign-objective contract before turning local efficiency into objective-dependent action or sizing.
- `Unknown` campaign objective explicitly caps mission-dependent bid/placement decisions to conservative hold/directional/shadow/experiment/manual-review outcomes rather than inventing action authority.
- Existing connector-capability, sample-sufficiency, realized-exposure, control-interaction, confounder, action-sizing and platform-capability safeguards remain additive and unchanged.

### Research

- Recorded `evalstate/fast-agent` as a high-adoption Apache-2.0 runtime/evaluation reference and rejected importing its runtime machinery because connector attachment, execution and orchestration remain external to this decision library.

## v1.2.0 — 2026-09-21

### Added

- User-facing documentation hierarchy with `docs/README.md`, `docs/CAPABILITIES.md`, `docs/ARCHITECTURE.md`, research/archive boundaries and a much smaller product-entry README.
- Campaign-objective context contract with bounded `Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, and safe `Unknown` roles.
- Operator/community research boundary: practitioner evidence can expose failure modes, but anecdotes and fixed percentages do not become repository defaults.

### Changed

- Superseded 2026-09-07 bootstrap plan/design moved out of active documentation so obsolete 11-Skill/direct-to-main guidance no longer competes with current repository governance.
- Optimization action proposals can preserve campaign-objective context when it materially changes a recommendation.

## v1.1.0 — 2026-09-21

### Added

- Deterministic SHA-256 and byte-size content identities for the selected Skill package and directly referenced shared resources returned by the custom-host context resolver.
- Explicit platform-integration guidance separating the repository-local resource manifest from the normative MCP Skills wire protocol.
- Repository-wide semantic-version governance with `VERSION` as the canonical source and CI coverage for README/runtime-manifest synchronization.

### Changed

- Release-readiness tests no longer hardcode `1.0.0`; they validate the active semantic version dynamically.
- Pull requests now classify version impact so substantial backward-compatible improvements advance MINOR versions and breaking public contracts advance MAJOR versions.

## v1.0.0

Initial public v1 release of the 15-Skill Amazon Ads decision library.
