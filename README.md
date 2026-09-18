# Amazon Ads Skills

A portable **Amazon Ads decision library for AI agents**.

It packages 15 focused Agent Skills for account audit, monitoring, diagnosis, growth, experiments, post-change review, search terms, targeting, bids, budgets, placements, profitability and orchestration.

> 当前版本：`v1.0.0`  
> **Default mode:** `Suggest`  
> **Live Amazon Ads writes:** not performed by this repository  
> **Runtime model:** Agent Skills + progressive loading + read-only deterministic helpers  
> **Connector model:** external MCP / API / warehouse / export / executor

---

## What this repository is

Use this repository when an AI agent needs repeatable Amazon Ads reasoning instead of one-off prompting.

The core design is:

```text
evidence
→ scope / lineage / connector checks
→ diagnosis or opportunity
→ guarded recommendation
→ optional experiment / shadow
→ external execution only when explicitly authorized
→ readback
→ post-change review
→ append-first optimization memory
→ regression / effectiveness evaluation
```

The repository is intentionally **not** an Amazon Ads API client, credential store, write executor or autonomous campaign bot.

---

## Quick start

Clone the complete repository and open the **repository root** in your agent runtime:

```bash
git clone https://github.com/zerlinpi/amazon-ads-skills.git
cd amazon-ads-skills
```

Then validate the checkout:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

For first-time Codex, Claude Code, WorkBuddy and manual-loading setup, use:

**[docs/GETTING-STARTED.md](docs/GETTING-STARTED.md)**

A simple bootstrap instruction is:

```text
Read the repository instructions first.
Select the one Skill under skills/ that best matches my task.
State the selected Skill, operating mode and missing inputs.
Default to Suggest.
Do not guess missing data and do not perform live Amazon Ads writes.
```

If the request spans several optimization domains, start with:

```text
skills/amazon-ads-optimizer/SKILL.md
```

---

## The 15 Skills

| Area | Skill | Primary job |
|---|---|---|
| Account | `amazon-ads-audit` | Account-level integrity, waste, structure and opportunity review |
| Orchestration | `amazon-ads-optimizer` | Route multi-domain work and resolve overlapping recommendations |
| Monitoring | `campaign-health-monitor` | Routine campaign health and watchlist triage |
| Monitoring | `anomaly-detection` | Separate meaningful anomalies from normal variance/events |
| Diagnosis | `performance-drop-diagnosis` | Trace sustained performance declines to supported causes |
| Growth | `growth-opportunity-finder` | Find qualified headroom after economics and readiness gates |
| Experimentation | `experiment-planner` | Design guarded tests when direct action is not yet justified |
| Learning loop | `post-change-review` | Verify application, evaluate outcome and detect confounders |
| Search | `search-term-analysis` | Interpret Search Term evidence, winners and harvest candidates |
| Targeting | `keyword-optimization` | Keyword/target structure, lifecycle and traffic ownership |
| Targeting | `negative-targeting` | Guarded negative decisions with collateral-damage protection |
| Control | `bid-optimization` | Evidence-bounded bid/CPC recommendations |
| Control | `budget-optimization` | Pacing, budget constraints and marginal allocation |
| Control | `placement-optimization` | Placement performance and coupled-control reasoning |
| Economics | `profitability-analysis` | Break-even ACOS, contribution margin and profit-after-ads |

The repository deliberately keeps this catalog small. New composite workflows should usually become a playbook or reference rather than a new Skill.

---

## Progressive loading

The repository follows the Agent Skills model:

```text
skill metadata
→ one selected SKILL.md
→ only the references / schemas / scripts required by that decision
```

Do **not** load all 15 Skills or the full research tree into context for an ordinary task.

Typical paths:

```text
skills/<skill>/SKILL.md
skills/<skill>/references/*
references/*
schemas/*
playbooks/*
```

`evals/` is for evaluation and historical replay, not normal account analysis.

---

## Safety model

The default operating modes are:

