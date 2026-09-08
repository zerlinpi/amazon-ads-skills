# CLAUDE.md

This repository is an Amazon Ads Agent Skills library. Use the canonical skill definitions in `skills/*/SKILL.md`; do not fork or duplicate their business rules into Claude-specific copies.

## How to work with this repository

1. Match the user intent to one skill under `skills/`.
2. Read that skill's `SKILL.md` first.
3. Load `references/` or `schemas/` only when the skill asks for them or the task requires exact definitions.
4. Use `skills/amazon-ads-optimizer/SKILL.md` when the request spans multiple optimization domains.
5. When compared windows come from different APIs, MCPs, exports, warehouses or report definitions, load `references/data-lineage.md` before high-confidence trend/causal conclusions.
6. Default to `Suggest` mode unless the user explicitly requests another mode and an external executor is available.

## Non-negotiable safety

- Skills in this repository do not directly mutate live Amazon Ads accounts.
- `Execute` means producing a validated action payload for an external connector/executor after explicit authorization.
- Never fabricate missing metrics, source lineage, or silently mix marketplaces, profile/account scopes, currencies, timezones, attribution windows, date ranges, or incompatible source definitions.
- Distinguish when data was fetched from which event dates are actually complete; `extracted_at` does not imply `available_through`.
- Detect promotional periods, operational confounders, and parent/variation-family retail changes before interpreting short-term child-ASIN performance changes.
- Never expose secrets or authentication material.

See `AGENTS.md` for repository-wide conventions, `references/data-lineage.md` for cross-source evidence rules, and `references/decision-boundaries.md` for execution guardrails.
