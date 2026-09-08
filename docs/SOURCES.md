# Methodology sources

This repository does not copy third-party skill text wholesale. Public repositories are used to discover generic methods, operating concepts and documentation structures. Ideas are independently rewritten for Amazon Ads, checked against the repository safety model, and kept connector/runtime neutral.

## Reviewed repositories

### nospicyplease/amazon-ppc-advanced-skills

Reviewed for thin `SKILL.md + references`, performance-drop diagnosis, contribution analysis, retail context, control-change timelines, Mixed-ASIN safety, negative attachment verification, growth headroom, post-change readback, optimization memory and approval-gated mutation concepts.

Only generic concepts were adopted. Vendor-specific APIs, storage implementations and fixed click/order/spend thresholds were not imported.

Repository: https://github.com/nospicyplease/amazon-ppc-advanced-skills

### AgriciDaniel/claude-ads

Reviewed for progressive loading, contextual benchmarks, marginal-return thinking, guardrails, validation/rollback and separation of observation, diagnosis, recommendation and mutation.

Repository: https://github.com/AgriciDaniel/claude-ads

### weisberg/agile_agentic_analytics

MIT-licensed repository reviewed for experiment lifecycle, power/MDE discipline when inputs exist, sample-ratio/contamination awareness, sequential-testing caution, realized-allocation integrity, holdout/control integrity and advertising-market interference.

Generic ideas that materially influenced experiment hardening:

1. a declared split or nominal control does not prove correct realized assignment/delivery;
2. in advertising markets, treatment can alter the comparison cohort through spillover or a changed auction opportunity set;
3. experiment validity must be checked before interpreting a treatment-only KPI lift;
4. control/assignment integrity is evidence that can become stale when the experiment environment changes.

These concepts were independently rewritten for Amazon Ads as query/target/ASIN overlap, shared-budget/routing/automation leakage, auction displacement, constrained-resource interference and dated control-boundary revalidation. No platform-specific experiment APIs, prose or implementation details were copied. No statistical significance is fabricated when expected allocation or assignment assumptions are missing.

Repository: https://github.com/weisberg/agile_agentic_analytics

### ir-anthology/ir-anthology.github.io

Public bibliography repository reviewed only as a discovery index for the WWW 2022 research topic **Interference, Bias, and Variance in Two-Sided Marketplace Experimentation: Guidance for Platforms**.

The project does not copy the paper, bibliography prose, formulas, code, or implementation. The high-level marketplace lesson used here is only that interacting units can bias naive treatment/control comparisons. It is independently adapted to Amazon Ads as shared auction opportunity, shared pacing capacity and substitution between advertising scopes.

Repository: https://github.com/ir-anthology/ir-anthology.github.io

### open-mercato/open-mercato

MIT-licensed multi-tenant application reviewed only for the generic engineering principle that tenant/organization scope should be explicitly carried through requests and sensitive access paths should fail closed when scope is missing or invalid.

No Open Mercato code, ACL model, schemas, or prose were copied. The concept was independently adapted to Amazon Ads optimization memory as a collision-safety rule: marketplace + profile/account scope must be resolved before entity ID/name history is merged or reused.

Repository: https://github.com/open-mercato/open-mercato

### unifyai/unify

MIT-licensed repository reviewed for separating deterministic contract tests from end-to-end capability evals and for treating capability failures as semantic/system-design failures rather than only code failures. Rewritten as `contract checks` vs `capability replay` in `evals/README.md`.

Repository: https://github.com/unifyai/unify

### Observal/Observal

Apache-2.0 repository reviewed for evidence-bearing evaluation criteria and a third state when evidence is insufficient. Rewritten as `met / not_met / insufficient_evidence`.

Repository: https://github.com/Observal/Observal

### TheQtCompanyRnD/agent-skills

Reviewed for a canonical skills tree shared across multiple agent runtimes, portable `SKILL.md + references`, and platform-specific manifests separated from business logic.

Repository: https://github.com/TheQtCompanyRnD/agent-skills

### noique/cross-border-ecommerce-skills

CC BY-NC 4.0 project reviewed only for high-level weekly PPC cadence, current/prior-period comparison, campaign triage, search-term review and prioritized actions. Its prose, fixed thresholds, API calls and export steps were not copied into this MIT repository.

Repository: https://github.com/noique/cross-border-ecommerce-skills

### heymoezy/porter

Reviewed only for the generic experiment anti-pattern that bundled concurrent changes destroy causal attribution. A repository-level license was not verified during review, so no prose, code, templates or implementation details were imported.

Repository: https://github.com/heymoezy/porter

### paperclipai/paperclip

Reviewed for generic execution-reliability patterns: partial application, ambiguous delivery, reconciliation and retry/idempotency. No implementation was imported. This repository keeps idempotency in the external Connector/Executor and uses Skills only to reason about `Unknown / Partial / Drifted` states.

Repository: https://github.com/paperclipai/paperclip

### prathamesh-git9/effect-broker

Reviewed for a particularly useful distinction between three side-effect classes: safely idempotent, reconcilable after uncertain delivery, and unsafe-to-repeat when neither guarantee exists. The important generic idea adopted here is **stable intent + explicit idempotency contract + authoritative reconciliation**.

This project does not import effect-broker code or prose. The idea was independently adapted into two complementary Amazon Ads evals:

- ambiguous mutation without trusted readback/idempotency → block blind retry;
- same stable intent with the same idempotency key and an explicit executor deduplication contract → connector-level retry may be safe, while application status still remains unconfirmed until reconciliation/readback.

