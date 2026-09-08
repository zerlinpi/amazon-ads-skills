# Weekly Amazon Ads Review Playbook

Use this playbook for recurring weekly account reviews. It is an operating rhythm, not a universal threshold sheet and not a replacement for the specialized Skills.

Default mode: `Suggest`. Use `Shadow` when simulating candidate changes. Live mutations remain external and separately authorized.

## Purpose

A weekly review should answer five questions in order:

1. Did the business materially improve, decline or stay within expected variation?
2. Which ASINs, campaigns, queries, targets or placements explain the movement?
3. Are any recent optimization actions still pending evaluation or producing side effects?
4. Where is there action-safe waste, recovery work or profitable growth headroom?
5. What should be changed, held, tested or monitored before the next review?

Do not turn the review into a list of every metric that moved.

## Progressive loading

Start with this playbook and the smallest useful data slice. Load specialized Skills only when a weekly finding requires them:

- sustained decline → `skills/performance-drop-diagnosis/SKILL.md`
- unexplained alert → `skills/anomaly-detection/SKILL.md`
- growth headroom → `skills/growth-opportunity-finder/SKILL.md`
- search-term harvest or query quality → `skills/search-term-analysis/SKILL.md`
- bid / budget / placement / negative decision → the corresponding optimization Skill
- unproven but testable hypothesis → `skills/experiment-planner/SKILL.md`
- recently changed entity → `skills/post-change-review/SKILL.md`
- current profitability ambiguity → `skills/profitability-analysis/SKILL.md`

When history exists, also load only the bounded relevant slice from `references/optimization-memory.md`.

## 1. Review-window gate

Use complete, comparable windows whenever possible.

Record:

- current review start/end;
- comparison start/end;
- marketplace, currency and timezone;
- attribution maturity by ad type/source;
- major promotion or retail events;
- data freshness and reconciliation warnings.

Prefer same-length completed periods. If the current period is attribution-immature, separate operational delivery signals from mature conversion conclusions.

Do not compare a partial current day/week directly against a completed historical period without normalization and a clear warning.

## 2. Business-first scorecard

Review business outcomes before campaign tuning.

Use available metrics such as:

- total sales and orders;
- ad-attributed sales and orders;
- spend;
- contribution profit or contribution margin when available;
- TACOS when total retail sales are available;
- ACOS / ROAS;
- impressions, clicks, CTR and CPC;
- CVR;
- AOV / ASP;
- organic order or sales share when the source supports it;
- BSR/rank only when dated and sufficiently reliable.

For every material movement distinguish:

`fact -> observation -> possible driver -> required drilldown`

Do not classify an account as healthy or unhealthy from a broad industry benchmark alone. Use `references/benchmark-policy.md` when external benchmarks are discussed.

## 3. Change-memory checkpoint

Before interpreting weekly movement, review recent actions that overlap the current window.

For affected entities check:

- latest proposed/applied action;
- readback status;
- validation-window maturity;
- active experiment status;
- rollback candidate or safety trigger;
- concurrent parent/child or cross-control changes;
- memory completeness/freshness warnings.

Classify each relevant recent action as:

- `Pending Evaluation`
- `Worked / Keep`
- `Monitoring`
- `Inconclusive`
- `Rollback Candidate`
- `Application Unknown`
- `Drifted`

Do not stack another opposite change on an entity merely because one immature week looks worse.

## 4. Contribution triage

Rank issues and opportunities by business contribution, not by visually extreme ratios.

Recommended ordering:

1. lost or gained sales/orders per day;
2. profit impact when known;
3. share of account/ASIN movement;
4. strategic importance;
5. evidence quality and actionability.

A low-volume target with a terrible ACOS should not automatically outrank a high-volume previous winner that lost material qualified traffic.

Suggested triage states:

- `Protect` — serving, inventory, listing, Buy Box / Featured Offer, dangerous spend or rollback condition;
- `Recover` — material prior winner or ASIN lost qualified traffic/conversion;
- `Optimize` — meaningful but non-critical efficiency issue;
- `Grow` — profitable winner with validated headroom;
- `Experiment` — plausible opportunity with insufficient causal evidence;
- `Hold` — not mature, contaminated, strategically protected or too uncertain.

These states are relative to account objectives and evidence, not fixed ACOS bands.

## 5. Campaign and ASIN review

For material campaigns and advertised ASINs inspect, when available:

- spend, sales, orders and contribution;
- traffic and conversion bridge;
- budget delivery / pacing;
- query and placement mix;
- advertised vs purchased ASIN distribution;
- inventory, offer status, price, promotion and listing readiness;
- recent bid/budget/placement/negative/state changes;
- Mixed-ASIN and halo risk.

