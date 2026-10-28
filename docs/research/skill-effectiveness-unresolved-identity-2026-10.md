# Skill-effectiveness longitudinal placeholder identity integrity — 2026-10-28

## Reproducible gap

Initial main: `50252c16aa6a98eac0ff7a5a96d7ac31021b96c6` (v2.1.0), no open PR, latest main CI SUCCESS. The read-only `evaluate_skill_effectiveness_comparability.py` compared equal placeholder labels as literal identities. Two records with `harness.model_version = "Unknown"` (or repeated `Partial` config, `Missing` tools, `Unsupported` evidence, `Not Applicable` evaluator, `N/A` fixture, malformed booleans/lists, padded model names) returned `Comparable`. Equality of missing provenance cannot certify a longitudinal measurement baseline. The JSON Schema excludes malformed types, but the standalone comparator accepts JSON without schema validation, so its own fail-closed contract matters.

## RED → GREEN

- Test-only commit `2922986394c2450fbce96e9b850f7fa0e1dfaf83`: [RED Actions #40623018203](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40623018203) — 2192 tests, 12 expected FAIL, 4 new compatibility tests passed.
- Minimal predicate correction `b0e0012dd8e408f8eeb51c388981b055a6fbf149`: [GREEN Actions #40623079319](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40623079319) — 2192/2192 PASS; 15 Skill and 55 Eval validators PASS.
- Whole-label normalized placeholders, padding and non-string values are `Unknown`. Concrete opaque IDs containing words like `unknown` remain comparable; real version differences remain `Not Comparable`; explicitly null `rubric_version` remains comparable as a no-rubric declaration. No schema/Skill/dependency or Ads write added.

## Sources, adoption and limits

- Repository-owned contract: [Skill effectiveness evaluation](../skill-effectiveness-evaluation.md) and [eval protocol](../../evals/SKILL-EFFECTIVENESS.md) require identical versioned measurement provenance. The implementation is independently authored from observed test failures.
- [OpenLineage](https://github.com/OpenLineage/OpenLineage), Apache-2.0; [OpenEvals](https://github.com/langchain-ai/openevals), MIT; [SkillsBench](https://github.com/benchflow-ai/skillsbench), Apache-2.0. These already-reviewed projects reinforce lineage and reproducible evaluation at the abstract methodology level. No code/schema/prompts/workflows imported; full security and transitive license review not completed.
- [Amazon Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) distinguishes missing data from zero but does not define Skill benchmark semantics. Public Reddit/operator claims about agent effectiveness remain hypotheses.
- This only verifies internal declared identity comparability, not provenance authenticity, causal agent lift, statistical significance, complete Amazon Ads observations or live write authority. External authorized Executor owns all mutations.

## Next gap

P0: trusted external dataset/account/subscription/window binding and completeness; P1: event/readback version alignment; P2: repeated paired Skill-eval measurement provenance and outcome maturity. Avoid adding another framework without a new reproducible failure.
