# Platform Integration

Use this guide when embedding this repository behind an advertising platform, custom agent host, MCP client, internal dashboard, or chat workflow.

The repository remains the **decision layer**. Authentication, API transport, live Amazon Ads mutation, retry/idempotency, reconciliation, secret storage, and production scheduling remain external platform/Connector/Executor responsibilities.

## Recommended host flow

```text
task
→ metadata-only Skill catalog
→ select one Skill
→ load one SKILL.md
→ resolve connector capabilities for that Skill/profile
→ observe active connector capability snapshot
→ run connector capability gate
→ acquire bounded evidence
→ run Skill reasoning
→ produce Suggest / Shadow proposal
→ external execution only after explicit authorization
→ trusted readback
→ post-change review / optimization event
```

For a custom host without native Agent Skills discovery, use:

```bash
echo '{"operation":"catalog"}' | python scripts/resolve_skill_context.py
```

This returns only `name`, `description`, and repository-local `entrypoint` for each Skill.

After routing to one Skill:

```bash
echo '{"operation":"resolve","skill":"bid-optimization","profile":"action-safe-proposal"}' \
  | python scripts/resolve_skill_context.py
```

The resolver returns exactly one preload entrypoint, deferred resource candidates, and the canonical connector capability profile. It does not return Skill body text, load research/evals, call Amazon Ads, or grant write authority.

## Amazon Ads MCP Server

Amazon announced the Amazon Ads MCP Server in open beta on February 2, 2026 for Amazon Ads partners with active API credentials. Amazon describes it as a translation layer between agent prompts and Amazon Ads API functionality, including reporting and workflows that may also create, update, or delete advertising objects.

Treat the Amazon Ads MCP Server as an **external Connector/Executor surface**, not as permission for this repository to mutate a live account.

Platform rule:

```text
connector exposes write tools
≠ Skill has write authority
≠ user authorized a mutation
≠ executor outcome is trusted current state
```

A host integrating the official Amazon Ads MCP Server, another MCP server, direct API, warehouse, or proprietary ad platform should map observed capabilities into:

- `schemas/connector-capability-snapshot.json`;
- canonical IDs from `references/connector-capability-catalog.json`;
- `scripts/evaluate_connector_capability_gate.py`.

Do not hardcode transient MCP tool names into Skills. Tool catalogs and prebuilt workflows may evolve independently from this decision library.

Official source reviewed:

- https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta

## Token-efficient loading

For a custom platform, use these defaults:

1. **Catalog only at discovery** — cache Skill `name + description + entrypoint`; do not inject all 15 bodies.
2. **One Skill at activation** — load only the routed `SKILL.md`.
3. **Resources on demand** — `resource_candidates` are pointers, not a preload list.
4. **Do not preload research/evals** — `docs/research/` and `evals/` belong to maintenance/evaluation paths unless the task explicitly needs them.
5. **Filter connector/tool exposure** — prefer the Skill's required/optional canonical capabilities rather than exposing a large MCP/API tool catalog to the model by default.
6. **Bound report payloads** — keep pagination/coverage metadata, but retrieve only decision-relevant rows/columns/windows. A truncated slice must remain explicitly partial.
7. **Keep host state out of model context when possible** — auth state, tool registry, policy state, caches, correlation IDs and retry/reconciliation metadata belong in application/runtime context.
8. **Measure usage** — record per-run input/output token usage in the host when the runtime exposes it. Compare token cost against decision-quality/effectiveness, not against prose length alone.

Agent Skills implementations commonly use metadata-first progressive disclosure; current OpenAI agent runtimes also support deferred tool loading and usage accounting. This repository does not depend on those runtimes, but the same host-level pattern is compatible with them.

## Platform adapter responsibilities

A platform adapter should preserve, when applicable:

- marketplace/profile/account identity;
- source system and acquisition channel;
- reporting generation and source dataset;
- date attribution and metric semantics;
- represented population / row eligibility;
- pagination/truncation;
- historical availability;
- freshness / available-through / backfill maturity;
- aggregation grain and filters;
- entity type + entity ID;
- connector capability evidence.

Missing or unsupported evidence remains unknown; it is never converted to zero.

## Read/write boundary

Recommended production rollout:

```text
Phase 1: Read-only
Phase 2: Suggest
Phase 3: Shadow / dry-run against external platform
Phase 4: explicitly authorized external execution
Phase 5: readback + reconciliation + post-change review
```

Do not skip readback merely because an executor or MCP tool returned success.

If the external platform supports write tools, enforce authorization and idempotency in that platform. This repository may produce a validated proposal in `Execute` mode, but it still does not perform the mutation itself.

## Keeping tactics current without bloating Skills

Current/high-volatility Amazon Ads features belong under `docs/research/` and `references/platform-capability-lineage.md`, not copied into every Skill.

See:

- `docs/research/amazon-ads-platform-watch-2026-09.md`
- `references/platform-capability-lineage.md`

Promote a new platform tactic into a Skill only when it changes a repeatable decision rule, has sufficiently current scope/eligibility evidence, and can be expressed without turning a temporary launch detail into a permanent heuristic.
