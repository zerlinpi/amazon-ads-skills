## v2.15.0 — 2026-10-30

### Fixed

- Explicit empty or provenance-only `account_identity` objects now fail closed as incomplete claims in measurement and comparison projections.
- Missing identity remains distinct from an explicit incomplete claim; no Skill, schema, dependency or Ads write.

### Verification

- Deterministic RED regression added before the minimal fix; full repository unit tests and Skill/eval validators are required on the final PR HEAD.

## v2.14.0 — 2026-10-29

### Weak-only account identity claims fail closed

- Explicit account identity objects containing only weak context such as `country_code` are rejected instead of silently treated as missing identity.
- Missing account identity remains missing; concrete advertiser or regional profile identifiers remain supported.
- Read-only provenance validation only. No Amazon Ads writes, retries, idempotency, reconciliation, new Skill, schema, dependency, or third-party code.

## v2.13.0 — 2026-10-29

### Realization partial-scope provenance

- Reject realization events that supply marketplace/profile scope without a concrete entity identity; preserve missing versus partial/unresolved scope semantics.
- RED→GREEN deterministic coverage added; no live Ads calls or writes.

## v2.11.0 — 2026-10-29

### Realization expected-scope placeholder integrity

- **RED→GREEN:** Added deterministic tests proving the realization projector rejected unresolved and padded `expected_scope` values before projection. The minimal fix reuses the existing concrete scope validator; no new Skill, schema, dependency, or live Ads capability.
- **Boundary:** This is a repository-local provenance contract. Amazon Ads official materials inform account/profile/scope identity concepts but do not define this internal validator. Missing/unknown/partial/unsupported remain non-zero, non-usable evidence.

## v2.10.0

- Validate supplied realization event scope even without `expected_scope`; reject unresolved or padded marketplace/profile/entity identity while preserving legacy entity-only events as missing scope.
- Added deterministic RED→GREEN tests; no new Skill, schema, dependency or Ads write capability.

## v2.8.0

- Reject unresolved/padded measurement scope placeholders in the read-only measurement-history projector.
- Add four deterministic RED→GREEN tests; no new Skill/schema/dependency or Ads write capability.

## v2.7.0

- Expose explicit Skill-eval trigger observation coverage and status (`complete`, `partial`, `unmeasured`) alongside the observed denominator.
- Preserve missing/null as unmeasured; no zero/false imputation.
- Deterministic RED→GREEN coverage tests added; no new Skill, schema, dependency, or Ads write capability.

# Changelog

## v2.12.0 — 2026-10-29

- RED tests prove that measurement and comparison history reject supplied marketplace/profile scope claims when entity identity is absent.
- Minimal fix makes `_event_scope` treat marketplace/profile as a claim even without a valid entity object; missing scope remains legacy-compatible and partial scope fails closed.
- No live Ads writes, retries, idempotency or reconciliation.


## v2.6.0 — 2026-10-28

### Validate trigger telemetry and report observed trigger denominator (MINOR)

