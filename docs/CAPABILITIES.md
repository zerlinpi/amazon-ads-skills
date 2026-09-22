# Capability map

The repository keeps 15 canonical Skills. Choose by decision, not by how many files can be loaded.

| Decision | Skill | Key boundary |
|---|---|---|
| Account integrity and opportunity audit | `amazon-ads-audit` | prove scope/completeness before ranking the account |
| Multi-domain plan | `amazon-ads-optimizer` | route, deduplicate and resolve conflicts |
| Routine campaign status | `campaign-health-monitor` | monitoring is not root-cause proof |
| Unexpected movement | `anomaly-detection` | anomaly is not automatically a causal diagnosis |
| Sustained decline | `performance-drop-diagnosis` | separate observation, hypothesis and supported cause |
| Growth headroom | `growth-opportunity-finder` | economics + retail readiness + marginal headroom + binding control |
| Controlled test | `experiment-planner` | test uncertain causal claims rather than overstate them |
| Previous change review | `post-change-review` | application/readback + measurement/control comparability before outcome attribution |
| Search-term evidence | `search-term-analysis` | row eligibility/origin before literal-query actions |
| Keyword/target lifecycle | `keyword-optimization` | configured structure and traffic ownership |
| Negative decisions | `negative-targeting` | collateral-damage and scope protection |
| Bid decision | `bid-optimization` | causal control state + marginal evidence |
| Budget decision | `budget-optimization` | effective budget, upstream constraints and opportunity cost |
| Placement decision | `placement-optimization` | coupled bid/placement controls and comparable state |
| Economics | `profitability-analysis` | historical profitability does not certify scale |

## Campaign objective contract

Before role-specific optimization, resolve the campaign objective from explicit account/user metadata when available. Supported reasoning roles are `Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, and `Unknown`. `Unknown` is a valid safe state; do not manufacture a role from one ACOS/TACOS snapshot or campaign name alone.

See `references/campaign-objective.md` and `schemas/campaign-objective.json`.

## Composite workflows

Use `playbooks/weekly-review.md` for recurring reviews. A playbook coordinates Skills; it does not duplicate their specialist logic.