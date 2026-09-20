# Methodology sources

This repository does not copy third-party skill text wholesale. Public repositories are used to discover generic methods, operating concepts and documentation structures. Ideas are independently rewritten for Amazon Ads, checked against the repository safety model, and kept connector/runtime neutral.

## Reviewed repositories

### nospicyplease/amazon-ppc-advanced-skills

Reviewed for thin `SKILL.md + references`, performance-drop diagnosis, contribution analysis, retail context, control-change timelines, Mixed-ASIN safety, negative attachment verification, growth headroom, post-change readback, optimization memory and approval-gated mutation concepts.

A recent review also reinforced that retail intelligence should carry freshness/coverage labels before trend claims and that parent/child variation changes belong in retail-readiness diagnosis.

Only generic concepts were adopted. Vendor-specific APIs, storage implementations and fixed click/order/spend thresholds were not imported.

Repository: https://github.com/nospicyplease/amazon-ppc-advanced-skills

### AgriciDaniel/claude-ads

Reviewed for progressive loading, contextual benchmarks, marginal-return thinking, guardrails, validation/rollback and separation of observation, diagnosis, recommendation and mutation.

Repository: https://github.com/AgriciDaniel/claude-ads

### Ecom-Wizards-Agency/Arcana

Public Amazon PPC skill repository reviewed for audit/data-quality methodology. Useful generic ideas included resolving profile-specific currency/timezone/objective, checking freshness/completeness before interpretation, aggregating additive base metrics before recomputing ratios, and reconciling account/profile totals with a complete campaign view instead of summing overlapping entity grains.

A repository-level license was not found during this review. Therefore no Arcana prose, MCP contracts, HTML-report template, tool names, fixed workflow text or implementation was copied. Only generic audit principles were independently rewritten into `skills/amazon-ads-audit/references/account-audit-framework.md` and the aggregation-integrity eval.

Repository: https://github.com/Ecom-Wizards-Agency/Arcana


### KuudoAI/amazon_ads_mcp

MIT-licensed Amazon Ads MCP implementation reviewed for connector-layer engineering rather than PPC decision rules. Useful generic ideas included explicit profile/region scope, asynchronous report/export lifecycle, progressive tool disclosure for very large tool catalogs, tool-catalog auditing, structured schema validation, and corrective error hints.

No MCP tool names, package catalog, field aliases, auth flow, middleware, prompts, report-field tables, code-mode implementation or error-envelope code were copied. These ideas were independently rewritten into the connector-neutral capability snapshot and reference.

Repository: https://github.com/KuudoAI/amazon_ads_mcp

### TrackIQ-HQ/amazon-seller-skills

MIT-licensed Amazon seller Skill repository reviewed for the generic lesson that advertising decisions may require adjacent retail evidence such as sales/traffic, inventory, returns, offer/Buy Box state, Brand Analytics/Search Query Performance and rank context.

No TrackIQ MCP interface, commercial workflow, tool names, skill prose or implementation was copied. The review only informed the optional retail-readiness capability classes documented in the connector capability research note.

Repository: https://github.com/TrackIQ-HQ/amazon-seller-skills

### ppcprophet/amazon-ads-mcp

Public repository with an MIT license file reviewed only as a capability-taxonomy reference; its README describes the hosted PPC Prophet MCP service as proprietary. Generic categories such as campaign/search-term/ASIN performance, period comparison, diagnosis, profile management and rule/change history were useful as a coverage check.

No hosted-service API, thresholds, commercial workflow, widget behavior, tool schema or proprietary implementation was copied.

Repository: https://github.com/ppcprophet/amazon-ads-mcp

### 2446573/amazon-ads-agent

MIT-licensed project reviewed as lower-weight evidence for the common pattern of combining exported advertising data with external competitor/retail context.

No scraper, rule engine, prompt, fixed thresholds or workflow was copied. External competitive data remains optional and must carry independent provenance.

Repository: https://github.com/2446573/amazon-ads-agent

