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
- entity history for avoiding duplicate or contradictory optimizations;
- explicit distinction between facts, hypotheses, missing data, confidence and actionability;
- approval-gated mutation design.

Adopted as independently rewritten concepts. Vendor-specific APIs and fixed click/order/spend thresholds are intentionally not imported as universal automation rules.

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
- prioritized action lists.

The project uses CC BY-NC 4.0 and includes fixed heuristic thresholds that are not suitable as universal automation rules. Its text and thresholds are therefore not copied into this MIT repository.

Repository: https://github.com/noique/cross-border-ecommerce-skills

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
10. Record reviewed sources here when they materially influence the project.
