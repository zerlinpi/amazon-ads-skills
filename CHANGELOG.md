# Changelog

## v1.41.0 — 2026-10-24

### Global SP campaign query pagination trace consistency (MINOR)

- When an external trusted adapter supplies optional `readback.pagination_trace`, validate exact campaign/account/product/scope/filter identity, per-page source and observation time, and an unbroken, nonrepeating `nextToken` chain ending at null. A contradictory, incomplete or malformed trace now yields `Unknown` rather than `Confirmed`, even when the envelope asserts `pagination_status: Complete`. Legacy envelopes without this optional trace remain compatible.
- RED-first synthetic regression `tests/test_global_sp_query_pagination_trace.py`: 889 unit tests, 23 failures before the fix (Actions 40079424196). Minimal implementation commit `b0913d6926beab7a028e3a272e9d2d2bf41f52dc` restored GREEN (Actions 40079467166). The query trace remains an external assertion, not independent API authentication or row-completeness proof.
- Official Global Sponsored Products documentation specifies paginated query responses with `nextToken` and separate HTTP 207 write receipts. No live Ads calls, retries, third-party code or new Skills.


## v1.40.0 — 2026-10-24

### Native Global SP campaign configured-state evidence cross-check (MINOR)

- When a trusted adapter explicitly retains `readback.raw_campaign`, cross-check native campaign/account/marketplace scope and derive per-marketplace configured states from native `state` plus `marketplaceConfigurations[].overrides.state`. Contradictory, incomplete or malformed native evidence now yields `Unknown`; a complete matching raw and normalized readback still yields `Drifted` when the intended state differs. Delivery health is never treated as configured state. Legacy normalized-only inputs remain compatible.
- RED-first synthetic regression `tests/test_global_sp_native_campaign_configuration.py`: 862 tests, 20 failures on previous behavior (Actions 40075256711). Minimal fix commit `f8dc5d518c1da9be3b5726e24d335a4b36ad85df` restored 862/862 GREEN (Actions 40075280259), with Skill and Eval validators passing.
- Amazon Global Sponsored Products official guide distinguishes configured campaign `state` / marketplace overrides from query `status.deliveryStatus`. The optional raw query snapshot is an externally asserted source, not independent authentication. No Ads writes or third-party code copied.


## v1.39.0 — 2026-10-24

### Raw marketplace identity evidence safety (MINOR)

- Extend the existing read-only Global SP campaign state/daily-budget readback gate: if raw marketplace IDs are explicitly retained on normalized rows, require a complete, one-to-one country-code crosswalk with explicit verified status and source lineage. Reject missing, duplicate, contradictory or malformed mapping evidence as `Unknown`; never treat unsupported mapping as zero, a configured state or a verified budget. Existing country-code-only envelopes remain compatible.
- RED-first synthetic regression in `tests/test_global_sp_raw_marketplace_identity.py`: 835 tests, 15 failures against v1.38.1 (Actions 40071280587). The minimal code fix is commit `903eb5eaa91862099ad0a879113e3169477644a8`. Final green validation is required before merge.
- Amazon's Global SP guide states that query `status.marketplaceSettings` can use raw marketplace IDs while resource configuration uses country codes. A source-attributed adapter crosswalk is a repository-defined assertion, not a native Amazon requirement or independent proof of adapter authenticity. Delivery status cannot substitute for configured state. No live Ads calls or third-party code copied.


## v1.38.1 — 2026-10-24

### Campaign 207 receipt identity binding (PATCH)

