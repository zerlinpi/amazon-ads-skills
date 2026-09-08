# Methodology sources

This repository does not copy third-party skill text wholesale. External repositories are used to discover useful patterns, operating concepts, and documentation structures. Reusable ideas are rewritten for this project, checked against the repository's safety model, and adapted to Amazon Ads.

## Reviewed repositories

### nospicyplease/amazon-ppc-advanced-skills

Useful patterns reviewed:

- one operator job per skill;
- concise `SKILL.md` with detailed logic moved to `references/`;
- performance-drop diagnosis based on exact windows, contribution analysis, retail context, control-change timelines, and mixed-ASIN safety;
- growth-opportunity analysis that combines ads evidence, retail readiness, ASIN/product context, ranking/organic context, budget or impression headroom and incrementality questions;
- post-change readback before judging outcome, plus current-state verification, monitoring and rollback-readiness concepts;
- snapshots/changelogs/entity-history as context for avoiding duplicate or contradictory optimizations;
- explicit distinction between facts, hypotheses, missing data, confidence, and actionability;
- approval-gated mutation design.

Adopted here as independently rewritten concepts, especially in `skills/performance-drop-diagnosis/`, `skills/growth-opportunity-finder/`, `skills/post-change-review/`, and their references. Vendor-specific capability names and fixed click/order/spend thresholds found in external material are intentionally not imported as universal automation rules.

Repository: https://github.com/nospicyplease/amazon-ppc-advanced-skills

### AgriciDaniel/claude-ads

Useful patterns reviewed:

- thin platform-specific skill entrypoints;
- progressive loading of measurement, benchmark, budget, bidding, policy and other references;
- contextual rather than universal benchmarks;
- marginal-return thinking for budget allocation;
- decision-complete growth actions with guardrails, validation and rollback;
- clear separation between observation, diagnosis, recommendation and mutation.

Repository: https://github.com/AgriciDaniel/claude-ads

### TheQtCompanyRnD/agent-skills

Useful structural patterns reviewed:

- one canonical `skills/` tree shared across multiple agent runtimes where practical;
- `SKILL.md + references` as a portable full-directory skill model;
- platform adapters/manifests kept separate from canonical skill business logic;
- multi-tool compatibility without maintaining duplicate domain instructions.

Only the architecture pattern is used here; Qt-specific skill content is not copied.

Repository: https://github.com/TheQtCompanyRnD/agent-skills

### noique/cross-border-ecommerce-skills

Useful high-level workflow ideas reviewed:

- weekly Amazon PPC operating rhythm;
- current vs prior-period comparison;
- campaign triage;
- search-term harvesting and negative review;
- prioritized action lists.

The project uses CC BY-NC 4.0 and includes fixed heuristic thresholds that are not suitable as universal automation rules. Its text and thresholds are therefore not copied into this MIT repository; only general workflow ideas may inform independently rewritten playbooks.

Repository: https://github.com/noique/cross-border-ecommerce-skills

## Integration rules

Before adopting an external idea:

1. Prefer generic methodology over vendor-specific APIs.
2. Do not copy substantial third-party prose.
3. Do not import client/account data or private examples.
4. Treat fixed thresholds as optional heuristics unless backed by account-specific evidence.
5. Preserve this repository's `Read-only / Suggest / Shadow / Execute` safety model.
6. Put detailed reusable knowledge in references/playbooks so Skills load progressively.
7. Keep canonical business logic tool-agnostic where possible; put runtime compatibility in manifests/adapters rather than duplicated Skills.
8. Record important reviewed sources here when they materially influence the project.
