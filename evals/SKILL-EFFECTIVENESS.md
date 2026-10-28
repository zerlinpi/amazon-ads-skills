# Skill Effectiveness Evaluation

Use this protocol when the question is not only whether a Skill behaves safely on a known fixture, but whether the Skill **actually improves an agent's results** relative to a reasonable baseline and whether it is discovered at the right time.

This complements `evals/README.md` capability replay. It does not replace deterministic repository validation or the existing safety fixtures.

## 1. Three different questions

Keep these separate:

1. **Contract integrity** — can the Skill package and eval fixture be loaded and parsed correctly?
2. **Capability behavior** — given a bounded case, does the Skill produce an acceptable Amazon Ads decision and avoid forbidden behavior?
3. **Incremental Skill effectiveness** — under the same task/harness conditions, does having this Skill available improve useful outcomes compared with a `without-skill` baseline?

Passing the first two does not prove the third.

## 2. Evaluation modes

### Discovery

Run the natural task with the Skill installed/available but **not explicitly forced**.

Measure whether the runtime selects the Skill when it should and avoids loading it when it should not. Discovery tests should use realistic task wording rather than embedding the Skill name in every prompt.

Record when possible:

- expected Skill(s);
- Skill(s) actually loaded;
- whether the correct Skill was selected early enough to influence the decision;
- false-negative discovery;
- unnecessary/incorrect Skill loading.

### Forced invocation

Explicitly invoke or otherwise guarantee the target Skill is loaded, while keeping the task and evidence the same.

This isolates **instruction/method quality after activation** from discovery quality. If Forced invocation succeeds but Discovery fails, improve metadata/routing before expanding the Skill body.

### Negative control

Use adjacent tasks that should **not** activate the Skill or should not change the answer materially.

Examples:

- a generic arithmetic question should not load Amazon Ads optimization Skills;
- a campaign-level budget question without a population-coverage claim should not require `report-coverage.md` merely because reporting is mentioned;
- a read-only explanation should not become an Execute action because an optimization Skill is installed.

Negative controls detect over-triggering and unnecessary token/context cost.

### Ablation / without-skill baseline

Run the same fixture/task under the same model, harness, configuration and evidence, but without the target Skill available or injected.

The baseline may still use the model's general knowledge. This is intentional: the measurement asks whether the Skill adds incremental value over the underlying agent, not whether the agent knows nothing without it.

Useful comparisons include:

```text
with-skill decision-quality score
- without-skill decision-quality score

with-skill forbidden-behavior rate
vs
without-skill forbidden-behavior rate
```

Do not claim the Skill caused the delta if model/version, tools, prompt, fixture, temperature, source access or other material settings also changed.

## 3. Repeated stochastic runs

One successful run is weak evidence for an LLM-based Skill.

A harness/scorer failure is not a failed business decision. Record whether each trial was actually measured; scorer errors, harness errors, and insufficient-evidence trials must not be coerced into boolean quality outcomes or zero scores. For paired with-Skill/without-Skill deltas, exclude the entire pair when either arm is not measured so denominators remain comparable. Assign a unique `trial_id` to every actual execution across the entire benchmark, not merely within a pair: reusing a run in another pair or variant must be rejected, including scorer/harness-error arms. A distinct declared ID is necessary but does not independently prove a distinct model execution. Optional resource measurements must also preserve their actual types and values: supplied `tokens` must be a non-negative integer and `latency_ms` a finite non-negative number. Reject invalid negative, boolean, fractional-token, string or non-finite values even on excluded trials; missing and explicit null remain unmeasured, never zero. This is internal validation, not proof that a declared harness run actually happened.

Trigger/discovery telemetry is optional, but when a trial supplies non-null `triggered` it must be a boolean even if the pair is excluded from effectiveness deltas. Reject malformed supplied strings, numbers, arrays or placeholders instead of silently omitting them. Missing and explicit null mean trigger status was not measured; they must not be treated as false or zero. Read `trigger_rate` together with `trigger_observed_count`, `trigger_observation_coverage`, `trigger_observation_status`, and `trial_count`: the rate denominator is the number of actual boolean trigger observations within comparable measured pairs, which can be smaller than the comparable trial count. `complete` means every comparable trial had a boolean observation; `partial` means some but not all did; `unmeasured` means none did. A 100% rate from one observed trigger is not 100% population coverage. No external harness authenticity or statistical lift is implied.

Before producing a measured paired summary, validate the required benchmark, Skill, fixture, mode, runtime, model and evaluator identities. Whole-label unresolved placeholders, padded or malformed identity strings and invalid modes are not measured provenance; optional config/tool/evidence hashes may be omitted or null but supplied non-null values must be concrete. An explicitly null rubric is a valid declaration that no rubric was used. These checks do not authenticate the external harness or guarantee independent executions.

After the task and verifier are stable, run repeated trials when the runtime is stochastic and record the actual number of trials `k`. Do not impose one repository-wide fixed `k`; choose enough repetitions for the decision being made and report the count transparently.

Useful summaries include:

- full-pass rate across trials;
- forbidden-behavior rate;
- trigger/discovery rate;
- `pass@k` when the question is whether at least one of `k` attempts succeeds;
- median/mean token usage and latency when available;
- variance or run-to-run instability.

Do not present `pass@k`, small-sample percentage differences, or a single positive delta as statistical significance unless an appropriate statistical design actually supports that claim.

## 4. Deterministic assertions first

Prefer deterministic evidence for facts that can be checked mechanically:

- selected Skill name;
- output decision enum;
- forbidden action absent/present;
- required field/reference present;
- generated file/state diff;
- synthetic account mutation absent;
- expected source/evidence identifier cited;
- no real Amazon Ads write attempted.