- Fix `scripts/evaluate_global_sp_readback.py`: explicit 207 receipt account, campaign, request and resource-type identities must agree with the intended campaign update. If the success item contains a returned campaign resource, validate native `campaignId` and normalized `campaign_id` aliases and any supplied account identity; malformed or contradictory evidence returns `Unknown` instead of falsely `Confirmed`. Legacy index-only receipts remain compatible under the existing trusted-adapter contract.
- RED-first deterministic regression `tests/test_global_sp_campaign_receipt_identity.py`: 816 tests, 10 failures on old behavior (Actions 40067650845). Minimal fix `e7ffb6c165dfc09c0c40afc7f19ac8a2f7140076` restored GREEN (Actions 40067675016). Final PR-head and merged-main required checks must pass before merge.
- Official Global SP documentation establishes indexed HTTP 207 success responses with returned campaign identities. This stricter optional-field contradiction guard is repository-defined safety policy, not a claim that Amazon requires a particular normalized adapter schema. No third-party code, API examples, prompts or workflows copied; no live Ads writes.

## v1.38.0 — 2026-10-24

### Read-only mixed-resource safety capability

- Add `scripts/evaluate_global_sp_mixed_plan_readback.py` and `references/global-sp-mixed-plan-readback.md` to classify a complete externally asserted Global SP optimization plan spanning campaign, ad-group, target and existing homogeneous batch readback gates. Require a single global account, complete trusted plan manifest, exact declared component coverage, ordered request IDs, and unique resource identities; never trust caller-supplied component verdicts.
- Reuse existing independently validated child receipts/readbacks. Whole-plan `Confirmed` requires every component `Confirmed`; `Unknown > Partial > Drifted > Confirmed` is a conservative repository policy. No new Skills, Ads writes, retries, idempotency, Executor reconciliation, FX inference, or causal outcome claims.
- The manifest's authenticity and completeness are **external Executor assertions**, not Amazon Ads native API fields or independently verified by this classifier.

### RED → GREEN

- Deterministic RED-first tests `24ab2d2aca9d725344a1fb12da44ad7e319cc223` (Actions `40063718187`, failure); implementation `486edab38de75b99bf8eccf500ba238716a5f34f` (Actions `40063745263`, success). An additional malformed-kind regression test `1a65f54389b7cf35cb7736a62d8e568037c26dc4` reproduced a TypeError (RED Actions `40063856519`); `227870b4b6455c249e0f097565765803da4118a8` now returns `Unknown` instead. All repository unit tests, Skill validator and Eval validator must pass on final PR HEAD. Final PR-head and merged-main checks must also succeed.

### Sources and copyright

- Amazon Ads official Global SP guide establishes distinct resource operations and indexed HTTP 207/query separation; plan-level completeness is a repository-owned external evidence contract. Fresh candidate license/adoption decisions are in `docs/SOURCES.md`. No third-party code, prompts, schemas, workflow, template or API example copied.

## v1.37.0 — 2026-10-24

### Read-only safety capability

- Add `scripts/evaluate_global_sp_adgroup_batch_readback.py` for one-call homogeneous Global SP multi-ad-group updates. Require unique ordered request/index binding, one Global Account, distinct ad-group identities and independent complete native-currency marketplace default-bid query evidence for every successful item. Reuse the existing single-ad-group readback gate rather than inferring default bids from target/campaign state or 207 receipts.
- Aggregate `Unknown > Partial > Drifted > Confirmed` conservatively; preserve indexed item outcomes. Explicit partial/unsupported/missing evidence never becomes zero or full confirmation. No Ads writes, retries, idempotency, or external Executor reconciliation.
- Keep the canonical 15 Skills and Codex/Claude Code/WorkBuddy runtime manifests synchronized.

### RED → GREEN

- RED-first synthetic tests: `d9ac164d2f0ac2efce40123ed79f646bb267998b`, import-path correction `3f6dcf407315ff4b9700fd8a2db4670d58f0f167`; Actions `40059332505` failed on missing batch verifier. Core implementation `2be858064fd5236f3def8cc45301e44311a4a9fa`; Actions `40059351920` succeeded. Final PR-head required validation and main validation must pass before merge.

### Sources and copyright