Escalate a sustained business-impact decline to `performance-drop-diagnosis` instead of trying to solve the root cause inside the weekly checklist.

## 6. Search-term and target review

Separate at least four cases:

### Proven query/target winner

Candidate for harvesting, structure improvement or controlled scaling only when conversion quality, economics and attribution are sufficiently reliable.

### New waste

A currently expensive non-converting route may be a negative/bid candidate, but first check multiple windows, attribution maturity, previous conversion history and Mixed-ASIN/halo exposure.

### Previous winner stopped converting

Treat as a diagnostic problem, not an automatic negative. Check retail readiness, query/placement mix and recent control changes.

### Discovery / low-evidence traffic

Keep, cap, test or observe according to objective and economics. Do not force a binary keep/negate decision when evidence is weak.

## 7. Budget, bid and placement review

Use marginal evidence rather than fixed weekly percentage adjustments.

Ask:

- is the campaign actually constrained by budget or auction competitiveness?
- does extra spend have evidence of incremental profitable demand?
- would more budget merely buy the same low-quality traffic?
- is CPC movement caused by auction pressure, placement mix or bid/control changes?
- are placement returns sufficiently stable and attributable?
- is a recent adjustment still inside its validation window?

Route action-level decisions to the corresponding Skill. Weekly review should identify the decision, not duplicate all optimization logic.

## 8. Retail and event confounders

Before attributing weekly changes to PPC, check relevant dated context:

- stockout / low inventory;
- Featured Offer / Buy Box loss;
- price change;
- coupon/deal/promotion start or end;
- listing suppression or content disruption;
- delivery promise changes;
- review/rating shock;
- parent/child variation changes;
- major seasonality or marketplace event;
- known competitor price/promotion/availability movement when reliable data exists.

A current snapshot cannot prove what happened earlier in the week without dated evidence.

## 9. Weekly action packet

Deduplicate findings into one prioritized packet.

### P0 — protect data and commerce

Examples: broken data, listing suppression, unbuyable ASIN, severe inventory risk, lost Featured Offer / Buy Box, dangerous spend or triggered rollback guardrail.

### P1 — recover material loss / stop action-safe waste

Only when causal and scope evidence is strong enough.

### P2 — improve efficiency

Bid, query, placement, budget or structure improvements that are meaningful but not urgent.

### P3 — grow validated winners

Use growth headroom and economics, not low ACOS alone.

### P4 — experiment / structural work

Test uncertain hypotheses or plan larger redesigns separately so they do not contaminate routine tuning.

Every proposed action should include:

- entity;
- current state when available;
- proposed action;
- evidence;
- expected mechanism;
- confidence;
- mode (`Suggest` or `Shadow` by default);
- validation window;
- rollback / stop condition;
- history or experiment dependency.

## 10. Hold list

Explicitly record what should **not** change this week and why.

Common reasons:

- attribution not mature;
- previous action still pending evaluation;
- active experiment;
- Mixed-ASIN ambiguity;
- low sample / unstable signal;
- event-dependent performance;
- retail-readiness blocker;
- strategically protected brand/defense traffic;
- conflicting evidence.

A useful weekly review contains holds, not just actions.

## 11. Next-review contract

End with a compact measurement plan:

- metrics to watch;
- entities to revisit;
- expected mechanism;
- earliest decision-useful date/window;
- required readback/history updates;
- experiment or rollback checkpoints.

Persist new proposed/applied/readback/evaluation events using the repository event/history contracts when the surrounding system supports them.

## Output template

### Weekly verdict

3-6 bullets covering business direction, main driver, biggest risk, biggest action-safe opportunity and major uncertainty.

### Data and attribution gate

Exact windows, freshness, maturity, confounders and missing data.

### Business scorecard

Current vs comparable period with absolute and relative movement where useful.

### Protect / Recover / Optimize / Grow / Experiment / Hold

Ranked findings with contribution and confidence.

### Recent-action review

Pending, worked, inconclusive, drifted or rollback-candidate actions affecting this week's interpretation.

### Prioritized action packet

P0-P4 actions with guardrails and validation plans.

### Hold list

Entities intentionally unchanged.

### Next review

What must be re-read or measured before the next decision.

## Prohibited shortcuts

- Do not use fixed universal ACOS, CTR, CVR, click, order or spend thresholds to color campaigns red/yellow/green.
- Do not automatically increase budget because it exhausted.
- Do not automatically negate a zero-order query without scope/history checks.
- Do not judge a fresh optimization before its decision window is mature.
- Do not treat attributed sales movement as proof of incrementality.
- Do not mix promotion weeks with normal weeks without labeling the comparison.
- Do not claim a live account action was applied unless an external executor and readback support it.
