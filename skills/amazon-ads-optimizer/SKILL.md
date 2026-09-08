---
name: amazon-ads-optimizer
description: Orchestrate Amazon Ads audit, monitoring, diagnosis, growth-opportunity, experiment planning, post-change review, search-term, keyword, bid, budget, placement, negative-targeting, profitability and anomaly skills into one memory-aware guarded action plan. Use for whole-account optimization, multi-domain analysis, recurring weekly reviews, or when the user does not know which Amazon Ads skill to choose.
---

# Amazon Ads Optimizer

Use this as the routing layer. Load only the selected child Skill, playbook and references needed for the current decision.

Default mode: `Suggest`. Use `Shadow` for simulation/backtesting. Never claim a live change succeeded unless an external connector/executor returned success and current state was read back when material.

## Route by intent

| Intent | Route |
|---|---|
| Recurring weekly / Monday PPC review, this week vs prior period | `../../playbooks/weekly-review.md` then only the required child Skills |
| Whole-account audit / account takeover | `amazon-ads-audit` |
| Routine campaign health / alerts | `campaign-health-monitor` |
| Sustained sales, orders, ROAS, ACOS or traffic decline; what dropped and why | `performance-drop-diagnosis` |
| Where to scale / which winners deserve more investment / growth headroom | `growth-opportunity-finder` |
| Promising but unproven optimization; design a controlled test | `experiment-planner` |
| Did a previous optimization actually apply/work; keep, monitor or rollback candidate | `post-change-review` |
| Search-term winners / harvesting / query quality | `search-term-analysis` |
| Keyword/target structure and lifecycle | `keyword-optimization` |
| Bid/CPC adjustment | `bid-optimization` |
| Budget, pacing, reallocation | `budget-optimization` |
| Top of Search / Product Pages / Rest of Search | `placement-optimization` |
| Negative keywords / negative product targeting | `negative-targeting` |
| Break-even ACOS / contribution profit / TACOS | `profitability-analysis` |
| Unexplained metric anomaly / monitoring signal | `anomaly-detection` |

## Routing rules

- For recurring weekly operating reviews, load `../../playbooks/weekly-review.md` first. It is a conductor playbook, not a replacement for specialist Skills.
- During a weekly review, escalate only material findings to the minimum specialist Skill needed; do not load every Skill preemptively.
- For a sustained business-impact decline, prefer `performance-drop-diagnosis` over a generic anomaly review.
- For an alert without a confirmed sustained decline, start with `anomaly-detection` or `campaign-health-monitor`.
- For “lower ACOS”, diagnose traffic quality, CPC, CVR, placement, budget, retail readiness and economics before routing to bid reduction.
- For “where can I grow?”, use `growth-opportunity-finder` before bid/budget tuning.
- If a growth or efficiency hypothesis is plausible but not action-safe, route to `experiment-planner` instead of pretending it is a proven optimization.
- Use `experiment-planner` when the user asks for an A/B test, holdout, phased rollout, switchback, test plan, success metric, guardrail or controlled validation.
- When the user asks whether a previous change worked, use `post-change-review` before proposing another edit on the same entity.
- Before a new control change, load `../../references/optimization-memory.md` when history is available or a recent action may overlap the entity/window.
- If the previous action is still pending evaluation, application is unknown/drifted, or a new action would contaminate an active experiment, prefer `Hold`, `Experiment Only` or `Manual Review` unless a safety guardrail has triggered.
- Load only the minimum child Skills required and only a bounded slice of relevant history.

## Shared checks

Before high-confidence recommendations confirm when relevant:

- marketplace, currency and timezone;
- exact date windows and attribution maturity;
- ad type and entity scope;
- business objective / target economics;
- promotion, price, inventory, Buy Box / Featured Offer and listing state;
- data freshness and sample sufficiency;
- mixed-ASIN / halo risk;
- recent actions, pending evaluations, active experiments or control changes affecting the same entity;
- memory freshness/completeness warnings when entity history is used.

Use `../../playbooks/weekly-review.md` for recurring weekly operating cadence.
Use `../../references/benchmark-policy.md` when external benchmarks affect a decision.
Use `../../references/optimization-memory.md` for read-before-recommend, anti-thrashing, staleness and event-lineage rules.
Use `../../references/decision-boundaries.md` for action permissions.
Use `../../schemas/experiment-plan.json` for structured experiment design.
Use `../../schemas/optimization-event.json` for action/readback/evaluation events.
Use `../../schemas/entity-history.json` for compact derived entity-history views.

## Conflict resolution

If Skills propose incompatible actions on the same entity:

1. fix data/serving/retail-readiness issues before tuning;
2. respect explicit business and profitability constraints;
3. inspect recent optimization events, current readback and unfinished validation windows;
4. when causal evidence is weak but testable, convert the conflict into a controlled experiment;
5. prefer protective, reversible and better-scoped actions;
6. if uncertainty remains, output `manual_review` / hold.

Invalid unresolved conflicts include increase+decrease on the same control, harvest+negate the same term, scaling structurally unprofitable traffic without an explicit strategic exception, or editing an entity again before the prior action is mature unless a safety guardrail triggered.

## Priority

1. **P0** data, serving, inventory, Buy Box / Featured Offer, listing or attribution failures.
2. **P1** material waste, dangerous control errors or triggered safety/rollback conditions.
3. **P2** efficiency repairs.
4. **P3** proven growth opportunities.
5. **P4** controlled experiments and structural redesigns.

## Output

Return executive summary, data confidence, routed findings, a deduplicated prioritized action plan, resolved/unresolved conflicts, hold/observe items, and the next validation point.

For weekly reviews, also return current/comparable windows, recent-action status, Protect/Recover/Optimize/Grow/Experiment/Hold triage, and the next-review measurement contract from `../../playbooks/weekly-review.md`.

When history materially changes a recommendation, also return history status, latest relevant action/readback, validation maturity, unresolved warnings and the event IDs supporting the decision when available.

Every actionable proposal should include entity, reason, evidence, confidence, mode, guardrails, validation window and rollback condition. Every experiment should additionally define a falsifiable hypothesis, comparison design, one primary metric, contamination risks and predeclared decision rules.