### LittleAksMax/amazon-ads-api-sdk-go

MIT-licensed public Amazon Ads SDK reviewed for a narrow, implementation-neutral reporting/query lesson: Amazon Ads entity-query surfaces can use `nextToken` pagination, while Reporting API v3 follows an asynchronous request → poll/fetch → download lifecycle. The repository itself explicitly describes its coverage as partial and Sponsored Products-oriented.

No SDK code, models, examples or API wrapper implementation were copied. The generic pagination lesson was independently adapted into the audit completeness gate: a returned page is not the full entity population while a continuation token remains, and whole-account ranking should wait for exhausted pagination or an equivalent trusted complete export.

Repository: https://github.com/LittleAksMax/amazon-ads-api-sdk-go

### agentskills/agentskills

Apache-2.0 Agent Skills specification and reference validator reviewed for cross-runtime skill packaging compatibility. The specification defines `name` and `description` as required frontmatter and allows only `license`, `compatibility`, `metadata`, and experimental `allowed-tools` as additional top-level fields. The reference validator explicitly rejects unknown top-level fields.

No specification prose or validator implementation was copied. The repository was independently normalized so repository-specific fields such as display names, localized descriptions, author and version live under the allowed `metadata` map; repository-owned Skills also declare `license: MIT`. This is a packaging/compatibility change only and does not broaden execution authority or alter Amazon Ads decision logic.

Repository: https://github.com/agentskills/agentskills

### sensein/agent_skills

Apache-2.0 public Agent Skills repository reviewed for deterministic portability checks around a canonical `skills/` tree. The useful generic lesson is that skill-format validation, broken-supporting-file detection and CI smoke checks can catch packaging regressions before an agent runtime discovers them interactively.

No validator code, installer implementation, test fixture or prose was copied. This repository independently implemented a small Python-stdlib validator focused on its own invariants: required/allowed frontmatter, folder-name identity, nested-skill rejection and repository-local relative Markdown references.

Repository: https://github.com/sensein/agent_skills

### ruicore/codex-skills

Apache-2.0 public Codex Skills repository reviewed for the broader operating principle `validation before confidence`: skill libraries benefit from explicit machine-readable/structural gates and repeatable validation commands rather than relying only on manual review or a single permissive runtime.

No registry schema, scripts, workflow code, skill prose or repository conventions were copied. The idea was independently adapted as a narrow deterministic validation layer that complements, rather than replaces, Amazon Ads capability replay/evals.

Repository: https://github.com/ruicore/codex-skills

### weisberg/agile_agentic_analytics

MIT-licensed repository reviewed for experiment lifecycle, power/MDE discipline when inputs exist, sample-ratio/contamination awareness, sequential-testing caution, realized-allocation integrity, holdout/control integrity and advertising-market interference.

Generic ideas that materially influenced experiment hardening:

1. declared split/nominal control does not prove realized assignment;
2. treatment can alter comparison cohorts through spillover or changed auction opportunities;
3. experiment validity must be checked before interpreting treatment-only lift;
4. control integrity can become stale when the environment changes.

These ideas were independently rewritten as Amazon Ads query/target/ASIN overlap, shared-budget/routing/automation leakage, auction displacement, constrained-resource interference and dated control-boundary revalidation.

Repository: https://github.com/weisberg/agile_agentic_analytics

### ir-anthology/ir-anthology.github.io

Public bibliography repository reviewed only as a discovery index for the WWW 2022 topic **Interference, Bias, and Variance in Two-Sided Marketplace Experimentation: Guidance for Platforms**.

No paper text, formulas or code were copied. The high-level interacting-units lesson was independently adapted to shared auction opportunity, pacing capacity and substitution between Amazon Ads scopes.

Repository: https://github.com/ir-anthology/ir-anthology.github.io

### open-mercato/open-mercato

MIT-licensed multi-tenant application reviewed only for the generic engineering principle that tenant/organization scope should be explicitly carried through requests and sensitive access paths should fail closed when scope is missing or invalid.