| Mode | Meaning |
|---|---|
| `Read-only` | Inspect and explain evidence |
| `Suggest` | Produce guarded recommendations; **default** |
| `Shadow` | Simulate or backtest without live mutation |
| `Execute` | Produce a validated action payload for an explicitly authorized external executor |

`Execute` does **not** mean this repository directly changes Amazon Ads.

Credentials, OAuth/LWA handling, live writes, retry policy, idempotency enforcement, reconciliation workers and secret storage belong to an external Connector / Executor.

Key safety invariants:

```text
missing data ≠ 0
unsupported connector capability ≠ 0
report completed ≠ full logical population
executor success ≠ trusted current state
proposed ≠ applied ≠ readback confirmed ≠ worked
same metric label ≠ same measurement definition
same entity id across scopes ≠ same optimization identity
historical winner ≠ automatically action-safe now
```

See **[AGENTS.md](AGENTS.md)** and **[references/decision-boundaries.md](references/decision-boundaries.md)** for repository-wide rules.

---

## MCP / Connector capability layer

The Skills are connector-neutral. They can consume evidence from an MCP server, API wrapper, export, warehouse or other authorized source.

The connector path is explicitly gated:

```text
Skill + decision profile
→ scripts/resolve_skill_capabilities.py
→ canonical capability IDs
→ active connector capability snapshot
→ scripts/evaluate_connector_capability_gate.py
→ Pass / Degraded / Blocked
→ metric interpretation
```

Canonical capability IDs and Skill decision profiles live in:

- `references/connector-capability-catalog.json`
- `references/connector-capability.md`
- `schemas/connector-capability-snapshot.json`

Example:

```bash
echo '{"skill":"bid-optimization","profile":"action-safe-proposal"}' \
  | python scripts/resolve_skill_capabilities.py
```

The resolver does not call Amazon. It only returns repository-owned required/optional capability IDs.

When a connector snapshot is available:

```bash
echo '{"snapshot": {...}, "required_capabilities": [...]}' \
  | python scripts/evaluate_connector_capability_gate.py
```

A `Degraded` or `Blocked` result caps the dependent decision to conservative outcomes such as Directional, Hold, Alternate Source, Missing Data or Manual Review.

The capability system has a permanent rule:

```text
missing_evidence_policy = never_zero
```

---

## Data reliability

High-confidence recommendations require more than matching column names.

The repository checks evidence dimensions such as:

- source system and source dataset;
- acquisition channel;
- reporting generation;
- marketplace / advertiser / profile identity;
- date range, timezone and currency;
- metric and attribution semantics;
- row eligibility / represented population;
- pagination and truncation;
- historical availability;
- freshness and `available_through`;
- backfill maturity;
- aggregation grain and filters.

Use:

- **[references/data-lineage.md](references/data-lineage.md)** for cross-source / cross-version comparability;
- **[references/report-coverage.md](references/report-coverage.md)** for row-inclusion and logical-population questions;
- **[references/cross-account-identity.md](references/cross-account-identity.md)** for account/profile identity;
- **[references/platform-capability-lineage.md](references/platform-capability-lineage.md)** for time-varying Amazon platform behavior.

Current Amazon reporting changes and other platform research are recorded under **[docs/research/](docs/research/)** instead of being duplicated into this README.

---

## Optimization memory

The learning loop is append-first:

```text
schemas/optimization-event.json
→ bounded read-only projectors
→ schemas/entity-history.json
→ read-before-recommend
```

Important helpers:

- `scripts/project_measurement_history.py`
- `scripts/project_realization_history.py`

The event ledger remains authoritative. Derived history must not manufacture missing account identity, metric semantics, attribution family, historical availability or current state.

See **[references/optimization-memory.md](references/optimization-memory.md)**.

---

## Experiments

Use `experiment-planner` when a plausible optimization is not yet action-safe.

The repository separates:

```text
Observation
→ Hypothesis
→ Cause evidence
→ Action / treatment
→ Outcome
```

