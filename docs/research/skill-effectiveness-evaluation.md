# Agent Skill effectiveness evaluation research

Reviewed: 2026-09-10

This note records public open-source evaluation ideas used to improve how this repository decides whether a Skill is actually useful, not merely well-formed. No third-party harness code, test schema, prompts, evaluator implementation, or long prose passages are copied.

## Public repositories reviewed

### tardigrde/agent-skill-eval

Repository:

- https://github.com/tardigrde/agent-skill-eval

License verified in the repository: MIT.

Generic ideas reviewed:

- evaluate Skills through real agent harnesses rather than only static file checks;
- compare runs with a Skill against a baseline where the Skill is unavailable;
- distinguish natural discovery/triggering from cases where the Skill is explicitly injected or forced;
- include should-not-trigger / negative-control cases to detect over-triggering;
- run repeated trials for stochastic agents and report pass-rate style summaries rather than relying on one favorable transcript;
- combine deterministic state/assertion checks with semantic judging where deterministic verification is insufficient;
- record token/time cost where useful.

Repository adaptation:

These ideas were independently rewritten into `evals/SKILL-EFFECTIVENESS.md` as a runtime-neutral protocol compatible with the repository's existing synthetic Amazon Ads fixtures. This repository does not adopt the source project's CLI, configuration schema, workspace implementation, provider adapters, grader prompts, or code.

### edonadei/caliper

Repository:

- https://github.com/edonadei/caliper

License verified in the repository: MIT.

Generic ideas reviewed:

- keep behavioral expectations stable while evaluating a Skill;
- use repeated trials when one stochastic run is not reliable evidence;
- use ablation to ask whether the Skill contributes incremental value;
- prefer deterministic assertions for mechanically verifiable outcomes.

Repository adaptation:

The repository uses these concepts only as methodology: hold task/harness/evidence constant between with-Skill and without-Skill arms, record actual trial count, and treat ablation as evidence of incremental Skill value rather than a replacement for Amazon Ads safety regression fixtures. No Caliper source code, schemas, command syntax or evaluator implementation is copied.

## Why this is high value

The repository already had two strong layers:

1. deterministic package/fixture validation;
2. capability replay against synthetic Amazon Ads safety cases.

Those layers can show that a Skill is valid and that the current agent can behave safely with it. They do not answer whether the Skill itself makes the agent better than a reasonable baseline, whether natural Skill discovery works, or whether the Skill over-triggers on adjacent tasks.

The additional evaluation layer therefore asks:

```text
Does the Skill add incremental decision value?
Does it trigger when needed?
Does it stay out of the way when not needed?
Is the improvement repeatable enough to justify the context/token cost?
```

## Adoption and safety boundary

The adaptation remains vendor/runtime neutral. Codex, Claude Code, WorkBuddy or another Agent Skills runtime may be used as an evaluation harness, but the business fixture and verifier contract remain repository-owned.

Effectiveness evaluation must use closed-world fixtures, read-only data, synthetic state, disposable workspaces or Shadow simulation. It does not authorize live Amazon Ads writes and does not require production advertiser credentials.


## 2026-09-19 measurement-status review

### open-multi-agent/open-multi-agent

Repository: https://github.com/open-multi-agent/open-multi-agent

License verified from repository metadata: MIT. Fresh review observed roughly 6.9k stars and active maintenance; stars are discovery context only.

High-value generic finding: evaluation infrastructure failures are not measured quality. Its evaluation design records scorer failures separately and excludes them from score aggregates rather than coercing them to zero. It also versions scorer definitions so measurement-logic drift can be distinguished from target behavior drift.

Repository adaptation in this project is narrower and independently authored:

- paired Skill-effectiveness trials gain an explicit measurement-status vocabulary;
- existing records with no status remain backward-compatible as `measured`;
- non-measured trials preserve decision booleans as null rather than invented false values;
- if either arm of a with-Skill/without-Skill pair is not measured, the entire pair is excluded from the effectiveness delta;
- an evaluation with no comparable measured pairs reports `Insufficient Evidence`, not zero effectiveness.

No Open Multi Agent TypeScript, scorer implementation, schema, prompt, storage layer, workflow, or documentation prose is copied.


## 2026-09-19 measurement-provenance review

### benchflow-ai/skillsbench

Repository: https://github.com/benchflow-ai/skillsbench

Fresh GitHub metadata during this review showed roughly 1.8k stars, Apache-2.0 licensing, a non-fork repository, tests/CI, and a versioned benchmark registry. Its dataset-versioning documentation namespaces results by dataset version and pins published benchmark sets to git tags/commits; task content is also tied to content digests.

Adoption: method-level only. This repository independently applies the narrower principle that an effectiveness trend is meaningful only when the fixture and evaluator/rubric measurement contract are version-identical. No SkillsBench task packages, verifier/oracle implementation, registry schema, benchmark scripts, prompts, leaderboard code, or prose are copied.

### open-multi-agent/open-multi-agent follow-up

The prior review already adopted its fail-honest scorer-error principle. A fresh code search also confirmed explicit scorer versions and run metadata such as prompt-version labels. The additional generic lesson is that measurement logic itself is part of result provenance, not an invisible implementation detail.

Adoption: independently authored `fixture_version` plus `measurement_contract.evaluator_id/evaluator_version/rubric_version`, and a read-only comparability helper. No OMA scorer code, record schema, CLI, storage logic, prompts, or tests are copied.

### fitchmultz/agent-eval — low-star corroboration, MIT

Fresh review found a small but concrete TypeScript project with tests and machine-readable output bundles that carry engine/schema versions plus release/config provenance. Its adoption signal is low, so it is not load-bearing evidence.

Adoption: corroboration only; no code/schema/workflow reuse.
