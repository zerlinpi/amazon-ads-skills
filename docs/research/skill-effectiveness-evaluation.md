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
