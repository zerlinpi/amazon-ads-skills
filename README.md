# Amazon Ads Skills

A portable **Amazon Ads decision library for AI agents**. It packages 15 focused Skills for audit, monitoring, diagnosis, growth, experiments, search terms, targeting, bids, budgets, placements, profitability and post-change learning without turning this repository into an autonomous write bot.

> Current version: `v1.2.0`  
> Default mode: `Suggest`  
> Live Amazon Ads writes: external Connector / Executor only

## What you can do

- Audit an Amazon Ads account without treating missing connector/report data as zero.
- Diagnose sustained performance drops and separate observations, hypotheses, causes, actions and outcomes.
- Analyze search terms, keyword/target structure, bids, budgets and placements with report-coverage and control-state gates.
- Evaluate break-even ACOS, contribution economics and TACOS without confusing historical efficiency with marginal headroom.
- Find guarded growth opportunities only after retail readiness, economics, incrementality and binding-control checks.
- Design experiments when evidence is not strong enough for a direct recommendation.
- Review previous changes using readback, validation windows, confounders and append-first optimization memory.
- Run recurring weekly reviews that preserve campaign mission instead of applying one universal ACOS rule to every campaign.

## Start here

Clone the repository, open the repository root in Codex, Claude Code, WorkBuddy or another file-capable agent, then run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

For setup, read [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md). For a broad account task start with `skills/amazon-ads-optimizer/SKILL.md`; for a narrow task select the matching Skill directly.

A useful bootstrap instruction is:

```text
Read the repository instructions first. Select the minimum Skill needed.
State the operating mode and missing evidence. Default to Suggest.
Do not infer missing data as zero and do not perform live Amazon Ads writes.
```

## How it works

```text
evidence
→ identity / lineage / coverage / connector checks
→ campaign objective + retail/economic context
→ observation
→ hypothesis
→ supported cause or unresolved uncertainty
→ guarded action / experiment / hold
→ external execution only when separately authorized
→ readback
→ outcome review + memory
```

The repository uses progressive loading: one selected `SKILL.md`, then only the references, schemas, playbooks and read-only helpers required by that decision.

## Capability map

| Need | Primary capability |
|---|---|
| Whole-account review | `amazon-ads-audit` |
| Multi-domain orchestration | `amazon-ads-optimizer` |
| Routine health / anomaly | `campaign-health-monitor`, `anomaly-detection` |
| Sustained decline diagnosis | `performance-drop-diagnosis` |
| Qualified growth headroom | `growth-opportunity-finder` |
| Controlled validation | `experiment-planner` |
| Post-change learning | `post-change-review` |
| Search terms / targeting | `search-term-analysis`, `keyword-optimization`, `negative-targeting` |
| Bid / budget / placement | `bid-optimization`, `budget-optimization`, `placement-optimization` |
| Profitability | `profitability-analysis` |

The catalog intentionally stays at 15 Skills. Composite operating procedures belong in `playbooks/`; shared decision contracts belong in `references/` and `schemas/`.

See [docs/CAPABILITIES.md](docs/CAPABILITIES.md) for the full capability and routing map.

## Safety boundaries

Core invariants:

```text
missing data ≠ 0
unsupported connector capability ≠ 0
returned rows ≠ complete logical population
same metric label ≠ same measurement definition
configured control ≠ effective control
proposed ≠ applied ≠ readback confirmed ≠ worked
historical profitability ≠ marginal profitability
campaign role/objective ≠ inferable from one ACOS snapshot
```

Operating modes are `Read-only`, `Suggest`, `Shadow`, and externally authorized `Execute`. Credentials, OAuth/LWA, live writes, retry/idempotency and reconciliation stay outside this repository. See `AGENTS.md` and `references/decision-boundaries.md`.

## Documentation

- [docs/README.md](docs/README.md) — documentation index and audience map.
- [docs/CAPABILITIES.md](docs/CAPABILITIES.md) — what the 15 Skills can do and how they route.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — connector, lineage, memory, experiment, evaluation and runtime architecture.
- [docs/SOURCES.md](docs/SOURCES.md) — reviewed sources, licenses and adoption boundaries.
- [docs/research/](docs/research/) — dated research notes, including operator/community evidence.
- [evals/README.md](evals/README.md) — deterministic replay and effectiveness evaluation.
- [CHANGELOG.md](CHANGELOG.md) — release history.

## Contributing

Use pull requests and RED→GREEN for behavioral changes: prove the gap with a deterministic test/eval, implement the smallest useful change, run unit/Skill/eval validators, and inspect GitHub Actions. Popular repositories and community posts are discovery evidence, not authority; license, engineering quality, Amazon official semantics, duplication and action safety control adoption.

## License

Repository-owned code and Skills are distributed under [MIT](LICENSE). Amazon documentation and third-party projects retain their own copyrights and licenses.