- Official Global SP guide confirms indexed HTTP 207 and per-marketplace ad-group default bids; normalized correlation/readback policy is repository-defined. Fresh candidate metadata and adopt/reject reasoning recorded in `docs/SOURCES.md`. No external code, prompts, API examples, schemas, or workflows copied.

## v1.36.0 — 2026-10-24

### Read-only safety capability

- Add `scripts/evaluate_global_sp_target_batch_readback.py` for one-call homogeneous Global SP positive-target batch updates. Require complete, unique 207 request indices, a single Global Account, unique target/request identities, and independently verified native-currency target bid query evidence for every successful item. Reuse the v1.35.0 single-target gate instead of weakening it or treating a 207 receipt as readback.
- Aggregate conservatively: `Confirmed` only if every item is confirmed; `Unknown` for missing/ambiguous/unsupported evidence (even alongside a partial receipt), `Partial` for error/partialSuccess, and `Drifted` for fully observed mismatched bids. Preserve per-index outcomes; no live Ads writes, retries, idempotency, or Executor reconciliation.
- Keep 15 canonical Skills and all three runtime manifests in version parity.

### RED → GREEN

- Initial RED test-first commit `0bbd87e8ad67fcd10e9cdda808b2043df25328a5` (Actions `40055866092`) proved the batch verifier absent. GREEN core implementation `c2138e8380cce577e176308149eef8dca223ac4c` (Actions `40055902890`). Additional malformed receipt-account RED `1967ca16be00679712d137c8e423c835e2efd39f` (Actions `40055937115`), then minimum fix `8f64024be8d5d9a1586528bb97f4d99da21e4338`. Final PR-head/main checks must pass before merge.

### Sources and copyright

- Official Global Sponsored Products API guide confirms indexed HTTP 207 success/error/partialSuccess and independent paginated query. The batch correlation and aggregation contract is repository-defined, not an Amazon-provided Executor or native request-ID field.
- External projects reviewed as alternatives; no third-party code, prompt, schema, template or workflow imported. See `docs/SOURCES.md`.


## v1.35.0 — 2026-10-24

### Read-only safety capability

- Add independent Global Sponsored Products **positive KEYWORD/PRODUCT target** configured-bid readback gate (`scripts/evaluate_global_sp_target_bid_readback.py`). Targets are one-marketplace resources, unlike global ad groups; the gate requires exact global account/campaign/ad group/target identity, native-currency Decimal bid, bound single-item 207 receipt, complete post-write query and connector capability evidence.
- Reject negative/THEME/unverified target types, missing or contradictory bid/lineage, partial/truncated/unsupported evidence and unsupported extra `expected_*` intent as `Unknown`; valid partial/error receipts remain `Partial`. Keep campaign state, ad-group default bids and target bids independent; no FX, auction-bid inference, batch reconciliation or live Ads writes.
- Preserve 15 Skills, default Suggest/Shadow safety, and external authorized Executor ownership of mutations/retries/idempotency.

### RED → GREEN

- RED test-first commit `d9ade7c81cdd2d3a380e2e9be2b8a43434783e0f`, Actions `40051661207`: 713 unit tests, 40 expected failures because target-specific gate was missing.
- GREEN initial implementation `82e140bb7845e25cdf8779e5a3246c693cae6769`, Actions `40051691194`: required validation passed. Additional contradictory target-type/negative evidence regression cases and fix follow on the same feature branch; final PR-head and merged-main required validation must succeed before merge.

### Sources and copyright

- Official Amazon Ads Global SP API guide checked 2026-10-24: targets have one marketplace and a target-specific bid distinct from ad-group default bid. Adapter request correlation and conservative row-level lineage are repository-defined safety contracts.
- Previously reviewed open-source candidates rechecked, none imported. No third-party code, schema, prompt, workflow or template copied. See `docs/SOURCES.md`.

## v1.34.0 — 2026-10-24

### Read-only safety capability

