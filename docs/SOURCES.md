# Methodology sources

This repository does not copy third-party skill text wholesale. External repositories are used to discover useful patterns, operating concepts, and documentation structures. Reusable ideas are rewritten for this project, checked against the repository's safety model, and adapted to Amazon Ads.

## Reviewed repositories

### nospicyplease/amazon-ppc-advanced-skills

Useful patterns reviewed:

- one operator job per skill;
- concise `SKILL.md` with detailed logic moved to `references/`;
- performance-drop diagnosis using exact windows, contribution analysis, retail context, control-change timelines and mixed-ASIN safety;
- growth-opportunity analysis combining ads evidence, retail readiness, product context, headroom and incrementality questions;
- post-change readback before judging outcome;
- shared optimization memory before legacy changelogs;
- applied/failed/unknown event history, pending evaluations and entity history for avoiding duplicate or contradictory optimizations;
- warnings when memory is local-only, partial or has unsynchronized/spooled events;
- weekly/downside/upside operating-system thinking that separates decline diagnosis, growth opportunities and action gates instead of collapsing everything into ACOS tuning;
- explicit distinction between facts, hypotheses, missing data, confidence and actionability;
- approval-gated mutation design.

Adopted as independently rewritten concepts. Vendor-specific APIs, storage implementations, local spool mechanics and fixed click/order/spend thresholds are intentionally not imported. This repository expresses the generic memory concept as an append-first event ledger plus a derived compact `entity-history` view so the canonical Skills remain connector- and runtime-neutral.

Repository: https://github.com/nospicyplease/amazon-ppc-advanced-skills

### AgriciDaniel/claude-ads

Useful patterns reviewed:

- thin skill entrypoints and progressive loading;
- contextual rather than universal benchmarks;
- marginal-return thinking;
- guardrails, validation and rollback;
- separation between observation, diagnosis, recommendation and mutation.

Repository: https://github.com/AgriciDaniel/claude-ads

### weisberg/agile_agentic_analytics

Useful experimentation concepts reviewed:

- experiment lifecycle as a distinct capability instead of mixing test design into every optimization skill;
- power/minimum-detectable-effect thinking only when required inputs support it;
- sample-ratio-mismatch and contamination awareness;
- sequential-testing/early-stopping caution;
- structured experiment results for later evaluation.

The repository is MIT licensed. This project does not copy its implementation or prose. The generic experimentation ideas were independently rewritten for Amazon Ads in `skills/experiment-planner/` with stricter `Suggest/Shadow` boundaries and account-specific economics, Mixed-ASIN, attribution, promotion and retail-readiness gates.

Repository: https://github.com/weisberg/agile_agentic_analytics

### unifyai/unify

Useful evaluation concepts reviewed:

- distinguish deterministic/symbolic contract tests from end-to-end capability evals;
- treat a capability failure as potentially coming from prompt/instruction/tool design rather than only programmatic code;
- use replay/caching as evidence of the exact model input/output rather than clearing evidence to make a failure disappear;
- separate infrastructure regression tests from semantic quality tests.

The repository is MIT licensed. No implementation or prose was copied. For this project the generic distinction was independently rewritten as `contract checks` vs `capability replay` in `evals/README.md`, with Amazon Ads-specific safety rubrics and synthetic fixtures.

Repository: https://github.com/unifyai/unify

### Observal/Observal

Useful evaluation concepts reviewed:

- criteria should be evidence-bearing rather than assumed;
- an evaluator benefits from an explicit third state for cases where the available trace cannot support a defensible pass/fail judgment.

The repository is Apache-2.0 licensed. This project independently expresses the concept as `met / not_met / insufficient_evidence` for decision-behavior evals. No source implementation or prose was copied.

Repository: https://github.com/Observal/Observal

### TheQtCompanyRnD/agent-skills

Useful structural patterns reviewed:

- one canonical `skills/` tree shared across multiple agent runtimes where practical;
- `SKILL.md + references` as a portable full-directory skill model;
- platform adapters/manifests separated from canonical business logic.

Only the architecture pattern is used; Qt-specific content is not copied.

Repository: https://github.com/TheQtCompanyRnD/agent-skills

### noique/cross-border-ecommerce-skills

Useful high-level workflow ideas reviewed:

- weekly Amazon PPC operating rhythm;
- current vs prior-period comparison;
- campaign triage;
- search-term harvesting and negative review;
- prioritized action lists;
- separating recurring weekly review from deeper structural diagnosis.

The project uses CC BY-NC 4.0 and includes fixed heuristic thresholds and vendor/tool-specific output steps that are not suitable as universal automation rules. Its text, thresholds, API calls and report-export instructions are therefore not copied into this MIT repository.

For this project's `playbooks/weekly-review.md`, only the generic concept of a recurring review cadence was retained. The implementation was independently rewritten to use business contribution, attribution maturity, optimization memory, Mixed-ASIN safety, action/hold states, marginal evidence and specialist-Skill escalation rather than fixed red/yellow/green ACOS or bid-change percentages.

Repository: https://github.com/noique/cross-border-ecommerce-skills

## Other memory/event-log patterns reviewed but not directly imported

During the optimization-memory pass, generic public agent repositories were also searched for persistent memory and event-log patterns. The useful general lesson was to keep facts/events distinct from mutable summaries and to treat stale memory as historical context rather than current state. No implementation or prose from those projects was copied; the resulting memory contract was designed specifically around this repository's existing `optimization-event.json`, Post-change Review lifecycle and Amazon Ads safety model.

## Integration rules

Before adopting an external idea:

1. Prefer generic methodology over vendor-specific APIs.
2. Do not copy substantial third-party prose.
3. Do not import client/account data or private examples.
4. Treat fixed thresholds as optional heuristics unless backed by account-specific evidence.
5. Preserve `Read-only / Suggest / Shadow / Execute` boundaries.
6. Put detailed reusable knowledge in references/playbooks for progressive loading.
7. Keep canonical business logic tool-agnostic; keep runtime compatibility in manifests/adapters.
8. For experiment designs, predeclare the decision question, hypothesis, primary metric, guardrails and stop rules before observing results.
9. Do not fabricate statistical confidence, power or MDE when the required inputs are missing.
10. For optimization memory, preserve event lineage, distinguish intent/application/readback/outcome, bound history retrieval, and never treat stale or partial memory as current complete state.
11. Prefer a playbook over another Skill when the new content composes existing capabilities into a recurring operating cadence rather than creating a new decision domain.
12. For evals, separate contract failures from capability failures and score decision behavior instead of exact wording.
13. Preserve `insufficient_evidence` as a real outcome when a replay cannot support a defensible pass/fail judgment.
14. Never weaken a regression fixture merely to make the current model pass; fixtures should represent intended safe behavior.
15. Record reviewed sources here when they materially influence the project.
