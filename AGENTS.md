# AGENTS.md

## Repository purpose

This repository contains reusable Amazon Ads Agent Skills. The canonical business logic lives under `skills/<skill-name>/SKILL.md` and must remain portable across Codex, Claude Code, WorkBuddy, and other Agent Skills-compatible runtimes.

## Skill discovery

- Treat every `skills/*/SKILL.md` as an independently invocable skill.
- Read only the matching skill first; load shared files from `references/` and `schemas/` only when needed.
- For cross-domain requests, use `skills/amazon-ads-optimizer/SKILL.md` as the orchestrator.
- When the task asks whether a previous optimization worked, route to `skills/post-change-review/SKILL.md` before proposing another edit on the same entity.
- Do not duplicate business logic into this file.

## Default operating mode

Default to `Suggest` mode. Analysis may propose actions, but no skill in this repository directly modifies a live Amazon Ads account.

Modes:
1. `Read-only` — inspect and explain data.
2. `Suggest` — generate recommended actions without applying them. **Default.**
3. `Shadow` — simulate actions for review/backtesting.
4. `Execute` — only after explicit authorization; hand validated actions to an external connector/executor.

## Safety rules

- Never invent missing advertising data.
- Do not recommend aggressive bid/budget changes when sample size is insufficient.
- Check marketplace, currency, timezone, attribution window, date range, promotion context, and data freshness before high-confidence recommendations.
- Treat Prime Day, Best Deal, Lightning Deal, Coupon, Prime-exclusive promotions, stockouts, listing suppression, and major price changes as confounders.
- Before reversing or stacking another action on the same entity, check whether a recent action is still inside its validation window when history is available.
- Do not place credentials, refresh tokens, client secrets, profile IDs, account IDs, or customer secrets in generated files or logs.
- Any `Execute` plan must include evidence, confidence, guardrails, validation window, and rollback criteria.
- A `Rollback Candidate` is a proposal only; this repository does not perform the rollback itself.

## Shared references

- Metrics: `references/amazon-ads-metrics.md`
- Optimization framework: `references/optimization-framework.md`
- Decision boundaries: `references/decision-boundaries.md`
- Benchmark policy: `references/benchmark-policy.md`
- Canonical data model: `references/data-schema.md`
- Action proposal schema: `schemas/optimization-action.json`
- Action/readback/evaluation event schema: `schemas/optimization-event.json`

## Contribution rules

New skills must:
- use kebab-case directory names;
- include YAML frontmatter with at least `name` and `description`;
- keep the core `SKILL.md` concise and progressively load shared references;
- state required inputs, workflow, output contract, safety checks, and stop conditions;
- output proposals rather than performing live account mutation.
