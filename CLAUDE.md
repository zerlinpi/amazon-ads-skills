# CLAUDE.md

This repository is an Amazon Ads Agent Skills library. Use the canonical skill definitions in `skills/*/SKILL.md`; do not fork or duplicate their business rules into Claude-specific copies.

## How to work with this repository

1. Match the user intent to one skill under `skills/`.
2. Read that skill's `SKILL.md` first.
3. Load `references/` or `schemas/` only when the skill asks for them or the task requires exact definitions.
4. Use `skills/amazon-ads-optimizer/SKILL.md` when the request spans multiple optimization domains.
5. Default to `Suggest` mode unless the user explicitly requests another mode and an external executor is available.

## Non-negotiable safety

- Skills in this repository do not directly mutate live Amazon Ads accounts.
- `Execute` means producing a validated action payload for an external connector/executor after explicit authorization.
- Never fabricate missing metrics or silently mix marketplaces, currencies, timezones, attribution windows, or date ranges.
- Detect promotional periods and operational confounders before interpreting short-term performance changes.
- Never expose secrets or authentication material.

See `AGENTS.md` for repository-wide conventions and `references/decision-boundaries.md` for execution guardrails.
