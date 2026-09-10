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

### LittleAksMax/amazon-ads-api-sdk-go

MIT-licensed public Amazon Ads SDK reviewed for a narrow, implementation-neutral reporting/query lesson: Amazon Ads entity-query surfaces can use `nextToken` pagination, while Reporting API v3 follows an asynchronous request → poll/fetch → download lifecycle. The repository itself explicitly describes its coverage as partial and Sponsored Products-oriented.

No SDK code, models, examples or API wrapper implementation were copied. The generic pagination lesson was independently adapted into the audit completeness gate: a returned page is not the full entity population while a continuation token remains, and whole-account ranking should wait for exhausted pagination or an equivalent trusted complete export.

Repository: https://github.com/LittleAksMax/amazon-ads-api-sdk-go

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

Repository: https://github.com/nexscope-ai/Amazon-Skills

### MicrosoftDocs/Advertising

Official Microsoft Advertising docs repository reviewed only for a vendor-neutral portfolio-budget lesson: controls sharing a constrained resource can interfere when control scopes do not align.

No Microsoft-specific behavior is asserted as Amazon Ads behavior. The generic concept was independently rewritten as budget-pool/external-pacing conflict logic.

Repository: https://github.com/MicrosoftDocs/Advertising

## Internal method hardening from observed failure modes

Some additions are independent safety hardening rather than adaptations of a single external source:

- **Retail snapshot freshness** — a Buy Box/inventory/price/listing snapshot proves only the state/time it observed.
- **Source-lineage drift** — same metric name can hide different attribution, refresh, filters, grain or semantic meaning.
- **Semantic metric-version drift** — one stable table/column can change meaning across a semantic cutover.
- **Asymmetric backfill drift** — same source + same metric version can still be incomparable when a frozen baseline is D+1 while a post window is D+7 and historical rows restate.
- **Historical restatement after decision** — mutable history must not rewrite what evidence was available at decision time; preserve snapshot identity and append a correction/re-evaluation when latest data materially changes the outcome interpretation.
- **Audit aggregation integrity** — profile/campaign/keyword/search-term/placement views overlap; choose one canonical additive grain, reconcile complete parent/child totals, and recompute ratio metrics from additive components.
- **Audit population completeness** — API pagination, connector row caps and context truncation are separate failure modes; preserve continuation metadata and do not claim whole-population rank from a partial slice.
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
28. Treat source/reporting switches near apparent breaks as competing explanations.
29. Treat parent/variation-family retail changes as upstream causal candidates.
30. Partial application is a realized treatment different from intended treatment.
31. Do not use promotion-contaminated windows as ordinary evergreen controls.
32. Retail-readiness failures are causal gates before traffic suppression.
33. Stale retail snapshots are historical evidence, not current proof.
34. Resolve marketplace + profile/account scope before merging memory.
35. Verified same-marketplace cross-profile migrations may carry bounded mature evidence but never clone current state.
36. Cross-marketplace migration defaults to directional evidence portability for performance/economic conclusions.
37. Timeout/unknown writes remain unresolved until reconciliation/idempotency makes repetition safe.
38. Stable idempotency keys stay bound to the same stable intent/payload.
39. Trusted current-state readback overrides earlier executor acknowledgement when they disagree.
40. Higher ROAS/revenue is not automatically higher profit.
41. A previous winner temporarily at zero orders needs conversion-break diagnosis before negative treatment.
42. Declared experiment allocation does not prove realized allocation integrity.
43. Fixed budget pools require source/destination opportunity-cost reconciliation.
44. Record reviewed sources here when they materially influence the project.