Use model/judge rubrics only for semantic qualities that cannot be reliably reduced to deterministic assertions, such as diagnosis quality or whether evidence supports the stated causal interpretation.

A judge should not override a deterministic safety violation.

## 5. Pair effectiveness cases with existing fixtures

Prefer reusing `evals/fixtures/*.json` as the closed-world decision case where possible.

A practical progression is:

```text
existing regression fixture
→ Forced invocation replay
→ Discovery replay
→ without-skill ablation
→ repeated trials if the result matters enough
```

This keeps the business case stable while changing only the Skill availability/routing condition.

Do not create a second near-duplicate fixture merely to run the ablation unless the existing fixture lacks the inputs needed for a fair comparison.

## 6. What to score

A Skill should improve the outcomes the repository actually cares about, not just produce longer or more specialized prose.

Recommended dimensions:

- decision lands in `acceptable_decisions`;
- forbidden behaviors avoided;
- required observations surfaced;
- data/scope/lineage uncertainty handled correctly;
- action is no more aggressive than evidence supports;
- output remains useful: clear Act / Hold / Experiment / Manual Review and next measurement;
- correct Skill discovery and low false-positive triggering;
- token/context cost is proportionate to the improvement.

A Skill is not automatically beneficial if it improves one rubric score but materially raises unsafe actions, false triggering or context cost.

## 7. Harness parity

For a with-skill / without-skill comparison, hold constant as much as possible. Every persisted benchmark must also version its fixture and measurement contract so a later trend does not silently combine different verifier/rubric logic:

- model/provider/version;
- agent runtime and system instructions;
- tool availability and permissions;
- task prompt and synthetic evidence;
- temperature/reasoning settings when configurable;
- external source access;
- starting filesystem/workspace state;
- fixture version;
- evaluator/verifier ID and version;
- rubric version, or explicit null when no semantic rubric is used (null means not applicable, not unknown).

Record unavoidable differences. Before comparing benchmark records longitudinally, use `../scripts/evaluate_skill_effectiveness_comparability.py` when available. A concrete mismatch is `Not Comparable`; missing, explicitly unresolved (whole-label Unknown/Partial/Missing/Unsupported/Not Applicable/N/A), padded, or malformed non-string fixture/model/harness/tool/evidence/evaluator identity is `Unknown`, never silently comparable. Explicit null `rubric_version` remains the valid no-rubric declaration; a string placeholder is not equivalent to null. If the runtime automatically changes context/tool behavior when Skills are installed, treat that as part of the tested system but disclose it.

## 8. Scratch and execution safety

Effectiveness evals must not require real Amazon Ads mutation.

Use one of:

- closed-world fixture replay;
- read-only data;
- synthetic account state;
- disposable/scratch workspace;
- Shadow simulation.

If a harness supports tools capable of external writes, deny or stub those writes for evals unless the target is an explicitly isolated synthetic test system. The repository's `Read-only / Suggest / Shadow / Execute` boundary still applies.

Never use production credentials, refresh tokens, customer identifiers, or a live advertiser account merely to prove a Skill works.

## 9. Interpreting failure patterns

### Discovery fails, Forced invocation passes

Likely routing/metadata problem. Improve `name`, `description`, task cues or orchestrator routing before adding more domain prose.

### Discovery passes, Forced invocation also fails

Likely Skill-method or evidence-contract problem. Inspect the Skill/reference/playbook logic and regression fixture.

### With-skill ~= without-skill

The Skill may be redundant, too generic, not being used, or the task may already be easy for the base model. Do not expand it just to create differentiation.

### With-skill is worse

Treat this as a regression. Possible causes include over-triggering, anchoring on a weak heuristic, excessive context, contradictory references, unsafe precision or degraded task routing.

### High variance

Do not call the Skill reliable from a good-looking best run. Increase repetitions, simplify the protocol, strengthen deterministic checks or narrow the Skill's responsibility.

## 10. Minimal result record

For each evaluated Skill/task pair, record when available:

```text
skill
fixture/task id
harness + model/version
mode: Discovery | Forced invocation | Negative control | Ablation
with-skill / without-skill
trial count k
measurement status: measured | insufficient_evidence | scorer_error | harness_error
trigger result
acceptable decision result
forbidden behaviors
required observations
rubric result
tokens / latency
notes on tool/source parity
```

Keep raw transcripts/results outside normal Skill loading paths. Summaries can live in evaluation artifacts or CI outputs rather than bloating `SKILL.md`.

## 11. Promotion gate for new or materially changed Skills

Before claiming a new Skill or major rewrite is effective, prefer evidence that shows at least:

1. deterministic package/fixture validation is clean;
2. the relevant regression/capability cases still pass;
3. Forced invocation produces the intended method on representative cases;
4. Discovery selects the Skill on positive cases;
5. Negative control does not cause obvious over-triggering;
6. a `without-skill` comparison is available for important changes, or the reason it is not meaningful is documented;
7. repeated runs are used when stochastic reliability materially affects the claim.

This is an evidence standard, not permission to weaken existing safety gates to improve a pass rate.

## 12. Source/adaptation note

This protocol independently adapts generic ideas from public agent-Skill evaluation tooling, especially:

- with-Skill vs without-Skill ablation;
- Discovery vs Forced invocation separation;
- negative trigger controls;
- repeated stochastic trials / pass-rate reporting;
- deterministic state assertions before semantic judging.

See `docs/research/skill-effectiveness-evaluation.md` for sources and license notes. No third-party harness implementation, test schema, prompts or evaluator code is copied here.