Repository: https://github.com/prathamesh-git9/effect-broker

### nexscope-ai/Amazon-Skills

MIT-licensed multi-agent-compatible Amazon skill collection reviewed for public Amazon-domain coverage, portable skill packaging, profitability modeling, multi-campaign strategy and portfolio-level budget thinking.

No skill prose, templates, fixed thresholds or fixed percentage budget rules were copied. The useful generic ideas retained are: budget allocation must reflect business objectives/product economics, and cross-campaign/portfolio decisions should not be reduced to one campaign's historical ACoS/ROAS.

Repository: https://github.com/nexscope-ai/Amazon-Skills

### MicrosoftDocs/Advertising

Official Microsoft Advertising documentation repository reviewed only for a vendor-neutral portfolio-budget lesson: when campaign controls share a constrained budget resource, partially overlapping control scopes can interfere with each other, so budget/control boundaries need to align before interpreting performance independently.

No Microsoft-specific product behavior is asserted as Amazon Ads behavior. The generic concept was independently rewritten as a business-budget-pool / external-pacing conflict model for Amazon Ads Agents.

Repository: https://github.com/MicrosoftDocs/Advertising

## Internal method hardening from observed failure modes

Some additions are not copied from an external repository at all. They are independent safety hardening derived from the repository's existing causal model and regression gaps.

Examples:

- **Retail snapshot freshness** — a Buy Box, inventory, price or listing snapshot only proves the state at the timestamp it observed. If that snapshot predates a later conversion decline, it must not be used as current-state proof to justify aggressive traffic suppression.
- **Verified entity migration lineage** — a deliberate restructure can preserve useful predecessor history, but only through an explicit auditable predecessor→successor mapping. Historical evidence may transfer as bounded context; successor Bid/Budget/State/readback never transfers as current truth.
- **Portfolio opportunity cost** — under a fixed business budget pool, locally attractive campaign increases can be mutually incompatible. A reallocation must identify the funding source, protected floors, marginal headroom and source opportunity cost.
- **Treatment/control interference** — a cohort can improve because it captures traffic, auction opportunity or budget that would otherwise have served the comparison cohort. When displacement is plausible, combined/pool outcomes and control-boundary integrity matter more than treatment-only lift.
- **Shared-budget starvation** — if treatment spends more from the same fixed pool and mechanically reduces control capacity, treatment growth is a redistribution signal until pool-level incrementality is demonstrated.
- **Variation-family substitution** — when treatment and control advertise sibling child ASINs, child-level growth can be a family mix shift. Parent-family totals and purchased-ASIN crossover are required before claiming child-level incrementality.
- **Long-test control-boundary drift** — a control verified at launch can become invalid after keyword/target harvesting, negative changes, automation scope changes, migrations, budget-pool changes, or other scope edits. Boundary evidence must be dated and revalidated after material changes.
- **Collision-safe optimization identity** — same entity ID/text/name is not enough when memory spans multiple marketplace/profile scopes. Scope-incomplete or conflicting history must fail closed rather than silently merge outcomes.

## Integration rules

Before adopting an external idea:

1. Prefer generic methodology over vendor-specific APIs.
2. Do not copy substantial third-party prose.
3. Do not import private/client data.
4. Treat fixed thresholds and fixed action percentages as optional heuristics unless supported by account evidence; do not make them universal defaults.
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
17. Treat experiment contamination, unexplained allocation mismatch, treatment leakage or treatment→control interference as readout limitations.
18. Treatment-only improvement is not proof of incrementality when treatment and control share query/ASIN/auction/budget opportunity; inspect combined or pool-level outcomes when displacement is plausible.
19. If treatment and control share a constrained budget/pacing resource, distinguish incremental performance from resource redistribution/starvation.
20. If sibling child ASINs can substitute, evaluate parent-family outcomes and purchased-ASIN crossover before claiming child-level incrementality.
21. Revalidate control boundaries after material scope-changing events during long experiments; launch-time isolation is not permanent evidence.
22. Treat partial application as a realized treatment different from intended treatment.
23. Do not compare promotion-contaminated windows as ordinary evergreen baselines.
24. Treat stockout/retail-readiness failures as causal gates before traffic suppression.
25. Treat stale retail snapshots as historical evidence, not current-state proof.
26. Resolve marketplace + profile/account scope before merging optimization memory. Missing, ambiguous or colliding scope must fail closed.
27. Do not transfer entity memory across recreated IDs without verified identity mapping; verified migrations may carry bounded historical context but never clone successor current state.
28. Treat timeout/unknown mutation outcomes as unresolved until readback/reconciliation or executor-level idempotency makes repetition safe.
29. Stable idempotency keys must stay bound to the same stable intent and payload; a new value is a new intent.
30. Trusted current-state readback overrides earlier executor acknowledgement when the states disagree; classify the difference as drift/partial/unresolved before outcome attribution.
31. Do not equate higher ROAS or revenue with higher profit; use contribution economics when the business objective is profitability.
32. A historically proven relevant query that temporarily has zero orders should be diagnosed as a possible conversion break before being treated as irrelevant traffic.
33. A declared experiment allocation does not prove realized allocation integrity; unexplained imbalance must be investigated before causal rollout.
34. Under a fixed budget pool, reconcile source and destination allocations and evaluate source opportunity cost; campaign-local efficiency does not prove portfolio-level optimality.
35. Record reviewed sources here when they materially influence the project.
