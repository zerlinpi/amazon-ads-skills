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

MIT-licensed repository reviewed for experiment lifecycle, power/MDE discipline when inputs exist, sample-ratio/contamination awareness, sequential-testing caution, realized-allocation integrity checks and structured experiment results. The generic idea adopted in the latest pass is that a declared split does not prove correct realized assignment: unexplained treatment/control imbalance can indicate assignment, filtering, logging, delivery or interference problems and should invalidate action-safe causal claims until explained.

Concepts were independently rewritten for Amazon Ads with stricter Suggest/Shadow, Mixed-ASIN, attribution, promotion and retail-readiness gates. No statistical significance is fabricated when expected allocation or assignment assumptions are missing.

Repository: https://github.com/weisberg/agile_agentic_analytics

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

MIT-licensed multi-agent-compatible Amazon skill collection reviewed for public Amazon-domain coverage, portable skill packaging, and profitability modeling that includes advertising spend alongside product/FBA/fee economics rather than treating ROAS as a complete profitability measure.

No skill prose, templates or fixed recommendations were copied. This repository already had its own contribution-profit model; the review reinforced the eval requirement that higher attributed revenue/ROAS must not override deteriorating contribution profit under a profit-maximization objective.

Repository: https://github.com/nexscope-ai/Amazon-Skills

## Internal method hardening from observed failure modes

Some additions are not copied from an external repository at all. They are independent safety hardening derived from the repository's existing causal model and regression gaps.

Latest example: **retail snapshot freshness**. A Buy Box, inventory, price or listing snapshot only proves the state at the timestamp it observed. If that snapshot predates a later conversion decline, it must not be used as current-state proof to justify aggressive traffic suppression. The system now requires refreshed or dated retail evidence, or it downgrades actionability.

## Integration rules

Before adopting an external idea:

1. Prefer generic methodology over vendor-specific APIs.
2. Do not copy substantial third-party prose.
3. Do not import private/client data.
4. Treat fixed thresholds as optional heuristics unless supported by account evidence.
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
17. Treat experiment contamination or unexplained allocation mismatch as a readout limitation.
18. Treat partial application as a realized treatment different from intended treatment.
19. Do not compare promotion-contaminated windows as ordinary evergreen baselines.
20. Treat stockout/retail-readiness failures as causal gates before traffic suppression.
21. Treat stale retail snapshots as historical evidence, not current-state proof.
22. Do not transfer entity memory across recreated IDs without verified identity mapping.
23. Treat timeout/unknown mutation outcomes as unresolved until readback/reconciliation or executor-level idempotency makes repetition safe.
24. Stable idempotency keys must stay bound to the same stable intent and payload; a new value is a new intent.
25. Trusted current-state readback overrides earlier executor acknowledgement when the states disagree; classify the difference as drift/partial/unresolved before outcome attribution.
26. Do not equate higher ROAS or revenue with higher profit; use contribution economics when the business objective is profitability.
27. A historically proven relevant query that temporarily has zero orders should be diagnosed as a possible conversion break before being treated as irrelevant traffic.
28. A declared experiment allocation does not prove realized allocation integrity; unexplained imbalance must be investigated before causal rollout.
29. Record reviewed sources here when they materially influence the project.