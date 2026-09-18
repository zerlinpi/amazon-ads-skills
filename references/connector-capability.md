# Connector capability contract

Load this reference when a decision depends on what the active MCP, API wrapper, export path, warehouse connector, or other acquisition channel can actually expose.

The purpose is to keep **platform capability**, **connector capability**, **returned data**, and **metric value** separate. A field that exists in Amazon Ads may be absent from the current connector. A supported connector operation may still return an incomplete page, a selected population, immature dates, or a report generated under different semantics.

Use `../schemas/connector-capability-snapshot.json` when a machine-readable capability snapshot is available.

## Core distinction

Keep these states separate:

```text
Amazon/platform supports a feature
≠ active connector supports the feature
≠ active connector exposed the required field for this call
≠ report returned an eligible row
≠ metric value is zero
```

In particular:

- `Unsupported` means the observed connector path does not expose the capability for the stated scope.
- `Partial` means some required scope, semantics, fields, history, or completeness signals are missing.
- `Unknown` means capability evidence is absent or stale.
- An empty response is a data result only when the connector/report contract proves that the requested population was completely evaluated. It is never a fallback representation for Unsupported or Unknown.

Do not infer support from a tool name alone. Do not infer absence from a missing tool alone when progressive discovery, package activation, permissions, advertiser eligibility, region/profile selection, or server-side feature flags can change the visible catalog.

## Capability snapshot

A snapshot should preserve:

```text
connector_id / version
captured_at
source_system
acquisition_channel
default_access_mode
catalog discovery mode
capabilities[]
```

Each decision-relevant capability should identify its bounded scope and, where observable, its reporting/data contract:

- marketplace/region/ad product/account type;
- advertiser/profile/account identity fields exposed;
- reporting generation;
- synchronous, asynchronous, push, or export lifecycle;
- pagination model and whether truncation/continuation is observable;
- row-inclusion / eligibility visibility;
- historical-availability limits;
- freshness and `available_through` visibility;
- per-metric semantic / attribution identity visibility;
- date-attribution semantics visibility;
- structured error behavior and whether unsupported/unauthorized/empty states are distinguishable.

The snapshot is evidence observed at `captured_at`; it is not a permanent truth about the vendor or Amazon Ads.

## Progressive tool discovery

Large MCP surfaces can consume substantial context merely by registering tool schemas. When the connector supports package-, namespace-, search-, or code-mode discovery, prefer a bounded catalog that exposes only the tools needed for the current task.

Record whether discovery is `bounded`, `progressive`, `full`, or `unknown`. A tool hidden by progressive discovery is not evidence that the underlying capability is unsupported. Resolve the catalog/package/namespace state before declaring a connector gap.

This repository does not require any vendor-specific discovery mechanism. The goal is to preserve the distinction between **not currently visible** and **not supported**.

## MCP tool annotations

MCP tool annotations such as `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` are useful risk vocabulary when exposed.

They are **advisory** metadata, **not authorization**, not a proof of implementation behavior, and not a replacement for repository policy or external executor controls. Treat annotations from an untrusted or unverified server as untrusted claims. When a capability matters to action safety, bind it to observed behavior, connector documentation, tests, or another auditable evidence source.

Repository policy still wins:

- default analysis mode is Read-only / Suggest / Shadow;
- this repository never performs live Amazon Ads mutation;
- executor write authority, retries, idempotency enforcement, reconciliation, and credentials remain external;
- a remote tool advertising `readOnlyHint=false` does not grant permission to use it.

## Error semantics

A useful connector error surface distinguishes at least:

```text
unsupported capability
unauthorized / forbidden
invalid request / schema mismatch
profile or marketplace scope mismatch
report pending / not ready
rate limited / transient
history unavailable / retired
completed but empty eligible population
pagination or truncation still pending
unknown
```

When the connector can expose retryability or corrective hints, retain them as diagnostics. Do not let a retry hint silently authorize a write, and do not use retries to convert an ambiguous timeout into a confirmed application.

A structured error envelope should reduce agent thrashing, but the repository must remain safe even when the connector returns only an opaque error.

## Reporting lifecycle

For asynchronous reports or exports, preserve the state transition rather than treating job creation as data retrieval:

```text
request accepted
→ job/report id
→ pending/running
→ completed
→ artifact downloaded/read
→ pagination/row-eligibility/completeness checked
→ measurement semantics verified
```