No ACL/code/schema was copied. The concept was independently adapted to marketplace + profile/account collision-safe optimization memory.

Repository: https://github.com/open-mercato/open-mercato

### datascale-ai/data_engineering_book

MIT-licensed data-engineering reference reviewed only for generic provenance/freshness concepts: heterogeneous sources have different ingestion paths/update frequencies, and downstream data should preserve source, timestamps and lineage rather than pretending all rows are measurement-equivalent.

The project does not copy chapter text, diagrams, code or templates. The idea was independently adapted into `references/data-lineage.md`: distinguish extraction time from event-date completeness, preserve semantic/filter/attribution context, and treat mutable historical backfill maturity as part of measurement comparability.

Repository: https://github.com/datascale-ai/data_engineering_book

### open-metadata/OpenMetadata

Apache-2.0 data-governance project reviewed only for the generic idea that metrics/data contracts are first-class governed metadata rather than anonymous column labels. This supports treating metric definition/version as part of measurement identity.

No OpenMetadata code, schemas, generated types, UI, API contracts or prose were copied.

Repository: https://github.com/open-metadata/OpenMetadata

### unifyai/unify

MIT-licensed repository reviewed for separating deterministic contract tests from end-to-end capability evals and for treating capability failures as semantic/system-design failures rather than only code failures. Rewritten as `contract checks` vs `capability replay`.

Repository: https://github.com/unifyai/unify

### Observal/Observal

Apache-2.0 repository reviewed for evidence-bearing evaluation criteria and a third state when evidence is insufficient. Rewritten as `met / not_met / insufficient_evidence`.

Repository: https://github.com/Observal/Observal

### TheQtCompanyRnD/agent-skills

Reviewed for a canonical skills tree shared across multiple agent runtimes, portable `SKILL.md + references`, and runtime-specific manifests separated from business logic.

Repository: https://github.com/TheQtCompanyRnD/agent-skills

### noique/cross-border-ecommerce-skills

CC BY-NC 4.0 project reviewed only for high-level weekly PPC cadence, current/prior-period comparison, campaign triage, search-term review and prioritized actions. Its prose, fixed thresholds, API calls and export steps were not copied into this MIT repository.

Repository: https://github.com/noique/cross-border-ecommerce-skills

### heymoezy/porter

Reviewed only for the generic experiment anti-pattern that bundled concurrent changes destroy causal attribution. A repository-level license was not verified during review, so no prose/code/templates were imported.

Repository: https://github.com/heymoezy/porter

### paperclipai/paperclip

Reviewed for generic execution-reliability patterns: partial application, ambiguous delivery, reconciliation and retry/idempotency. No implementation was imported. Idempotency remains an external Connector/Executor concern.

Repository: https://github.com/paperclipai/paperclip

### prathamesh-git9/effect-broker

Reviewed for the distinction between safely idempotent, reconcilable-after-uncertain-delivery, and unsafe-to-repeat side effects. Independently adapted as **stable intent + explicit idempotency contract + authoritative reconciliation**.

Repository: https://github.com/prathamesh-git9/effect-broker

### nexscope-ai/Amazon-Skills

MIT-licensed multi-agent-compatible Amazon skill collection reviewed for public Amazon-domain coverage, portable skill packaging, profitability modeling, multi-campaign strategy and portfolio-level budget thinking.

No skill prose/templates/fixed thresholds were copied. Generic ideas retained: allocation reflects objective/economics, and cross-campaign decisions should not reduce to one campaign's historical ACoS/ROAS.

A later review of its PPC Skill found useful examples of why fixed thresholds should remain local examples rather than repository defaults: the public Skill contains concrete order/click timing and bid-adjustment heuristics. Those values were **not** imported. Instead, this repository added a regression that explicitly rejects transferring third-party example percentages/thresholds into action-safe account recommendations without account-specific calibration.

Repository: https://github.com/nexscope-ai/Amazon-Skills

### MicrosoftDocs/Advertising