- Add independent single-item Global Sponsored Products **ad-group** marketplace **default-bid** 207/readback gate (`scripts/evaluate_global_sp_adgroup_bid_readback.py`). It requires external request/receipt correlation, exact global account/campaign/ad-group identity, source-supported complete query coverage, per-marketplace native currency/Decimal amounts, and post-write time lineage.
- Keep the existing campaign configured-state/budget gate separate: campaign `Confirmed` never certifies an ad-group or target update. Unknown/Partial/Unsupported data never become zero or confirmation. No Ads API writes, retries, FX, multi-item batch reconciliation, or additional Skills.

### RED → GREEN

- RED: synthetic 35-case test suite first, commit `f2ca5a42455b8770a8d3961cc5a023f6f0de0a34`, Actions `40046688664`: 673 unit tests, 35 expected failures because independent gate was missing.
- GREEN: implementation commit `56fddc9bdb3258494c3f9ceb3f869a1b4f6a7de1`, Actions `40046773273`: required validation passed. Latest PR-head and merged-main validation are required before merge.

### Sources and copyright

- Official Amazon Ads Global SP guide checked 2026-10-24: ad-group `bid.marketplaceSettings` native `currencyCode`/`defaultBid` is distinct from campaign state/budget and target bids. External request/receipt correlation is repository-owned normalization, not an Amazon API-mandated response field.
- Existing MIT/Apache-2.0/NOASSERTION open-source candidates rechecked; none adopted as a dependency. No third-party code, prompts, schemas, workflows, or templates copied. See `docs/SOURCES.md`.

## v1.33.0 — 2026-10-24

### Safety

- Global SP single-item campaign receipt/readback evaluator now rejects unverified extra `expected_*` intent (including marketplace/ad-group/target bids and placement adjustments) with `Unknown`. Previously it could return `Confirmed` solely from campaign configured state while ignoring an explicitly requested separate bid change.
- Preserve supported campaign-state and optional daily monetary-budget readback, partial/error 207 precedence, and the 15-Skill read-only/external Executor boundary. No ad-group/target readback capability is claimed.

### RED → GREEN

- Deterministic RED commit `a7839cd1b0fa9603b11079f76364d9bb17e9d20c`, Actions `40041109634`: 638 tests, 5 expected failures proving false confirmation.
- Minimal GREEN fix commit `0e4e50165becfec5ee56d49df1c3bf391e65b6ce`; final PR-head and merged-main required validation must succeed before merge.

### Sources / copyright

- Official Amazon Ads Global SP guide (checked 2026-10-24) distinguishes campaign state/budget and marketplace-specific ad-group bids. Previously reviewed MIT/Apache-2.0/NOASSERTION repositories not copied or imported. See `docs/SOURCES.md`.

## v1.32.0 — 2026-10-24

### Safety

- Reject explicit per-marketplace Global SP configured-state row source, observation time, or global-account/campaign identity that contradicts the trusted readback envelope or original request. Previously, stale or cross-connector state rows could be falsely `Confirmed`.
- Preserve optional row metadata, single-item HTTP 207 `Partial` precedence, state drift detection, daily monetary-budget comparison, 15 Skills and the read-only/external Executor boundary.

### RED → GREEN

- RED commit `d41cb0d16a826960a04cf5472e0de467ab722d5e`, Actions `40036180458`: 629 tests, 10 failed on ignored state-row provenance.
- GREEN commit `9b730eaf98f8390fdb3b8c4e5fd4bb7c99b580b1`, Actions `40036236621`: 629/629 tests and both validators passed; final PR-head and merged-main checks remain required.

### Sources and reuse

- Amazon Ads Global SP guide (checked 2026-10-24): platform facts for global identity, per-marketplace state and 207/readback separation. Row-lineage contradiction is an independent repository safety rule, not an Amazon-mandated payload field.
- Previously reviewed KuudoAI Amazon Ads MCP (MIT), OpenLineage (Apache-2.0), Promptfoo (MIT) and Agent Skills (Apache-2.0) were not adopted; no third-party code, schema, prompts, templates or workflows copied.


