# Methodology sources

## 2026-10-25: Sponsored Products video value-evidence review

- **Official platform evidence:** Amazon Ads, *Sponsored Products video: A complete guide*, https://advertising.amazon.com/library/guides/sponsored-products-video (checked 2026-10-25). Video bid boosts are distinct from placement adjustments and may stack. This supports separate observed control evidence, not a hard-coded cross-marketplace ceiling, a bid-stacking formula, or causal attribution from a single observation.
- **Open-source candidates (metadata observed 2026-10-25):** KuudoAI/amazon_ads_mcp (74 stars, MIT, non-fork, recent successful public integration Actions); vaibuep/amazon-ads-mcp (0 stars, MIT, non-fork, recent integration success, separate PR-title check failure); aws/agent-toolkit-for-aws (3055 stars, Apache-2.0, non-fork, recent CodeQL/dependency checks successful); nospicyplease/amazon-ppc-advanced-skills (14 stars, MIT, non-fork, older code activity). These observations are not full security, issue/PR, or implementation audits. The current video-value defect is deterministic and needs no external SDK/MCP, so all were **rejected for integration**. Generic capability/least-privilege ideas only; no third-party code, prompt, schema, template, or workflow copied. License scope for any nested vendored content must be separately verified before future reuse.


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

## Non-empty control collection completeness and incremental source scan — 2026-09-21

This round closed a control-state evidence gap exposed by deterministic regression: a non-empty returned collection is not proof that the collection is complete. For registry-required list-valued controls, decision use now requires machine-readable enumeration, pagination, and connector-capability completeness rather than inferring completeness from the presence of one or more rows.

### Amazon official evidence

- **Adjust Sponsored Products bids**, updated 2026-09-14: Amazon documents audience bid adjustments as a collection of independently configured audience boosts and currently allows selecting up to 10 audiences. This supports treating audience-adjustment state as an enumerable control surface rather than a single boolean/value. Source: https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5
- **Bidding strategies for Sponsored Products**, updated 2026-09-14: Amazon separately documents dynamic/fixed/rule-based bidding and audience bid adjustments. Source: https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7
- **Sponsored Products audience bid boosting**, public launch documentation: audience controls can be activated through Amazon Ads API / Ads Console and have audience-level performance reporting. Source: https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products
- **Unified reporting**, generally available 2026-06-08: Amazon documents campaign/placement/audience dimensional reporting across accounts and ad products. This is reporting-surface evidence only; it does not prove connector extraction completeness or remove pagination/truncation requirements. Source: https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Amazon documentation is public vendor documentation, not open-source implementation material. Only factual product behavior and generic evidence-safety implications are independently paraphrased; no Amazon prose, API schema, payload, examples, or proprietary workflow is copied.

### GitHub projects reviewed this round

Stars and activity below are point-in-time discovery context only, not adoption criteria.

- `denisneuf/python-amazon-ad-api` — ~202 stars observed; MIT; active through 2026-09-17; non-fork; public Amazon Advertising API wrapper with tests plus CodeQL/CI/release workflows. Useful as connector/API-surface engineering evidence, including explicit profile/marketplace routing, but it does not define this repository's causal or collection-completeness semantics. No wrapper code, endpoint model, credential pattern, exception implementation, or schema was copied.
- `google/agents-cli` — ~5.97k stars observed; Apache-2.0; active through 2026-09-16; non-fork; ships cross-coding-agent Skills and explicit eval run/generate/grade/compare/analyze lifecycle commands for Claude Code, Codex, and other coding agents. The generic lesson—keep evaluation lifecycle/versioned artifacts explicit—is already materially represented by this repository's deterministic tests and Skill-effectiveness contracts, so no CLI/Skill/eval implementation was imported.
- `GoogleCloudPlatform/agent-starter-pack` — ~6.56k stars observed; Apache-2.0; real tests/CI, but its own README marks it maintenance-mode and directs new development to `google/agents-cli`. It is retained as historical corroboration rather than a new implementation source; no templates, Terraform, CI/CD, evaluation configs, or deployment code were copied.
- `comet-ml/opik` — ~22.2k stars observed; Apache-2.0; very active on 2026-09-21 with extensive unit/integration/e2e/guardrail/evaluation CI. Strong general evidence for separating tracing, datasets, experiments, evaluation, and production monitoring, but adopting the platform would expand this repository's runtime/dependency surface without improving the specific Amazon control-collection proof boundary. No SDK, evaluator, trace schema, optimizer, prompt, or workflow was copied.
- `opendatadiscovery/odd-platform` — ~1.43k stars observed; Apache-2.0 metadata; active through 2026-09-20 with backend/frontend tests and CI. Its lineage/observability architecture is relevant generic corroboration, but source/acquisition/reporting/freshness/backfill lineage is already a first-class contract here. Rejected as a dependency and implementation source for this change.

Previously reviewed Amazon Ads MCP repositories (including KuudoAI, PPC Prophet, Xnurta, Hologrow/DataDoe-adjacent connector surfaces) were de-duplicated rather than counted again when no materially new decision-safety evidence appeared. Forks, curated link lists, hosted-service shells, and projects without a clear reusable license boundary were not treated as independent implementation evidence.

### Adoption decision

Adopt only the repository-owned invariant proven by RED→GREEN regression: **returned rows do not establish complete control state**. Every top-level list-valued registry-required control must carry complete enumeration + complete pagination + supported capability evidence before it can participate in a causal isolation result. Missing/partial/truncated/unsupported evidence remains `Unknown`; no live Amazon Ads write authority is added.

## Nested rule-collection completeness and incremental source scan — 2026-09-21

This round extends the existing collection-completeness invariant to decision-material lists nested inside structured Sponsored Products control state. A returned nested rule list is evidence of observed rows, not proof that every applicable rule was enumerated.

### Amazon official evidence

- **Understand budget rules in Sponsored ads**, updated 2026-09-02: Amazon documents schedule-based and performance-based budget rules that automatically increase Sponsored ads campaign budgets. Source: https://advertising.amazon.com/help/GNSMLANWNF344YBE
- **A complete guide to budget rules**: Amazon documents multiple budget/bidding rule types and automated rule behavior. Source: https://advertising.amazon.com/library/guides/budget-rules
- **Schedule based bid rules now available for Sponsored Products**, 2023-11-06: Amazon documents campaign bid rules for times of day, days of week, and date ranges, available through the Ads console and Amazon Ads API. Source: https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products
- **Events for schedule bid rules**, 2025-01-02: Amazon documents event-based bid-rule configuration for Sponsored Products. Source: https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers
- **Hours of day for schedule-based budget rules**, 2023-11-30: Amazon documents hourly schedule-based budget rules through the console or Amazon Ads API. Source: https://advertising.amazon.com/resources/whats-new/hours-of-day-available-for-schedule-based-budget-rules

These Amazon sources are vendor documentation, not reusable implementation artifacts. This repository independently paraphrases only factual platform behavior and the resulting evidence-safety requirement; no Amazon prose, API payload, schema, prompt, or workflow is copied.

### GitHub projects reviewed this round

Stars/activity are discovery context only and are not adoption criteria.

- `NVIDIA/SkillEvaluator` — ~494 stars observed; Apache-2.0; active on 2026-09-20; non-fork; real `tests/`, CI, security workflow, deterministic validation, deduplication, and paired live skill evaluation. Its tiered evaluation model is strong corroboration for separating deterministic contracts from live effectiveness measurement. Rejected as a dependency for this change because it does not address Amazon control-state enumeration or connector pagination; no evaluator, prompt, rubric, schema, or workflow was copied.
- `awslabs/agent-evaluation` — ~375 stars observed; Apache-2.0; non-fork; public `tests/` and CI/CD workflows; supports concurrent multi-turn agent evaluation and CI integration. Useful general evaluation evidence, but the repository's current deterministic causal-state regression is more direct and provider-neutral. No source, hooks, evaluator orchestration, or config was copied.
- `cisco-ai-defense/mcp-scanner` — ~1.07k stars observed; Apache-2.0; active through 2026-09-19; non-fork; substantial tests plus CI/CodeQL and explicit MCP readiness/security scanning. Relevant to future Connector/MCP execution-safety review, but it does not improve this round's read-only Amazon rule-enumeration contract. No scanner, YARA rule, analyzer, prompt, or security workflow was copied.
- `semgrep/mcp` — ~688 stars observed; MIT; public tests/workflows but archived, with last code push observed in 2025-10. Retained only as historical MCP security context and rejected as an active implementation source because the project is archived.

Previously reviewed Amazon Ads MCP/skills repositories and high-star agent/eval projects were de-duplicated rather than counted again when they provided no materially new evidence for nested rule completeness.

### Adoption decision

Adopt only the repository-owned fail-closed invariant proven by RED→GREEN tests: for decision-material nested rule lists, a structured parent object and a list value are insufficient proof. Each required nested collection must independently establish complete enumeration, complete pagination, and supported connector capability before it can participate in a causal isolation result. Missing/partial/truncated/unsupported/unknown nested evidence remains `Unknown`. No Amazon Ads write capability is added.



## Sponsored Products routing/site-state review — 2026-09-21

### Amazon Ads official — Amazon Business exclusive campaigns for Sponsored Products

Amazon's official launch page **Reach business shoppers with Amazon Business exclusive campaigns**, dated 2025-05-05, documents a Sponsored Products campaign-level Sites restriction for Amazon Business exclusive campaigns. Amazon states that API-created exclusive campaigns use `site Restrictions = AMAZON_BUSINESS`, that these campaigns serve only on the Amazon Business store, and that existing Sponsored Products reports for those campaigns reflect Amazon Business performance.

Adoption boundary: this source is used only to establish that campaign routing/site state can materially change the eligible traffic pool and therefore belongs in causal comparability for Sponsored Products bid/budget reviews. This repository does not copy an Amazon write payload, does not implement the write endpoint, and does not infer a default site state when a connector cannot expose it. Missing routing/site evidence remains Unknown.

Source: https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product

### Incremental GitHub review

Stars and activity are discovery context only, not adoption criteria. Previously reviewed projects, including `nexscope-ai/Amazon-Skills`, were de-duplicated instead of counted again.

- `linkfox-ai/linkfox-skills` — 104 stars observed on 2026-09-21; MIT; non-fork; recent push 2026-09-14. The public repository exposes a large API-driven skill catalog including Amazon Ads auth, management, reporting and SP insights, but its runtime depends on the LinkFox service/API and the root scan showed no repository-level tests or GitHub Actions workflows. Useful only as connector-capability coverage context. Rejected as an implementation source for this change because Amazon official documentation is stronger evidence for routing semantics and private/service-specific interfaces do not improve repository-owned decision safety. No prompt, schema, API wrapper or workflow was copied.
- `zach22-1999/amazon-skills` — 195 stars observed on 2026-09-21; MIT; non-fork; recent push 2026-08-20. The repository contains public Amazon seller analysis skills, including Brand Analytics and search-term workflows, plus release-gate documentation, but the root scan showed no repository-level tests or GitHub Actions workflows. It is relevant to Amazon analysis methodology but does not provide stronger evidence for campaign site routing or causal control identity. Rejected for this routing change as duplicative/domain-adjacent; no thresholds, prompts, report templates or implementation were copied.
- `adkit/ads-skills` — 27 stars observed on 2026-09-21; non-fork; recent push 2026-08-03. Its custom AdKit Skills License restricts redistribution and use in competing products, and the catalog is centered on non-Amazon advertising strategy. The root scan showed no repository-level tests or GitHub Actions workflows. Rejected for direct adoption on both relevance and license grounds. Only the abstract observation that portable ad skills benefit from runtime packaging separation was considered; no protected text, schema, prompt, workflow or implementation was reused.

Adoption decision: keep the current 15-Skill catalog unchanged. The only repository change justified by this review is the fail-closed `targeting_or_routing` requirement on the existing Sponsored Products bid/budget causal surfaces, backed by Amazon official evidence and deterministic regression coverage.


