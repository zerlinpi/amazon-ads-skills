# CLAUDE.md

This repository is an Amazon Ads Agent Skills library. Use the canonical skill definitions in `skills/*/SKILL.md`; do not fork or duplicate their business rules into Claude-specific copies.

For first-run installation, cloning, plugin/workspace choices, bootstrap prompts, and smoke tests, read `docs/GETTING-STARTED.md`. Prefer the whole repository as the workspace so `CLAUDE.md`, the canonical `skills/` tree, and shared references stay resolvable. If automatic Skill discovery fails, explicitly load the matching `skills/<name>/SKILL.md` instead of inventing a runtime-specific copy or path.

## How to work with this repository

1. Match the user intent to one skill under `skills/`.
2. Read that skill's `SKILL.md` first.
3. Load `references/` or `schemas/` only when the skill asks for them or the task requires exact definitions.
4. Use `skills/amazon-ads-optimizer/SKILL.md` when the request spans multiple optimization domains.
5. When compared windows come from different APIs, MCPs, exports, warehouses or report definitions, load `references/data-lineage.md` before high-confidence trend/causal conclusions.
6. When a conclusion depends on whether the active MCP/connector actually exposes the required scope, report, metric, history or semantic identity, load `references/connector-capability.md`; when a capability snapshot is available, run `scripts/evaluate_connector_capability_gate.py` before metric interpretation. Missing connector support is not a zero measurement.
7. When compact history needs decision-time measurement identity, use the read-only `scripts/project_measurement_history.py` projection contract rather than inventing lineage from current metrics.
8. When evaluating whether a Skill adds value, use `schemas/skill-effectiveness-benchmark.json` plus `scripts/summarize_skill_effectiveness.py` only for completed paired trial records; actual model/harness execution remains external.
9. Default to `Suggest` mode unless the user explicitly requests another mode and an external executor is available.

## Non-negotiable safety

- Skills in this repository do not directly mutate live Amazon Ads accounts.
- `Execute` means producing a validated action payload for an external connector/executor after explicit authorization.
- Never fabricate missing metrics, source lineage, or silently mix marketplaces, profile/account scopes, currencies, timezones, attribution windows, date ranges, or incompatible source definitions.
- Missing/retired historical reporting, unsupported connector fields, or absent report rows are not zero unless the source contract explicitly proves zero.
- Distinguish when data was fetched from which event dates are actually complete; `extracted_at` does not imply `available_through`.
- Detect promotional periods, operational confounders, and parent/variation-family retail changes before interpreting short-term child-ASIN performance changes.
- Effectiveness summaries do not call models, claim statistical significance, or authorize live advertising mutation.
- Never expose secrets or authentication material.

See `AGENTS.md` for repository-wide conventions, `docs/GETTING-STARTED.md` for runtime setup and prompts, `references/data-lineage.md` for cross-source evidence rules, `references/optimization-memory.md` for measurement-state memory, and `references/decision-boundaries.md` for execution guardrails.