This file records user-visible repository releases. The canonical current version is stored in `VERSION`.

## v1.31.0 — 2026-10-24

### Safety

- Reject explicit per-row Global SP monetary-budget source, observation time, or global-account/campaign identity that contradicts the trusted readback envelope and original request. Missing optional row metadata still inherits the trusted envelope contract; a contradictory row never becomes `Confirmed`.
- Preserve single-item HTTP 207 `Partial` precedence, state-only compatibility, decimal/currency exactness, 15 Skills, and read-only/Suggest/Shadow with an external authorized Executor.

### RED → GREEN

- RED commit `57ab2ed44ba694ceafe63f5bffb011f2c8f9e2c9`, Actions `40029482779`: 614 unit tests, 9 failed on ignored row provenance.
- GREEN commit `fa816aab6f3e6a7fda49b34eedfed82c1fec17b2`, Actions `40029540853`: 614/614 unit tests passed. Required Skill and eval validators passed; final PR-head and merged-main validation required.

### Sources and reuse boundary

- Amazon Ads Global Sponsored Products API guide (checked 2026-10-24): independent factual basis for Global Account, marketplace-specific budget identity and 207/readback separation. The row-level contradiction rule is a repository-owned conservative safety invariant, not an Amazon-mandated payload field.
- Previously reviewed KuudoAI Amazon Ads MCP (MIT), OpenLineage (Apache-2.0), Promptfoo (MIT), and Agent Skills (Apache-2.0) remain non-adopted for this narrow deterministic guard. No third-party code, schema, prompts, workflows or templates copied.

## v1.30.0 — 2026-10-24

### Safety / capability

- Extend the read-only, **single-item** Global Sponsored Products 207 receipt/readback gate with an optional, independent **daily monetary budget** comparison per marketplace. Verify native currency identity, exact nonnegative decimal-string amounts, budget type/recurrence, observed row evidence and budget-specific coverage/pagination/connector capability; never treat missing, partial or unsupported budget evidence as zero or as state-only `Confirmed`.
- Classify complete, observed budget/currency/recurrence disagreements as `Drifted`; incomplete, malformed or unobserved evidence as `Unknown`. Preserve legacy state-only inputs, HTTP 207 `Partial` semantics, and the 15-Skill external-Executor safety boundary. No live Ads writes, retries, FX conversion, or multi-item batch support.

### RED → GREEN

- RED: commit `f00f5630d2dee351a8ea831a7ec647265b16fbf9`, Actions `40021864643`: 597 unit tests, 17 failed on missing optional monetary-budget verification.
- GREEN: independently authored read-only guard and deterministic synthetic tests; verify unit tests plus both Skill/eval validators at the latest PR HEAD and after merge.

### Sources and copyright

- Amazon Ads official Global Sponsored Products API guide (reviewed 2026-10-24): marketplace-local monetary budgets/currencies, Global Account scope, and 207/readback separation. Only independently expressed factual semantics used; no vendor code, schema, payload example, prompt or workflow copied.
- KuudoAI Amazon Ads MCP (MIT), Promptfoo (MIT), Agent Skills specification (Apache-2.0) rechecked; none imported because existing deterministic checks suffice and external connectors do not prove budget-readback completeness.

## v1.29.0 — 2026-10-24

### Safety / capability

- Add a read-only, **single-item** Global Sponsored Products campaign-update receipt/readback evaluator. A 207 `success` is not proof of applied per-marketplace state; `partialSuccess`/`error` stay `Partial`, and missing/ambiguous source, global-account/campaign identity, pagination, connector capability, time, or marketplace coverage stays `Unknown`.
- Confirm only complete source-supported post-write effective configured state for every requested marketplace; report `Drifted` when verified overrides disagree. Do not substitute global campaign state or deliveryStatus for per-marketplace configured state. Multi-item batches deliberately remain outside this narrow helper.
- Keep all 15 Skills, the external-authorized-Executor boundary, and existing event status enums unchanged. No live Ads writes, retries, idempotency, or connector SDK dependency.