Official Microsoft Advertising docs repository reviewed only for a vendor-neutral portfolio-budget lesson: controls sharing a constrained resource can interfere when control scopes do not align.

No Microsoft-specific behavior is asserted as Amazon Ads behavior. The generic concept was independently rewritten as budget-pool/external-pacing conflict logic.

Repository: https://github.com/MicrosoftDocs/Advertising

### actions/checkout and actions/setup-python

GitHub's official MIT-licensed workflow actions were reviewed during the v1.0 release-readiness pass after the repository's CI emitted a Node 20 deprecation warning. Current official documentation/release metadata uses `actions/checkout@v7` and `actions/setup-python@v7`; these releases run on the current Node 24 action runtime generation. The hosted GitHub runner observed by this repository was already new enough for the documented runtime requirement.

Only the action major-version references in `.github/workflows/validate-skills.yml` were updated. No GitHub Action source code, workflow implementation, examples, composite action internals, or documentation prose was copied into this repository. This is infrastructure maintenance only and does not change Amazon Ads decision logic or execution authority.

Repositories:

- https://github.com/actions/checkout
- https://github.com/actions/setup-python

License/adoption note: both repositories are MIT licensed. Version/runtime facts were verified from GitHub's official repositories; the repository continues to use its own minimal validation workflow and independent test contracts.

## High-star agent / MCP / evaluation review — 2026-09-18

A point-in-time GitHub review of widely adopted projects is recorded in `docs/research/high-star-agent-project-review-2026-09.md`. Projects include `mem0ai/mem0`, `microsoft/autogen`, `crewAIInc/crewAI`, `langchain-ai/langgraph`, `vercel-labs/agent-skills`, `agentskills/agentskills`, `promptfoo/promptfoo`, `letta-ai/letta`, `modelcontextprotocol/python-sdk`, `confident-ai/deepeval`, and `modelcontextprotocol/registry`.

Stars are treated only as discovery metadata, not authority. The review records observed stars, license signals, engineering overlap, and explicit adoption/rejection reasons.

This round independently adopted one generic idea from the MCP Registry / Agent Skills ecosystem: stable capability identity should live in an explicit catalog rather than transient model wording. The implementation is repository-authored in `references/connector-capability-catalog.json` and `scripts/resolve_skill_capabilities.py`; no third-party registry schema, code, prompt, workflow, or template was copied.

A later connector-binding pass reviewed the MCP Registry's server identity/version/namespace verification model and Amazon Ads' distinct reporting/push acquisition surfaces. The repository independently applies the narrower principle that a canonical Amazon Ads capability claim should be traceable to a concrete connector surface plus observed scope/evidence before high-confidence use. This is implemented in `schemas/connector-capability-snapshot.json` and the repository-authored runtime gate; no MCP Registry `server.json`, OpenAPI schema, Amazon report schema, third-party MCP tool definition, or connector implementation was copied.

Generic orchestration/memory/evaluation frameworks were not imported as dependencies because their runtime concerns belong outside this portable Amazon Ads decision library. Their own licenses and copyrights remain with their projects.

### Incremental high-star / active-project scan — 2026-09-20

A fresh GitHub discovery pass used multiple domain queries rather than a fixed repository shortlist. Generic Agent Skills, MCP, evaluation, multi-agent and lineage searches were filtered toward projects with substantial adoption (including `stars:>1000` or `stars:>5000` where applicable) and recent pushes; Amazon Ads/MCP discovery used a lower `stars:>10` floor because the domain is much smaller. Stars are discovery context only, not an adoption criterion.

