# Campaign objective

A campaign's mission changes how evidence should be interpreted. There is **no universal ACOS/TACOS threshold** that makes every campaign good or bad.

Supported reasoning roles:

- `Discovery` — learn query/target demand under explicit spend/economic guardrails.
- `Control` — stable, interpretable traffic ownership for proven targets/queries.
- `Growth` — pursue qualified incremental volume after retail/economic/headroom gates.
- `Profit` — prioritize contribution economics and marginal efficiency.
- `Defense` — protect strategically important branded/owned traffic with explicit cost guardrails.
- `Experiment` — isolate a falsifiable treatment with predeclared metrics/stop conditions.
- `Unknown` — objective is unresolved; keep role-specific recommendations conservative.

## Evidence hierarchy

Prefer explicit user/account strategy, structured campaign metadata or a documented operating plan. Campaign names and performance patterns may be supporting evidence but are not authoritative.

**Do not infer** a campaign objective solely from ACOS, TACOS, match type, campaign name, current rank, spend level, or a short performance window. If an inferred role is used for exploratory analysis, label `source=inferred`, state the evidence/confidence, and do not silently convert it into action authority.

## Metric interpretation

- A Discovery campaign may tolerate weaker short-run ACOS only when the exploration budget/stop conditions are explicit; exploration is not permission for unbounded loss.
- A Growth campaign needs marginal headroom and retail/economic readiness; low historical ACOS is not enough.
- A Profit campaign should be judged against contribution economics, not a generic industry ACOS benchmark.
- A Defense campaign can have strategic value that is not captured by direct-attributed ACOS alone, but that value must be explicit rather than assumed.
- An Experiment campaign is judged first on treatment/control integrity and the declared primary metric, not on opportunistic post-hoc KPI selection.

TACOS and organic sales/rank can provide business context when their source/semantics are comparable, but movement does not by itself prove advertising incrementality or ranking causation.

## Action contract

Preserve `campaign_objective` on optimization proposals/events when it materially affects the decision. If the objective is `Unknown`, prefer `Hold`, `Directional`, `Experiment`, or `Manual Review` over role-specific action claims that require a known mission.