### RED → GREEN

- RED: commit `25dadf6b696a2960105a52b75838fcde8029b5ef`, Actions `40014494466`: 20 deterministic tests failed because the Global SP readback gate did not exist.
- GREEN: subsequent implementation and release PR-head checks must pass unit tests, Skill Validator, and Eval Validator; final merged main requires a fresh success check.

### Sources and copyright

- Amazon Ads official Global Sponsored Products API guide (reviewed 2026-10-24): HTTP 207 per-index multi-status, marketplaceConfigurations overrides, and paginated query readback. Only factual semantics informed an independent normalized contract. No vendor code, schema, example payload, prompt, or workflow copied.
- `coaxon/amazon-mcp` (MIT, 1 star, non-fork, last push 2026-07-01) reviewed but not imported: tests exist, independent CI not confirmed; external MCP implementation does not prove this repository's readback safety contract. Existing Promptfoo/MCP/Agent Skills candidates remained non-adopted for this gap.

## v1.28.0 — 2026-10-24

### Safety

- Fail closed on unverified direct and deep list descendants inside **registry-required object-valued** material controls, including placement, routing, and budget-rule state during a Sponsored Products bid review. Previously the generic recursive completeness gate covered extra objects and required top-level lists but skipped required objects. No missing, Partial, Truncated, Unsupported or Unknown collection proof is interpreted as a zero or unchanged state.
- Reuse existing per-list completeness checks without adding Skills, API write capability or external dependencies. Synthetic legacy fixtures that previously assumed an empty budget-rule list proved completeness now carry explicit source-like collection evidence instead of weakening the new gate.

### Verification

- RED: commit `bf78c4af0147c8b798a010f3ed8abddb579a786d` failed 6 of 552 tests in Actions `40005645373`; old code falsely isolated a bid change when required routing/placement lists lacked proof.
- GREEN: commit `61a311a12220f80bf70787756ddb31918df66ef8` passed 554 unit tests and both validators in Actions `40005896074`. Final release PR HEAD and merged main must pass their own checks.

### Sources and copyright

- Amazon Ads official Global SP API and 2026 Amazon Business guidance provide platform context, not copied implementation. Third-party MCP/Agent candidates and anecdotal PPC posts did not justify a dependency or fixed bidding rule. All test data and implementation are repository-authored; no third-party code, prompts, schemas, workflows or templates were imported.

## v1.27.0 — 2026-10-24

### Safety

- Fail closed on unverified nested collections inside registry-required top-level list controls, including Sponsored Products audience bid adjustments. A complete root list does not establish completeness of its descendant arrays. Each descendant requires independent RFC 6901 pointer-keyed enumeration, pagination and connector-capability evidence.
- Preserve verified nested collections, flat root lists, isolated/confounded classifications and all 15 Skills. No live Ads write, retry, idempotency or executor capability was added.

### Verification

- RED: commit `cb6f002ccaf783ebc2c6bb7cf73134a6d326e45e` failed 7 of 542 unit tests in GitHub Actions `39998447014`; the old comparator incorrectly isolated a bid change despite missing required-audience descendant evidence.
- GREEN: commit `2aaa27ce2691d6a65b1ff4db86ec6c9ceff6338b` passed 542 unit tests and both validators in GitHub Actions `39998570537`. Final release PR HEAD and merged main require their own checks.

### Sources and copyright

- Derived independently from the repository's existing material-control and collection-completeness contracts using synthetic regressions. Amazon Ads official API documentation supplies context, not imported code or schemas. Third-party candidates were not copied or adopted; no new dependencies.

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
