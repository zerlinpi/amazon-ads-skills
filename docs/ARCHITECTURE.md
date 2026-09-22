# Architecture

## Runtime model

The canonical source is `skills/<name>/SKILL.md`. Codex, Claude Code and WorkBuddy entry files point to the same tree. Runtime manifests describe discovery/packaging only; they do not create an Amazon Ads connection.

## Progressive loading

Load metadata → one selected Skill → only decision-relevant references/schemas/playbooks/scripts. Do not preload all Skills or research notes for ordinary analysis.

## Evidence and connector layer

Connectors may be MCP servers, API wrappers, exports or warehouses. Before dependent interpretation, resolve required capability IDs and evaluate the active connector snapshot. Missing/partial/unsupported evidence remains unknown; it never becomes numeric zero or proof that a platform feature is absent.

High-confidence decisions may require source system, acquisition channel, reporting generation, metric semantics, date attribution, row eligibility, pagination/truncation, historical availability, freshness/backfill maturity, grain, marketplace/profile identity and control-state comparability. Repository-owned read-only helpers such as `scripts/compare_control_state.py` and `scripts/compare_measurement_composition.py` turn bounded evidence envelopes into fail-closed comparability classifications; they do not authorize writes or replace decision-specific reconciliation.

## Decision model

Keep `Observation → Hypothesis → Cause → Action → Outcome` distinct. Campaign objective is a separate context contract, not a result inferred from one performance ratio.

## Memory

Optimization history is append-first through `schemas/optimization-event.json`. Proposed, approved, applied, readback and evaluated states remain distinct. Derived history must not manufacture current state or missing semantics.

## Experiments

When causal evidence is weak but testable, use `experiment-planner` and `schemas/experiment-plan.json`. A ready experiment is ready for external execution review, not authorization for this repository to mutate Amazon Ads.

## Evaluation

Validation has three layers: deterministic repository contracts, synthetic capability/decision replay, and Skill-effectiveness evaluation. Behavioral changes should start with a RED regression and end with unit tests, Skill/eval validators and GitHub Actions evidence.

## Execution boundary

Default modes are `Read-only`, `Suggest`, and `Shadow`. `Execute` means a validated payload may be handed to a separately authorized external executor. Credentials, writes, retries, idempotency and reconciliation stay outside this repository.