## MCP Skills content-integrity review — 2026-09-21

### modelcontextprotocol/ext-skills

The official MCP Skills extension repository was re-reviewed after SEP-2640 reached Final status in September 2026. Point-in-time GitHub metadata showed about 658 stars, active maintenance through 2026-09-18, a non-fork/non-archived repository, Apache-2.0 code licensing, and CC-BY-4.0 documentation licensing.

The stable extension defines Skill discovery/retrieval over MCP and binds published Skill files to a complete resource manifest carrying content digests and byte sizes. This exposed a concrete gap in this repository's existing custom-host progressive-loading helper: selected resource paths had no stable content identity for verification/cache invalidation.

Adoption boundary: the repository independently added SHA-256 + byte-size identities to its own `scripts/resolve_skill_context.py` output. It did not copy the MCP schema, TypeScript interfaces, examples, URI structure, server implementation, approval model, or documentation prose, and it does not claim that the repository-local `resource_manifest` is an MCP `skills/get` response.

Repository: https://github.com/modelcontextprotocol/ext-skills

Detailed source/candidate review: `docs/research/mcp-skills-content-integrity-2026-09.md`.

### 2026-09-21 de-duplicated high-star / Amazon API scan

A fresh multi-query GitHub pass rechecked directly relevant Agent Skills/MCP/runtime and Amazon Advertising API projects. Previously documented projects were de-duplicated rather than re-counted.

- `mattpocock/skills` — ~266.5k stars, MIT, active, non-fork; real Skills/scripts/docs/release workflow. Rejected for this change because a broad engineering Skill catalog does not strengthen Amazon Ads decision semantics or the normative MCP integrity boundary. No content or implementation copied.
- `obra/superpowers` — ~289.3k stars, MIT, active, non-fork; multi-runtime projections plus tests/scripts. Test-first/runtime-portability ideas overlap existing repository policy, so no dependency/content was adopted.
- `addyosmani/agent-skills` — ~97.8k stars, MIT, active, non-fork; Skills/references/evals/scripts plus plugin-install CI. Useful corroboration only; normative Agent Skills/MCP specifications remain stronger implementation evidence. No prompt, Skill, hook, eval or workflow copied.
- `denisneuf/python-amazon-ad-api` — ~202 stars, MIT, active, non-fork; code, tests and multiple CI workflows. Relevant as Amazon Advertising API transport engineering, but authentication/execution/retry belong to the external Connector/Executor. No SDK implementation copied.
- `amzn/amazon-advertising-api-php-sdk` — ~92 stars, Apache-2.0, archived, last observed push in 2020; rejected as stale evidence for current platform capability semantics.
- `StacklokLabs/skills-mcp` — ~2 stars, recently active, no clear repository license surfaced in GitHub metadata; lower-weight corroboration only, with no code/schema/workflow reuse.

Stars are recorded only as discovery context. License clarity, current maintenance, engineering evidence, scope fit, duplication and decision/action-safety value controlled the adoption decision.


## Operator/community evidence expansion — 2026-09-21

Evidence discovery now extends beyond GitHub to Amazon Seller Forums, Reddit and mature Amazon-operator knowledge bases. Community evidence is used to discover recurring workflows, trade-offs and failure modes; it is **not** treated as platform authority or as sufficient evidence for universal numeric rules.

### Sources reviewed

- Amazon Seller Forums — practitioner discussions around search-term harvesting, campaign structure/mission, TACOS vs ACOS, retail readiness and change tracking.
- Reddit communities including r/FulfillmentByAmazon and AmazonFBA-related communities — recurring operator discussion around discovery vs controlled traffic, ranking/growth vs profit trade-offs, placement mix, inventory/listing readiness, negative-keyword caution and over-optimization.
- Amazon-focused practitioner/vendor knowledge bases — corroboration for search-term harvesting and mission separation.
- Quora was included in discovery, but direct page access was blocked by robots during this review. No Quora-derived factual claim, threshold, workflow or text was adopted without direct verification.

### Adoption decision