- The paired Skill-effectiveness summarizer silently ignored supplied non-boolean `triggered` values, changing the denominator of its `trigger_rate` without warning. It now rejects non-null malformed trigger values for every trial, including excluded scorer/harness/insufficient-evidence arms; missing/null remain unmeasured, never false or zero.
- Add `trigger_observed_count` to each comparable variant summary so the number of measured boolean trigger observations is explicit and can be distinguished from `trial_count`. A partial observation rate is still a rate among observed booleans, not proof of complete discovery coverage. Existing valid paired decision rates remain unchanged.
- RED test-only `81b3eb4a73cd503e98667554a73117bfa0f89584`: [Actions #40645366608](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40645366608), 2258 tests / 12 FAIL / 3 ERROR. Minimal fix `86a33d549bb5b32047e075a959e41c15ac46bc1a`: [GREEN #40645433397](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40645433397), 2258 PASS, 15 Skills and 55 Evals PASS. Sixteen synthetic deterministic tests; no new Skill, schema, dependency, live harness or Ads write.
- Internal benchmark schema and evaluation protocol are the normative basis; Amazon Ads official documentation and third-party harnesses do not define this internal field. See research and SOURCES for reviewed provenance, license and rejection decisions.

## v2.5.0 — 2026-10-28

### Fail closed on unresolved single-run Skill-evaluation measurement identity (MINOR)

- The paired summarizer previously returned `Measured` even when required benchmark/fixture/model/runtime/evaluator identity was missing, malformed, padded or a whole-label `Unknown`/`Partial`/`N/A`; it also accepted an invalid evaluation mode and malformed optional non-null evidence/config/tool hashes. The existing longitudinal comparator already rejected unresolved identity for comparability, but the summarizer did not validate its own input before producing a measured result.
- The read-only summarizer now requires concrete required identities and one of the four benchmark modes. Optional hash fields remain omittable/null; explicit null rubric remains valid. Real opaque IDs containing placeholder words remain valid. No schema expansion, model execution or Amazon Ads writes.
- RED test-only `a34d6e6178dfbab9bdd2262c4ec46e8a82c4b822`: [Actions #40639471528](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639471528), 2241 tests / 18 expected FAIL / 4 compatibility PASS. First fix `2b9df331f7e6f9ca42f6e6fd46ec6afef8ec1cf8`: [GREEN #40639535046](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639535046), 2241 PASS. Additional malformed-mode test `dfd79dc4919e4d5b3625edeee6d93daea11a9124`: [RED #40639552609](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639552609), 2242 tests / 1 ERROR (unhandled list mode). Final fix `767c12de1126c82419e9574f9a93ff6d906d7a76`: [GREEN #40639597102](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40639597102), 2242 PASS, 15 Skills PASS, 55 Evals PASS.
- This validates declared benchmark identity only, not actual harness provenance, statistical lift, source authenticity or account-level Ads mutations. Source/license boundary and test reproduction recorded in research and SOURCES.

## v2.4.0 — 2026-10-28

### Validate optional paired Skill-eval resource measurements (MINOR)

- `scripts/summarize_skill_effectiveness.py` previously averaged negative/fractional/boolean/non-finite token or latency values, or silently omitted supplied strings, despite the existing benchmark schema requiring non-negative integer tokens and non-negative numeric latency. A NaN/Infinity mean can leak non-standard JSON and negative means misstate resource cost. Present invalid values now raise `ValueError`, including on excluded scorer/harness arms; missing and explicit null remain unmeasured, never zero.
- RED test-only `36ab94d2be4fe8156f1150413c59159cac91f8f8` ([Actions #40634376428](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40634376428)): 2219 tests, 14 expected FAIL, 3 new compatibility PASS. Minimal fix `42bef5d18faaae4a5b2c19dcf3faf09994588681` ([Actions #40634431673](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40634431673)): 2219 PASS, Skill and eval validators PASS.
- Seventeen synthetic deterministic tests; no Schema, Skill, dependency, model execution or live Amazon Ads write. Internal resource measurement integrity does not authenticate external harness runs or establish statistical significance. Research and source/license boundary recorded separately.

## v2.3.0 — 2026-10-28

### Reject reused Skill-effectiveness trial execution IDs (MINOR)

- The paired read-only summarizer grouped by pair and variant but did not enforce global `trial_id` uniqueness. A reused execution could be counted as an independent second sample across different pairs, including error/insufficient-evidence trials. It now rejects duplicates with a clear `ValueError` rather than inflating evidence.
- RED test-only `7f72057ef040c15e10515c50ae3e1c6197b5e394` ([Actions #40628820306](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40628820306)): 2202 tests / 7 expected FAIL; three new compatibility tests passed. Minimal fix `68938647643cb074ef475029cc1e8c7bba27604f` ([Actions #40628897528](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40628897528)): verify final GREEN and validators before merge.
- Ten deterministic synthetic tests. No Schema change, dependency, new Skill, actual harness execution or live Amazon Ads write. This validates declared IDs, not their external authenticity or statistical independence.

## v2.2.0 — 2026-10-28

### Reject unresolved longitudinal Skill-effectiveness identities (MINOR)

- A pair of benchmark records previously returned `Comparable` when both repeated the same whole-label `Unknown`/`Partial`/`Missing`/`Unsupported` identity, a padded string or malformed non-string field. The read-only comparator now returns `Unknown` for unresolved fixture, model, runtime, tool, evidence, config and evaluator/rubric identities; concrete mismatches remain `Not Comparable`. Explicit null rubric version remains a valid no-rubric declaration.
- RED test-only `2922986394c2450fbce96e9b850f7fa0e1dfaf83` ([Actions #40623018203](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40623018203)): 2192 tests / 12 expected FAIL, 4 compatibility PASS. Minimal GREEN `b0e0012dd8e408f8eeb51c388981b055a6fbf149` ([Actions #40623079319](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40623079319)): 2192 PASS, 15 Skills PASS, 55 Eval fixtures PASS. Sixteen deterministic synthetic tests; no schema, dependency, new Skill or Ads write.
- Research: `docs/research/skill-effectiveness-unresolved-identity-2026-10.md`; source and copyright decisions: `docs/SOURCES.md`. The comparator checks declared identity consistency only, not agent lift or real Amazon Ads evidence.


## v2.1.0 — 2026-10-28

### Stream v1/v2 explicit dataset identity parity (MINOR)

- Verified v1 delta proof previously allowed explicit unresolved `stream_dataset`; v2 placeholder regex also misread literal 's', missing `Missing` and `Unsupported`. Reuse existing dataset guard for both generations and correct regex. Omitted optional dataset and valid opaque labels stay compatible; source authentication and delivery completeness remain external.
- RED `b2f62de401e0f83725d2e5c4003c4b52d8d5702a` ([Actions #40617171450](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617171450)): 2174 tests, 8 FAIL. Intermediate fix `222a7d0f6f43a13bde730c7bdbc956f20bcd083b` ([#40617232281](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617232281)): 1 FAIL. Additional v2 RED `ba8d1bd63605909c067d311b2fb386b9432ca4dc` ([#40617295510](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617295510)): 2176 tests, 3 FAIL. GREEN `0c3203e6e3313b0c33894f5f21b64ba0d7ba592a` ([#40617361659](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40617361659)): 2176 PASS, 15 Skills and 55 Evals PASS.
- Research: `docs/research/stream-v1-explicit-dataset-identity-parity-2026-10.md`; sources and licensing: `docs/SOURCES.md`. No live Ads write or new dependency.

## v2.0.0 — 2026-10-28

### Require Stream v1 delta idempotency and delivery-window proof (MAJOR)

- **Breaking decision/output behavior:** Marketing Stream v1 previously returned `Allowed` for additive/disjoint rows without verified delta deduplication. It now requires `stream_delta_reconciliation` with exactly `idempotency_id_coverage`, `idempotency_id_deduplication`, and `delivery_window_coverage`, all `Verified`. Missing/Partial/Unknown/malformed evidence returns `Unknown`, never zero. V1 `stream_reconciliation_status` changes from `Not Applicable` to `Unknown` or `Verified`. V2 retains independent record-key/highest-version reconciliation.
- **Migration:** downstream v1 callers must have their authorized external ingestion/warehouse verify the three properties for the exact dataset/account/time window and pass the evidence envelope. The repository does not deduplicate messages, perform retries, authenticate the source or write to Amazon Ads.
- **RED→GREEN:** tests-only `5a33aa85cf390d5f4e3f7999bbf7a547e41c383d` ([RED Actions #40611132056](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40611132056)): 2163 tests, 10 expected FAIL. Production `f8846a21c1565c746e0cef917c06781c25d69e89`, legacy expectation adjustments `0e8fb144390e4534be82bd321c5766a2c0dd16c7` and `948e7e33571e72ab367b2c8d955818d66e0c8e41` ([GREEN Actions #40611237705](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40611237705)): 2163 PASS, 15 Skills and 55 Evals PASS.
- Research: `docs/research/stream-v1-delta-idempotency-2026-10.md`; sources/IP: `docs/SOURCES.md`.


## v1.116.0 — 2026-10-28

### Reject explicitly unresolved Stream v2 dataset identity (MINOR)

- Explicit Stream v2 `stream_dataset` identity now fails closed when supplied as null, non-string, blank, padded, or whole-label Unknown/Partial/Missing/Unsupported/Unavailable/Not Applicable. Such claims return `Unknown` despite Verified record-key/version flags; omitted legacy metadata and concrete opaque dataset labels remain compatible. This is a narrow read-only metadata consistency check, not raw S3/SQS authentication or full-window completeness.
- RED tests-only `008fecf36a59f39c3ea75be01e590b08e04571a3` ([Actions #40604217809](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40604217809)): 2149 tests, 7 FAIL. GREEN `92f9d56b18d8bb079ac779641a2eabfc464cecdd` ([Actions #40604282411](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40604282411)): 2149 PASS; Skill/Eval validators PASS. Ten deterministic tests. No new Skill, schema, dependency, live Ads write, retry or executor.
- Research: `docs/research/stream-v2-explicit-dataset-identity-2026-10.md`; sources and licensing boundaries: `docs/SOURCES.md`.

## v1.115.0 — 2026-10-28

### Reject unproven extra direct arrays in observed SP rule events (MINOR)

- Close a reproducible read-side completeness gap: paired outer `rule_collection_evidence` only proves registered schedule/event/active-budget rule lists, but previously extra sibling arrays (even empty) could pass as verified `Confounded` evidence. Return `Unknown` for such arrays on either event phase. Valid registered lists, scalar metadata and flat legacy events remain compatible; no schema, dependency, new Skill or Ads write.
- RED tests-only `38480f18c1e0e2a2e523ed8c96b4cb9f8f29552e` ([Actions #40597911676](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40597911676)): 2139 tests, 5 FAIL, 4 new compatibility tests passed. GREEN production `08730525aab90660f5a01dfee33e372fbd480616` ([Actions #40597993016](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40597993016)): 2139 PASS, 15 Skills PASS, 55 Evals PASS. Nine deterministic tests.
- Research: `docs/research/intervening-sp-rule-extra-direct-list-2026-10.md`; source/licensing boundaries: `docs/SOURCES.md`. Full-window event coverage and external source authenticity remain unproven. Authorized external Executor alone owns all Ads writes, retries, idempotency and reconciliation.

## v1.114.0 — 2026-10-28

### Reject unproven non-rule SP event collections (MINOR)

- Reuse endpoint completeness guards for positively observed mid-window routing/audience event arrays. Direct routing lists and deep routing/audience member lists (including empty arrays) now return `Unknown` instead of a fabricated confounder. Flat legacy events remain compatible; no new schema, Skill, dependency or live Ads write.
- RED tests-only `d2193043bcf823fba91bb2e3b7ce3027d8316f79` ([Actions #40589410469](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40589410469)): 2130 tests / 5 FAIL. GREEN code `4c8ac7ee0fd88dcc0c2f74d19e712c61a28ba66d` ([Actions #40589486007](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40589486007)): 2130 PASS, 15 Skills PASS, 55 Evals PASS. Nine deterministic tests (5 negative, 4 compatibility).
- Research: `docs/research/intervening-nonrule-sp-collection-evidence-2026-10.md`; sources/license review: `docs/SOURCES.md`. External authorized Executor exclusively owns Ads writes, retries, idempotency and reconciliation.

## v1.113.0 — 2026-10-28

### Optional paired JSON Pointer completeness proof for nested SP rule events (MINOR)

- Add backward-compatible `rule_descendant_collection_evidence` to observed SP schedule/event/budget rule transitions. Each before/after phase independently proves every nested list with exact RFC 6901 pointers, Complete enumeration/pagination and Supported capability. Require valid outer `rule_collection_evidence`; reject incomplete, malformed, one-sided and extra/unmapped pointers as `Unknown`. Omitted proof still fails closed for nested arrays; valid flat rule events remain compatible. No new Skill, dependency or Amazon Ads write.
- RED tests-only `e49a11ecf5d0ca9737d89abdf5a71159209e5e88` ([Actions #40572576136](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40572576136)): 2121 tests / 5 FAIL. GREEN production/schema `ea7916a699f767ff4eb5682e8c11d9209664bc90` ([Actions #40572696421](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40572696421)): 2121 PASS, 15 Skills and 55 Evals validators PASS. Fourteen synthetic deterministic tests.
- Research: `docs/research/intervening-rule-descendant-pointer-proof-2026-10.md`; official/license review: `docs/SOURCES.md`. All live Ads mutations, retries, idempotency and reconciliation remain external authorized Executor responsibilities.

## v1.112.0 — 2026-10-28

### Reject unproven descendant collections inside observed SP rule events (MINOR)

- Reuse the existing deep nested-list completeness guard for positively observed mid-window Sponsored Products schedule/event/budget rule states. Top-level `rule_collection_evidence` does not cover nested arrays inside rule members. Without an event descendant-proof contract, classify even empty nested arrays as `Unknown`, not a certified `Confounded` transition. Valid flat members, top-level empty lists and legacy non-nested events remain compatible; no schema field, dependency, new Skill or live Ads write.
- RED tests-only `dfbd5081e706f9e80c06518e2c3a4f3a9a71c497` ([Actions #40562520498](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40562520498)): 2107 tests, 4 FAIL. Production fix `38bc8e2c68150f0472954aa82d2f3cc345f6bd59` ([Actions #40562550569](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40562550569)). Eight synthetic deterministic tests; final CI outcome is independently checked on the PR head.
- Research: `docs/research/intervening-sp-rule-descendant-completeness-2026-10.md`; source/license review: `docs/SOURCES.md`. External authorized Executor owns all Ads writes, retries, idempotency and reconciliation.

## v1.111.0 — 2026-10-28

### Optional paired completeness proof for observed mid-window SP rule collections (MINOR)

- Add backward-compatible optional `rule_collection_evidence` to normalized positive `control_events`, with independent before/after enumeration, pagination and capability declarations for SP schedule/event/budget rule lists. Explicit incomplete, one-sided or unmapped evidence is `Unknown`; complete proof preserves valid confounders. Omitted legacy evidence remains compatible but never proves continuous or exhaustive event capture. No Skill, dependency or live Ads write.
- RED tests-only `fa2c5e5d034ff5858fc5dd4cf58e68feef702815` ([Actions #40553399677](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40553399677)): 2099 tests, 2 FAIL / 1 ERROR. GREEN `7e5842eadff32ed6c88b981d55f05cb7fd175b1a` ([Actions #40553566614](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40553566614)): 2099 PASS, 15 Skills PASS, 55 Evals PASS. Thirteen synthetic deterministic tests.
- Research: `docs/research/intervening-rule-collection-proof-2026-10.md`; sources/licensing: `docs/SOURCES.md`. External authorized Executor retains all Ads writes/retries/idempotency/reconciliation.

## v1.110.0 — 2026-10-27

### Reject unmapped Sponsored Products placement dimensions (MINOR)

- Fail closed on extra placement keys in SP endpoint snapshots and positive mid-window control events. Only `top_of_search`, `rest_of_search`, `product_pages` and optional `amazon_business` are recognized by the current normalized adapter contract. Unknown keys cannot manufacture `Confounded` or `Treatment Isolated`; valid standard/B2B placement evidence remains compatible. No new Skill, schema field, dependency or Ads write.
- RED tests-only `94a19671d814f18a280e42ded7b401873fa12c29` ([Actions #40534057133](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40534057133)): 2086 tests / **5 FAIL**. Minimal GREEN `69a9413469b526ba0269669deef487ea9cac98bd` ([Actions #40534159070](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40534159070)): 2086 tests PASS; Skill and Eval validators PASS. Eight synthetic deterministic tests.
- Research: `docs/research/sp-unmapped-placement-dimension-evidence-2026-10.md`; source/license review: `docs/SOURCES.md`. No full-window event coverage or external Amazon Ads response authentication; authorized external Executor owns all live writes/retries/idempotency/reconciliation.

## v1.109.0 — 2026-10-27

### Require paired activation evidence for observed mid-window SP rule transitions (MINOR)

- Reuse the endpoint identity-keyed activation evidence parity check for positively observed `control_events` on registered SP bid/budget surfaces. For common schedule/event/active-budget rule IDs, reject one-sided optional `activation_status` or `activation_effective_at` as `Unknown`. Preserve both-absent metadata, real observed activation changes and added/removed rule IDs. No new Skill, schema field, dependency or live Ads write.
- RED tests-only `5690d1fe5720f5302328cbab65e6e7ccb3af3295` ([Actions #40523992555](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40523992555)): 2078 tests, 6 FAIL. GREEN `b092b4481cdc703197e2b17007f917d2bebeac09` ([Actions #40524098654](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40524098654)): 2078/2078 PASS, 15 Skills and 55 Eval fixtures PASS. Eleven deterministic synthetic tests.
- Research: `docs/research/intervening-sp-rule-activation-parity-2026-10.md`; source/license review: `docs/SOURCES.md`. Positive events remain non-exhaustive and unauthenticated; authorized external Executor alone owns Ads writes/retries/idempotency/reconciliation.

## v1.108.0 — 2026-10-27

### Reject incompatible co-observed Sponsored Products routing/placement events (MINOR)

- When two positively observed mid-window SP control events share a concrete source readback, reject `ACROSS_RETAILERS` routing together with an Amazon Business placement modifier in either co-observed before/after phase as `Unknown`. Different/missing readbacks are not joined solely by timestamp. Valid Amazon Store and no-business-placement states remain compatible. No Skill, schema field, dependency or live Ads write added.
- RED tests-only `ea99994252628a83800a341113dac2310846e166` ([Actions #40515556189](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515556189)): 2066 tests, 1 FAIL. Initial fix `2821101d95f24551f458a48b649909e8cd346635` ([Actions #40515691037](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515691037)) exposed an empty-event ERROR. Corrected `54d03a4035a4abbc299d8f2bff14c7b6d316ccc8` ([Actions #40515711043](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515711043)): 2066 PASS, Skills/Evals PASS. Added pre-transition regression test `5c94bc61efa108ec468b4fcf65586b19a550fdeb` before final PR HEAD validation.
- Research: `docs/research/intervening-sp-coobserved-routing-placement-2026-10.md`; source/licensing decisions: `docs/SOURCES.md`. No authenticated complete event-history proof; only external authorized Executor may write to Ads.

## v1.107.0 — 2026-10-27

### Reject contradictory intervening event observation identities (MINOR)

- For positively observed mid-window `control_events`, reject a concrete `source.readback_id` reused across distinct exact UTC event instants and conflicting same-control transitions asserted at one instant. Preserve valid same-instant multi-control observations, equivalent offsets, identical duplicate transitions, distinct readbacks and non-exhaustive logs. No new Skill, schema field, dependency or Ads write.
- RED tests-only `f2002b28626e99194e2b333d7932c57bf0eb7fab` ([Actions #40506427213](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40506427213)): 2061 tests, 4 FAIL. GREEN `d0ee5795c0aab844a7dcfc090519b20918227106` ([Actions #40506525853](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40506525853)): 2061 PASS, Skill/Eval validators PASS. Eleven synthetic deterministic tests.
- Research: `docs/research/intervening-event-observation-collision-2026-10.md`. The event list remains optional and non-exhaustive; the external authorized Executor alone owns writes/retries/idempotency/reconciliation.

## v1.106.0 — 2026-10-27

### Reject explicit nested null material-state evidence (MINOR)

- Fail closed on nested null in Complete observed endpoint controls or positive mid-window events, while preserving measured zero/false, omitted optional dimensions and null provenance outside state. No schema, Skill, dependency or Ads write added.
- RED `f15065538febbac1293774bc629fd6b413493fdf` ([Actions #40499231832](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40499231832)): 2050 tests, 4 FAIL. GREEN `da257cb33ef0a5b42732a9f74b0d709b6c2fb8e9` ([Actions #40499291654](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40499291654)): 2050 PASS, Skill/Eval validators PASS. Seven synthetic deterministic tests.
- Research: `docs/research/nested-null-material-state-evidence-2026-10.md`.


## v1.105.0 — 2026-10-27

### Reject one-sided optional Sponsored Products mid-window budget evidence (MINOR)

- For observed SP bid/budget `control_events`, reject one-sided base/effective daily budgets or average-daily-budget policy as `Unknown`. Both-absent optional bid-surface evidence and valid observed rule changes remain compatible. Preserve the existing Amazon Business placement addition/removal as a real observed confounder, not an unknown value. No schema, Skill, dependency or Ads write added.
- RED tests-only `57fd389bf8fa90c5a344256237742611e8bcd8bd` ([Actions #40491508793](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491508793)): 2043 tests, 8 FAIL. Initial fix `02aba1491c353665266283704e1ffae85c05b090` ([Actions #40491584220](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491584220)) exposed one pre-existing compatibility regression (1 FAIL). Corrected `33b4be37d1e4be9095c81702510238c39b66d787` ([Actions #40491683393](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40491683393)): 2043 PASS, Skill/Eval validators PASS. Twelve synthetic deterministic tests.
- Research: `docs/research/intervening-sp-optional-budget-evidence-parity-2026-10.md`. Source/licensing notes: `docs/SOURCES.md`. Missing/partial/unsupported/unknown never become zero; empty/omitted events never prove continuous control stability.

## v1.104.0 — 2026-10-27

### Reject invalid mid-window Sponsored Products budget and routing event states (MINOR)

- Apply source-supported SP budget amount/policy and site/retailer routing semantics to explicit post-owned `control_events` before/after states. For budget-change reviews, event budget state must contain base/effective budget, active rules and policy; bid-change reviews preserve partial legacy budget shapes but reject invalid explicit values. Unmapped or contradictory routing and one-sided retailer scope return `Unknown`. Observed valid transitions remain `Confounded` or `Treatment Isolated` as appropriate.
- RED `4076b1fe06d202437ec13483c5d1f3a1e2e0fc50` ([Actions #40482958315](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40482958315)): 2029 tests, 10 FAIL. First GREEN `0ef6014bd1c80ed55dc0d67c4b8063a705b2d7ee` ([Actions #40483041208](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483041208)): 2029 PASS. Additional type-safety RED `96674486cf6dbcf84f5cbff990929eb8b4bd0e94` ([Actions #40483075939](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483075939)): 2031 tests, 2 ERROR; GREEN `ca024abd07ebe448b87d032be8ae77441da021da` ([Actions #40483095636](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40483095636)): 2031 PASS, Skills/Evals PASS.
- Sixteen deterministic synthetic tests; no new Skill, schema field, dependency or live Amazon Ads write. This is internal event-value consistency, **not** authenticated complete event history or eligibility proof. Research: `docs/research/intervening-sp-budget-routing-state-semantics-2026-10.md`; source and copyright boundary: `docs/SOURCES.md`.

## v1.103.0 — 2026-10-27

### Reject invalid observed Sponsored Products event-only control values (MINOR)

- Reuse existing source-supported value semantics for optional intervening `control_events` in Sponsored Products causal comparisons. Invalid base/video bid, placement, audience or bidding-strategy before/after evidence is `Unknown`, not a manufactured competing transition or isolated treatment. Valid decimal strings, zero, actual observed confounders and supported bidding aliases remain compatible.
- RED `a3ed449a99b36228cd6c8cb6d708e22bf3248a25` ([Actions #40475574154](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40475574154)): 2012 tests, 14 FAIL. GREEN `5761b7760e851bfaa8ca2f56560a9ea37e0bf2d3` ([Actions #40475654662](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40475654662)): 2012 PASS, Skills/Evals PASS. Further alias compatibility tests and final PR validation are tracked in PR #216.
- No new Skill, schema field, dependency or Ads mutation. See `docs/research/intervening-sp-event-state-semantics-2026-10.md` and `docs/SOURCES.md`. Missing/unsupported/partial/unknown never become zero; external authorized Executor remains responsible for any live write.

## v1.102.0 — 2026-10-27

### Detect observed intervening material-control changes missed by endpoint-only readbacks (MINOR)

- Added optional post-owned `control_events` to the read-only control snapshot contract. A positively observed, scope/source-bound mid-window competing change is `Confounded` even when endpoint states match after a reversion. Invalid/partial/derived, out-of-window, duplicate, mismatched or endpoint-readback-colliding events are `Unknown`. The intended treatment still needs its own verified endpoint change.
- RED tests-only `02d082dcb7f9bce5f4961352443e0e661cf05dfc` ([Actions #40469314324](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40469314324)): 1990 tests, 17 FAIL. Initial GREEN `a2cb16ff682c5ebf15ab2c0631e1362a55fb8044` ([Actions #40469412526](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40469412526)): 1990 PASS. Two additional regression tests and provenance/treatment guard were added before final CI.
- Synthetic deterministic tests only; no API writes. Empty/omitted event arrays preserve legacy endpoint behavior and **do not** certify full-window history. Research: `docs/research/intervening-control-events-2026-10.md`; source/licensing review: `docs/SOURCES.md`. 15 Skills preserved; VERSION, README and all three runtime manifests synchronized.


## v1.101.0 — 2026-10-27

### Reject N/A and Not Applicable material-control evidence (MINOR)

- Complete observed control inventories no longer launder whole-label N/A/Not Applicable in scalar, nested or list state, or Sponsored Products schedule/event/budget rule and audience identities, into isolated or comparable decisions. Whitespace/hyphen/underscore variants are unresolved; real opaque identifiers, observed zero/false and competing control changes remain compatible.
- RED tests-only `7b66c043256d95376c3d3c0f9e00f3e1eeb887eb` (Actions #40463277508): 1970 tests, 12 FAIL. GREEN minimal fix `d0ccfd996b1d3c28d252b7add1fdcd9b6cd4682b` (Actions #40463362413): 1970 PASS, Skill/Eval validators PASS. Seventeen synthetic deterministic tests; no live Ads calls or writes.
- Research: `docs/research/material-state-na-rule-member-evidence-2026-10.md`; source/licensing notes in `docs/SOURCES.md`. VERSION, README and three runtime manifests synchronized. No new Skill, schema or dependency.


## v1.100.0 — 2026-10-27

### Reject contradictory transition provenance under reused readback identity (MINOR)

- Same concrete `source.readback_id` can no longer return `Comparable` with contradictory optional per-control transition actor, management mode, actor-evidence status, reason or transition timestamp. One-sided evidence is unresolved; exact UTC fractional seconds, distinct IDs and omitted legacy fields remain compatible. This is internal read-only consistency, not external actor authentication or continuous rule-history proof.
- RED `bc3c7949fa53b463de96c6d6de1153193d8861a9` ([Actions #40457523558](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40457523558)): 1953 tests / 9 FAIL. GREEN `185a77312dee0a6e686ee2e5ea840b768bda8378` ([Actions #40457609259](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40457609259)): 1953 PASS, 15 Skills and 55 Evals PASS. Fifteen synthetic deterministic tests.
- Research: `docs/research/control-readback-transition-provenance-integrity-2026-10.md`. VERSION, README and all three runtime manifests synchronized. No new Skill, schema, dependency or Ads writes.


## v1.99.0 — 2026-10-27

### Reject unresolved N/A and Not Applicable scope/source identities (MINOR)

- The read-only control comparator no longer treats repeated whole-label `N/A` or `Not Applicable` as concrete marketplace, profile, campaign, entity, account, source-system, acquisition-channel or connector evidence. Whitespace, underscore and hyphen variants fail closed to `Unknown`; valid opaque IDs containing those tokens and legacy optional readback omissions remain compatible. No new Skill, schema, dependency or Ads write capability.
- RED tests-only `e9712f65c70c15521cf41c06d0c898f6474988ef` ([Actions #40451514757](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40451514757)): 1938 tests, 14 FAIL; GREEN minimal fix `98bcb0eb97a30616aef90c1ec53c0dd34467d1da` ([Actions #40451585223](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40451585223)): 1938 PASS, Skill/Eval validators PASS. Seventeen deterministic synthetic tests, three compatibility cases.
- Research and source/licensing boundary: `docs/research/control-scope-source-not-applicable-identity-2026-10.md`. Version synced across VERSION, README and all three runtime manifests.

## v1.98.0 — 2026-10-27

### Guard reused readback control effective-time and evidence-status consistency (MINOR)

- A reused concrete `source.readback_id` cannot describe conflicting material-control `effective_at` or `evidence_status` even when state and observation time match. The read-only comparator returns `Unknown` for these contradictions; equivalent UTC instants including nanosecond fractions, distinct IDs, and legacy omitted/null IDs remain compatible. No source authentication, full-window control proof or live Ads write capability is implied.
- RED tests-only `077767d6dcd9db6109d7d9e21e4013652442d52d` ([Actions #40445576097](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40445576097)): 1921 tests / 5 FAIL. GREEN fix `0bb42f303c9a8b00654fa008600403672f53ea1d` ([Actions #40445622542](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40445622542)): 1921 PASS; Skill/Eval validators PASS. Eleven deterministic synthetic tests. See `docs/research/control-readback-effective-evidence-integrity-2026-10.md`.
- Version synced to 1.98.0 in VERSION, README, Codex/Claude Code/WorkBuddy manifests. Skills remain 15; no schema change, dependency, third-party code reuse or Amazon Ads write.

## v1.97.0 — 2026-10-27

### Guard explicit control readback provenance and exact observation identity (MINOR)

- An explicitly supplied non-null `source.readback_id` can no longer be a placeholder, padded, blank or non-string identifier. Two snapshots reusing one valid ID must also agree on the exact UTC `observed_at` instant, including submicrosecond precision; identical ID with different times cannot prove `Comparable` or causal isolation. Omitted/null optional legacy IDs, distinct concrete IDs and offset-equivalent timestamps remain compatible. This is internal consistency, not authenticated full-window control history or Ads write authority.
- RED `daa1b8b53f9a9b0d8c655a56dcf45971bdab1fdc` ([Actions #40440704449](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40440704449)): 1910 tests, 12 FAIL. GREEN `763cf684410688387cdde53d2647a978f277799e` ([Actions #40440800591](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40440800591)): 1910 PASS; Skill/Eval validators PASS. Nineteen deterministic tests; research: `docs/research/control-readback-provenance-integrity-2026-10.md`.

## v1.96.0 — 2026-10-27

### Fail closed on reused readback observation identities (MINOR)

- Before/after control snapshots previously could reuse the same explicit non-null `source.readback_id` while claiming different bid/budget/rule/placement states, producing a misleading isolated/confounded/directional classification. Now return `Unknown` for the contradiction; distinct IDs, legacy omissions, one-sided IDs and unchanged states remain compatible. No new Skill, schema, dependency or Ads write authority.
- RED `a45f2530f23fd0de54157a79b527e4bf345f977e` ([Actions #40434390981](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40434390981)): 1891 tests / 4 FAIL. GREEN `1e68bda948ddbc6a4b960b187e9153c67fc5b455` ([Actions #40434481521](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40434481521)): 1891 PASS; Skills/Evals PASS. Nine deterministic tests. Research: `docs/research/control-readback-identity-reuse-2026-10.md`.

## v1.95.0 — 2026-10-27

### Validate explicitly supplied material-change re-verification instants (MINOR)

- A Ready holdout previously ignored an explicit `material_scope_changes[].reverified_at` even when null, Unknown, earlier than the change or later than the latest clean check. The optional field now requires known-offset RFC3339 and exact UTC ordering `change.timestamp <= reverified_at <= latest_verified_at`. Omitted legacy timestamps, valid equal/offset instants and exploratory plans remain compatible. No claim of authenticated or continuous Amazon Ads control history.
- RED `5bbbfed737c56b4a391cbb098f1afc44fd5385d7` ([Actions #40428169436](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40428169436)): 1882 tests / 8 FAIL. GREEN `d41bb195eb1c2d8377e3ee781a4e58342db9644a` ([Actions #40428221122](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40428221122)): 1882 PASS, Skill/Eval validators PASS. 15 Skills unchanged; no Ads writes.

## v1.94.0 — 2026-10-27

### Preserve exact fractional-second Ready holdout evidence chronology (MINOR)

- Python `datetime.fromisoformat` truncates seventh and later fractional digits, previously allowing a later isolation proof, launch check or material change to compare equal to a claimed latest clean boundary verification. Use exact original RFC3339 fractional seconds with UTC whole seconds for chronology; preserve valid arbitrary-precision timestamps, offset equivalence, optional legacy omissions and exploratory plans. No new Skill/schema/dependency, continuous-control proof, or Ads write authority.
- RED `22e46b287532b9a05a6cf5a55e72a791324277c3` ([Actions #40421697469](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40421697469)): 1868 tests / 6 FAIL; eight compatibility cases passed. GREEN `34bd6cbde493cf4e4dc6ad22f2ad62efae468458` ([Actions #40421775715](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40421775715)): 1868 PASS; Skill/Eval validators PASS. Fourteen deterministic tests. Research: `docs/research/ready-holdout-exact-fractional-chronology-2026-10.md`.


## v1.93.0 — 2026-10-27

### Guard Ready holdout latest monitoring chronology (MINOR)

- When a Ready holdout supplies boundary monitoring, its latest verification must be at least as recent as every valid, positively verified isolation proof timestamp. UTC instant comparison preserves offsets/fractions, optional legacy fields, unverified records and exploratory statuses. No new Skill, schema, dependency, source authentication, full-window coverage claim or Ads write authority.
- RED `1ffd1edf70f27a9f54cf5ca66e42d907e690ed40` ([Actions #40414421617](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40414421617)): 1854 tests / 5 FAIL. GREEN `57c998ae97e706f79a253fe58045a23ad754401c` ([Actions #40414491229](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40414491229)): 1854 PASS, Skills/Evals PASS. Eleven synthetic tests; research: `docs/research/ready-holdout-isolation-monitoring-chronology-2026-10.md`.

## v1.92.0 — 2026-10-27

### Reject whitespace-obfuscated Not Applicable combined metric identities (MINOR)

- Correct a bounded regex escaping error so `Ready` combined primary/guardrail metric labels such as `Not  Applicable`, tabs, newlines and nonbreaking spaces are unresolved rather than accepted as concrete. Valid metrics, non-combined Ready, Shadow Only and existing placeholder forms remain compatible. No new Skill, schema, dependency, source authentication or Ads write capability.
- RED `b1b031f4ec9009d4e34c70cdd4079acbce1aceaa` ([Actions #40407197848](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40407197848)): 1843 tests / 7 FAIL. GREEN `95e5e5381f43d763a04fc3633699c25c8f2ab0fb` ([Actions #40407278247](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40407278247)): 1843 PASS; Skill/Eval validators PASS. Thirteen synthetic tests. Research: `docs/research/ready-combined-not-applicable-whitespace-2026-10.md`.


## v1.91.0 — 2026-10-27

### Require known-offset RFC3339 Ready holdout evidence (MINOR)

- Reject -00:00, space separators and second-resolution timezone offsets as Ready holdout verification; preserve valid RFC3339 offsets/fractions, chronology, omitted legacy fields and exploratory plans. No external attestation or Ads writes.
- RED 9118fb40901f92a6b814efb092d8a2746668656d ([Actions #40398537707](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40398537707)): 1830 tests / 9 FAIL. GREEN 14a96bec12da27084d490273fee16e2f7fb5e6ac ([Actions #40398664913](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40398664913)): 1830 PASS; Skill/Eval validators PASS. Fourteen synthetic tests; research: docs/research/ready-holdout-rfc3339-known-offset-2026-10.md.


## v1.90.0 — 2026-10-27

### Reject additive official Amazon Ads benchmark rates (MINOR)

- Both the standalone aggregation gate and Ready combined experiment gate now reject additive or non-additive-deduplicated declarations for bounded official purchase/add-to-cart/detail-page-view/branded-search rates, cost-per-purchase/detail-page-view, and percent-of-purchases-new-to-brand metrics. No automatic ratio calculation, raw source authentication, or Ads write capability.
- RED `5aa792219be0fad06f9dc6e9b6226abf7c4682ad` ([Actions #40390201710](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40390201710)): 1816 tests, 14 FAIL. GREEN ([Actions #40390377095](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40390377095)): 1816 PASS; Skill/Eval validators PASS. Twenty-one deterministic synthetic tests; additive counts, ratio-derived declarations, non-combined and exploratory plans retain compatibility.
- Research: `docs/research/official-benchmark-derived-rate-aggregation-2026-10.md`. Source definitions from Amazon Ads benchmark reporting updated 2026-10-06. No Skill, schema or third-party dependency added.

## v1.89.0 — 2026-10-27

### Reject unresolved Ready combined-readout metric identities (MINOR)

- A `Ready` combined experiment now rejects whole-label unresolved, blank, padded and non-string primary or decision-driving guardrail metric names, including when aggregation is declared additive or ratio-derived. This aligns the Ready experiment entrypoint with the earlier standalone metric-identity safety gate; valid concrete names, non-combined Ready and exploratory plans remain compatible.
- RED fixture commit `7bc237b9ddeaaeb763a26a88af967442436a789a` ([Actions #40380168947](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40380168947)): 1795 tests, 15 FAIL / 0 ERROR. GREEN `38316fce2522ba4077d2a60f243d61955d47ae1a` ([Actions #40380281413](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40380281413)): 1795 PASS; Skill/Eval validators PASS. Twenty synthetic deterministic tests.
- No new Skill, schema, dependency, Amazon Ads write, or external source authentication. Research: `docs/research/ready-combined-metric-identity-parity-2026-10.md`.


## v1.88.0 — 2026-10-27

### Reject explicitly unresolved Ready combined-readout requirements (MINOR)

- When a `Ready` experiment explicitly supplies `comparison.requires_combined_readout`, require a JSON boolean. Null, placeholder strings, numeric and collection values no longer bypass the combined ratio KPI gate; omitted legacy fields, explicit false and exploratory plans remain compatible.
- RED `f9646ea99d354aa21c705be0b98abac5cf81bb1d` ([Actions #40371547946](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40371547946)): 1775 tests, 8 FAIL. GREEN `472dc5c7e3ee8edbca2af96ff358f568c0a2387b` ([Actions #40371654073](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40371654073)): 1775 PASS; Skill/Eval validators PASS. Twelve deterministic synthetic tests.
- No new Skill, schema, dependency, external data authentication or Amazon Ads write. Research: `docs/research/ready-combined-readout-requirement-2026-10.md`.

## v1.87.0 — 2026-10-27

### Reject explicitly unresolved standalone aggregation metric identities (MINOR)

- The read-only standalone gate distinguishes omitted optional `metric_name` from explicitly supplied null, blank, whole-label Unknown/Partial/Unsupported/Not Available/N/A or non-string names. Explicit unresolved identity with additive/disjoint declarations returns Unknown, not Allowed. Omitted legacy names, concrete additive names, ratio and overlap guards remain compatible.
- RED `ae3ef9647afd3dba7104725609d468521625c8ee` ([Actions #40362141223](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40362141223)): 1763 tests / 12 FAIL. GREEN `381d2d79d86ffa586e1f54f36e0cdd348f615941` ([Actions #40362301091](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40362301091)): 1763 PASS; Skill/Eval validators PASS. Nineteen synthetic tests.
- No new Skill, schema, dependency, remote authentication or Ads write. Research: `docs/research/standalone-explicit-unknown-metric-identity-2026-10.md`.

## v1.86.0 — 2026-10-26

### Reject explicit unresolved Ready holdout monitoring evidence (MINOR)

- `scripts/validate_experiment_plan.py` distinguishes omitted optional `comparison.boundary_monitoring` from explicitly supplied null/non-object. A supplied object cannot silently accept explicit null `launch_verified_at` or non-array `material_scope_changes`. Empty arrays and genuinely omitted optional fields remain compatible; exploratory plans retain unknown evidence.
- RED `bf292aa59a1b0e41f515c401fc2f6cb0ea3a2f62` ([Actions #40352431603](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40352431603)): 1744 tests, 9 FAIL. GREEN `9db9ae89691b126b4085b457d75ed62ffd498d1e` ([Actions #40352546029](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40352546029)): 1744 PASS, Skill/Eval validators PASS. Fourteen deterministic synthetic tests.
- No new Skill, schema, dependency, Amazon Ads write or external Executor change. Internal checks do not authenticate external holdout allocation or continuous rule execution. Research: `docs/research/ready-holdout-explicit-monitoring-evidence-2026-10.md`.

## v1.85.0 — 2026-10-26

### Block additive CPA/CPM/vCPM/ROI contradictions across both aggregation gates (MINOR)

- The standalone direct-sum gate and `Ready` combined experiment validation now recognize bounded CPA, CPM, vCPM and ROI ratio KPI tokens in addition to ROAS/ACOS/TACOS/CVR/CTR/CPC. Reject contradictory `additive` semantics (and `non_additive_deduplicated` in Ready combined readouts); keep genuine additive Spend/Impressions, unknown semantics, legacy unnamed, Shadow and non-combined callers compatible.
- RED test commit `28513208d2081202873f64c7fec3ecfd34d096b2` ([Actions #40343010591](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40343010591)): 1730 tests, 10 FAIL. GREEN commits `78ce6aa01cfae11516d5b139a40595f1e470b6b0`, `a0c638891937fa784e1a37a82de90bf3ededd752` ([Actions #40343137676](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40343137676)): 1730 PASS, Skill and Eval validators PASS. 19 synthetic deterministic tests.
- No additional Skill, schema, dependency, Amazon Ads mutation or external Executor change. This does not authenticate denominators, attribution, currency, date, grain, source completeness or causal lift. Research: `docs/research/extended-cost-return-ratio-aggregation-2026-10.md`.

## v1.84.0 — 2026-10-26

### Block contradictory additive ratio KPIs in standalone direct-sum gate (MINOR)

- When supplied, a bounded canonical ratio `metric_name` (ROAS, ACOS, TACOS, CVR, CTR, CPC) cannot authorize a direct sum under a contradictory `additive` declaration, even when `source_relation=disjoint`. Return Blocked; unnamed legacy calls, additive Sales/Impressions, and unknown semantics remain compatible. This is an internal contradiction check, not a recomputation or source-authenticity guarantee.
- RED `df175e0065e9c4fa7999860aca51bd9c87835e44` ([Actions #40339525064](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40339525064)): 1711 tests, 8 FAIL. GREEN `f656e102e21e5217ed7ee0969248a733ace7f497` ([Actions #40339653449](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40339653449)): 1711 tests and Skills/Evals validated. Fifteen deterministic synthetic tests.
- No new Skill, schema, dependency, Amazon Ads write, or external Executor change. Research: `docs/research/standalone-ratio-direct-sum-contradiction-2026-10.md`.

## v1.83.0 — 2026-10-26

### Separate unambiguous retail/rank metrics from attributed conversion names (MINOR)

- `Ready` experiment plans no longer force exact Total Retail Sales, Retail Sales, Organic Sales or Sales Rank into ad-attributed conversion semantics, or match "sale" inside unrelated Wholesale Traffic. Bare Sales, Total Sales, Ad-Attributed Sales, Purchases, and explicit conversion-family claims remain gated; applies to primary and guardrail metrics.
- RED `958827676f9c9613f3c22c7b2681e93eea01cdcd` ([Actions #40327402552](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40327402552)): 1696 tests, 6 FAIL. GREEN `4251870e93e694e3acc8e846c14a1adf9fb9d6e7` ([Actions #40327563792](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40327563792)): 1696 PASS, Skill/Eval validators PASS. 14 deterministic synthetic tests.
- No new Skill, schema, dependency, live Amazon Ads mutation or external Executor change. Research: `docs/research/experiment-retail-metric-name-boundary-2026-10.md`.

## v1.82.0 — 2026-10-26

### Fail closed on canonical ratio KPI aggregation in Ready combined readouts (MINOR)

- `Ready` experiments with `comparison.requires_combined_readout=true` reject `additive` or `non_additive_deduplicated` aggregation declarations for bounded ROAS/ACOS/TACOS/CVR/CTR/CPC names, in primary metrics and guardrails. Require `ratio_or_derived` instead; recompute from compatible, complete base components and check source/grain/attribution separately. This is an internal semantic consistency check, not an automatic recomputation or remote data authenticity proof.
- RED `40227502f362a635d3e54a4d33332010ec2c8ac6` ([Actions #40317709806](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40317709806)): 1682 tests, 8 FAIL. GREEN `d714b9805a020ea21738e3e32e184b90c0d093e2` ([Actions #40317743385](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40317743385)): 1682 PASS, Skill and Eval validators PASS. 14 deterministic synthetic tests.
- No new Skill, schema, dependency, Amazon Ads mutation, or external Executor change. Research: `docs/research/experiment-combined-ratio-aggregation-2026-10.md`.


## v1.81.0 — 2026-10-26

### Fail closed on additional Ready conversion metric aliases (MINOR)

- ACOS, CVR, Attributed Orders/Units and Units Sold primary metrics or guardrails can no longer declare traffic/Unknown to bypass conversion attribution family and semantic version. ACOS/CVR use bounded tokens so TACOS (total retail sales) is not mistaken for ad-attributed ACOS. Genuine non-conversion and exploratory plans remain compatible.
- RED `81fb26b7dceddf1afbc42f91c8effd5e6a02bbd8` ([Actions #40310486694](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40310486694)): 1668 tests, 10 FAIL. GREEN `c7ba5a903a5a74cf1f06b4da4d147d889224135f` ([Actions #40310592404](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40310592404)): 1668 PASS, 15 Skills, 55 eval fixtures. Fifteen synthetic tests.
- No new Skill, schema, dependency, Amazon Ads write or external Executor logic; internal metric labels do not authenticate remote attribution. Research: `docs/research/experiment-ready-conversion-alias-coverage-2026-10.md`.

## v1.80.0 — 2026-10-26

### Fail closed on contradictory Ready conversion metric identity (MINOR)

- Ready Purchases/Sales/ROAS primary metrics and conversion guardrails cannot use a declared non-conversion or Unknown metric family to bypass the attribution gate. Whole-label placeholder attribution family or semantic version is unresolved; concrete, valid labels and non-conversion/exploratory plans retain compatibility.
- RED `28abfc14c5af075973556045dd0dcb794911a6e7` ([Actions #40301701019](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40301701019)): 1652 tests / 7 FAIL. GREEN `2c156db5e53e46171ea8051f74eec888d00be9dd` ([Actions #40301895414](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40301895414)): 1653 PASS, 15 Skills, 55 eval fixtures. Fourteen deterministic synthetic tests.
- No new Skill, schema, dependency, or Amazon Ads writes; semantic labels are not external provenance authentication. Research: `docs/research/experiment-ready-conversion-semantic-identity-2026-10.md`.


## v1.79.0 — 2026-10-26

### Resolve claimed Ready holdout isolation evidence (MINOR)

- A `Ready` holdout can no longer use `verified: true` with whole-label unavailable/padded `isolation_evidence[].evidence` to claim a verified boundary. Explicit optional `source` and `verified_at` must be concrete and timezone-aware; absent optional fields, valid narrative evidence and exploratory Shadow/Hold/Redesign plans retain compatibility.
- RED `4ae7cd51a0807bb2d42684a5e1a1e1a4acf2cc89` ([Actions #40294180163](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40294180163)): 1639 tests / 8 FAIL. GREEN `a28cc1c9e50f771b9defb6c35ebdd6f8fe3ab03f` ([Actions #40294279133](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40294279133)): 1639 PASS, 15 Skills, 55 eval fixtures. Twelve synthetic deterministic tests.
- No new Skill, schema, dependency or live Ads write; internal consistency does not authenticate holdout delivery. Research: `docs/research/experiment-ready-isolation-evidence-integrity-2026-10.md`.


## v1.78.0 — 2026-10-26

### Complete optional Ready holdout monitoring evidence (MINOR)

- Supplied `comparison.boundary_monitoring` for a `Ready` holdout must contain `current_status = Clean` and a valid timezone-aware `latest_verified_at` even without recorded scope changes. Optional `launch_verified_at` must be a valid instant no later than the latest verification. Previously the empty/no-change path skipped these checks.
- RED `6983ef9dcc136206d89bcddc46ba50b78ca045b1` ([Actions #40281384600](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40281384600)): 1627 tests, 9 FAIL; GREEN `209584832e0dc89f92a076e29d3c43a92d428f52` ([Actions #40281435606](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40281435606)): 1627 PASS, 15 Skills and 55 eval fixtures PASS. Fourteen synthetic deterministic tests.
- Monitoring remains optional for legacy Ready holdouts; Shadow/Hold/Redesign remain exploratory. No new Skill, schema, dependency, live Ads writes or Executor behavior. Internal evidence consistency is not remote delivery authentication. Research: `docs/research/experiment-ready-boundary-monitoring-completeness-2026-10.md`.


## v1.77.0 — 2026-10-26

### Positive re-verification for material holdout boundary changes (MINOR)

- A `Ready` holdout now requires explicit boolean `reverified: true` on every recorded `comparison.boundary_monitoring.material_scope_changes` entry. Previously missing, null or non-boolean flags were accepted whenever the latest verification timestamp was later; that timestamp does not itself prove each change was re-verified. Existing chronology, Clean status and positive evidence remain necessary.
- RED `5370f7fbcbeefc113ff3cc0b38b6f48892fa765d`, [Actions #40276084171](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40276084171): 1613 tests, 6 FAIL; GREEN `eba5db8b194f3907186ecda1f1ec9e4a3ef8b93c`, [Actions #40276152016](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40276152016): 1613 PASS, 15 Skills and 55 eval fixtures PASS. Ten synthetic deterministic tests; `Shadow Only`/`Hold`/`Redesign` unchanged.
- No new Skill, schema, dependency, Amazon Ads account write, retry, idempotency or Executor logic. This internal readiness gate does not authenticate external holdout delivery or source records. Research: `docs/research/experiment-material-change-positive-reverification-2026-10.md`.


## v1.76.0 — 2026-10-26

### Concrete Ready experiment identity and arm-boundary guard (MINOR)

- The read-only `scripts/validate_experiment_plan.py` now rejects whole-label unavailable/placeholder identities and padded marketplace/profile/entity-type/treatment IDs for `status=Ready`. Duplicate treatment IDs, and explicitly supplied duplicate/placeholder/overlapping control-arm IDs, cannot pass readiness.
- Valid opaque IDs containing words such as `unknown` remain supported; control IDs remain optional for platform-randomized/hard-boundary holdouts; `Shadow Only`, `Redesign` and `Hold` continue to preserve unresolved scope.
- RED-first synthetic tests: commit `a6152af0b3f7dc26968e0b0eee1fe102f95e72f4`, [Actions #40271192479](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40271192479): 1603 tests, 10 FAIL. Production repair `854e0ddbace1ac2d467b603b7e8449dd3d5b27bb` plus whitespace normalization correction `be860dd7958742a76a4ca42ff78555d2b42a1cbe`; [GREEN Actions #40271281809](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40271281809): 1603/1603 PASS, 15 Skill validators, 55 eval fixtures.
- This is a repository-owned readiness identity contract, not an Amazon-native ID grammar, independent control allocation verification, raw API authentication or Ads write authority. No new Skill or external dependency; Executor boundaries unchanged.
- Official platform context, public project re-review and copyright decisions are documented in `docs/SOURCES.md` and `docs/research/experiment-ready-identity-boundary-2026-10.md`.

## v1.75.0 — 2026-10-26

### Stable identity-keyed SP rule member comparison (MINOR)

- Registered Sponsored Products bid/budget control-state comparisons now ignore source enumeration order **only** for complete, validated `schedule_rules`, `event_rules` and `active_budget_rules` with unique concrete `rule_id`. Reordering alone no longer fabricates an additional competing material-control change; actual member additions/removals, modifier/activation changes, malformed/one-sided evidence and other material list order remain guarded. This does not prove continuous rule execution or advertiser eligibility.
- RED `f51b605bbe0aaef47f9819a57aaf98ca2e9c2895` [Actions #40266042350](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40266042350): 1590 tests, 3 FAIL; seven compatibility/safety controls passed. GREEN `63c7976d5ea23e1e72e9b7c9368786d1b44c6b2a` [Actions #40266103247](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40266103247): 1590 PASS, 15 Skills and 55 eval fixtures PASS. Ten deterministic tests.
- Research: `docs/research/sp-rule-member-order-invariance-2026-10.md`. No new Skill, schema, dependency, Amazon Ads account write, retry, idempotency or external Executor behavior.


## v1.74.0 — 2026-10-26

### Feature eligibility capability-level source evidence guard (MINOR)

- A feature-specific source reference cannot reuse any `capabilities[].evidence[].reference`, including from non-required or Unsupported capabilities. Prior binding-level collision protection remains; both Eligible and Ineligible collisions degrade to Unknown rather than Pass/unsupported exclusion. No source authenticity or Amazon Ads entitlement is inferred from distinct labels.
- RED `47520eb3787d75c0d75a9e5435bb5c610c3f91f1` [Actions #40261027113](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40261027113): 1580 tests, 4 FAIL. GREEN `17b798291ba143d779c077eb4248e2a7293ad027` [Actions #40261080915](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40261080915): 1580 PASS, 15 Skills and 55 eval fixtures PASS. Seven deterministic synthetic tests.
- Research: `docs/research/feature-eligibility-capability-evidence-reference-2026-10.md`. No additional Skill, schema, dependency, Amazon Ads account write, retry, idempotency or Executor behavior.

## v1.73.0 — 2026-10-26

### Feature eligibility cross-capability source-reference guard (MINOR)

- A feature-specific eligibility source reference cannot reuse a binding ID, surface ID or probe reference from ANY observed connector capability in the same snapshot, even if that capability is not required for the decision or its binding is Unverified/Unsupported. Both Eligible and Ineligible self-references degrade to Unknown; only the source-reference collision check expands. Distinct labels are not remote-source authentication. Preserve 15 Skills, existing capability selection, data/time/identity gates, default Suggest/Shadow and external-only Executor.
- RED `c971a41633c3fe2328909c5a2682bc64aed60da6` [Actions #40256092116](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40256092116): 1573 tests, 6 FAIL. GREEN `83310e41df04a0ed15689556c7b283e67259ec27` [Actions #40256160583](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40256160583): 1573/1573 PASS, Skill and eval validators PASS. Nine deterministic synthetic tests.
- Research: `docs/research/feature-eligibility-cross-capability-reference-2026-10.md`. No new Skill, dependency, schema, live Ads write, retry, idempotency or external Executor behavior.

## v1.72.0 — 2026-10-26

### Feature eligibility unverified-binding self-reference guard (MINOR)

- A required connector capability may have both a Verified binding and an Unverified probe. Feature eligibility cannot reuse the Unverified probe's binding ID, surface ID or evidence reference as independent feature-specific proof. Such Eligible/Ineligible claims become Unknown/Degraded rather than Pass or a purported verified exclusion. Existing valid distinct references, required capability validation, 15 Skills and external-only Executor boundary remain unchanged.
- RED `438bfd3395c68bafc232b581aa206375443aa719` [Actions #40250988299](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40250988299): 1564 tests, 4 FAIL. GREEN `96ecd664f08a69bcfd238fc3e22ad4c0e6b40840` [Actions #40251036262](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40251036262): 1564 PASS, 15 Skills and 55 eval fixtures. Six deterministic tests.
- Research: `docs/research/feature-eligibility-unverified-binding-reference-2026-10.md`. No new external dependency, raw HTTP authentication or live Amazon Ads write.

## v1.71.0 — 2026-10-26

### Concrete campaign identity for Sponsored Products causal reviews (MINOR)

- Registered SP bid/budget control-state comparisons now require a concrete campaign ID on both baseline and post snapshots. Repeated missing/null campaign IDs cannot produce `Treatment Isolated` even with identical profile/marketplace and complete control lists; valid opaque IDs and non-SP surfaces retain existing behavior. No schema change, new Skill, live Ads write or Executor.
- RED `d2a58cb88d5420a53c6c4d72e274b0e3b61a0465` [Actions #40246750015](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40246750015): 1558 tests, 4 FAIL. GREEN `49d49d3fbbaf59bb27315d61d8578b99e2276399` [Actions #40246791399](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40246791399): 1558 PASS, 15 Skills, 55 eval fixtures. Seven deterministic tests.
- Research: `docs/research/sp-causal-campaign-scope-2026-10.md`. Disproved duplicate candidate PR #183 closed unmerged.

## v1.70.0 — 2026-10-26

### Feature eligibility self-reference provenance guard (MINOR)

- Reject an eligibility `source_reference` that exactly repeats a Verified required connector binding's ID, surface ID or supporting evidence reference. Both self-referential Eligible and Ineligible assertions become Unknown/Degraded rather than high-confidence Pass or a purported verified exclusion. Expose `feature_source_independence_effect`; preserve distinct-reference eligibility, existing scope/time/freshness checks, legacy calls, 15 Skills, and external-only execution. This is not raw API authentication.
- RED `ef887fedffc413f5baa9498e9ae259e1cf5a929f` [Actions #40241663063](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40241663063): 1551 tests / 4 FAIL. Initial GREEN `47dc61a042084f7b808ed7589ed78f88b912dd8d` [Actions #40241697745](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40241697745): 1551 PASS, 15 Skills and 55 eval fixtures PASS. Eight synthetic tests.
- Research: `docs/research/feature-eligibility-self-reference-2026-10.md`.

## v1.69.0 — 2026-10-26

### Feature eligibility as-of connector snapshot chronology (MINOR)

- An independently Verified feature-specific Eligible record cannot combine with a connector snapshot captured after the requested feature decision `as_of` to yield high-confidence Pass. Expose `feature_snapshot_chronology_effect` as `pass`, `unknown` or `not_evaluated`; missing/invalid/future capture degrades. Preserve independently verified Ineligible blocking, explicit connector freshness requirements, equal/earlier capture and legacy no-feature requests. No inferred TTL, Amazon-native entitlement claim, live writes or new Skills.
- RED `fb1b05f68475947bf300626bc43d729e2910c12d` [Actions #40237374264](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40237374264): 1543 tests, 12 FAIL. Code `0dda06bd1e145df833323a8741c2df5e71850d83`; GREEN fixture `bd3f46630bd94bb33c3f63d7025ecaca1e575948` [Actions #40237456989](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40237456989): 1543 PASS, 15 Skills PASS, 55 Eval fixtures PASS. Twelve synthetic tests.
- Research: `docs/research/feature-eligibility-snapshot-asof-chronology-2026-10.md`.

## v1.68.0 — 2026-10-26

### Exact-scope feature eligibility evidence join (MINOR)

- Add an optional, independently supplied feature-specific eligibility evidence subgate to the existing read-only connector capability gate. Join feature, marketplace, advertiser account, campaign, concrete source and observation horizon; preserve legacy requests. Verified Ineligible blocks; unknown/partial/stale/mismatched/unverified/generic product-group evidence degrades, never becomes zero or inferred enrollment. No Amazon Ads writes, new Skills, or external Executor.
- RED `e426200e49ab7172832a9ae3f38ac11e6653feb0` [Actions #40232208710](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40232208710): 1531 tests, 20 FAIL + 1 ERROR. GREEN `59af08746c112ac516ff454749a64c423f75780a` [Actions #40232275602](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40232275602): 1531 PASS, 15 Skills and 55 eval fixtures PASS. 22 synthetic tests.
- Research: `docs/research/feature-eligibility-evidence-join-2026-10.md`.


## v1.67.0 — 2026-10-26

### Canonical observation-only connector access evidence (MINOR)

- Align the canonical `*-observe` capability catalog with the snapshot schema and read-side gate. A Verified `observe` surface can satisfy only a catalog-declared `observe` requirement; it cannot substitute for report/read access or authorize execution. Preserve all binding, identity, scope, freshness and data-contract checks and legacy transport behavior.
- RED `75c26edc14b9ab52f57e16504fc62f2ddab46735` [Actions 40227658177](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40227658177): 1509 tests, 6 FAIL. GREEN `3b4bc4b6ea5895b6ed88471b325ad92a4fb72fe6` [Actions 40227736857](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40227736857): 1509 PASS, 15 Skills and 55 eval fixtures PASS. Fourteen synthetic tests; no Ads writes or new Skills.
- Research: `docs/research/connector-observe-access-catalog-2026-10.md`.

## v1.66.0 — 2026-10-26

### Exact advertiser-account/campaign connector scope (MINOR)

- Add optional exact advertiser-account and campaign scope checks to the generic read-only connector capability gate and capability/binding JSON schema. Require independent bounded membership for both surfaces; opaque IDs compare case-sensitively. Preserve existing marketplace/ad-product scope behavior, unknown-versus-blocked distinction and legacy requests. This does not assert Amazon feature eligibility or authorize execution.
- RED test commits `f3b4c62493bf1c86bebd87da123d650ec517bf80` / `06696562cdaf134c986a66faa4be72c79fffecb2`: [Actions 40223225257](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40223225257) 1495 tests, 3 FAIL + 16 ERROR. GREEN code/schema `20d4473c5105d9524f39250892906f47984fe01a`: [Actions 40223291984](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40223291984) 1495 PASS, 15 Skills and 55 eval fixtures PASS. Twenty synthetic tests; no Ads account writes or new Skills.
- Research: `docs/research/connector-account-campaign-scope-2026-10.md`.

## v1.65.0 — 2026-10-26

### Global Sponsored Products concrete identity provenance (MINOR)

- Reject echoed unavailable or whitespace-padded account/campaign/explicit request IDs, readback connector/source identities and raw marketplace crosswalk IDs/source identities before claiming `Confirmed`. This closes a distinct Global SP readback gap rather than modifying the generic Connector Capability Gate. Preserve legitimate identifiers containing placeholder substrings, valid state/budget crosswalks, and legacy index-only receipts. `Unknown` is not a zero value or proof of failure.
- RED `99c1cfdd07bc1befa262c26ba8e7c8ed1c541259` [Actions 40218402467](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40218402467): 1475 tests, 15 FAIL. GREEN `ba70013601547d7145f0d12651760c09feb1aab1` [Actions 40218449534](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40218449534): 1475/1475 PASS; 15 Skills and 55 eval fixtures PASS. Eighteen deterministic synthetic tests, no Amazon Ads writes or new Skills.
- Research: `docs/research/global-sp-concrete-identity-evidence-2026-10.md`.


## v1.64.0 — 2026-10-26

### Reporting sunset capture-time consistency (MINOR)

- A required reporting generation marked active/sunset_scheduled with an already-passed declared `sunset_at` at snapshot capture is unreconciled: return Unknown/Degraded rather than high-confidence Pass. This does not automatically retire a reporting generation or hard-code Amazon's changing migration dates. Preserve future/equal sunsets, explicit retired blocks, and no-generation requests.
- RED `597329a99a6ef14c156f0541ab0aeb36f0714ab2` [Actions 40213666049](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40213666049): 1457 tests, 3 FAIL. GREEN `e4ed8e6bb5edac71cff49e4aca63114522a6c48c` [Actions 40213715351](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40213715351): 1457 PASS, 15 Skill and 55 eval fixture validators PASS. Eight deterministic synthetic tests; no live Ads writes or new Skills.
- Research: `docs/research/reporting-sunset-capture-consistency-2026-10.md`.


## v1.63.0 — 2026-10-25

### Historical availability capture-horizon integrity (MINOR)

- A per-grain observed `available_through` more than one calendar day beyond snapshot capture cannot prove already-retrievable history for an exact requested window. Return Unknown/Degraded rather than high-confidence Pass. One-day date-only tolerance avoids inventing a marketplace timezone; no Amazon API SLA or data-maturity claim. Preserve earlier valid ranges, explicit unavailable/retired blocks and no-history behavior.
- RED `66e09b0a5eee15d1dbfc8f5a226de0bb1988f83b` [Actions 40208517094](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40208517094): 1449 tests, 3 FAIL. GREEN `315dac82d12335f219364278da0b439bee0af2f6` [Actions 40208569404](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40208569404): 1449 PASS, Skill/Eval validators PASS. Ten deterministic tests; no new Skill or live Ads write.
- Research: `docs/research/connector-history-capture-horizon-2026-10.md`.

## v1.62.0 — 2026-10-25

### Historical reporting grain identity evidence (MINOR)

- Reject placeholder/padded requested historical grain identities and degrade padded observed apparent matches, including valid-plus-padded duplicate ambiguity. Concrete case-insensitive grains and bounded dates remain compatible; no new Skill or live Ads writes.
- RED `0f1195bef1c2d509f7cd332edbb96f0345b58f96` [Actions 40203462802](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40203462802): 1439 tests, 8 FAIL. GREEN `6f1a632f255ce3a4b6a58c84182f12b29f675da0` [Actions 40203519607](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40203519607): 1439 PASS, 15 Skills and 55 eval fixtures PASS. Fourteen synthetic tests.
- Research: `docs/research/historical-grain-identity-evidence-2026-10.md`.


## v1.61.0 — 2026-10-25

### Reporting-generation identity evidence (MINOR)

- Reject unavailable, placeholder or whitespace-padded requested reporting-generation identities; repeated Unknown is not verified report compatibility. Explicitly unavailable or padded observed generation degrades to Unknown rather than proving a concrete mismatch or a false match. Concrete matches and mismatches retain existing semantics. No live Ads mutation, new Skill or external runtime dependency.
- RED commit `78e8072f56dc58e206bdcab6bd5e8eebaa887a13` [Actions 40199527214](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40199527214): 1425 tests, 13 FAIL. GREEN commit `e354a59688f88a8104bbb77c2793bd2c7379b76c` [Actions 40199576967](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40199576967): 1425/1425 PASS, Skill and Eval validators PASS. Eighteen deterministic synthetic cases.
- Research: `docs/research/reporting-generation-identity-evidence-2026-10.md`.


## v1.60.0 — 2026-10-25

### Connector unknown scope final-gate classification (MINOR)

- Fix the mismatch between `scope_effect=unknown` and the final `Blocked` decision for **observed unmatched unknown/malformed scope members**. Such evidence is now `Degraded` without high confidence; missing/unbounded capability scope and fully concrete mismatch remain `Blocked`, and concrete matches remain compatible. No live Ads write or new Skill.
- RED commit `1e8bbe031ee918cff0022d06d8c59fc19626e66f` [Actions 40194559495](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40194559495): 1407 tests, 6 FAIL. GREEN commit `e94535bd29acadad70633cb33e6e63ff32f86328` [Actions 40194643701](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40194643701): 1407/1407 PASS, Skill and Eval validators PASS. Ten synthetic deterministic tests.
- Research: `docs/research/connector-unknown-scope-gate-classification-2026-10.md`.


## v1.59.0 — 2026-10-25

### Connector scope identity and exclusion evidence (MINOR)

- Reject unavailable or whitespace-padded requested decision scope labels; a matching Unknown label cannot prove marketplace/account/ad-product support. A capability/binding scope with unmatched unknown/malformed members is `unknown`, not proof of exclusion. Preserve verified concrete matches and fully concrete mismatches. This is read-side evidence only, not Amazon Ads entitlement or live writes.
- RED `50500f991d8f92fe7f45d66f872d5eb5fcc33838` [Actions 40190109725](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40190109725): 1397 tests, 12 FAIL. GREEN `f4fabf40499d5b71f323792d8638758f9925a254` [Actions 40190166935](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40190166935): 1397/1397 PASS, 15 Skill and 55 eval fixtures PASS. 17 synthetic deterministic tests; no new Skill, dependency or Executor.
- Research: `docs/research/connector-scope-placeholder-evidence-2026-10.md`.


## v1.58.0 — 2026-10-25

### Connector snapshot/source provenance identity (MINOR)

- A Supported/Verified connector read capability cannot yield high-confidence Pass when required snapshot connector identity is missing, unknown, null, or whitespace-padded; explicitly invalid optional source/acquisition identities also degrade the overall gate. Valid source identities and omitted legacy optional fields remain compatible.
- RED [Actions 40186241773](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40186241773): 1380 tests, 11 FAIL. GREEN [Actions 40186288201](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40186288201): 1380/1380 PASS, 15 Skill and 55 eval fixture validators PASS. No new Skill, dependency, Ads write, retry, or Executor functionality. Research: `docs/research/connector-snapshot-source-identity-2026-10.md`.


## v1.57.0 — 2026-10-25

### Read-side connector capability access-mode evidence (MINOR)

- A `Supported` connector capability with a `Verified` binding still needs a concrete read-side `access_mode`. A `write`-only capability is `Blocked`; `mixed`, `unknown`, missing, malformed or unsupported modes are `Degraded`. Only explicit `read`, `report`, `export` or `stream` access can pass the access-mode preflight, subject to other evidence gates. A second binding or snapshot default mode cannot override write-only access. This repository-owned read-side check does not authenticate remote tool behavior, grant write permission, or replace an authorized external Executor.
- RED `06dc8d93e11d1c47861881bc59a3f52f0b9e6f35` [Actions 40181875717](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40181875717): 1366 tests, 9 FAIL. GREEN `f81560b145411a20eeb4f8d43913eb130fec4c76` [Actions 40181914834](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40181914834): 1366 PASS, 15 Skills PASS, 55 eval fixtures PASS. No Amazon Ads writes.
- Research: `docs/research/connector-read-access-evidence-2026-10.md`. No new Skill or external dependency.


## v1.56.0 — 2026-10-25

### Verified connector binding identity integrity (MINOR)

- Reject unavailable placeholder or whitespace-padded `binding_id`/`surface_id` and evidence `kind`/`reference` from Verified connector surface proof; a repeated `Unknown` is not independent provenance. Valid alternate bindings, mixed evidence and real IDs containing such words remain compatible.
- RED-first 17 synthetic deterministic tests: 1353 total, 13 failures on previous behavior (Actions 40177634475); minimum repair GREEN 1353/1353 plus 15 Skill and 55 eval validators (Actions 40177671009).
- Read-only normalized evidence integrity only. No Amazon API enum, marketplace/advertiser entitlement, authenticated raw HTTP, new Skills, third-party dependency or Ads write.


## v1.55.0 — 2026-10-25

### Finite connector freshness horizon (MINOR)

- Reject NaN, positive/negative infinity and overflowing `freshness_requirement.max_age_seconds` values before connector snapshot/binding freshness checks. A non-finite horizon can no longer turn stale evidence into a high-confidence `Pass`; finite zero and positive horizons retain their behavior.
- RED-first 8 deterministic tests: 1336 total, 3 failures on previous behavior (Actions 40174166525). Minimal repair GREEN 1336/1336 plus 15 Skill and 55 eval validations (Actions 40174214895).
- Read-only decision-evidence guard; no Amazon-native TTL policy, account writes, new Skills, third-party dependencies or live connector authentication.


## v1.54.0 — 2026-10-25

### Verified connector binding temporal lineage (MINOR)

- A `Supported` connector capability and `Verified` surface binding can no longer produce a high-confidence Pass with impossible or malformed provenance chronology when no freshness horizon is supplied. Validate snapshot capture, binding verification and explicitly dated supporting evidence; reject unknown `-00:00` offsets and future/invalid times. A separate valid binding can still pass. Legacy undated supporting evidence remains compatible without a freshness claim.
- RED-first 13 deterministic tests: 1328 total, 10 failures on old behavior (Actions 40170267499); minimum repair GREEN 1328/1328 plus 15 Skills and 55 eval fixtures (Actions 40170330502).
- Connector-neutral read-side evidence guard only; no native Amazon Ads schema, eligibility proof, authenticated HTTP guarantee, account writes, new Skills or external dependency.


## v1.53.0 — 2026-10-25

### Optional Sponsored Products retailer-scope and Amazon Business control consistency (MINOR)

- Validate explicit normalized `targeting_or_routing.state.retailer_scope` (`AMAZON_STORE` or `ACROSS_RETAILERS`) in SP bid/budget causal comparisons. Unmapped/malformed or one-sided evidence is `Unknown`. Across-retailers scope cannot prove an Amazon Business placement modifier (including numeric zero) or Business-exclusive site routing. A real retailer-scope change remains a confounder.
- RED-first 21 deterministic tests: 1315 total, 15 failures on old behavior (Actions 40166608309); minimal repair passed 1315/1315 plus 15 Skills and 55 eval fixtures (Actions 40166648485). Both-absent legacy retailer scope stays compatible without eligibility proof.
- Repository-owned read-side labels only; no Amazon-native API schema, entitlement claim, Ads writes, new Skills, third-party code or dependency.


## v1.52.0 — 2026-10-25

### Scope, account and connector identity evidence (MINOR)

- Reject repeated unavailable labels and blank/whitespace-padded scope, account and source identifiers before causal classification; valid identifiers and both-absent optional connector IDs remain compatible.
- RED-first 20 deterministic tests: 1294 total, 17 failures on old behavior (Actions 40163083690); minimum fix passed 1294/1294, 15 Skill validations and 55 eval fixtures (Actions 40163139367).
- Repository-owned read-side evidence check only. No Ads writes, new Skills, dependencies or third-party code/schema.

## v1.51.0 — 2026-10-25

### Generic material-control placeholder evidence (MINOR)

- Close a cross-surface causal-isolation gap: an extra or fixture-required material control with repeated explicit Unknown/Unsupported/Partial/Missing/Unavailable, blank strings, or non-finite numbers could be treated as stable despite a Complete inventory and `observed` status. Validate all material state leaves recursively and return `Unknown` before causal classification. This does not infer zero/false or change the registry's required controls.
- RED-first 23 deterministic tests: 1274 total, 17 failures on old behavior (Actions 40159277435). Initial fix still failed four placeholder normalization cases (Actions 40159315750); corrected whitespace normalization and passed 1274/1274, 15 Skill validations and 55 eval fixtures (Actions 40159327265). Valid observed zero, booleans, descriptive strings, complete lists and actual competing changes retain existing behavior.
- Repository-owned read-side validation only; no live Amazon Ads writes, Executor logic, new Skills, external dependencies or third-party code.


## v1.50.0 — 2026-10-25

### Optional Sponsored Products rule activation transition-time evidence (MINOR)

- Extend the normalized read-only rule-member evidence contract with optional `activation_effective_at`: require timezone-aware RFC3339, no future transition relative to snapshot observation, an explicit valid `activation_status`, and symmetric presence across shared rule identities. Reject repeated Unknown/Unsupported/malformed/future timestamps rather than confirming unchanged controls.
- RED-first 18 deterministic tests: 1251 total, 15 failures on old behavior (Actions 40156028288); minimal repair passed 1251/1251, 15 Skills and 55 eval fixtures (Actions 40156066387). Verified changes in transition instant remain confounders. Both-absent legacy fields remain compatible; snapshots do not prove continuous execution, eligibility or intervening triggers. No live Amazon Ads writes, new Skills, external runtime or third-party code.

## v1.49.0 — 2026-10-25

### Optional Sponsored Products rule activation evidence (MINOR)

- Close an observed causal-isolation gap: a schedule/event bid rule or active budget rule could include repeated explicit `activation_status: Unknown`/`Unsupported` while a base-bid or budget change still returned `Treatment Isolated`. Reject invalid normalized activation status and one-sided activation evidence for the same rule identity; preserve valid `active`/`inactive`/`scheduled` states and real activation changes as competing controls.
- RED-first 18 deterministic tests: 1233 total, 13 failures on previous behavior (Actions 40151792978). Minimal production repair passed 1233/1233 tests, 15 Skill validations and 55 eval fixtures (Actions 40151826044). Both-absent legacy activation fields remain compatible but are not activation/continuous-time proof. No Amazon Ads writes, new Skills, third-party code, or new runtime dependency.

## v1.48.2 — 2026-10-25

### Sponsored Products rule-member evidence (PATCH)

- Fix a verified causal-isolation defect: complete schedule/event bid-rule and active budget-rule collections could contain duplicate/missing rule identities, Unknown/Unsupported modifiers, boolean/negative/non-finite values or malformed rows while the comparator still returned `Treatment Isolated`. Check each normalized member's unique nonblank `rule_id` and finite nonnegative `bid_increase` (schedule/event) or `increase_percent` (active budget rule). Active budget-rule members are checked during both bid and budget reviews.
- RED-first 34 deterministic tests: 1215 total, 28 failures on old behavior (Actions 40147934489); minimal fix passed 1215/1215 plus 15 Skills and 55 eval fixtures (Actions 40147983329). Observed numeric zero and valid decimal strings remain distinct from missing values; verified empty collections and genuine rule changes retain existing semantics. No native Amazon API schema, rule-activation guarantee, Ads write, new Skill or dependency.


## v1.48.1 — 2026-10-25

### Sponsored Products site-routing evidence (PATCH)

- Fix a real causal-readback gap: a repeated missing/Unknown/Unsupported `targeting_or_routing.state.site_restriction` could previously yield `Treatment Isolated` for Sponsored Products base-bid or budget changes. The comparator now requires a source-supported, explicitly mapped normalized site routing label (`ALL_ELIGIBLE` or `AMAZON_BUSINESS`) on both snapshots; unrecognized/malformed labels fail closed. A verified routing change remains a competing control (`Confounded`).
- RED-first 22 deterministic tests: 1181 total, 17 failures before the fix (Actions 40144118642); production fix passed 1181/1181 (Actions 40144167464). The normalized routing labels are not an Amazon Ads API schema and do not prove eligibility, platform-wide routing completeness or actual delivery. No new Skill, dependency, Ads write, retry or Executor behavior.

## v1.48.0 — 2026-10-25

### Sponsored Products rule-based ROAS guardrail evidence (MINOR)

- Amazon's rule-based bidding strategy uses a ROAS guardrail and is distinct from schedule/event bid rules. An unchanged bare `rule_based` label no longer proves treatment isolation; the normalized read-side `bidding_strategy.state` requires exactly `{"strategy":"rule_based","roas_guardrail":3}` (illustrative positive ROAS ratio) with source-supported, finite, strictly positive guardrail evidence. Unknown, unsupported, zero, negative, non-finite and unverified extra rule fields fail closed. This is not an Amazon API payload or proof of eligibility, activation or realized auction bids.
- RED-first 21 deterministic cases: 1159 tests, 9 failures on old comparator (Actions 40140153095). The updated comparison distinguishes stable complete rule-based evidence from guardrail changes, which are competing controls. Existing positive strategy fixture migrated; no new Skills, third-party dependencies or Ads writes.


## v1.47.4 — 2026-10-25

### Sponsored Products bidding-strategy evidence (PATCH)

- Fail closed when registered SP bid/budget causal snapshots supply Unknown, Unsupported, Partial, missing, malformed or unrecognized bidding strategy states; a repeated placeholder is not stable control evidence.
- Recognize four repository-normalized strategy families (dynamic down only, dynamic up and down, fixed, rule based), including hyphen spellings. Verified strategy changes remain confounders. These are local evidence labels, not Amazon-native API enums or proof of account eligibility.
- RED-first 21 deterministic tests: 1138 total, 14 failures on previous comparator (Actions 40135424725). A first implementation run exposed one overly strict test-reason assertion; corrected without weakening production behavior. No Ads writes, new Skills, dependencies or third-party code reuse.


## v1.47.3 — 2026-10-25

### Sponsored Products audience-member value and identity evidence (PATCH)

- Fix false Treatment Isolated or misclassified Confounded when complete audience collections contain invalid boosts, missing or duplicate IDs, malformed members or placeholders. Require unique nonblank string audience IDs and finite nonnegative observed boosts in repository-normalized readback. Retain verified empty collections, numeric zero, decimal strings and genuine audience-change confounders.
- RED-first 29 deterministic tests: 1117 total, 21 failures on old comparator (Actions 40130929665). Minimal repair and migration of older synthetic fixtures to the stronger member contract restored 1117/1117, Skill and Eval validation (Actions 40130997972).
- Official audience guidance supports per-audience bid controls but the normalized member shape is repository-owned. No new Skills, dependencies, live Ads writes, Executor behavior, universal platform ceiling or third-party code reuse.


## v1.47.2 — 2026-10-25

### Sponsored Products base-bid value evidence (PATCH)

- Fix false `Treatment Isolated` classifications when registered Sponsored Products bid/budget causal snapshots contain invalid `base_bid` values. Reject status placeholders, booleans, negative/non-finite numbers, percent strings and structured placeholders; do not treat missing as numeric zero.
- RED-first 21 synthetic tests: 1088 total, 15 failures on previous comparator (Actions 40126940011). Minimal repair restored 1088/1088 (Actions 40126986158), with Skill and Eval validators successful. Valid numeric/decimal-string bids and distinct budget treatment remain supported.
- This read-only validation does not assert Amazon marketplace bid minima/ceilings or authenticate the connector. No live Ads writes, new Skills, dependencies, third-party code or Executor changes.

## v1.47.1 — 2026-10-25

### Sponsored Products video bid value evidence (PATCH)

- Fix false `Treatment Isolated`/`Confounded` classifications when a registered SP bid/budget causal snapshot contains an invalid `video_bid_adjustment` value. Require finite nonnegative observed numeric evidence; reject Unknown/Unsupported/Partial, booleans, negative/non-finite numbers, percent strings and structured placeholders. Do not convert missing data to zero or invent a universal platform ceiling.
- RED-first 15 deterministic tests: 1067 tests, 11 failures on the previous comparator (Actions 40121930613); minimal repair restored 1067/1067, 15 Skill validations and 55 Eval validations (Actions 40121987510). Observed zero and decimal-string modifiers remain valid, and a real video-boost change remains a confounder.
- Official Sponsored Products video guide confirms video-specific bid boosts are separate from and can stack with placement adjustments. No live Ads writes, new Skills, dependencies, third-party code reuse, or Executor behavior changes.


## v1.47.0 — 2026-10-25

### Amazon Business placement modifier evidence (MINOR)

- Extend the read-only Sponsored Products bid/budget causal gate to validate an explicitly supplied `placement_adjustment.state.amazon_business` independently from Top of Search, Rest of Search and Product Pages. Invalid numeric evidence and one-sided omission now fail closed to `Unknown`; a changed observed B2B modifier is a confounder.
- RED-first synthetic regression: 1052 tests with 12 expected failures on the prior comparator (Actions 40118010958). Positive cases retain numeric zero, decimal-string values, and legacy three-placement snapshots without falsely claiming B2B capability proof.
- Amazon Ads official help updated 2026-09-28 identifies B2B placement separately and excludes across-retailers Sponsored Products from B2B placement adjustment. No marketplace eligibility assumption, exact bid-stacking formula, live Ads write, new Skill, dependency or third-party code reuse.


## v1.46.2 — 2026-10-25

### Sponsored Products placement modifier value evidence (PATCH)

- Fix false `Treatment Isolated` from placeholder, boolean, negative or non-finite Top of Search, Rest of Search and Product Pages modifiers in bid/budget causal comparisons. Require finite nonnegative observed values; do not invent a universal modifier ceiling or convert unsupported evidence to zero.
- RED-first 1036 tests with 12 confirmed failures after correcting two positive-control test expectations (Actions 40113083149; initial draft: 14 failures, Actions 40113031972); focused repair restored 1036/1036 and Skill/Eval validation (Actions 40113090733). Positive regression cases retain zero, plain decimal string and numeric modifiers.
- No new Skill, runtime dependency, Amazon Ads write, Executor retry or third-party code reuse.


## v1.46.1 — 2026-10-24

### Sponsored Products budget-state value evidence (PATCH)

- Fix false Treatment Isolated classifications from Unknown/Unsupported budget placeholders, boolean, negative/non-finite amounts and empty/unknown daily-budget policy. Plain decimal strings and explicit observed numeric zero remain distinct from missing data.
- RED-first 1019 tests with 11 failures (Actions 40108252702); minimal repair restored 1019/1019 plus 15 Skill and 55 Eval validations (Actions 40108325621). Additional boundary tests cover stable Unknown and explicit zero.
- Read-only only: no new Skills, Ads writes, retries, dependencies or third-party code reuse.

## v1.46.0 — 2026-10-24

### Global SP native campaign query-response membership proof (MINOR)

- Add an optional, read-only trusted-adapter `pagination_trace.pages[].response_body` consistency contract. If any page supplies native response evidence, every page must supply a `campaigns[]` array and `nextToken` matching the page trace; the complete `raw_campaign` must appear exactly once on the page identified by `raw_campaign_provenance.page_index`. Unexpected, missing, duplicate, displaced or internally contradictory campaign resources cannot produce false `Confirmed`.
- RED-first 20 synthetic tests: 1007 total, 14 failures (Actions 40103908902). Minimal fix `15f1a3e8ab23acbd0ea2e65087846269710af08a` restored 1007/1007 plus both validators (Actions 40103962004). Legacy traces without native page response bodies remain compatible.
- The adapter remains responsible for authentic HTTP capture, source completeness and execution; no Amazon Ads writes, retries, external code copying, new Skills or runtime dependencies.


## v1.45.0 — 2026-10-24

### Global SP native query-request filter and pagination binding (MINOR)

- Add an optional, read-only adapter-retained `pagination_trace.query.request_filters` and per-page `request_body` consistency contract. Every query must uniquely select the intended Sponsored Products GLOBAL campaign, reject additional ambiguous filters, and bind each continuation page's actual request token to the trace. A query fingerprint by itself remains an unverified adapter assertion.
- RED-first 24 synthetic tests (987 total, 20 RED failures; Actions 40099355669); minimal implementation restores 987/987 GREEN (Actions 40099426067). Legacy fingerprint-only traces remain compatible; explicit partial or contradictory native request evidence is `Unknown` rather than false `Confirmed`.
- No live Amazon Ads mutation, retry, idempotency, third-party code reuse, new Skill, or connector authentication claim.


## v1.44.1 — 2026-10-24

### Global SP query-level source contradiction guard (PATCH)

- Fix a false-`Confirmed` path when an explicitly retained `pagination_trace.query.source` contradicts the readback envelope and query pages. Malformed, incomplete and null explicit query sources now yield `Unknown`; legacy traces without query-level source remain compatible.
- RED-first 9 synthetic tests: 963 tests, 7 failures (Actions 40095254247). No new Skills, dependencies, Ads writes, retries, idempotency or Executor reconciliation.


## v1.44.0 — 2026-10-24

### Global SP supported marketplace identity guard (MINOR)

- Fail closed on unsupported, malformed or incorrectly aliased country codes across campaign configured-state/daily-budget, ad-group default-bid and positive target-bid readback. Amazon's dated Global SP guide enumerates eligible codes; `GB` is required instead of `UK`. A 207 receipt and an echoed unknown code cannot prove valid resource identity.
- RED-first 16 synthetic tests: 954 tests with 11 failures (Actions 40091597995); minimal shared eligibility guard restores 954/954 GREEN (Actions 40091645120), plus 15 Skill and 55 Eval validators. Existing valid marketplaces remain compatible. Unsupported/new marketplace eligibility requires fresh official verification before expanding the code set.
- Read-only classification only. No Amazon Ads writes, retries, idempotency, FX conversion, third-party code or new Skill.

## v1.43.0 — 2026-10-24

### Global SP retained native campaign budget cross-check (MINOR)

- When a trusted adapter explicitly retains native campaign `budgets` and the request includes supported daily monetary budget intent, cross-check the native marketplace monetary amounts/currencies/recurrence against independently normalized budget rows. Missing, malformed, duplicated or contradictory native budget evidence is `Unknown`; native and normalized agreement with a different requested amount remains `Drifted`.
- Native monetary numeric lexemes must be preserved as plain decimal strings; float/boolean source values cannot prove exact precision. The native budget field is optional for backward compatibility, and a state-only request does not claim budget verification.
- RED-first 27 synthetic tests: 938 tests, 21 failures (Actions 40087100016). Minimal read-only implementation: 938/938 passing, 15 Skills and 55 Eval fixtures validated (Actions 40087160510). No Ads writes, SDKs, or external code copying.


## v1.42.0 — 2026-10-24

### Global SP native campaign-to-query-page provenance (MINOR)

- When both optional `raw_campaign` and `pagination_trace` are supplied, require `raw_campaign_provenance` to bind campaign/account/filter/source/time to exactly one page. Unbound or contradictory adapter assertions return `Unknown` instead of false `Confirmed`; native-only and pagination-only legacy evidence remain supported. A complete but different state still returns `Drifted`.
- RED-first 20 synthetic tests in `tests/test_global_sp_native_page_provenance.py`: 911 tests, 15 failures (Actions 40083450668). Minimal code fix `58ea73207c5db3c0450058667f15c5cdea6291c2` restored 911/911 and both validators (Actions 40083485657).
- This is an internal trusted-adapter consistency check, not independent Amazon API authenticity, source completeness, or permission to write. No new Skills, dependencies or copied third-party code.


## v1.41.0 — 2026-10-24

### Global SP campaign query pagination trace consistency (MINOR)

- When an external trusted adapter supplies optional `readback.pagination_trace`, validate exact campaign/account/product/scope/filter identity, per-page source and observation time, and an unbroken, nonrepeating `nextToken` chain ending at null. A contradictory, incomplete or malformed trace now yields `Unknown` rather than `Confirmed`, even when the envelope asserts `pagination_status: Complete`. Legacy envelopes without this optional trace remain compatible.
- RED-first synthetic regression `tests/test_global_sp_query_pagination_trace.py`: 889 unit tests, 23 failures before the fix (Actions 40079424196). Minimal implementation commit `b0913d6926beab7a028e3a272e9d2d2bf41f52dc` restored GREEN (Actions 40079467166). The query trace remains an external assertion, not independent API authentication or row-completeness proof.
- Follow-up RED regression: 891 tests, 1 failure (Actions 40079540140) exposed a terminal `nextToken: null` followed by an extra page. Minimal correction `7ee85ecf5ed4e31670c0ae31af75eed5b206fa9d` rejects pages after a terminal token; final GREEN must validate all 891 tests.
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


## v2.9.0

- Reject unresolved or padded observed measurement scope when an event supplies scope without expected_scope.
- Preserve missing scope as missing; concrete opaque IDs remain compatible.
- Reject unresolved or padded account identity values in measurement and realization history projections.
- Preserve missing account identity as missing; concrete opaque identifiers remain compatible.
