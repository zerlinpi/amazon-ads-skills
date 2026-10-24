# Amazon Ads Skills

A portable **Amazon Ads decision library for AI agents**. It packages 15 focused Skills for audit, monitoring, diagnosis, growth, experiments, search terms, targeting, bids, budgets, placements, profitability and post-change learning without turning this repository into an autonomous write bot.

> 当前版本：`v1.43.0`  
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
- When both native Global SP campaign configuration and its paginated query trace are supplied, require an explicit source/time/filter/identity binding to one enumerated query page before confirming; contradictory or missing page provenance is `Unknown`. Native-only or trace-only legacy evidence remains compatible.\n- For Global SP campaign queries, an optional source-attributed pagination trace must have a complete terminating nextToken chain, stable campaign/account/filter identity, consistent source, and post-write page timestamps; contradictory traces cannot be marked `Confirmed`.
- For Global SP campaign updates, reject explicitly contradictory campaign/account/request identities in the HTTP 207 receipt before independently verifying per-marketplace configured-state readback; optional daily monetary-budget changes additionally require per-marketplace currency, amount, recurrence and independently complete budget readback. Explicitly supplied per-budget-row source, observation time, and account/campaign identity must also agree with the enclosing readback; a successful receipt is not a confirmed application.
- When a Global SP campaign configured-state or daily-budget readback includes raw marketplace IDs, require a complete, uniquely sourced raw-ID-to-country-code crosswalk and exact row binding; missing, duplicate or contradictory identity evidence returns `Unknown`. Country-code-only legacy evidence remains supported; this is not independent adapter authentication.
- When a trusted adapter retains a complete native Global SP campaign query resource in `readback.raw_campaign`, independently recompute marketplace configured states from top-level `state` and `marketplaceConfigurations` overrides; reject contradictions as `Unknown`. When a monetary-budget update is being verified and that native resource explicitly includes `budgets`, cross-check its per-marketplace daily monetary amounts, currencies and recurrence against the normalized budget rows; contradictions are `Unknown`, not false `Confirmed`. The adapter must preserve exact native budget numeric lexemes as decimal strings. Never derive configured state from `deliveryStatus`. Legacy normalized envelopes remain supported; raw query authenticity remains an external adapter responsibility.
- Do not interpret a Global SP campaign-state/budget `Confirmed` as verification of separate ad-group/target bid or placement changes: unsupported `expected_*` intent now returns `Unknown`, not false confirmation.
- Independently verify a **single Global SP ad-group** 207 update against complete native-currency marketplace **default-bid** query readback using `scripts/evaluate_global_sp_adgroup_bid_readback.py`; this is separate from campaign/target verification and never writes Ads.
- Independently verify a **single-call Global SP multi-ad-group batch** with `scripts/evaluate_global_sp_adgroup_batch_readback.py`: correlate every 207 index with one distinct ad-group request and independently complete native-currency marketplace default-bid readback for each success; Unknown/Partial/Drifted never become a blanket Confirmed. No Ads writes.
- Independently verify a **single positive Global SP keyword/product target** bid update with `scripts/evaluate_global_sp_target_bid_readback.py`: one marketplace, target-specific identity, native-currency bid, a bound 207 receipt and complete post-write query evidence. Never substitute ad-group default bid, campaign status, or an auction bid.
- Independently verify a **single-call Global SP positive-target batch** using `scripts/evaluate_global_sp_target_batch_readback.py`: bind every 207 index to its ordered target request, require unique target/request identities and exactly one independently complete query readback for each successful item; a mixed or incomplete batch never becomes Confirmed.
- Independently classify a **mixed-resource Global SP optimization plan** with `scripts/evaluate_global_sp_mixed_plan_readback.py`: a trusted complete plan manifest must bind every declared campaign, ad-group, target, or homogeneous batch component to its own readback verifier. Partial, drifted, unsupported or missing evidence cannot become a whole-plan `Confirmed`. The manifest is an external assertion, not an Amazon-native response or Executor reconciliation.
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
unsupported report request ≠ metric zero
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
- `scripts/project_measurement_history.py` — bounded measurement-history projection.
- `scripts/evaluate_global_sp_readback.py` and `references/global-sp-readback-evidence.md` — read-only Global SP 207/per-marketplace readback gate (single-item campaign updates).
- `scripts/summarize_skill_effectiveness.py` and `schemas/skill-effectiveness-benchmark.json` — paired Skill-effectiveness measurement.
- [CHANGELOG.md](CHANGELOG.md) — release history.

## Contributing

Use pull requests and RED→GREEN for behavioral changes: prove the gap with a deterministic test/eval, implement the smallest useful change, run unit/Skill/eval validators, and inspect GitHub Actions. Popular repositories and community posts are discovery evidence, not authority; license, engineering quality, Amazon official semantics, duplication and action safety control adoption.

## License

Repository-owned code and Skills are distributed under [MIT](LICENSE). Amazon documentation and third-party projects retain their own copyrights and licenses.