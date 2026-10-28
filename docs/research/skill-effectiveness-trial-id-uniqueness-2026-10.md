# Global Skill-effectiveness trial execution identity — 2026-10-28

## Verified gap

Initial main `c991f838025825d7e26a03cc0a96409f0763ec2f` (v2.2.0), zero open PRs and latest main `validate` SUCCESS. The read-only summarizer checked duplicate variants only inside one `pair_id`. Two pairs could reference the same `trial_id`, and both would be counted in `pair_count`/`comparable_pair_count` and effectiveness deltas. A duplicate can also span opposite variants or an excluded scorer/harness-error arm. No live account incident or real model-run collision is asserted; synthetic metadata reproduced the issue.

## Deterministic RED → GREEN

- Test-only `7f72057ef040c15e10515c50ae3e1c6197b5e394`: [RED Actions #40628820306](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40628820306) — 2202 tests, 7 expected FAIL (duplicate executions accepted), 3 new compatibility tests passed.
- Minimal fix `68938647643cb074ef475029cc1e8c7bba27604f`: [GREEN Actions #40628897528](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40628897528) — re-run unit, 15 Skills, 55 Evals; verify final run status before merge.
- Check global set of `trial_id` before counting any measured or non-measured trial. Preserve legitimate two-arm pairing and distinct-run exclusion semantics. No schema field, Skill, third-party dependency or live write.

## Source and license boundary

Repository-owned `evals/SKILL-EFFECTIVENESS.md` and `docs/research/skill-effectiveness-evaluation.md` already specify repeated paired trials and honest measurement statuses. OpenLineage (Apache-2.0), OpenEvals (MIT), and SkillsBench (Apache-2.0) reinforce provenance and repeated evaluation as abstract methodology, but their code, prompts, schemas, fixtures and workflows are not imported. Amazon Ads official API material governs ad data, not the repository's internal trial identity. Reddit practitioner anecdotes are not normative platform or statistically valid evidence.

## Limitations / next gap

Uniqueness of declared IDs cannot prove two differently named trials were actually independently executed. External harness must bind trial IDs to real execution records and stable model/tool/fixture provenance. Next priorities: external dataset/account/subscription/window binding, control event/readback version linkage, and genuine paired Skill-effectiveness repetitions. Read-only/Suggest/Shadow only; external authorized Executor owns all Ads writes.