A `Ready` experiment is ready for **external execution review**, not permission to mutate Amazon Ads.

Machine-readable experiment plans use:

- `schemas/experiment-plan.json`
- `scripts/validate_experiment_plan.py`

---

## Evaluation

There are three different validation layers:

1. **Repository contract checks** — file/schema/routing invariants.
2. **Synthetic capability replay** — decision and safety regressions under `evals/fixtures/`.
3. **Skill effectiveness** — with-Skill vs without-Skill, discovery vs forced invocation, negative controls and repeated trials.

Start with:

- **[evals/README.md](evals/README.md)**
- **[evals/SKILL-EFFECTIVENESS.md](evals/SKILL-EFFECTIVENESS.md)**
- `schemas/skill-effectiveness-benchmark.json`
- `scripts/summarize_skill_effectiveness.py`

The repository's deterministic tests run before any claim that a behavioral change is safe.

---

## Repository structure

```text
amazon-ads-skills/
├── skills/                 # 15 canonical Agent Skills
├── references/             # shared decision/data/connector rules
├── playbooks/              # multi-Skill operating workflows
├── schemas/                # machine-readable contracts
├── scripts/                # read-only validators/projectors/resolvers
├── tests/                  # deterministic policy/unit tests
├── evals/                  # synthetic replay + effectiveness contracts
├── docs/
│   ├── GETTING-STARTED.md
│   ├── SOURCES.md
│   └── research/
├── AGENTS.md               # repository-wide agent instructions
├── CLAUDE.md               # Claude Code entry instructions
├── .codex-plugin/
├── .claude-plugin/
└── .workbuddy-plugin/
```

---

## Runtime compatibility

The same canonical `skills/` tree is used across runtimes.

| Runtime | Repository entrypoints |
|---|---|
| Codex | `AGENTS.md`, `.codex-plugin/plugin.json`, `skills/` |
| Claude Code | `CLAUDE.md`, `.claude-plugin/plugin.json`, `skills/` |
| WorkBuddy | `.workbuddy-plugin/plugin.json`, `skills/` |
| Other file-capable agents | explicit `skills/<name>/SKILL.md` |

Runtime manifests describe packaging/discovery only. They do not create an Amazon Ads connection.

See **[docs/GETTING-STARTED.md](docs/GETTING-STARTED.md)** for current setup guidance.

---

## Documentation map

Use the narrowest document that owns the question:

| Need | Read |
|---|---|
| Install / first run | `docs/GETTING-STARTED.md` |
| External sources and adoption boundaries | `docs/SOURCES.md` |
| Recent platform/engineering research | `docs/research/` |
| Amazon metric definitions | `references/amazon-ads-metrics.md` |
| Data comparability | `references/data-lineage.md` |
| Report completeness | `references/report-coverage.md` |
| Connector capability | `references/connector-capability.md` |
| Optimization memory | `references/optimization-memory.md` |
| Action sizing | `references/action-sizing.md` |
| Execution boundaries | `references/decision-boundaries.md` |
| Weekly operating flow | `playbooks/weekly-review.md` |
| Regression/eval behavior | `evals/README.md` |

---

## Contributing decision logic

For behavioral changes:

```text
prove the old failure with a deterministic RED test / eval
→ implement the smallest useful change
→ run unit tests
→ validate Skills
→ validate eval fixtures
→ inspect GitHub Actions
```

Do not add rules only because another repository is popular or highly starred. External projects are evidence sources, not authority over Amazon Ads behavior.

Third-party implementations, prompts, schemas, workflows and templates are not copied into this repository unless licensing and scope explicitly justify it. Generic ideas are independently rewritten and documented in `docs/SOURCES.md` or `docs/research/`.

---

## License

Repository-owned code and Skills are distributed under **[MIT](LICENSE)**.

Amazon documentation and third-party projects retain their own copyrights and licenses. See **[docs/SOURCES.md](docs/SOURCES.md)** for adoption boundaries.