The non-duplicative repository gap supported by this evidence was **campaign objective / mission as first-class decision context**. The repository now uses bounded analytical roles `Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, and safe `Unknown`; these are repository-owned analytical metadata, not a claim that Amazon exposes all roles as native campaign settings.

Community evidence also reinforced existing rules for retail readiness, search-term traffic ownership, change/readback history, placement separation and contribution economics. Those were not duplicated into new Skills.

### Explicitly rejected shortcuts

No universal default was adopted for fixed bid-change percentages, placement multipliers, budget allocation percentages, click/order/spend thresholds, exact waiting periods, one-keyword-per-campaign architecture, dayparting schedules, ranking promises, or claims that paid spend necessarily causes organic-rank lift. Such ideas remain account-specific hypotheses or caller policy unless stronger evidence makes them action-safe.

Detailed review: `docs/research/operator-community-objectives-2026-09.md`.


### Incremental runtime/evaluation review — 2026-09-21

- `evalstate/fast-agent` — 3,921 stars observed on 2026-09-21; Apache-2.0; non-fork/non-archived; pushed 2026-09-20; substantial unit/integration/e2e test trees and GitHub Actions workflows. Reviewed for Skills/MCP/ACP runtime composition, transport diagnostics, evaluation workflows and explicit runtime connection boundaries. The project is strong engineering evidence for keeping runtime orchestration, connector attachment and execution diagnostics outside a portable domain decision library. No dependency, agent workflow, configuration, prompt, MCP implementation, test fixture or schema was copied because those concerns overlap this repository's existing external-runtime boundary and do not improve the specific campaign-objective gap closed in bid/placement decisions.

Adoption decision: no runtime framework added. The current change remains a repository-authored, decision-layer campaign-objective gate; external Connector/Executor ownership and progressive-loading boundaries stay unchanged.

Repository: https://github.com/evalstate/fast-agent


## Campaign-objective lineage review — 2026-09-21

### Amazon Ads official evidence

Amazon Ads' **Sponsored Brands goal-based campaigns** launch documentation states that advertisers express a campaign goal and Amazon optimizes against goal-specific success metrics such as clicks or top-of-search impression share. Amazon's **How to measure and improve your campaigns** guide likewise says campaign success should be judged using KPIs selected for the intended goal, while its current Sponsored Products targeting guidance recommends establishing benchmarks from goals and historical performance.

Adoption boundary: these official pages support the decision-safety principle that a historical optimization must retain the objective and success/guardrail metrics that justified it. They do not define this repository's analytical role taxonomy, event schema, history projection, or objective-drift policy. No Amazon prose, UI, payload, schema, prompt, or workflow was copied.

Sources:
- https://advertising.amazon.com/resources/whats-new/sponsored-brands-goal-based-campaigns
- https://advertising.amazon.com/library/guides/measure-improve-campaigns
- https://advertising.amazon.com/library/guides/targeting-with-sponsored-products

### Incremental high-star agent/evaluation scan

Stars/activity are point-in-time discovery context only.

- `mozilla-ai/any-agent` — ~1.24k stars observed; Apache-2.0; non-fork/non-archived; public tests and CI; cross-framework agent execution/evaluation abstraction. Useful corroboration for keeping evaluation context explicit across heterogeneous runtimes. Rejected as a dependency because this repository needs a narrow Amazon decision-lineage contract, not another runtime adapter. No code, evaluator, trace schema, prompt, fixture, or workflow copied.
- `google/adk-go` — ~8.8k stars observed; Apache-2.0; non-fork/non-archived; active on 2026-09-21 with substantial CI and agent/memory packages. Strong runtime/memory engineering evidence, but its session/runtime memory machinery is broader than the append-first Amazon optimization ledger here. Rejected as a dependency or implementation source; no memory API, runner, schema, tool, prompt, or workflow copied.
- `mlflow/mlflow` — ~28.1k stars observed; Apache-2.0; non-fork/non-archived; active on 2026-09-21 with extensive testing/workflows and experiment/evaluation tracking. Reviewed for the generic principle that evaluation context and run lineage should remain attached to the historical decision rather than being silently overwritten by later context. No MLflow tracking model, schema, SDK, evaluator, trace format, or workflow was copied.

Previously reviewed Agent Skills, MCP, Amazon Ads API, evaluation and memory projects were de-duplicated rather than counted again.

### Adoption decision

The only new repository behavior justified by this round is narrower: preserve the **action-time campaign objective** with the latest-action history summary, detect objective drift during post-change/weekly review, evaluate a historical action against the objective/primary metric/guardrails that existed when it was taken, and use the current objective only for the next decision. This remains read-only/Suggest/Shadow logic and does not add executor/write/retry/reconciliation behavior.


## Test-harness integrity review — 2026-09-22

A schema-regression test on PR #78 initially used top-level pytest-style functions while repository CI runs `python -m unittest discover`. GitHub Actions therefore returned a false green because those functions were not collected. This round added a repository-owned unittest-discovery contract that fails when any `tests/test_*.py` file introduces top-level `test_*` functions under the current runner. After converting the regression to `unittest.TestCase`, CI exposed the intended missing-schema RED.

### Incremental high-value project review

Stars/activity are point-in-time discovery context only.

- `microsoft/skills` — ~3.0k stars observed on 2026-09-22; MIT; non-fork/non-archived; active through 2026-09-21; dedicated test-harness and skill-evaluation workflows plus a substantial `tests/` tree. Adopted only the abstract engineering principle that the CI runner and test authoring contract must agree and that Skill evaluation needs an explicit harness. No Microsoft test harness, prompt, workflow, SDK code, schema, or acceptance criteria were copied.
- `alibaba/skill-up` — ~1.0k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active through 2026-09-21; multiple CI/evaluation/security workflows. Useful evidence for treating Skill evaluation infrastructure as a first-class engineering surface. Rejected as a dependency because this repository already has deterministic unit/eval contracts and the immediate gap was local unittest discovery, not Skill-generation/evolution runtime. No code, evaluator, workflow, prompt, or schema copied.
- `SalesforceAIResearch/MCPEval` — ~156 stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; MCP-focused agent evaluation system. Relevant to MCP evaluation architecture but does not improve the concrete Amazon Ads schema-parity or unittest-discovery gap enough to justify another framework. No code, evaluator, prompt, schema, or workflow copied.

Amazon official reporting semantics remain the authority for measurement-composition behavior: Sponsored Display can combine modeled and directly attributed conversions in the same conversion columns and can expose `Unallocated` rows at lower reporting grains; Amazon DSP similarly combines modeled and directly measured conversions in campaign reporting. The repository adopts only the safety abstraction and does not copy Amazon schemas or implementation details.

Adoption decision: keep the current dependency-free unittest runner, make its collection contract explicit, and add the missing optional measurement-composition schema surface. Do not introduce pytest, a third-party evaluation framework, or live Amazon Ads execution capability solely to solve this gap.


## Post-change measurement-composition review — 2026-09-22

### Amazon Ads official evidence

Amazon Ads' Sponsored Display modeled-conversion documentation states that modeled conversions are reported in the same conversion columns as directly attributed conversions and that lower-grain reports can contain `Unallocated` (API example `-20`) rows when meaningful allocation cannot be produced. Amazon DSP likewise reports directly measured and modeled off-Amazon conversions together as a combined campaign result.

Adoption boundary: these official pages support a narrow safety rule for post-change review — compare measurement composition and lower-grain allocation coverage before attributing conversion/ROAS movement to an optimization action. No Amazon report schema, API payload, prose, prompt, or workflow was copied.

Sources:
- https://advertising.amazon.com/resources/whats-new/modeled-conversions-for-sponsored-display-campaigns
- https://advertising.amazon.com/resources/whats-new/modeled-attribution-for-off-amazon-conversions-for-us-advertiser

### Incremental lineage-project review

Stars/activity are point-in-time discovery context only.

- `OpenLineage/OpenLineage` — ~2.7k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active through 2026-09-21 with extensive CI. Useful canonical evidence that lineage metadata should remain explicit rather than inferred after the fact. Rejected as a dependency because this repository only needs a bounded Amazon Ads measurement-composition decision contract. No OpenLineage schema, client, event model, code, workflow, or documentation text was copied.
- `open-metadata/OpenMetadata` — ~15.3k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active on 2026-09-22 with dozens of CI/integration workflows. Strong evidence for explicit context/quality metadata, but far broader than the repository's append-first optimization memory. Rejected as a dependency and implementation source; no metadata model, test harness, connector, schema, or workflow copied.
- `datahub-project/datahub` — ~12.7k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active on 2026-09-22 with substantial build/test and connector workflows. Relevant to dataset/semantic lineage but duplicative of existing repository-owned source/measurement identity contracts for this decision gap. No DataHub schema, ingestion model, SDK code, workflow, prompt, or implementation was copied.

Previously reviewed Amazon Ads API/MCP, Agent Skills, runtime and evaluation projects were de-duplicated rather than counted again.

### Adoption decision

The only behavior adopted this round is repository-authored and narrower: if baseline and post-change modeled/direct inclusion, allocation coverage, `Unallocated` state or allocation grain differ materially, treat that **composition drift** as a measurement confounder. Do not promote affected conversion/ROAS movement directly to causal `Worked` / `Failed`; keep the result `Inconclusive`, directional, Hold or Manual Review until reconciled or replaced with a stronger comparable counterfactual. This remains read-only/Suggest/Shadow and adds no executor/write/retry/reconciliation capability.


## Measurement-composition comparator review — 2026-09-22

### Amazon Ads official evidence

Amazon Ads continues to document that Sponsored Display modeled conversions are reported in the same conversion columns as directly attributed conversions and that lower-grain reports can emit `Unallocated` / API `-20` rows when attribution cannot be meaningfully allocated at that reporting breakdown. Amazon DSP similarly combines directly measured and modeled off-Amazon conversions in campaign reporting.

The repository therefore treats lower-grain composition/allocation identity as explicit evidence. The new comparator is repository-authored and only classifies whether two already-captured composition envelopes are comparable enough for causal review. No Amazon report schema, payload, API client, prose, or workflow was copied.

Sources:
- https://advertising.amazon.com/resources/whats-new/modeled-conversions-for-sponsored-display-campaigns
- https://advertising.amazon.com/resources/whats-new/modeled-attribution-for-off-amazon-conversions-for-us-advertiser
- https://advertising.amazon.com/help/G3BB9TWP5KC375TJ

### Incremental data-quality project review

Stars/activity are point-in-time discovery context only.

- `fivetran/great_expectations` — ~11.8k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active through 2026-09-18 with a substantial CI/test workflow. Useful corroboration for explicit, deterministic data expectations and validation results. Rejected as a dependency because this repository needs a five-field in-memory comparator, not a general data-quality framework. No expectation implementation, validator, schema, workflow, or documentation text was copied.
- `sodadata/soda-core` — ~2.4k stars observed on 2026-09-22; non-fork/non-archived; active through 2026-09-21; licensed under Elastic License 2.0 rather than a permissive OSS license. Useful only as ecosystem evidence that data contracts should be machine-checkable. Rejected for implementation reuse and dependency introduction on both scope and licensing grounds. No code, contract syntax, workflow, prompt, or protected implementation was copied.

Previously reviewed OpenLineage, OpenMetadata, DataHub, Agent Skills/eval projects and Amazon Ads API/MCP projects were de-duplicated rather than counted again.

### Adoption decision

Add one dependency-free, read-only comparator for `measurement_composition`. It fails closed to `Unknown` when any required composition field is missing, null, invalid or explicitly unknown/unavailable; returns `Not Comparable` when modeled-conversion inclusion semantics or allocation grain change; returns `Directional` when split observability, allocation coverage or `Unallocated` state changes; and returns `Comparable` only when every bounded field is explicit and equal. Missing evidence is never synthesized as zero, false, direct-only, complete allocation or unchanged state. The helper adds no Amazon Ads write/executor/retry/reconciliation capability.


## Measurement-comparison audit-lineage review — 2026-09-22

### Amazon Ads official evidence

Amazon Ads' current conversion-attribution guidance, updated August 5, 2026, reinforces that attribution semantics are first-class measurement context rather than a generic sales label. Amazon Ads also continues to document Sponsored Display modeled conversions in the same conversion columns as directly attributed conversions, with lower-grain `Unallocated` / API `-20` rows when meaningful allocation is unavailable. Unified Reporting now standardizes attribution methodology and is replacing legacy report centers, which further increases the need to retain exact decision-time measurement identities when historical outcomes are audited.

Adoption boundary: these official sources justify preserving the evidence identity and comparison reason that gated a historical outcome. No Amazon schema, payload, report model, API client, prose, or workflow was copied.

Sources:
- https://advertising.amazon.com/help/G3BB9TWP5KC375TJ
- https://advertising.amazon.com/resources/whats-new/modeled-conversions-for-sponsored-display-campaigns
- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

### Incremental agent-observability / provenance project review

Stars/activity are point-in-time discovery context only.

- `openlit/openlit` — ~2.8k stars observed on 2026-09-22; Apache-2.0; non-fork/non-archived; active through 2026-09-21 with broad multi-language CI. Useful corroboration that agent/tool evaluations become more reproducible when trace/evaluation metadata is retained with the run. Rejected as a dependency because this repository needs a tiny append-first decision-audit contract, not an observability backend or OpenTelemetry stack. No OpenLIT trace schema, instrumentation, evaluator, workflow, prompt, or implementation was copied.
- `Arize-ai/phoenix` — ~11.6k stars observed on 2026-09-22; non-fork/non-archived; active on 2026-09-22 with substantial unit/integration/CI evidence; current repository license is Elastic License 2.0. Relevant ecosystem evidence for attaching evaluation context to traces, but rejected for implementation reuse and dependency introduction on both licensing and scope grounds. No Phoenix schema, trace model, evaluator, code, workflow, or protected implementation was copied.
- `langfuse/langfuse` — ~34.9k stars observed on 2026-09-22; active with extensive CI. This project had already been reviewed in prior repository research, so it was de-duplicated rather than counted as new evidence. Its repository uses MIT Expat for most non-enterprise content with separate enterprise-directory licensing; no code, schema, workflow, evaluator or trace format was reused.

### Adoption decision

Keep the authoritative optimization event ledger self-contained and dependency-free. When `compare_measurement_composition.py` materially affects an `evaluated` or `corrected` outcome, preserve the repository-owned comparator identity, classification, changed fields, deterministic reasons, and baseline/post evidence snapshot IDs in `measurement_comparison`. This lets a later reviewer distinguish allocation drift from modeled-inclusion/grain incompatibility without re-inventing history. Null source identities remain unknown. No observability service, external trace backend, Amazon Ads write path, retry, idempotency, or reconciliation capability is added.


## Action-example schema-parity review — 2026-09-28

### Normative / primary evidence

- JSON Schema 2020-12 documentation — schema validation constrains instance structure and data types; repository examples that are presented as copyable canonical payloads should therefore stay valid against the repository's declared schema. Source: https://json-schema.org/learn/getting-started-step-by-step
- Amazon Ads Advanced Tools Center reporting documentation — retained as primary Amazon reporting/API context; no Amazon payload, schema, prose, or implementation is copied by this maintenance change. Source: https://advertising.amazon.com/API/docs/en-us/mcp/reporting

Adoption boundary: this round fixes a repository-owned example/contract mismatch only. It does not change Amazon Ads metric semantics, add a connector, or grant write authority.

### Incremental high-star / active project review

Stars are discovery context only and can change.

- `NVIDIA/SkillEvaluator` — 518 stars observed from GitHub on 2026-09-28; Apache-2.0; active through 2026-09-26; substantial tests/CI and explicit deterministic validation plus live skill evaluation. Adopted only the abstract principle that deterministic artifact contracts should gate examples and generated artifacts before live evaluation. Rejected as a dependency because the immediate gap is a tiny repository-local schema/example mismatch already covered by dependency-free unittest. No NVIDIA code, prompts, schemas, workflows, rubrics, or datasets copied.
- `benchflow-ai/skillsbench` — ~1.8k stars observed from GitHub on 2026-09-28; Apache-2.0; active benchmark with verifier/oracle task structure and reproducible task validation. Useful corroboration for executable artifact checks. Rejected as a dependency because introducing a benchmark runner would not improve this scalar schema-parity regression. No task, verifier, Skill, dataset, schema, or workflow copied.
- `google/agents-cli` — ~6.0k stars observed from GitHub on 2026-09-28; Apache-2.0; active through 2026-09-22; supports multiple coding-agent runtimes and carries schemas/skills/runtime packaging. Useful portability evidence, but its Google Cloud deployment/runtime surface is outside this repository's Amazon Ads decision-library boundary. No code, Skill, schema, runtime manifest, prompt, or workflow copied.
- `evalstate/fast-agent` — high-star project discovered by the >500-star query; Apache-2.0 verified from the repository; active through 2026-09-27 with CI-backed MCP/agent/runtime work. Relevant to MCP/runtime interoperability, but not a better solution to the current example/schema mismatch. No code, shell contract, MCP implementation, prompt, schema, or workflow copied.

Previously reviewed SkillSpector, Skill-Up, Microsoft Skills, OpenLineage/OpenMetadata/DataHub, Amazon Ads wrappers/MCP projects and evaluation frameworks were de-duplicated rather than counted again.

### Adoption decision

Keep the existing `schemas/optimization-action.json` numeric `confidence` contract and make the copyable action example conform to it. Add a deterministic repository test that parses action JSON blocks in `examples/README.md` and rejects scalar contract drift. This is narrower and safer than weakening the canonical schema or adding a third-party validation/evaluation dependency.

## Sponsored Products video bid-control promotion — 2026-09-29

### Amazon official evidence

- Amazon Ads Help, **Adjust Sponsored Products bids**, updated 2026-09-23: documents a distinct Sponsored Products video bid adjustment and states that applicable video, audience, and placement adjustments combine when determining the final bid. Source: https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5
- Amazon Ads, **A complete guide to setting up Sponsored Products video**: documents a video-specific bid boost in Campaign Manager and states that the boost applies on top of other placement adjustments. Source: https://advertising.amazon.com/library/guides/sponsored-products-video

Adoption boundary: only the independently rewritten decision-safety implication is adopted: `video_bid_adjustment` is a material configured control for Sponsored Products causal review when applicable. Amazon prose, examples, screenshots, API payloads, formulas, and implementation remain Amazon copyrighted material and were not copied. Marketplace/category eligibility remains capability evidence; unsupported or missing connector evidence is not treated as zero.

### Incremental GitHub scan

This round re-ran multiple Amazon Advertising API/PPC/MCP and Agent Skills/evaluation/security searches. High-adoption projects such as `denisneuf/python-amazon-ad-api`, `KuudoAI/amazon_ads_mcp`, `NVIDIA/SkillEvaluator`, `benchflow-ai/skillsbench`, `google/agents-cli`, and `evalstate/fast-agent` were re-discovered but are already reviewed in this repository. They were de-duplicated rather than counted as new evidence. No third-party code, prompt, schema, workflow, request template, runtime, or connector dependency was imported because Amazon's current official control semantics are the direct authority for this gap.



## Long-Term Sales estimate vs realized maturity — 2026-10-05

Amazon official measurement documentation was reviewed for the evidence boundary between modeled/projected long-horizon value and realized outcomes.

- **Long-term sales launch documentation** defines LTS/LTS ROAS as ad-attributed measures that estimate incremental sales value expected over the next 12 months from new-to-brand engagement, based on historical 12-month return patterns.
- **Measurement in AI-driven advertising**, published 2026-09-30, states that Long-Term Sales estimates 12-month campaign sales impact and that Accumulated Sales validates those estimates over time against actual sales.
- Current **campaign reporting** documentation likewise describes long-term sales as immediate sales plus projected value from customer engagement over the next 12 months.

Adoption boundary: Amazon pages are vendor documentation, not open-source implementation material. No Amazon prose, API payload, schema, prompt, workflow, or proprietary implementation is copied. The repository independently adopts only the decision-safety invariant that a modeled/projected estimate is a different evidence class from a realized observation; unavailable or immature realized evidence is not zero, and a long-horizon estimate alone cannot prove a post-change action worked.

Public references reviewed:

- https://advertising.amazon.com/resources/whats-new/long-term-sales
- https://advertising.amazon.com/en-gb/library/expert-advice/ai-measurement-advertising
- https://advertising.amazon.com/measurement-analytics/campaign-reporting


### AgentEvalHQ/AgentEval

MIT-licensed agent-evaluation toolkit reviewed during the 2026-10-05 incremental scan. Approximately 154 stars were observed, the repository was actively updated on 2026-10-05, and it exposes substantial CI/security/calibration workflow evidence. Relevant generic ideas include deterministic tool-chain assertions, explicit side-effect/confirmation gates, stochastic reliability measurement, and separating execution traces from evaluation claims.

No .NET runtime, evaluator, red-team corpus, assertion API, scoring formula, schema, prompt, workflow, or implementation was copied. The project is explicitly preview/experimental and is centered on Microsoft Agent Framework/.NET; importing it would expand this repository's runtime surface without improving the specific Amazon Ads Long-Term Sales maturity boundary. Existing dependency-free eval fixtures, contract tests, external execution boundary, and paired effectiveness contracts already cover the directly applicable safety principles.

Repository: https://github.com/AgentEvalHQ/AgentEval


## Platform-managed control transition provenance — 2026-10-06

Amazon official product/API documentation establishes that a current control state and the actor that produced its latest transition are separate evidence questions.

- **Automatic deal selection** — Amazon documents that the feature can continuously add high-performing deals and remove low-performing deals without manual intervention. Through the public Deal Management API (beta), system-managed inventory groups use `curationSourceType=AMAZON_CURATED_AGENT`, explicitly distinguishing a platform-managed actor/origin from advertiser-curated inventory groups. Advertisers can retrieve the managed group and associated deals programmatically.
- **Review Requests** — Amazon's 2026-09-29 launch announcement states that product eligibility is checked both when a campaign is created and while it runs, and Review Requests pause automatically once the product reaches the 1,000 ratings/reviews threshold. The product is announced for U.S. open beta in late October 2026 through Amazon Ads Agent and the Unified Campaign Management API.
- **Sponsored Ads auto-optimization** — Amazon's current roadmap states that, when enabled, the platform can add keywords/product targets and pause underperforming keywords while advertisers can inspect, edit, or reverse those actions. U.S. availability is announced for January 2027. This is roadmap evidence for platform-managed mutation, not proof of a stable public API provenance field today.

Adoption boundary: these Amazon pages are factual vendor documentation. No Amazon API payload, enum schema, workflow, prompt, implementation, or proprietary documentation text is copied into repository code. The repository independently adopts only the generic decision-safety rule that observed current state does not prove transition authorship, and that missing platform actor/change-history evidence must remain unknown rather than being attributed to the advertiser or an external Executor.

Public references reviewed:

- https://advertising.amazon.com/en-gb/resources/whats-new/automatic-deal-selection
- https://advertising.amazon.com/resources/whats-new/get-product-reviews-faster-with-review-requests
- https://advertising.amazon.com/en-ca/library/expert-advice/sponsored-ads-small-business-tools

GitHub discovery was re-run with multiple Amazon Ads/MCP, agent provenance/event-sourcing, evaluation/trace-safety and lineage queries. Previously reviewed projects including `denisneuf/python-amazon-ad-api`, `KuudoAI/amazon_ads_mcp`, `MarketplaceAdPros/amazon-ads-mcp-server`, `OpenLineage/OpenLineage`, Langfuse/OpenLIT/Phoenix and AgentEval were de-duplicated rather than counted as new evidence. A newly surfaced `Birkity/agentic-governance-ledger` repository was reviewed only as abstract event-sourcing/audit context: 0 stars, no clear license surfaced, and no GitHub Actions workflow surfaced, so no code, event schema, MCP surface, prompt, workflow, or implementation was reused.


## Actor-provenance capability binding — 2026-10-09

Official Amazon Ads source semantics and public engineering evidence were reviewed to separate state readback from source-supported transition actor history.

- Amazon automatic deal selection (April 15, 2026) explicitly documents `AMAZON_CURATED_AGENT` as an inventory-group management origin for the specific DSP Streaming TV feature. It does **not** promise universal actor history on all ad-product APIs.
- Amazon's official Ads Advanced Tools GitHub repository, `amzn/ads-advanced-tools-docs`, is MIT-0 licensed and includes real code samples/Postman assets plus maintained discussion/issue surfaces. An Amazon-side maintainer response in discussion #364 explains that `/history` queries need appropriate parent scope and correct `pageOffset`; an empty result after a mis-scoped query is not evidence of no changes.
- An unanswered user-submitted discussion #491 reports HTTP 200 / zero events while the console showed campaign changes. It is a diagnostic report, not proof of a universal API defect. Do not turn community anecdotes into normative Amazon behavior; require connector-level runtime verification.
- The published `/history` description for older Sponsored Ads change history notes limited ad-product support and no change-author identity. Treat this as surface/version-scoped historical evidence only; verify current behavior for the exact connector, marketplace, ad product, and endpoint.

Source URLs:
- https://advertising.amazon.com/en-gb/resources/whats-new/automatic-deal-selection
- https://github.com/amzn/ads-advanced-tools-docs
- https://github.com/amzn/ads-advanced-tools-docs/discussions/364
- https://github.com/amzn/ads-advanced-tools-docs/discussions/491

Engineering adoption: a repository-owned, optional list of required provenance dimensions on the existing `entity-state-readback` capability is checked before authorship-dependent causal claims. `Supported` state readback and generic history availability alone are insufficient. No Amazon proprietary API schema, endpoint payload, Postman collection, prompt, workflow, or protected implementation was copied. Existing third-party MCP libraries and high-star evaluation/lineage projects were re-discovered but already reviewed, or provide only transport/evaluation infrastructure instead of actor-provenance semantics; they were not duplicated or imported.


## Marketing Stream v2 record/version reconciliation — 2026-10-09

**Canonical official facts.** The [Amazon Marketing Stream v2 overview](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) states that v2 delivers S3 Parquet files and SQS notifications, each record contains a **total for its time window** rather than a delta, and consumers select the **highest `streamBatch.version` per record** before reducing to reporting grain. The [official v1→v2 migration guide](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/migrate-from-v1) says `ads-performance-v1` unifies four v1 ad-product performance datasets and advises parallel reconciliation before retiring v1. It lists the v1 shutdown date as 2027-06-30; that date is an external capability watch item, not a hard-coded decision threshold.

**Real gap closed.** Our generic read-only metric aggregation gate previously allowed additive/disjoint sums from a Stream v2 input even if the same logical record had multiple total-valued revisions. The new v2-specific optional input to that existing gate requires source-supported full-record-identity coverage and highest-version-per-record reconciliation before allowing a direct sum. It does **not** ingest files, design keys, own event storage, call an API, or override delivery/freshness/attribution/metric completeness gates.

**GitHub source de-duplication and rights.**

- `amzn/amazon-marketing-stream-examples`: **20 stars**, **MIT-0**, non-fork/non-archived, last pushed **2026-04-13** (observed 2026-10-09). Real Amazon-owned CLI/CDK/test infrastructure but its published subscription examples are **v1 traffic/conversion/SQS/Firehose** oriented; do **not** treat it as authoritative for v2 totals/version reconciliation. Already reviewed for v1 coverage; no code, CDK, config or workflow copied.
- `amzn/ads-advanced-tools-docs`: **180 stars**, **MIT-0**, non-fork/non-archived, pushed **2026-09-30**. Amazon-owned official supplementary samples and documents, previously reviewed. Useful as source-discovery context, but current v2 guide is the stronger normative source for exact delivery semantics; no Postman collection, template, migration skill or schema imported.
- `OpenLineage/OpenLineage`: **2,693 stars**, **Apache-2.0**, active push **2026-10-08**, non-fork/non-archived; prior repository review already established that data lineage/provenance should remain explicit. Adding an OpenLineage client or event schema would be disproportionate to this existing aggregation-gate defect. Rejected as a dependency; no code/schema copied.
- `KuudoAI/amazon_ads_mcp`: **72 stars**, **MIT**, last push **2026-09-06**, non-fork/non-archived; previously reviewed connector engineering. Does not supersede Amazon's Stream v2 version semantics; no code/tool schema/ingestion workflow reused.

Stars and activity are point-in-time discovery context, **not** proof of technical fitness. Forks/mirrors and already-reviewed projects were not counted as novel sources. Amazon official documentation remains copyrighted vendor material: only short factual semantics were independently expressed as repository-owned MIT decision rules, tests and synthetic data. No protected prompt, schema, source code, migration procedure or provider workflow was copied.


## Sponsored Brands v4 coverage and Fire TV display measurement — 2026-10-19

### Official, version-scoped Sponsored Brands reporting evidence

Amazon Ads' [Sponsored Brands v4 migration guide](https://advertising.amazon.com/API/docs/en-us/sponsored-brands/v4-migration-guide) documents that legacy v3 campaign reads can omit additional ad groups/ads in multi-ad-group campaigns. The guide and [legacy Sponsored Brands Reporting API v2 reference](https://advertising.amazon.com/API/docs/en-us/reference/sponsored-brands/2/reports) describe the `creativeType: all` inclusion condition for the applicable legacy report requests. These facts are scoped to the documented API generations; they do not establish the same filter for Reporting API v3 or Unified Reporting. A successful partial response cannot prove population completeness or metric zero.

Adopted: independent, source/version/request-aware completeness reasoning in `docs/research/sponsored-brands-v4-report-coverage-2026-10-19.md`. Rejected: universal connector schema changes, automatic API request rewrites, invented coverage, and a sixteenth Skill. Vendor documentation is copyrighted; no Amazon code, prose, API schema, examples, prompt, template, or workflow was copied.

### Official, date-scoped Fire TV display measurement evidence

Amazon Ads' [support-center notice](https://advertising.amazon.com/help/ref=ams_head_help), checked on 2026-10-19, announces a Fire TV display-supply measurement-methodology change effective 2026-10-08. It estimates an aggregate approximately 15% impression and 11% click impact, varying by advertiser/campaign/marketplace/placement. These figures are not individual-campaign correction factors and do not establish whether historical data was restated.

Adopted: the independently expressed cross-cutover comparability warning in `docs/research/fire-tv-measurement-methodology-2026-10-19.md`. Rejected: multiplying observed data by platform averages, assuming retroactive restatement, extending the change to unrelated ad products, and unverified runtime behavior changes. No copyrighted vendor text, code, schema, prompt, workflow, or template was copied. Both entries are research-only and preserve the existing read-only/suggest/shadow and external-authorized-Executor boundaries.


## 2026-10-22 official migration-tool limitations (source review)

Official Amazon Ads Help: *Migrate your scheduled reports to unified reporting*,
updated **2026-10-12**:
https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A

**Incremental evidence:** only active saved/scheduled report configurations
from the preceding 24 months are eligible for the migration tool; some report
types are not supported; fields can be dropped where legacy and new metric
reporting grains differ (notably lower-grain `topOfSearchImpressionShare`).
This is a **migration-tool/report-grain** constraint, not proof of universal
API unavailability or a zero-valued metric.

**Adopted:** independently written source and measurement-lineage clarification
in `docs/research/unified-reporting-migration.md`. **Rejected:** adding a
sixteenth Skill, hard-coded vendor capability list, direct report migration,
or external connector dependency; no nonduplicative runtime behavior gap was
established. The official page retains its copyright. No provider prose,
code, schema, prompt, report template, or workflow was copied.

## 2026-10-22 Full-Funnel and Global SP official evidence review

Sources: Amazon Ads Full-Funnel launch (2026-09-29), https://advertising.amazon.com/resources/whats-new/full-funnel-campaigns-from-discovery-to-sales ; Amazon Ads Agent launch (2026-09-29), https://advertising.amazon.com/en-us/library/news/amazon-ads-agent/ ; Global Sponsored Products API guide (reviewed 2026-10-22; publication date unverified), https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns .

Adopted: independently expressed shared-budget/managed-delivery and modeled Long-Term Sales boundaries, plus Global SP's marketplace-specific budget, bid, currency, state, identity, pagination, auto-expansion and partial-result evidence. Recorded as non-normative research in `docs/research/amazon-ads-platform-watch-2026-09.md`; existing decision contracts remain authoritative.

Rejected: vendor uplift as a causal or universal bid/budget rule, per-account/API eligibility inferred from UI availability, global campaign state as proof of every marketplace's delivery, partial write as full success, direct cross-currency arithmetic, additional Skill/runtime or live mutation.

Copyright: only factual platform behavior was independently paraphrased; no Amazon prose, code, schema, API example, report template, prompt or workflow copied. Reddit anecdotes and third-party repository implementations were not reused.

## 2026-10-24 Global SP 207 receipt/readback implementation review

**Official source:** Amazon Ads, [Global campaigns for Sponsored Products](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), reviewed 2026-10-24 (publication date not verified). The guide documents HTTP 207 per-index `success`/`error`/`partialSuccess` for create/update/delete, paginated query, and per-marketplace `marketplaceConfigurations` state overrides. `status.deliveryStatus` is delivery status, not configured effective state. Adopted: a new, **single-item only**, independently authored read-only receipt/readback gate and synthetic deterministic tests, described in `references/global-sp-readback-evidence.md`. Rejected: assuming 207 success proves application, conflating global and per-marketplace state, and introducing write/retry/idempotency logic. Amazon's copyrighted prose, API schema, example payloads and workflows were not copied.

**Open-source candidate:** [coaxon/amazon-mcp](https://github.com/coaxon/amazon-mcp), GitHub metadata checked 2026-10-24: **1 star**, **MIT**, non-fork, non-archived, last pushed 2026-07-01, public `tests/` present, no `.github/workflows` found, zero open PRs in the checked page. Rejected for direct adoption: a seller/Ads MCP adapter does not independently prove complete Global SP marketplace readback, and this library intentionally does not bundle an external executor. Only the abstract separation of connector read paths and decision safety was considered; no code, tool names, prompt, schema or workflow reused.

Previously reviewed `promptfoo/promptfoo` (MIT, ~26,346 stars, active CI), `amzn/amazon-marketing-stream-examples` (MIT-0, 20 stars, public tests), `agentskills/agentskills` (Apache-2.0, ~26,516 stars), and `modelcontextprotocol/servers` (repository metadata NOASSERTION, ~91,520 stars) did not justify a new dependency or license-uncertain content reuse for this narrow gap. Stars and activity are discovery signals only. No third-party implementation, prompt, schema, template or workflow was copied.

## 2026-10-24 Global SP marketplace monetary-budget readback safety review

**Official source:** Amazon Ads, [Global campaigns for Sponsored Products](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24 (publication date not verified). The official guide describes marketplace-specific daily monetary budgets in local currencies, distinct marketplace bid settings, Global Account identity, and per-request-index HTTP 207 responses. Adopted: **only** independently expressed marketplace currency/amount/recurrence and separate readback-completeness requirements for a narrowly scoped optional *daily monetary budget* comparison in `scripts/evaluate_global_sp_readback.py`. Explicitly rejected: converting currencies, assuming successful HTTP 207 implies application, inferring missing budget as zero, extending the gate to unsupported budget types/periods or bid operations, and introducing Ads write/retry logic. No Amazon source code, API schema, example payload, workflow, template, or prose was copied.

**Open-source checks** (GitHub repository metadata, 2026-10-24; stars are mutable discovery signals):
- [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp): **74 stars**, MIT, non-fork, non-archived, last pushed 2026-10-14; public CI and integration workflows, open PRs. Already reviewed as an external Ads MCP. **Rejected as dependency**: its broad read/write API surface does not establish exact source-observed per-marketplace budget readback for this repository's independent decision gate; no code, tool schema, prompt or workflow reused.
- [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo): **26,348 stars**, MIT, non-fork, recent push 2026-10-23, public CI and open PRs. Previously reviewed. **Rejected as dependency**: deterministic unit/Skill/eval validators already cover this narrowly specified contract; no benefit shown from an LLM eval runner for this behavior.
- [agentskills/agentskills](https://github.com/agentskills/agentskills): **26,518 stars**, Apache-2.0, non-fork, last push 2026-08-09, no CI workflow found in checked root workflow path, open PRs. Previously reviewed. **No new dependency**; maintain existing 15 portable Skills and their validator. No upstream specification, schema, template, or prompts copied.

Public practitioner/Reddit PPC anecdotes are not evidence for fixed FX rates, cross-market bid multipliers, causal lift, or platform API semantics. No anecdotal thresholds adopted. The connector/adapter remains responsible for trustworthy source normalization and complete marketplace currency identity; this repository only classifies supplied evidence.


## 2026-10-24 Global SP budget-row lineage contradiction review

**Primary source:** [Amazon Ads Global campaigns for Sponsored Products](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. The official guide distinguishes Global Account identity, marketplace-local budget currencies, multi-status HTTP 207 receipts and later paginated query reads. It does **not** mandate the optional normalized row-level fields introduced here. The repository independently adopts a conservative invariant: if an adapter supplies per-row source/time/account/campaign metadata, explicit contradictions with its trusted envelope are `Unknown` and cannot be ignored to obtain budget `Confirmed`. Existing single-envelope-only adapters remain compatible.

**Open-source candidate recheck** (GitHub metadata, 2026-10-24; stars are time-varying): [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, last push 2026-10-14; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, last push 2026-10-21; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,351 stars, MIT, non-fork, last push 2026-10-23; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,522 stars, Apache-2.0, non-fork, last push 2026-08-09. All previously reviewed. Rejected new dependencies and reimplementation of external lineage schemas/eval harnesses: no evidence that these add value to the focused existing Python contract. This metadata review is not an independent test/CI audit of all candidate code or PRs.

**Copyright:** no vendor/third-party source code, schema, prompt, workflow, example payload, or template reused; only platform facts and generic provenance principles independently expressed. Public practitioner/Reddit anecdotes do not establish Global SP API semantics, FX conversions, causal lift, or action thresholds. No live Ads write or retry logic added.


## 2026-10-24 Global SP configured-state row lineage review

**Official factual source:** Amazon Ads, [Global campaigns for Sponsored Products](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24; publication date unverified. The guide distinguishes Global Account, per-marketplace configured state, HTTP 207 multi-status updates and later paginated query evidence. It does **not** mandate the optional normalized row-level lineage fields introduced here. **Adopted:** independently specified fail-closed validation of explicit state-row source/time/account/campaign identity against the trusted readback envelope, supported by synthetic RED→GREEN tests. **Rejected:** inferring row lineage from 207 receipts, treating absent metadata as zero, conflating delivery with configured state, and adding live Ads writes/retries/batch reconciliation/FX.

**Previously reviewed open-source candidates rechecked 2026-10-24** (GitHub metadata; stars mutable): [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, last push 2026-10-14, public CI/integration workflows; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, last push 2026-10-21, public CI; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,352 stars, MIT, non-fork, last push 2026-10-23, public CI; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,525 stars, Apache-2.0, non-fork, last push 2026-08-09, no workflow directory found at the checked path. **Rejected as new dependencies:** no demonstrated gain over the narrow read-only deterministic contract. Stars and workflow presence do not establish complete test/CI quality or licensing of every vendored path. No external code, prompts, schemas, templates or workflows copied. Public expert/Reddit PPC anecdotes are not platform API specifications, fixed bid thresholds, or causal proof.


## 2026-10-24 Global SP unsupported-intent false-confirmation guard

**Official platform source:** [Amazon Ads Global Sponsored Products campaigns API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. Its examples distinguish campaign configured state/budgets from marketplace-local **ad-group** bid settings and target resources. Independent repository invariant: a campaign-only 207/state/budget readback cannot confirm an ad-group/target bid, placement, or unrecognized `expected_*` change. Unsupported expected dimensions return `Unknown`; explicit partial/error receipts remain `Partial`. No external API schema, payload, code, prompt or workflow copied.

**Open-source metadata recheck (2026-10-24, stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,352 stars, MIT, non-fork, pushed 2026-10-23; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,527 stars, Apache-2.0, non-fork, pushed 2026-08-09; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,525 stars, repository license metadata NOASSERTION, non-fork, pushed 2026-10-22. All are previously reviewed; no new dependency: their interfaces/LLM eval/lineage models do not prove the missing bid readback. No third-party code, schema, prompt, workflow or template reused; NOASSERTION is not permission to copy. Repository metadata/workflow presence is not a full independent CI/issue audit. Practitioner and Reddit PPC anecdotes were not adopted as platform facts or causal rules.

## 2026-10-24 Global SP ad-group native-currency default-bid readback

**Official API evidence:** [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. Ad-group update/query resources are separate from campaign and target resources; `bid.marketplaceSettings` carries marketplace-local `currencyCode` and `defaultBid`; writes use indexed HTTP 207 and query uses paginated HTTP 200. The new independent, single-item read-only gate requires complete query evidence and exact global-account/campaign/ad-group identity. Normalized `request_id` receipt binding is a conservative repository/Executor assertion, **not** a claim about Amazon's native response fields.

**Existing candidate recheck (2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, last push 2026-10-14, public CI and tests, open PRs; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,352 stars, MIT, non-fork, pushed 2026-10-23, public workflows and open PRs; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, public workflows and open PRs; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,528 stars, Apache-2.0, non-fork, pushed 2026-08-09, no workflow/tests directory at checked paths; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,525 stars, NOASSERTION repository metadata, non-fork, pushed 2026-10-22. No demonstrated need to import any dependency for deterministic native-currency bid readback. Stars, test paths, workflow presence and PR activity are not proof of full CI quality or path-level license coverage.

**Rejected:** generic agent eval/lineage/MCP frameworks add dependencies and cannot independently prove the adapter's ad-group readback completeness; no import. NOASSERTION is not a license grant. No source code, API examples, prompts, schemas, workflow text, or templates copied. Amazon official bidding advice and practitioner/Reddit PPC reports are not used as fixed bid thresholds or causal evidence.

## 2026-10-24 Global SP positive single-marketplace target bid readback

**Official platform source:** [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24 (page publication date not independently established). The guide distinguishes `targets` from `adGroups` and `campaigns`, gives targets one marketplace, shows target-specific native `bid.marketplaceSettings` and indexed 207 receipts, and documents paginated query. The new gate adopts only these facts plus independently designed conservative identity/source/time/completeness requirements. External `request_id` binding and normalized `target_type` are adapter contracts, **not** asserted native API fields. [Amazon Ads dynamic bidding guide](https://advertising.amazon.com/library/guides/dynamic-bidding-sponsored-products) confirms that a configured bid is not a realized auction bid; its tactical percentages are not imported as fixed rules.

**Candidate recheck (GitHub metadata 2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14, 4 public workflows and tests; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,354 stars, MIT, non-fork, pushed 2026-10-24, 19 public workflows; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, 8 public workflows; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,529 stars, Apache-2.0, non-fork, pushed 2026-08-09, no workflows/tests found at checked paths; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,526 stars, repository SPDX NOASSERTION, non-fork, pushed 2026-10-22. Existing research already covers these; workflow presence, stars and issue counts do not independently validate code/CI quality or file-level licensing. **Decision:** no dependency added: none establishes trusted target query evidence for this narrow gate. NOASSERTION is not a copying grant.

**Copyright and practitioner boundary:** no external code, prompts, API example payloads, schemas, workflows, or templates copied. Public practitioner/Reddit PPC reports are useful for experiment hypotheses, not evidence of native target field semantics, stable bid multipliers, or causal outcomes. No live Ads write/retry/executor capability added.

## 2026-10-24 Global SP multi-target batch index/readback verification

**Official factual basis:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. Global SP target update responds HTTP 207 with per-request `index` across `success`, `error`, `partialSuccess`; independent target queries are paginated. **Adopted:** an independently designed conservative *normalized adapter* contract mapping the exact ordered target requests to indexed receipt entries and post-update target-specific readbacks. This is not a claim that Amazon provides the normalized `request_id` or readback completeness fields. No batch executor/retry/idempotency/write code added.

**External candidate review (2026-10-24, GitHub repository metadata; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,355 stars, MIT, non-fork, pushed 2026-10-24; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,530 stars, Apache-2.0, non-fork, pushed 2026-08-09; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,527 stars, repository metadata NOASSERTION, non-fork, pushed 2026-10-22. These were previously reviewed in SOURCES/research. Additional candidate [denisneuf/python-amazon-ad-api](https://github.com/denisneuf/python-amazon-ad-api) 203 stars, MIT, non-fork, pushed 2026-10-23, publicly maintained wrapper; [vanling1111/amazon-ads-api-python-sdk](https://github.com/vanling1111/amazon-ads-api-python-sdk) 3 stars, MIT, non-fork, pushed 2026-05-30, tests described but API-coverage claims not independently validated; [wangjoshuah/Amazon-Ads-Sponsored-Products-API-Python-Client](https://github.com/wangjoshuah/Amazon-Ads-Sponsored-Products-API-Python-Client) 15 stars, MIT, non-fork, last pushed 2022-01-12, older v2 client. Workflow presence, open-issue counts, stars, and license metadata alone do not prove current tests, successful CI, compatibility with Global SP, or permission to reuse every path.

**Decision:** reject dependencies and code import. None supplies verifiable independent target-query coverage or batch correlation; older v2 client and broad execution SDKs are particularly mismatched to the repository's read-only contract. NOASSERTION is not a copying grant. No third-party code, API example, prompt, schema, workflow, or template copied. Amazon Ads budget/bidding guides and Reddit PPC anecdotes are not evidence for fixed bid percentages or causal claims. [Amazon Ads DSP bid-adjustment testing](https://advertising.amazon.com/API/docs/en-us/guides/dsp/bid-adjustments/testing) recommends controlled tests over naive before/after inference for DSP; it is **not** treated as a Global SP API contract.

## 2026-10-24 Global SP multi-ad-group batch default-bid readback

**Platform facts:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24, distinguishes update/adGroups from campaign/target resources, indexed HTTP 207 success/error/partialSuccess, separate paginated query, and ad-group `bid.marketplaceSettings` with native `currencyCode`/`defaultBid`. **Adopted:** a conservative repository-owned *normalized external adapter* contract for one homogeneous ad-group batch: ordered request/index binding, unique ad-group identity, exact successful-item query correlation, and per-marketplace independent complete default-bid readback. Normalized `request_id`, evidence source, pagination and connector capability are external assertions, not Amazon native API guarantees. No Ads write/retry/idempotency code.

**Fresh external repository review (2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14; latest visible Actions run (2026-10-19) success. [denisneuf/python-amazon-ad-api](https://github.com/denisneuf/python-amazon-ad-api) 203 stars, MIT, non-fork, pushed 2026-10-23; latest visible Actions runs (2026-10-23) success. [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,357 stars, MIT, non-fork, pushed 2026-10-24; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21. Previously reviewed in this file/research. Repository metadata and selected Actions success do not independently prove file-level licensing, full code quality, or compatibility with Global SP indexed readback; issue/PR counts are not evidence of a bug-free implementation.

**Decision and copyright:** reject new SDK/MCP/eval/lineage dependencies for this focused deterministic gate: none independently proves trusted request-order correlation or native-currency marketplace query completeness, and additional dependencies would expand surface without validated benefit. No third-party code, prompts, schema, API sample payload, workflow or template copied. [Amazon Ads dynamic bidding guide](https://advertising.amazon.com/library/guides/dynamic-bidding-sponsored-products) supports treating configured default bids separately from effective auction bids; it does not prove causal impact or prescribe a universal multiplier. Public expert/Reddit PPC anecdotes remain experiment hypotheses, not official API contracts.


## 2026-10-24 Global SP mixed-resource plan readback evidence

**Official platform source:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), rechecked 2026-10-24. Campaign, ad-group and target updates are separate resources; write calls return indexed HTTP 207 outcomes and query readback is a separate paginated operation. **Adopted:** independently designed read-only composition of existing resource verifiers with a complete externally asserted plan manifest, unique resource/request identity, exact component coverage, and Unknown > Partial > Drifted > Confirmed precedence. The plan manifest, `plan_id`, component IDs and completeness/source fields are repository-defined normalized external assertions, **not native Amazon Ads fields**. An authorized Executor must authenticate and preserve the actual complete plan ledger; this classifier cannot verify external plan truth or causality.

**Previously reviewed GitHub candidates, metadata rechecked 2026-10-24 (stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, last push 2026-10-14; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,358 stars, MIT, non-fork, last push 2026-10-24; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, last push 2026-10-21; [denisneuf/python-amazon-ad-api](https://github.com/denisneuf/python-amazon-ad-api) 203 stars, MIT, non-fork, last push 2026-10-24; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,534 stars, Apache-2.0, non-fork, last push 2026-08-09. Repository metadata, workflow presence, issue counts and public tests do not independently prove latest CI quality or path-level licensing. **Decision:** no new dependency: none authenticates an external multi-call optimization plan or establishes missing readback lineage. Already reviewed in SOURCES/research; avoid duplicate development.

**Copyright and evidence boundary:** no external code, prompt, schema, workflow, template or Amazon example payload copied. Public PPC practitioner/Reddit anecdotes may inform experiment hypotheses but are not platform API specifications, stable bid thresholds, or causal proof. No Ads write/retry/idempotency/reconciliation capability added.


## 2026-10-24 — Global SP campaign 207 returned-resource identity contradiction guard (v1.38.1)

**Official platform evidence:** [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) describes HTTP 207 indexed `success`/`error`/`partialSuccess` update results, with returned campaign resource IDs in its examples, and separate paginated HTTP 200 queries. The repository's optional normalized receipt identity checks are a stricter **local safety rule**, not an Amazon-mandated normalization schema. A 207 receipt for a different campaign cannot prove the intended campaign update, even when a later unrelated query matches.

**RED→GREEN:** synthetic `tests/test_global_sp_campaign_receipt_identity.py` exposed 10 false confirmations in 816 tests (RED Actions 40067650845); independently authored minimal fix `e7ffb6c165dfc09c0c40afc7f19ac8a2f7140076` passed all 816 (GREEN Actions 40067675016). This is a PATCH bug fix, not a new Skill or Executor.

**Rechecked previously reviewed candidates (GitHub public metadata, 2026-10-24, stars change over time):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp): 74 stars, MIT, non-fork, pushed 2026-10-14; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage): 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo): 26,358 stars, MIT, non-fork, pushed 2026-10-24; [nospicyplease/amazon-ppc-advanced-skills](https://github.com/nospicyplease/amazon-ppc-advanced-skills): 14 stars, MIT, non-fork, pushed 2026-05-28. Public metadata/issue counts alone cannot certify full test/CI quality or per-path reuse rights. **Reject dependency adoption:** the defect is a narrow local receipt-identity comparison already covered by deterministic unit tests; importing a general MCP, lineage framework, eval framework or PPC prompt package adds cost without evidence of better safety. All four had prior SOURCES/research review; no repeated code ingestion.

**Copyright and execution boundary:** platform facts and abstract verification principles only; no copied third-party code, prompt, schema, workflow, template or Amazon example payload. No Ads API mutation, retry, idempotency or Executor reconciliation. Practitioner and Reddit claims are not treated as official protocol or causal proof.


## 2026-10-24 — Global SP raw marketplace ID crosswalk guard (v1.39.0)

**Official source:** [Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. The guide explicitly states that query `status.marketplaceSettings[]` may use raw marketplace IDs (for example, the UK identifier) rather than ISO country codes, while resource `marketplaces` and campaign configuration use country codes. This is a factual namespace distinction, **not** authorization to infer configured state from delivery status.

**Adopted:** independently authored, opt-in source-attributed one-to-one crosswalk for raw IDs explicitly retained in normalized state/budget rows. Any partial, missing, duplicate or contradictory mapping fails closed as `Unknown`. Existing trusted normalized country-code-only envelopes stay compatible. The adapter's `verified` mapping status is an external assertion, not cryptographic authentication or an Amazon-required field. RED test commit `61c268ff6cbda0ef2715041b9c3a0a74e0e2edde` exposed 15 false confirmations in 835 tests (Actions 40071280587); fix `903eb5eaa91862099ad0a879113e3169477644a8`.

**Fresh previously reviewed GitHub candidates (2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14; latest visible scheduled CI success 2026-10-19. [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,359 stars, MIT, non-fork, pushed 2026-10-24; latest public PR workflows mixed success/failure. [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; latest visible PR runs action_required. [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,538 stars, Apache-2.0, non-fork, pushed 2026-08-09; latest visible dynamic runs failure. [denisneuf/python-amazon-ad-api](https://github.com/denisneuf/python-amazon-ad-api) 203 stars, MIT, non-fork, pushed 2026-10-24; latest visible release workflow success. Repository-level license/CI metadata does not certify per-file rights, code quality, issue resolution or support for Global SP raw-ID normalization. All were already reviewed in SOURCES/research; no new dependency adopted because none independently proves this exact mapping.

**Copyright and practitioner boundary:** no external code, prompt, schema, workflow, template or API example copied. Public PPC discussions about placements/bids are unverified operator observations; no fixed multiplier, profitability rule or causal conclusion was imported. No Amazon Ads writes, retries, idempotency or Executor reconciliation.

## 2026-10-24 — Global SP native campaign configured-state source cross-check (v1.40.0)

**Official platform facts (checked 2026-10-24):** [Amazon Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) distinguishes top-level campaign `state`, per-marketplace `marketplaceConfigurations[].overrides.state`, and query `status.deliveryStatus`. The latter is delivery health, not configured state. Query responses have separate paginated `nextToken` semantics. **Adopted:** an independently authored, optional trusted-adapter native campaign snapshot cross-check: when `readback.raw_campaign` is supplied, recompute configured state and reject contradictions with normalized state, identity, product or marketplace scope. No assertion that Amazon requires the repository's `raw_campaign` field, or that an adapter's source is cryptographically verified.

**Deterministic evidence:** RED commit `f3ba784eac0c3ac075ac1d6f8d54666e334bb0d9`, Actions 40075256711 (862 tests, 20 false-confirmation failures). GREEN fix `f8dc5d518c1da9be3b5726e24d335a4b36ad85df`, Actions 40075280259 (862/862 unit tests plus both validators pass). No extra Skill or runtime dependency.

**Candidate review (GitHub public metadata, 2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp), 74 stars, MIT, non-fork, last pushed 2026-10-14, 5 open issues; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), 26,360 stars, MIT, non-fork, pushed 2026-10-24, 841 open issues; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage), 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, 412 open issues. These were previously assessed in SOURCES/research. New candidate [MarketplaceAdPros/amazon-ads-mcp-server](https://github.com/MarketplaceAdPros/amazon-ads-mcp-server), 29 stars, MIT, non-fork, pushed 2026-10-22, 1 open issue and 1 open PR. Its public package declares no automated test script, and its repository has no visible GitHub Actions runs or workflow directory; the service uses a third-party bearer token and paid subscription for some functions. Repository license metadata does not prove per-file provenance or independently validate Amazon Global SP field mappings.

**Decision:** reject all new dependencies and code import. None proves native-query configured-state derivation or trustworthy query completeness; a third-party service integration would add an external authentication/dependency boundary without solving this deterministic discrepancy. Public expert/Reddit PPC claims remain hypotheses, not API specifications or causal proof. No third-party code, prompt, schema, workflow, template, API sample, or proprietary material copied. No Amazon Ads writes, retries, idempotency or Executor reconciliation.


## 2026-10-24 — Global SP campaign query pagination-chain guard (v1.41.0)

**Official API fact:** [Amazon Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24: query calls return HTTP 200 with resource arrays and `nextToken` pagination; update calls return HTTP 207 with per-request `success`, `error`, `partialSuccess` indices. The repository-owned optional `pagination_trace` is NOT an Amazon-defined field. Its page-chain/source/filter/time consistency gate detects contradictory adapter evidence but cannot authenticate original HTTP responses or prove every matching resource was retrieved.

**Adopted:** narrow, read-only check of explicitly supplied query page-chain and source/identity evidence. RED test commit `94397f53903a720e7e0a8a0baf794fe96834528d`, Actions 40079424196 (889 tests, 23 failures). GREEN code commit `b0913d6926beab7a028e3a272e9d2d2bf41f52dc`, Actions 40079467166 (unit tests and both validators success). No new Skill or runtime dependency.

**Public candidate recheck (2026-10-24, mutable metadata):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp): 74 stars, MIT, non-fork, pushed 2026-10-14, last visible scheduled Actions success 2026-10-19; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo): 26,362 stars, MIT, non-fork, pushed 2026-10-24, latest visible PR Actions success; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage): 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, recent PR runs `action_required`; [coaxon/amazon-mcp](https://github.com/coaxon/amazon-mcp): 1 star, MIT, non-fork, pushed 2026-07-01, dry-run/core-pro split and older public dynamic CI; [MarketplaceAdPros/amazon-ads-mcp-server](https://github.com/MarketplaceAdPros/amazon-ads-mcp-server): 29 stars, MIT, non-fork, pushed 2026-10-22, third-party token/service dependency. Earlier candidates already reviewed in SOURCES/research; coaxon is a new low-activity candidate. Stars/license/CI metadata do not certify page-chain correctness, per-file rights, or open issue/PR resolution.

**Decision and copyright boundary:** reject new SDK/MCP/eval/lineage dependencies: no candidate provides verifiable provenance for this exact source-filtered pagination chain, and import would expand auth/runtime surface without evidence of safety benefit. Only generic pagination and lineage principles independently implemented; no third-party code, prompt, schema, workflow, template or API sample copied. Amazon Ads official product guidance and public practitioner/Reddit bidding anecdotes are not adopted as fixed PPC rules or causal proof. Default Read-only/Suggest/Shadow; live write/retry/idempotency/reconciliation remains with an external authorized Executor.

## 2026-10-24 — Global SP native campaign query-page binding (v1.42.0)

**Official API fact:** [Amazon Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24: campaign query returns campaign resources with `nextToken` pagination, separately from indexed HTTP 207 write receipts. Amazon does not define this repository's `raw_campaign_provenance` object. **Adopted:** independently implemented consistency gate for an adapter-retained native campaign and its page trace. If both are supplied, their campaign/account/filter/source/observation instant must bind to one enumerated query page. A conflicting or missing binding is `Unknown`, never a confirmed application. RED `a43a3b3ca3d7039a6fc02e1602aa6b95876560e5`, Actions 40083450668: 911 tests, 15 failures. GREEN `58ea73207c5db3c0450058667f15c5cdea6291c2`, Actions 40083485657: 911 tests and both validators successful. No additional Skill or runtime dependency.

**Previously reviewed candidate recheck (public metadata, 2026-10-24, mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14, 5 open issues; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,362 stars, MIT, non-fork, pushed 2026-10-24, 842 open issues; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, 412 open issues; [MarketplaceAdPros/amazon-ads-mcp-server](https://github.com/MarketplaceAdPros/amazon-ads-mcp-server) 29 stars, MIT, non-fork, pushed 2026-10-22, 1 open issue; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,533 stars, license metadata NOASSERTION, non-fork, pushed 2026-10-22, 139 open issues. These are repository-level metadata checks, not complete per-candidate CI/test/issue/PR audits or proof of per-file reuse rights. The last project's ambiguous repository-level license means no code/schema/template copying.

**Decision:** reject importing any candidate: none authenticates an external adapter's raw Global SP page association, and a new dependency would add complexity without verified safety gain. [Amazon's international campaigns guide](https://advertising.amazon.com/en-us/library/guides/checklist-for-new-international-ad-campaigns/) discusses budget/bid/reporting tactics, but its suggestions are not API constraints. Public Reddit PPC anecdotes (including 2026-10 discussions about dynamic bidding and limited clicks) are uncontrolled hypotheses, not causal or normative evidence. No external code, prompts, schemas, workflows, examples or templates copied. No live Ads writes, retries, idempotency or Executor reconciliation.


## 2026-10-24 — Global SP native monetary-budget consistency (v1.43.0)

**Official source:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24. Global campaign resources can carry `budgets[]` with `budgetType`, `recurrenceTimePeriod`, and marketplace-local `monetaryBudget.currencyCode/value`; the campaign query uses HTTP 200 and `nextToken`, while updates return indexed HTTP 207. The budget configuration is part of the campaign resource: no separate native budget endpoint is inferred. [Amazon Sponsored Products budget guide](https://advertising.amazon.com/library/guides/sponsored-products-budget-best-practices) discusses pacing and budget rules, but those are not equivalent to native configured budget readback or causal outcome proof.

**Verified gap / adopted:** Previously, when the trusted adapter retained both native campaign budget settings and normalized per-marketplace budgets, a direct currency/amount/recurrence contradiction could still return `Confirmed`. Independently authored optional cross-check now rejects malformed, missing, duplicate, unsupported and contradictory explicitly retained native budget settings as `Unknown`. The adapter must preserve numeric JSON lexemes as decimal strings; native floats cannot establish exact source precision. Native and normalized agreement with a different intended amount remains `Drifted`. Legacy envelopes without explicit native budgets stay compatible. RED commit `72395b0e1e90e7a3a21f3a1dc6ebd2b9be98598b`, Actions 40087100016: 938 tests, 21 failures. GREEN commit `152265a2201ce97e44624d3c4797d33d7dd075f2`, Actions 40087160510: 938 tests, all passing, both validators success.

**Fresh candidate metadata (2026-10-24; stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, pushed 2026-10-14, recent visible scheduled CI success 2026-10-19; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,363 stars, MIT, non-fork, pushed 2026-10-24, latest PR CI mixed/in-progress; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21, recent PR runs action_required; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,547 stars, Apache-2.0, non-fork, pushed 2026-08-09, last visible dynamic runs failed; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,535 stars, repository-level license NOASSERTION, non-fork, pushed 2026-10-22, latest scheduled runs mixed. All were previously assessed in SOURCES/research. Stars, issue/PR counts, recent activity and a few CI runs do not independently certify every source file's licensing, code tests, security or applicability to exact Global SP budget semantics.

**Decision / rights:** reject new dependencies: none independently authenticates retained campaign budget lexemes or improves the narrow deterministic cross-check enough to justify new runtime/auth surface. NOASSERTION is not permission to copy. No third-party code, prompt, schema, workflow, template, API sample, or proprietary content copied. Public expert/Reddit budget-change anecdotes are uncontrolled hypotheses, not Amazon platform limits, stable change percentages or causal evidence. Default Read-only/Suggest/Shadow; Amazon Ads writes, retries, idempotency and reconciliation remain with the separately authorized Executor.


## 2026-10-24 Global SP marketplace country-code eligibility guard (v1.44.0)

**Official fact, checked 2026-10-24:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) explicitly enumerates 21 supported marketplace country codes (AE, AU, BE, BR, CA, DE, EG, ES, FR, GB, IN, IT, JP, MX, NL, PL, SA, SE, SG, TR, US) and states that the United Kingdom uses GB. The guide distinguishes those codes from raw marketplace IDs in some status responses. **Adopted:** independently authored, read-only fail-closed country-code eligibility checks for campaign, ad-group and target readback, with dated evidence and deterministic regression. This is time-varying platform scope, not a universal ISO country-code registry; a new code needs fresh official confirmation, not an automatic alias. It does not prove individual account eligibility or HTTP provenance.

**Previously reviewed GitHub candidates, public metadata rechecked 2026-10-24 (stars mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp): 74 stars, MIT, non-fork, pushed 2026-10-14, tests directory present, latest visible Actions 2026-10-19 success, open PRs; [denisneuf/python-amazon-ad-api](https://github.com/denisneuf/python-amazon-ad-api): 203 stars, MIT, non-fork, pushed 2026-10-24, latest visible Actions 2026-10-24 success, open dependency PRs; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo): 26,366 stars, MIT, non-fork, pushed 2026-10-24, latest visible Actions success and open PRs; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage): 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers): 91,537 stars, NOASSERTION metadata, non-fork, pushed 2026-10-22. Repository metadata, selected workflows, tests directory and open PRs do not independently certify latest full code/CI quality or file-level licensing. Existing SOURCES/research already review these candidates; no duplicate adoption.

**Decision / copyright:** no new dependency or code import. A small local membership check is sufficient; generic MCP, eval and lineage frameworks cannot independently establish Amazon's current supported country list or a specific account's eligibility. NOASSERTION does not grant reuse rights. No external code, prompts, schemas, templates, workflow definitions, API example payloads or practitioner content copied. Public expert/Reddit PPC claims are not platform eligibility rules or evidence of causal lift. No live Amazon Ads write/retry/executor logic added.

## 2026-10-24 Global SP explicit query source binding (v1.44.1)

**Official platform basis:** [Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24, documents paginated campaign queries separately from indexed HTTP 207 updates. It does **not** mandate the normalized `pagination_trace.query.source` object. **Verified gap:** a trusted adapter could explicitly declare a query source conflicting with otherwise matching page/envelope lineage and still obtain `Confirmed`. **Adopted:** minimal independently authored fail-closed validation of an explicitly supplied query-level source. An omitted query source remains backward compatible. RED commit `9d4af31e59c4d36df7e85876c0c0eea7eef946d7`, Actions 40095254247: 963 tests, 7 failures. This only checks internal consistency; it does not authenticate HTTP responses or prove complete query coverage.

**Previously reviewed open-source candidates, metadata rechecked 2026-10-24 (mutable):** [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) 74 stars, MIT, non-fork, last push 2026-10-14; [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 26,367 stars, MIT, non-fork, pushed 2026-10-24; [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) 2,721 stars, Apache-2.0, non-fork, pushed 2026-10-21; [agentskills/agentskills](https://github.com/agentskills/agentskills) 26,552 stars, Apache-2.0, non-fork, pushed 2026-08-09; [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 91,538 stars, repository-level license NOASSERTION, non-fork, pushed 2026-10-22. This is a public metadata recheck, **not** a full CI/test/issue/PR or per-file licensing audit. **Rejected:** new SDK/MCP/lineage/eval dependency: none independently establishes query source authenticity for this narrow consistency bug. NOASSERTION does not grant reuse rights. No third-party code, prompts, schemas, workflows, templates or API examples copied. Official budget-rule/average-daily-budget guidance is platform context, not proof of realized spend or causal lift; public practitioner/Reddit heuristics are not platform rules. Live Ads writes, retries and reconciliation remain with the authorized external Executor.

## Global SP native query filter/page binding review — 2026-10-24

Highest-value verified gap: the existing optional `pagination_trace` required a consistent `query_fingerprint`, but the fingerprint was only an adapter assertion. Explicit native query request filters and per-page request bodies could contradict that assertion without preventing a false `Confirmed`. The repository-owned optional request binding now checks a uniquely scoped campaign query and the actual per-page continuation request against the existing token trace. RED: 987 unit tests, 20 failures (Actions 40099355669); GREEN: 987/987 (Actions 40099426067). No claim of independent HTTP authenticity or complete API coverage is made.

Platform fact: Amazon's [Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) (checked 2026-10-24) describes POST campaign queries with ad-product, marketplace-scope, campaign-ID filters and optional maxResults/nextToken. Its 207 update receipt is distinct from the 200 paginated query. Only the factual API surface was paraphrased; no vendor schema, sample payload, code or text was copied.

Incremental GitHub candidate review (2026-10-24, stars point-in-time): `KuudoAI/amazon_ads_mcp` (74, MIT, non-fork, pushed 2026-10-14), `denisneuf/python-amazon-ad-api` (203, MIT, non-fork, pushed 2026-10-24), `promptfoo/promptfoo` (26,368, MIT, non-fork, pushed 2026-10-24), `OpenLineage/OpenLineage` (2,721, Apache-2.0, non-fork, pushed 2026-10-21), and `jshorwitz/awesome-agentic-advertising` (45, no established license, discovery-only). These were already reviewed in SOURCES/research or are adjacent generic tooling. None supplies independently authenticated native Amazon query evidence or a compelling reason to add an SDK/MCP/eval/lineage dependency for this narrow gap. Repository metadata and visible activity were checked; a full independent audit of each candidate's code/tests/CI/issues/PRs was **not** completed. No third-party code, prompts, schemas, workflows, templates or substantial prose were copied; the unlicensed index was not reused.

A September 2026 Reddit discussion of high Sponsored Products CPC under multiple bid/placement adjustments is treated only as a possible confounder and experiment prompt, **not** an Amazon platform rule or fixed bidding formula. The existing control-interaction and marginal-economics gates remain unchanged.


## Global SP native campaign query-response membership — 2026-10-24 (v1.46.0)

**Official platform fact:** [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns), checked 2026-10-24, shows the POST campaign query response as a `campaigns[]` resource array plus `nextToken`; HTTP 207 update receipts are separate from query responses. The repository-owned optional `response_body` trace is NOT a native Amazon API requirement. The prior page-index provenance contract could falsely confirm a native campaign absent from the claimed page. RED-first 20 synthetic tests (1007 total, 14 failures, Actions 40103908902) reproduce that gap; minimal fix `15f1a3e8ab23acbd0ea2e65087846269710af08a` passes 1007 tests plus Skill/Eval validators (Actions 40103962004). The adopted check verifies internal equality and uniqueness of explicitly retained campaign resources, not external HTTP authenticity, completeness, or causality.

**De-duplicated public open-source review (2026-10-24 snapshot):** `KuudoAI/amazon_ads_mcp` (74 stars, MIT, non-fork, pushed 2026-10-14, tests directory and successful public Actions on 2026-10-19); `denisneuf/python-amazon-ad-api` (203, MIT, non-fork, pushed 2026-10-24, test directory and successful Actions on 2026-10-24); `promptfoo/promptfoo` (26,370, MIT, non-fork, test directory, latest observed public run failed on 2026-10-24); `OpenLineage/OpenLineage` (2,721, Apache-2.0, non-fork, spec directory, latest observed public run `action_required` on 2026-10-23); `modelcontextprotocol/servers` (91,541, GitHub license metadata `NOASSERTION`, non-fork). GitHub open-issue counters include PRs; a one-PR sample and workflow status are not full issue, security or test-path audits. These projects were previously recorded in SOURCES/research and do not supply independent native-response authentication. **Decision:** reject dependency import and code/schema/prompt/workflow copying. Retain only the general, independently implementable principle that evidence membership and provenance should be checked. MIT/Apache-2.0 permit reuse subject to terms, but reuse was unnecessary; `NOASSERTION` does not establish blanket permission for every subdirectory. Public practitioner/reddit bid and budget experiences are hypothesis material only, not platform specifications or causal proof.

**Copyright boundary:** Only public product facts are paraphrased from Amazon's guide; no external implementation, template, API example, prompt or workflow was copied. The native response binding and tests are repository-authored. No live Ads account mutation, retry, idempotency or Executor reconciliation was added.


## 2026-10-24 — Budget state value evidence (v1.46.1)

Confirmed defect: compare_control_state previously accepted effective_daily_budget = Unknown, base_average_daily_budget = false, negative/non-finite amounts and average_daily_budget_policy = Unsupported as observed control values, sometimes returning Treatment Isolated. RED-first 1019 tests, 11 failures (Actions 40108252702); minimal fix 1019/1019 and Skill/Eval validators pass (Actions 40108325621). This change validates numeric evidence and known policy labels, not external Adapter authenticity or live Amazon budget settings.

First-party sources: Amazon Ads May 9, 2023 daily-budget policy (https://advertising.amazon.com/resources/whats-new/sponsored-ads-daily-budgeting-policy-and-options) describes an account setting and an up-to-100% extra daily-spend option; its budget-rules guide (https://advertising.amazon.com/library/guides/budget-rules/) describes scheduled/performance-triggered increases. An evergreen Sponsored Products guide still describes 25% flexibility. These date/scope differences do not authorize a fixed policy multiplier: observed account/platform policy remains necessary.

New candidate review: WaytoAIC/waytoaic-amazon-ads-skills is a small public Skill repository whose LICENSE.md states PolyForm Noncommercial 1.0.0 plus project-specific additional terms, not an OSI open-source license. Reject copying Skill text, prompts, schemas, scripts or workflows; only generic independently known principles were considered. hashgraph-online/awesome-codex-plugins has an Apache-2.0 root license but mirrors third-party plugin bundles with potentially different rights; no import, and the root license is not assumed to cover every mirrored asset. Previously reviewed SDK/MCP/eval/lineage candidates do not fix this budget value-level defect. No third-party code, templates, prompts, schemas, workflows or proprietary examples were copied. Public practitioner stories are hypotheses, not platform rules.

## 2026-10-25 — Sponsored Products placement modifier value evidence (v1.46.2)

**Verified local gap:** the read-only control-state comparator checked only non-null values for the three required Sponsored Products placement modifiers. Synthetic RED-first tests demonstrated that `Unknown`, `Unsupported`, `Partial`, boolean, negative, non-finite, percent-string and structured placeholders could be treated as stable evidence and lead to `Treatment Isolated` (1036 tests, 12 confirmed failures after correcting two positive-control test expectations; Actions 40113083149; initial draft had 14 failures, Actions 40113031972). The minimal finite/nonnegative numeric-evidence fix passed 1036/1036 plus Skill/Eval validators (Actions 40113090733). This is a repository-owned evidence rule, not an Amazon API schema or live-write path.

**Official sources checked 2026-10-25:** Amazon Ads, *Rest of Search Bid Adjustment for Sponsored Products* (2024-01-09), https://advertising.amazon.com/resources/whats-new/improve-campaign-performance ; Amazon Ads, *Sponsored Products best practices*, https://advertising.amazon.com/library/guides/sponsored-products-best-practices ; Amazon Ads, *Bidding strategies for Sponsored Products* (updated 2026-09-28), https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7 . The first two describe three distinct placement adjustment surfaces and positive bid boosts; they do not justify treating missing modifiers as zero. Numeric ceiling, availability and control composition require dated scope-specific evidence, not a hard-coded universal rule. Amazon Business placement is a distinct potentially interacting surface requiring a later capability/coverage review, not silently folded into these three fields.

**Incremental candidate/license review (GitHub public metadata snapshot 2026-10-25):** `amekala/ads-mcp` (105 stars, MIT, non-fork, pushed 2026-10-20; visible repository Skills/agents and latest public Actions success; 9 open issue/PR counter, 0 sampled open PRs) is a third-party service-backed integration and was **rejected** as an unnecessary write-capable dependency for this deterministic read-only value check. `jhrendon/amazon-mcp` (2 stars, no license identified in GitHub metadata, non-fork, last pushed 2026-07-09; vitest workspace and latest visible Actions success; no open PR) was **rejected**, and its code/templates/workflows cannot be reused without license authorization. Previously reviewed `KuudoAI/amazon_ads_mcp` (74 stars, MIT) and `promptfoo/promptfoo` (26,377 stars, MIT) add no needed proof for this gap. GitHub stars, a passing CI run and repository metadata do not establish production suitability or comprehensive security/issue/PR quality. No third-party code, prompts, schemas, templates, workflow or proprietary examples copied. Public practitioner claims remain hypotheses rather than Amazon policy or causal evidence.


## 2026-10-25 — Amazon Business placement modifier evidence (v1.47.0)

**Verified repository gap:** Sponsored Products bid/budget causal comparator checked only Top of Search, Rest of Search and Product Pages numeric modifiers. If the trusted Adapter explicitly supplied an `amazon_business` modifier with Unknown/Unsupported/Partial/boolean/nonfinite/negative evidence, it could still classify a base-bid change as `Treatment Isolated`; one-sided B2B presence could be misread as a normal observed change instead of incomplete control evidence. RED-first 16 deterministic tests (1052 total) demonstrated 12 failures on the old implementation (Actions 40118010958). The minimal fix validates the optional fourth value and rejects one-sided presence, preserving valid numeric zero and legacy both-absent compatibility. Both-absent legacy evidence is **not** independent proof of B2B coverage, ineligibility, or zero. This is a partial evidence-hardening step, not an external connector completeness or HTTP-authenticity claim.

**Official platform evidence reviewed 2026-10-25:** Amazon Ads, *Adjust Sponsored Products bids*, updated 2026-09-28, https://advertising.amazon.com/help/GYYZVM7LGSRYGWV5 explicitly distinguishes Amazon Business placements from three ordinary placements and says across-retailers Sponsored Products campaigns cannot use Amazon Business placement adjustments. Amazon Ads, *Advertising on Amazon Business*, https://advertising.amazon.com/channels/amazon-business confirms a B2B placement boost on existing Sponsored Products campaigns. Amazon Ads, *Reach business shoppers with Amazon Business exclusive campaigns*, 2025-05-05, https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product documents separately scoped site restrictions. None of these proves universal campaign eligibility or an account-level modifier setting. Do not apply a generic B2B percentage or infer causal uplift from the promotional examples.

**Practitioner evidence:** Public Reddit threads in r/AmazonFBA (2026-09-03) and r/AmazonPPCoptimization (2026-08-07) discuss overlapping B2B and ordinary placement modifiers, but are unverified account anecdotes and not an authoritative bidding formula, price-ceiling rule or causal result. No community advice was copied into executable logic.

**Incremental open-source/license review (GitHub public metadata snapshot 2026-10-25):** `amekala/ads-mcp` (105 stars, MIT, non-fork, pushed 2026-10-20, 9 issue/PR count) and `promptfoo/promptfoo` (26,378 stars, MIT, non-fork, pushed 2026-10-24, 846 issue/PR count) were **rejected** as dependencies: a deterministic control-evidence check needs neither an external ads executor nor an LLM-eval framework. `AlchemyCollectives/amazon-seller-agent` (0 stars, fork, GitHub license NOASSERTION, last push 2026-05-18) and `MarketplaceAdPros/amazon-seller-agent-claude-code` (3 stars, fork, GitHub license NOASSERTION, last push 2026-05-18) were **rejected**; README distinguishes MIT starter scaffolding from separately licensed bundled third-party Skills, so a root/template license cannot authorize copying all included prompts/workflows. No complete code/security/CI/issue-PR audit is claimed; stars and recent push activity do not prove quality. No third-party code, prompts, schemas, workflows, templates or proprietary examples were imported. Repository-owned tests and guard logic only.