For push/stream sources, preserve event time, arrival time, scope, dataset/version, and completeness assumptions separately from pull-report freshness.

A report job completing successfully proves only that the report completed under its contract. It does not prove full logical population coverage or that omitted rows are zero.

## Capability evidence and freshness

Prefer capability evidence in this order when available:

1. observed active connector/tool response for the exact scope;
2. current connector documentation or machine-readable manifest;
3. connector implementation/test evidence;
4. current platform/API documentation that proves the platform feature exists but not necessarily that this connector exposes it.

Record `captured_at` or `observed_at`. Re-check a capability when a decision depends on an exact field, report generation, profile/region behavior, history range, or write/readback function that may have changed.

## Canonical capability IDs

Do not invent connector capability identifiers ad hoc. Use the repository-owned registry at `connector-capability-catalog.json`.

For a Skill decision profile, resolve the canonical IDs with:

```text
echo '{"skill":"bid-optimization","profile":"action-safe-proposal"}'
→ scripts/resolve_skill_capabilities.py
→ required_capabilities[] / optional_capabilities[]
```

The registry is intentionally connector-neutral. A vendor may expose differently named tools, endpoints, packages, or datasets; the adapter/connector maps those external surfaces onto the canonical repository capability IDs. A hidden tool under progressive discovery is not automatically `Unsupported`; resolve the connector catalog/namespace state first, then publish the observed status into the capability snapshot.

Current profile names are repository decision profiles such as `live-analysis`, `action-safe-proposal`, `ready-experiment`, and `outcome-review`. Unknown Skill/profile names fail closed in `../scripts/resolve_skill_capabilities.py` rather than creating a new identifier implicitly.

The catalog contains only read/report/observe/stream capabilities. It does not register live mutation authority.

## Runtime decision gate

When a Skill depends on live MCP/API/connector evidence, run the capability check **before metric interpretation** whenever a machine-readable snapshot is available. Use `../scripts/evaluate_connector_capability_gate.py` with the snapshot plus the exact capability IDs required for the decision.

The deterministic result is:

- `Pass` — every required capability is `Supported`; high-confidence interpretation may proceed, subject to ordinary data-lineage, sufficiency and business-safety checks.
- `Degraded` — at least one required capability is `Partial` and none are blocked; the maximum decision class is Directional/Hold/Alternate Source/Missing Data/Manual Review until the missing scope or semantics are resolved.
- `Blocked` — at least one required capability is `Unsupported`, `Unknown`, or absent from the snapshot; do not promote the dependent observation into a high-confidence recommendation.

The helper always emits `missing_evidence_policy = never_zero`. This is a semantic safety rule, not a numeric default: connector uncertainty must not be converted into zero spend, zero orders, zero inventory, unchanged state, no prior action, or any other fabricated observation.

Example input:

```json
{
  "snapshot": {
    "connector_id": "example",
    "captured_at": "2026-09-18T00:00:00Z",
    "default_access_mode": "Read-only",
    "capabilities": [
      {
        "capability_id": "campaign-performance-read",
        "status": "Supported",
        "access_mode": "read"
      }
    ]
  },
  "required_capabilities": ["campaign-performance-read"]
}
```

The helper is read-only and dependency-free. It does not discover tools, call Amazon, validate metric values, grant write permission, or replace the stronger source-comparability and action-safety gates elsewhere in this repository.

## Decision gate

Before a high-confidence recommendation that requires a connector field or operation:

1. identify the required capability;
2. resolve connector status for the exact marketplace/profile/ad-product scope;
3. verify the data contract needed by the decision;
4. if status is Partial/Unsupported/Unknown, identify an allowed alternate source or downgrade the decision;
5. never substitute zero, unchanged state, or no prior action for missing connector evidence.

Use `data-lineage.md` after resolving capability status when comparing the returned measurements. Use `platform-capability-lineage.md` when the uncertainty is about Amazon's platform behavior rather than the connector.

## What belongs outside this repository

This contract deliberately does not implement:

- Amazon/LWA credentials or token refresh;
- live Amazon Ads writes;
- automatic retry/idempotency/reconciliation;
- tenant/profile secret storage;
- report artifact storage;
- vendor-specific tool names;
- private connector schemas or workflows.

Those remain responsibilities of an authorized external Connector / Executor. This repository consumes bounded capability evidence so its Skills know what they can safely conclude.
