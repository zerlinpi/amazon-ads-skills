# Amazon Ads Skills

A portable **Amazon Ads decision library for AI agents**. It packages 15 focused Skills for audit, monitoring, diagnosis, growth, experiments, search terms, targeting, bids, budgets, placements, profitability and post-change learning without turning this repository into an autonomous write bot.

> 当前版本：`v1.71.0`  
> Default mode: `Suggest`  
> Live Amazon Ads writes: external Connector / Executor only

## What you can do

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