# Contributing

Thanks for contributing to Amazon Ads Skills.

This is a public repository. External contributors should work through a fork or feature branch and submit a pull request into `main`.

## Contribution flow

```text
fork / feature branch
→ make a focused change
→ add or update deterministic tests when behavior changes
→ run repository validation
→ open a pull request against main
→ review / CI
→ maintainer merge
```

Do not commit directly to `main`.

## Before opening a pull request

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

For behavioral changes, prefer RED → GREEN:

1. add a deterministic test or eval that proves the old behavior is insufficient;
2. confirm the regression fails for the intended reason;
3. implement the smallest useful change;
4. rerun unit tests, Skill validation and eval validation;
5. document external sources and license/adoption boundaries when relevant.

## Scope and safety

Contributions should preserve these repository invariants:

- default to Read-only / Suggest / Shadow;
- no live Amazon Ads mutations from this repository;
- missing data, unsupported connector capability, absent report rows and unavailable history are not zero;
- preserve marketplace/profile/account identity, source lineage, reporting generation, metric semantics and attribution semantics when they affect a decision;
- keep executor writes, credentials, retries, idempotency and reconciliation in an external authorized Connector / Executor;
- do not copy third-party prompts, schemas, workflows, templates or protected implementation unless the license and scope explicitly permit reuse.

## Skill design

Prefer strengthening the existing 15 Skills.

Before adding a new Skill, check whether the change belongs in:

- an existing `skills/<name>/SKILL.md`;
- a skill-local or shared `references/` file;
- `playbooks/`;
- `schemas/`;
- `scripts/`;
- `tests/` or `evals/`.

Keep Skill entrypoints compact and use progressive loading.

## Pull request expectations

A pull request should explain:

- the problem or decision gap;
- what changed;
- why the change is not duplicative;
- tests or eval evidence;
- external sources used, including license/copyright handling;
- whether any behavior, schema or safety contract changed.

Maintainers may request changes or decline contributions that add duplicated Skills, unsupported Amazon Ads claims, unsafe write behavior, fixed thresholds without evidence, or unnecessary framework dependencies.

## Repository ownership

`main` is the protected integration branch and should be updated only through reviewed pull requests.

Repository maintainers remain responsible for merging accepted changes. CODEOWNERS is defined in `.github/CODEOWNERS`.