- `anthropics/skills` — surfaced in the >1k-star Agent Skills scan and had recent commits through 2026-09-10. No repository-root license file was found in this review, so no code, prompt, Skill, schema or workflow was reused. Its packaging/runtime concerns overlap methods already covered by the Agent Skills sources above.
- `google/skills` — Apache-2.0; actively updated through 2026-09-18. Reviewed for routing/catalog packaging only. No implementation was adopted because the current gap is Amazon targeting identity, not Skill discovery.
- `openai/openai-agents-python` — MIT; actively updated through 2026-09-17. Reviewed for execution/evaluation safety context. Its agent runtime and approval machinery remain outside this repository's read-only Amazon Ads decision layer.
- `microsoft/agent-framework` — MIT; actively updated through 2026-09-18. Reviewed for general validation/execution-safety engineering. No runtime dependency or implementation was adopted because it does not improve the specific Amazon Ads evidence-identity gap.
- `apache/hamilton` — Apache-2.0; recent maintenance through 2026-08-19. Reviewed as a mature lineage/dataflow reference; the repository's existing lineage contracts already cover the decision need, so no DAG/runtime dependency was added.
- `KuudoAI/amazon_ads_mcp` — MIT; still active through 2026-09-06 and already reviewed above. Re-discovered in the Amazon Ads MCP scan and de-duplicated rather than counted as new evidence.
- `zach22-1999/lingxing-mcp` — MIT; public initial implementation in 2026 with later documentation maintenance. Reviewed as connector-domain context only; no code/schema/workflow was reused because connector-specific implementation does not resolve the current Amazon reporting identity issue.

This scan produced no third-party implementation worth importing. The actionable evidence for this round came instead from Amazon's official Reporting v3 semantics below.

## Reviewed public MCP documentation

### Model Context Protocol tool annotations and server instructions

Current MCP documentation was reviewed for two connector-interface facts: tool annotations such as `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` are advisory hints rather than enforcement; and server instructions can explain cross-tool workflows but cannot guarantee critical security behavior. Those facts support preserving annotations/instructions as observed connector metadata while keeping authorization and safety gates deterministic.

No MCP SDK/spec prose or implementation was copied. The repository independently defines its own connector capability evidence contract.

Public references reviewed:

- https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- https://blog.modelcontextprotocol.io/posts/2025-11-03-using-server-instructions/

Licensing/adoption note: these are public protocol documentation sources used for factual protocol behavior. No SDK source or specification text is redistributed here.

## Reviewed public Amazon Ads documentation

### Amazon Ads MCP Server open beta

Amazon's official February 2, 2026 announcement was reviewed because the user plans to pair this Skill library with an advertising platform. Amazon describes the Amazon Ads MCP Server as an agent-facing translation layer for Amazon Ads API functionality, available in open beta to Amazon Ads partners with active API credentials, with reporting plus workflows that can include creating, updating, or deleting advertising objects.

Repository adoption is deliberately narrower: the MCP server is treated as an external Connector/Executor candidate. Its write-capable tools do not grant this repository mutation authority, and transient MCP tool/workflow names are not copied into canonical Skills. A custom host should map observed capabilities into the repository-owned connector capability snapshot/catalog and keep authorization, secrets, retry/idempotency and reconciliation outside the Skill layer.

Official source reviewed:

- https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta

Licensing/adoption note: this is public vendor documentation used for factual product/capability behavior. No Amazon prose, MCP tool schema, API request, workflow template, connector implementation, or proprietary code was copied.

### Sponsored Ads Reporting v3 targeting identity

Amazon's official Sponsored Ads Reporting v3 documentation was reviewed for entity-identity semantics. The `spTargeting` report contains both ordinary keywords and targeting expressions. Amazon documents `keywordType` as the discriminator: `BROAD`, `PHRASE`, and `EXACT` identify keyword rows, while `TARGETING_EXPRESSION` and `TARGETING_EXPRESSION_PREDEFINED` identify targeting-expression rows. The v2→v3 migration guide also maps the former `targetId` field into the v3 `keywordId` field.

That means an identifier field/value alone is not sufficient proof of the same targeting entity across reporting generations or targeting kinds. The repository independently applies the narrower safety rule that a populated control-state `entity_id` must be paired with a semantic `entity_type`, and baseline/post snapshots with a missing or changed type fail closed instead of being treated as comparable.

Public references reviewed:

- https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v3/report-types.html
- https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/reference/migration-guides/reporting-v2-v3.html
- https://d3a0d0y2hgofx6.cloudfront.net/ja-jp/guides/reporting/v2/metrics.html

Licensing/adoption note: these are Amazon public vendor documentation pages used only for factual reporting semantics. No Amazon prose, API request examples, report schema, templates, or proprietary implementation was copied; the schema/comparator changes are repository-authored.

### Unified Reporting and Amazon Marketing Stream

Current Amazon Ads public documentation was reviewed to verify that connector capability must distinguish reporting generation, cross-account/ad-product scope, history windows, and pull vs push acquisition paths. Unified Reporting can span multiple manager/advertiser accounts, ad products and countries and is replacing legacy Sponsored Ads/DSP reporting surfaces; Amazon Marketing Stream is a push-based source for hourly metrics and campaign-change messages for API-integrated advertisers.

No Amazon API schema, report template, documentation prose or implementation was copied. These facts only inform the connector-neutral reporting lifecycle and acquisition-channel capability fields.

Public references reviewed:

- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting
- https://advertising.amazon.com/solutions/products/amazon-marketing-stream


### Amazon Ads budget and bidding rules

Public Amazon Ads documentation was reviewed for current platform behavior, not as an open-source code source. Relevant public pages describe schedule/event-based bid rules, performance/schedule-based budget rules, advertiser-selected ROAS guardrails, dynamic bidding strategies, placement adjustments, account/portfolio budget controls, and modeled budget-opportunity metrics.

Two current support-center details materially hardened the budget workflow:

- **Edit your Sponsored ads campaign budget**, updated September 2, 2026, documents a Sponsored Products account-level daily budget cap for Sellers and points non-Sellers toward portfolio budget caps. This establishes a real upstream constraint that can bind even when an individual campaign budget is raised.
- **Performance metrics**, updated June 30, 2026, describes estimated missed clicks/impressions/sales as estimates based on historical/similar-campaign signals rather than realized outcomes. The current **Optimize your campaign** page, updated August 11, 2026, also defines `Average time in budget` as a serving-coverage signal and surfaces estimated missed opportunity metrics.

These facts support two narrow repository conclusions: budget feasibility must be evaluated across campaign → portfolio/account/business/external constraints, and platform missed-opportunity estimates are useful directional evidence but not guaranteed incrementality.

No Amazon documentation prose, UI assets or examples were copied into Skills. The repository independently rewrote the principles into `skills/budget-optimization/SKILL.md`, its on-demand `references/portfolio-budget-conflicts.md`, and a synthetic regression fixture.

Public references reviewed:

- https://advertising.amazon.com/library/guides/budget-rules
- https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers
- https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products
- https://advertising.amazon.com/library/guides/sponsored-products-best-practices
- https://advertising.amazon.com/help/GVYUKBJQFPH7ZQ2L
- https://advertising.amazon.com/help/GG44RFW942U9F6F5
- https://advertising.amazon.com/help/GJHF6GB7WZUMPYJ6

Licensing/adoption note: these are public vendor documentation pages, not relicensed source code. Only factual platform behavior and generic control-design implications were independently paraphrased; no copyrighted prose, images, API examples or proprietary implementation was imported.

## Internal method hardening from observed failure modes

Some additions are independent safety hardening rather than adaptations of a single external source:

- **Retail snapshot freshness** — a Buy Box/inventory/price/listing snapshot proves only the state/time it observed.
- **Source-lineage drift** — same metric name can hide different attribution, refresh, filters, grain or semantic meaning.
- **Semantic metric-version drift** — one stable table/column can change meaning across a semantic cutover.
- **Asymmetric backfill drift** — same source + same metric version can still be incomparable when a frozen baseline is D+1 while a post window is D+7 and historical rows restate.
- **Historical restatement after decision** — mutable history must not rewrite what evidence was available at decision time; preserve snapshot identity and append a correction/re-evaluation when latest data materially changes the outcome interpretation.
- **Audit aggregation integrity** — profile/campaign/keyword/search-term/placement views overlap; choose one canonical additive grain, reconcile complete parent/child totals, and recompute ratio metrics from additive components.
- **Audit population completeness** — API pagination, connector row caps and context truncation are separate failure modes; preserve continuation metadata and do not claim whole-population rank from a partial slice.
- **Contextual action sizing** — raw economic/directional estimates do not prove the final allowed change magnitude; without account policy, calibrated response, marginal headroom or declared experiment constraints, preserve direction instead of inventing a repository-global percentage/damping constant.
- **Upstream budget-cap feasibility** — campaign-level headroom is not independently actionable when an account/portfolio/business cap binds; modeled missed-opportunity metrics remain directional until pool feasibility and marginal economics are reconciled.
- **Agent Skills metadata compatibility** — runtime portability requires strict frontmatter compliance; repository-specific metadata belongs under the spec-defined `metadata` map instead of arbitrary top-level YAML keys.
- **Deterministic Skill packaging validation** — progressive loading is only reliable when entrypoints and referenced support files remain mechanically resolvable; structural validation should fail before runtime discovery when packaging drifts.
- **Parent/variation-family retail shock** — child conversion can move because family structure/sibling retail/purchased-ASIN mix changed.
- **Verified migration lineage** — explicit predecessor→successor mappings may preserve bounded historical context but never clone current state.
- **Verified cross-profile migration** — explicit same-marketplace profile moves are distinct from accidental cross-profile collisions.
- **Cross-marketplace portability limit** — verified mapping may preserve semantic relevance/business intent/failure patterns, but marketplace-specific bid/CPC/CVR/ACOS/ROAS/budget/profitability outcomes default to directional-only evidence until successor-market calibration.
- **Portfolio opportunity cost** — fixed business budget pools require source opportunity-cost reasoning.
- **Treatment/control interference** — treatment lift can be traffic/budget displacement rather than incrementality.
- **Shared-budget starvation** — treatment can mechanically consume control capacity.
- **Variation-family substitution** — child-level growth can be a family mix shift.
- **Long-test control-boundary drift** — control cleanliness is time-varying evidence.
- **Collision-safe optimization identity** — same entity text/ID is insufficient across marketplace/profile scopes.

## Integration rules

Before adopting an external idea:

