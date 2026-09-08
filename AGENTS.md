# AGENTS.md

## Repository purpose

This repository contains reusable Amazon Ads Agent Skills. The canonical business logic lives under `skills/<skill-name>/SKILL.md` and must remain portable across Codex, Claude Code, WorkBuddy, and other Agent Skills-compatible runtimes.

## Skill discovery

- Treat every `skills/*/SKILL.md` as an independently invocable skill.
- Read only the matching skill first; load shared files from `references/`, `playbooks/` and `schemas/` only when needed.
- For cross-domain requests, use `skills/amazon-ads-optimizer/SKILL.md` as the orchestrator.
- For recurring weekly/Monday account reviews, start with `playbooks/weekly-review.md`, then load only specialist Skills required by material findings.
- When the task asks whether a previous optimization worked, route to `skills/post-change-review/SKILL.md` before proposing another edit on the same entity.
- When prior actions may overlap a new decision, load `references/optimization-memory.md` and retrieve only the bounded relevant entity history.
- Historical replay fixtures under `evals/` are test inputs, not reusable operating instructions; do not load them during ordinary account analysis unless explicitly running an eval.
- Do not duplicate business logic into this file.

## Default operating mode

Default to `Suggest` mode. Analysis may propose actions, but no skill or playbook in this repository directly modifies a live Amazon Ads account.

Modes:
1. `Read-only` — inspect and explain data.
2. `Suggest` — generate recommended actions without applying them. **Default.**
3. `Shadow` — simulate actions for review/backtesting.
4. `Execute` — only after explicit authorization; hand validated actions to an external connector/executor.

## Safety rules

- Never invent missing advertising data or missing optimization history.
- Do not recommend aggressive bid/budget changes when sample size is insufficient.
- Check marketplace, currency, timezone, attribution window, date range, promotion context, and data freshness before high-confidence recommendations.
- Treat Prime Day, Best Deal, Lightning Deal, Coupon, Prime-exclusive promotions, stockouts, listing suppression, and major price changes as confounders.
- Before reversing or stacking another action on the same entity, check whether a recent action is still inside its validation window when history is available.
- Distinguish `proposed`, `applied`, `readback confirmed`, and `worked`; none of these imply the next stage automatically.
- If history is unavailable or partial, expose that limitation instead of treating the ledger as complete.
- Prefer `Hold`, `Experiment Only`, or `Manual Review` when application is unknown/drifted, evaluation is still pending, or a new action would contaminate an active experiment unless a safety guardrail triggered.
- Weekly reviews must include a hold list; do not force every material entity into an action.
- Do not place credentials, refresh tokens, client secrets, profile IDs, account IDs, or customer secrets in generated files or logs.
- Any `Execute` plan must include evidence, confidence, guardrails, validation window, and rollback criteria.
- A `Rollback Candidate` is a proposal only; this repository does not perform the rollback itself.

## Shared references, playbooks and evals

- Weekly operating cadence: `playbooks/weekly-review.md`
- Metrics: `references/amazon-ads-metrics.md`
- Optimization framework: `references/optimization-framework.md`
- Decision boundaries: `references/decision-boundaries.md`
- Benchmark policy: `references/benchmark-policy.md`
- Optimization memory: `references/optimization-memory.md`
- Canonical data model: `references/data-schema.md`
- Action proposal schema: `schemas/optimization-action.json`
- Action/readback/evaluation event schema: `schemas/optimization-event.json`
- Derived entity-history schema: `schemas/entity-history.json`
- Experiment plan schema: `schemas/experiment-plan.json`
- Historical replay framework: `evals/README.md`
- Eval-case schema: `schemas/eval-case.json`

## Evaluation rules

When adding or changing decision logic, prefer adding a focused synthetic replay fixture for material failure modes.

- Keep contract checks separate from capability evals.
- Score decision behavior rather than exact prose.
- Use `met`, `not_met`, or `insufficient_evidence`; do not coerce missing evidence into pass/fail.
- A fixture may allow multiple conservative outcomes, but must list forbidden unsafe behaviors explicitly.
- Do not weaken a fixture merely because a current model fails it; change the Skill only when the fixture represents the intended behavior.
- Prefer synthetic identifiers and values. Never commit client/account secrets or proprietary exports as fixtures.
- Eval fixtures must remain closed-world by default and must not trigger live Amazon Ads writes.

## Contribution rules

New skills must:
- use kebab-case directory names;
- include YAML frontmatter with at least `name` and `description`;
- keep the core `SKILL.md` concise and progressively load shared references;
- state required inputs, workflow, output contract, safety checks, and stop conditions;
- output proposals rather than performing live account mutation.

Add a playbook instead of a new Skill when the new material is primarily a recurring operating rhythm that composes existing Skills rather than a distinct decision capability.

Shared memory/history features should prefer append-first events plus derived compact summaries rather than mutable prose logs.

When a change materially affects negatives, bid/budget reversals, Mixed-ASIN safety, growth qualification, experiments, readback, or rollback decisions, add or update a replay fixture when practical.
