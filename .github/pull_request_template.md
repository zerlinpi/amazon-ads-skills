## What changed

<!-- Describe the focused change. -->

## Why

<!-- Describe the problem, gap, or failure mode this addresses. -->

## Evidence / tests

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python scripts/validate_skills.py .`
- [ ] `python scripts/validate_evals.py .`

For behavioral changes:

- [ ] A deterministic RED test/eval demonstrated the previous failure.
- [ ] The minimal GREEN implementation passes the relevant checks.

## Source / license review

<!-- List external sources used. Explain license/copyright handling and what was independently rewritten. -->

## Safety checklist

- [ ] No live Amazon Ads write authority was added.
- [ ] Missing/unsupported/unavailable evidence is not converted to zero.
- [ ] Scope, identity, metric semantics and attribution semantics are preserved where relevant.
- [ ] Executor credentials/retries/idempotency/reconciliation remain outside this repository.
- [ ] This change does not add a new Skill solely for catalog size.
