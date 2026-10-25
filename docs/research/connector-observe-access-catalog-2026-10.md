# Canonical observation-only connector access — 2026-10-26

## Reproduced non-duplicate gap

Baseline main: `780bfd75a53c99051c637e3028cdc14f2200d145`. The canonical catalog declares six observation capabilities with `access_mode=observe`, including `report-completeness-observe` and `metric-semantics-observe`. The connector snapshot schema omitted this mode, while the runtime gate unconditionally degraded it. The prior `tests/test_connector_read_access_evidence.py` correctly rejects `observe` as proof of a campaign report, so a global allowlist expansion would be unsafe.

## Minimum behavior and safety

Accept `observe` only for a required capability whose canonical catalog access mode is `observe`; all existing Verified binding, concrete source, bounded scope, chronology, freshness, data-contract and history checks still apply. `observe` on read/report capabilities remains Degraded; write-only remains Blocked; mixed/unknown remain Degraded. Existing read/report/export/stream transport behavior remains compatible. This is repository-owned read-side evidence semantics, not an Amazon Ads API enum, entitlement, actual metric completeness or execution permission.

## Deterministic RED→GREEN

- Test commit `75c26edc14b9ab52f57e16504fc62f2ddab46735`: [RED Actions #40227658177](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40227658177), 1509 tests, 6 FAIL.
- Production/schema head `3b4bc4b6ea5895b6ed88471b325ad92a4fb72fe6`: [GREEN Actions #40227736857](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40227736857), 1509 PASS, 15 Skills and 55 eval fixtures PASS.
- Fourteen synthetic tests. No Amazon Ads account reads/writes or new Skills.

## Sources, license and next gap

Official Amazon Ads MCP and reporting docs support distinguishing report metadata from report access; they do not define this internal contract. Open-source metadata, license review and explicit rejection decisions are in `docs/SOURCES.md`. No third-party implementation, schema, prompt, workflow or template copied. Community PPC discussion is hypothesis-only, not a causal rule.

Next P0: independently dated advertiser/campaign/marketplace feature eligibility evidence joined to exact connector identity; P1 continuous rule activation; P2 raw HTTP provenance; P3 confounder/economic interactions.