1. Prefer generic methodology over vendor-specific APIs.
2. Do not copy substantial third-party prose.
3. Do not import private/client data.
4. Treat fixed thresholds/action percentages as optional heuristics unless supported by account evidence.
5. Preserve `Read-only / Suggest / Shadow / Execute` boundaries.
6. Keep detailed knowledge in references/playbooks for progressive loading.
7. Keep canonical business logic runtime neutral.
8. Predeclare experiment question, hypothesis, primary metric, guardrails and stop rules.
9. Never fabricate statistical confidence, power, MDE or allocation-integrity significance.
10. Preserve event lineage and distinguish intent, application, readback and outcome.
11. Prefer playbooks for recurring compositions of existing Skills.
12. Separate contract failures from capability failures in evals.
13. Preserve `insufficient_evidence` as a real outcome.
14. Never weaken a regression fixture merely to make a model pass.
15. Verify negative/control attachment scope before causal attribution.
16. Treat coupled auction controls as interacting parameters.
17. Treat experiment contamination/allocation mismatch/leakage/interference as readout limitations.
18. Treatment-only improvement is not incrementality proof when cohorts share demand/resources.
19. Shared budget/pacing requires pool-level reasoning.
20. Sibling child-ASIN substitution requires family-level/purchased-ASIN readout.
21. Revalidate long-test boundaries after material scope changes.
22. Longitudinal comparisons must verify source, available-through, attribution, scope, grain, filters, metric semantics and snapshot/backfill maturity.
23. Same table/column is not proof of same metric definition.
24. Same source/semantic version is not proof of same snapshot maturity when history can restate.
25. Preserve decision-time evidence identity when later historical restatement can change an optimization outcome.
26. Aggregate compatible base metrics first; recompute ratios; never sum overlapping entity grains as separate account traffic.
27. Exhaust pagination or verify equivalent complete coverage before whole-population audit rankings.
28. Separate raw monetary-control anchors from final allowed action magnitude; do not invent repository-global bid/budget percentages or damping constants when account-specific sizing evidence is absent.
29. Reconcile campaign, portfolio, account/business and external budget constraints before treating a campaign-level increase as independently deliverable; keep estimated missed-opportunity metrics labeled as modeled evidence.
30. Keep Skill frontmatter within the Agent Skills allowed top-level field set; custom metadata belongs under `metadata`.
31. Run deterministic structural validation after Skill/reference/schema/playbook changes; packaging confidence and capability confidence are separate gates.
32. Treat source/reporting switches near apparent breaks as competing explanations.
33. Treat parent/variation-family retail changes as upstream causal candidates.
34. Partial application is a realized treatment different from intended treatment.
35. Do not use promotion-contaminated windows as ordinary evergreen controls.
36. Retail-readiness failures are causal gates before traffic suppression.
37. Stale retail snapshots are historical evidence, not current proof.
38. Resolve marketplace + profile/account scope before merging memory.
39. Verified same-marketplace cross-profile migrations may carry bounded mature evidence but never clone current state.
40. Cross-marketplace migration defaults to directional evidence portability for performance/economic conclusions.
41. Timeout/unknown writes remain unresolved until reconciliation/idempotency makes repetition safe.
42. Stable idempotency keys stay bound to the same stable intent/payload.
43. Trusted current-state readback overrides earlier executor acknowledgement when they disagree.
44. Higher ROAS/revenue is not automatically higher profit.
45. A previous winner temporarily at zero orders needs conversion-break diagnosis before negative treatment.
46. Declared experiment allocation does not prove realized allocation integrity.
47. Fixed budget pools require source/destination opportunity-cost reconciliation.
48. Record reviewed sources here when they materially influence the project.

## Sponsored Products budget-control and incremental source scan — 2026-09-20

Detailed review: `docs/research/sponsored-products-budget-control-state-2026-09.md`.

Amazon official documentation reviewed this round establishes two decision-safety facts used by the repository: Sponsored Ads budget rules can automatically change a campaign's effective daily budget based on schedule/event or performance conditions, and the configured daily budget is an average-daily concept whose realized day-level spend can differ under the applicable policy/settings. These facts are independently adapted into a `sponsored_products_budget_change` control-state surface and effective-budget evidence gate; no Amazon prose, API schema, UI, examples or proprietary implementation is copied.

New GitHub candidates reviewed and de-duplicated:

- `MarketplaceAdPros/amazon-ads-mcp-server` — ~29 stars observed, MIT, last code push 2025-05-21; real TypeScript MCP wrapper but no repository CI/test suite surfaced and core value depends on a hosted service. Rejected for implementation reuse.
- `Xnurta/Xnurta-MCP` — ~14 stars observed, active through 2026-09-18; no root license file/license metadata surfaced. Abstract connector-domain context only; no code/Skill/prompt/schema/workflow reused.
- `jshorwitz/awesome-agentic-advertising` — ~40 stars observed, no license surfaced, README-only curated index. Discovery aid only; not counted as independent engineering evidence.
- `elementary-data/elementary` — ~2.4k stars observed, Apache-2.0, active with substantial CI. Strong generic data-quality/observability reference, but its runtime overlaps lineage/freshness/backfill controls already present here; no dependency added.
- `langfuse/langfuse` — ~34.8k stars observed, very active; core MIT with separately licensed enterprise directories. Strong external eval/trace infrastructure, but it does not improve the specific Amazon budget control-state proof boundary enough to justify a runtime dependency; no code/schema/prompt/evaluator copied.

Stars/activity are recorded only to reduce repeated discovery work; none of them override license, engineering fit, duplication, or action-safety criteria.

