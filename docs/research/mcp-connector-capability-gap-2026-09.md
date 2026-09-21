# MCP / Connector capability gap review — 2026-09

## Scope

This review asks a narrow question: which connector-layer capabilities materially improve the decision quality and action safety of this repository's existing 15 Amazon Ads Skills?

It does **not** select a vendor, import a third-party MCP schema, or add live Amazon Ads mutation. Public repositories were deduplicated by origin where practical; obvious forks/mirrors were not counted as independent engineering evidence.

## High-signal projects reviewed

### KuudoAI/amazon_ads_mcp — MIT

High-value generic lessons:

- separate the MCP **tool layer** from higher-level Skills/workflows;
- bind advertiser profile and region explicitly instead of allowing an agent to guess scope;
- model asynchronous reporting as create -> poll -> complete -> download/read rather than one implicit read;
- expose bounded/progressive tool discovery when a very large API surface would otherwise consume substantial model context;
- make schema/argument failures diagnostic with structured corrective hints;
- audit the active tool catalog and its context footprint.

Repository adoption: only these connector-neutral principles. No Kuudo tool names, argument aliases, report-field tables, middleware, package catalog, auth flow, code-mode implementation, prompt, or error-envelope implementation is copied.

### AgriciDaniel/claude-ads — MIT

High-value generic lessons:

- capability claims should be evidence-bearing rather than aspirational;
- implementation, fixture/test evidence, source provenance, mode and disabled reason can be tracked independently;
- read-only should remain the default until an exact capability passes a stronger lifecycle.

Repository adoption: a smaller connector-neutral capability evidence contract. No control-plane manifest, scoring implementation, release workflow, adapters, mutation lifecycle, or schemas are copied.

### TrackIQ-HQ/amazon-seller-skills — MIT repository

High-value generic lesson:

Amazon Ads decision quality often depends on adjacent retail evidence that the Ads API alone may not supply, including sales/traffic, inventory, returns, Buy Box/offer history, Brand Analytics/Search Query Performance and rank context.

Repository adoption: treat these as **optional adjacent connector capability classes**, not required Amazon Ads fields and not proof that any specific connector supplies them. No TrackIQ MCP interface, skill prose, commercial workflow, tool name or implementation is copied.

### nospicyplease/amazon-ppc-advanced-skills — MIT

Already reviewed elsewhere in this repository. This pass reconfirmed the value of live preflight, exact entity resolution, product/ASIN context, recent-change checks and readback before treating an action as executable or effective.

Repository adoption remains method-level only; vendor-specific Rocketcart interfaces and execution workflows are not copied.

### Ecom-Wizards-Agency/Arcana — no repository-level license found

High-value generic lessons:

- a production MCP can intentionally expose only analytical reads;
- tenant/profile scope can be bound outside individual tool arguments;
- read access and auditability are separate requirements;
- mutation tooling can be deliberately absent from the MCP even when the wider product can perform controlled writes.

Because no repository-level license was found, no Arcana MCP contract, source code, tool names, deployment workflow or prose is copied. Only abstract safety principles are considered.

### ppcprophet/amazon-ads-mcp — repository MIT; hosted service described as proprietary

High-value generic lesson:

A practical Ads connector may expose analytical capability classes such as campaign/search-term/ASIN performance, period comparison, diagnosis, profile management and change/rule history rather than only raw endpoint mirroring.

Repository adoption: tool **categories only** as a coverage check. No hosted-service API, commercial workflow, thresholds, UI/widget behavior or proprietary implementation is copied.

### 2446573/amazon-ads-agent — MIT

Reviewed as lower-weight engineering evidence. It demonstrates one common pattern: combining exported ad data with external competitor/retail context before generating recommendations.

No scraping implementation, thresholds, prompt, rule engine or workflow is adopted. External competitive data must carry its own provenance and is not required by this repository.

### Lower-confidence / excluded candidates

- Numerous repositories named `amazon_ads_mcp` were direct forks or mirrors of KuudoAI/amazon_ads_mcp and were not counted independently.
- AdlevateDE/amazon-ppc-skills did not expose enough license/documentation evidence in this review to justify adoption.
- Newly discovered Selling Partner / Vendor Central MCP repositories show that adjacent retail connectors are emerging, but sparse or newly published projects were not used as load-bearing evidence without deeper validation.

## Resulting capability gap

The repository already had strong **policy** for connector uncertainty in `references/data-lineage.md`, but lacked a machine-readable answer to:

```text
What can this active connector expose,
for which scope,
under which report lifecycle,
with which completeness/semantic signals,
and with which access risk?
```

That gap made it possible for agents or integrations to collapse these different states:

```text
connector unsupported
connector capability unknown
field not exposed
report still pending
page truncated
row ineligible
history unavailable
completed empty population
metric value = 0
```

The first seven are not zero-valued observations.

## Adopted repository design

The connector-neutral contract is split into:

- `schemas/connector-capability-snapshot.json` — machine-readable observed capability state;
- `references/connector-capability.md` — interpretation and action-safety policy;
- `references/data-lineage.md` — routing from acquisition-path uncertainty into the capability contract.

The contract intentionally preserves:

- connector identity/version and observation time;
- default access mode;
- bounded/progressive/full catalog discovery state;
- capability status: Supported / Partial / Unsupported / Unknown;
- access mode: read/report/export/stream/write/mixed/unknown;
- marketplace/region/ad-product/account scope;
- reporting generation and sync/async/push/export lifecycle;
- pagination/truncation signals;
- row eligibility, history, freshness and `available_through` visibility;
- metric/date-attribution semantics visibility;
- structured error distinctions;
- MCP tool risk annotations as observed metadata.

MCP tool annotations remain advisory only. They are not authorization and never override repository policy.

## Missing MCP capability priorities

### P0 — needed for dependable use of the current Skills

1. **Profile/account identity resolution**
   - list/resolve advertiser profiles;
   - marketplace, country/region, currency, timezone;
   - global/regional/legacy advertiser identity where exposed;
   - explicit active scope confirmation.

2. **Connector capability discovery**
   - active tool/data-set support;
   - package/namespace/feature activation;
   - read/write mode;
   - capability observation time and evidence;
   - supported scope and semantic fields.

3. **Reporting lifecycle + completeness**
   - create/query/poll/download for async reports where applicable;
   - reporting generation;
   - pagination/continuation/truncation;
   - row-inclusion/eligibility contract;
   - historical range/retirement state;
   - freshness and `available_through`;
   - metric and date-attribution semantics.

4. **Structured error/capability envelope**
   - unsupported vs unauthorized vs invalid request vs pending vs rate-limited vs unavailable history vs completed-empty;
   - retryability and corrective hints when reliable;
   - no coercion of an error into an empty dataset.

5. **Current-state/readback and change-history reads**
   - exact current bid/budget/state/targeting/placement/negative configuration where relevant;
   - recent material changes and timestamps;
   - enough readback evidence to distinguish proposed, applied, confirmed and drifted.

6. **Progressive tool discovery**
   - bounded tool catalog, namespace/package activation, search or another on-demand discovery mechanism;
   - avoid loading hundreds of unrelated tool schemas into agent context.

### P1 — high value but not mandatory for every PPC task

7. **Amazon Marketing Stream / near-real-time read path**
   - hourly performance and campaign-change messages;
   - event/arrival time and dataset identity;
   - stream completeness/lag signals.

8. **Retail-readiness connector surface**
   - inventory/availability;
   - price and offer / Featured Offer or Buy Box state;
   - total retail sales/traffic where authorized;
   - returns and listing state;
   - Brand Analytics / Search Query Performance where eligible;
   - product/ASIN mapping and rank context where a verified source exists.

9. **DSP / AMC / export / recommendations read surfaces**
   - exposed only when required by a Skill/task and supported for the advertiser.

10. **Auditable connector call provenance**
    - capability/tool invoked;
    - bounded scope;
    - request/report identity;
    - observation time;
    - sanitized error/status;
    - no credential logging.

## Deliberately outside this repository

The following should remain in an external authorized Connector / Executor rather than being implemented by these Skills:

- OAuth/LWA secret handling;
- Amazon Ads live mutation;
- automatic retry and idempotency enforcement;
- reconciliation workers;
- tenant credential/profile storage;
- report artifact persistence;
- vendor-specific private MCP interfaces.

This keeps the Skills portable and preserves the repository's Read-only / Suggest / Shadow default.


## Exact material-control observability binding — 2026-09-21

A subsequent RED→GREEN review found a structural gap between the versioned control-state requirement registry and connector capability preflight. The repository could require `targeting_or_routing`, schedule/event rules, audience adjustments, budget/pacing and other material controls for a causal decision surface, while the connector gate only knew that a generic `entity-state-readback` capability was `Supported`. That generic claim could not prove the connector exposed every decision-material control type.

The adopted design keeps capability taxonomy small instead of creating one capability ID per control. `resolve_skill_capabilities.py` accepts a registered `decision_surface`, resolves the exact `required_control_types` from `references/control-requirement-registry.json`, and attaches them as a data requirement on the existing `entity-state-readback` capability. `schemas/connector-capability-snapshot.json` now records `data_contract.control_types_exposed`, and `evaluate_connector_capability_gate.py` blocks high-confidence dependent decisions when any required type is missing or unproven. Per-window control evidence remains a separate responsibility of `schemas/control-state-snapshot.json` and `scripts/compare_control_state.py`.

External evidence reviewed for this change:

- Amazon Ads official **Reach business shoppers with Amazon Business exclusive campaigns**, 2025-05-05: Sponsored Products Sites restriction can change eligible delivery to Amazon Business only and is exposed in the Ads API. This reinforces that routing/site state is a material, independently observable control rather than a derived performance metric.
- Amazon Ads official schedule-bid-rule and budget-rule documentation: automated bid and budget rules are separate advertiser controls that can alter effective delivery/bidding state over time.
- Model Context Protocol official 2026-03-16 tool-annotations guidance: `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` are hints and must not be treated as trustworthy proof of implementation behavior without a trusted source. This aligns with the repository rule that generic tool metadata cannot prove exact Amazon control-state coverage.

No Amazon API payload, MCP implementation, third-party prompt, connector schema, or workflow was copied. The repository independently implemented only the provider-neutral invariant: exact decision-material observability must be proven before a connector capability can support a high-confidence causal conclusion.
