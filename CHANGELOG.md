# Changelog

This file records user-visible repository releases. The canonical current version is stored in `VERSION`.

## v1.9.0 — 2026-09-22

### Added

- Shared report-request compatibility gate that separates an unsupported `reportTypeId × groupBy × columns × timeUnit × filters` configuration from advertiser metric zero.
- Regression coverage for Reporting API v3 daily/summary date-column semantics and multi-`groupBy` filter compatibility.

### Changed

- Report coverage now validates request compatibility before metric interpretation while keeping generation, extraction completeness and population coverage as separate evidence states.
- Unsupported, partial or unknown request compatibility fails closed to missing/alternate-source/hold/manual-review behavior rather than silently substituting a nearby metric or grain.

### Research

- Re-verified current Amazon Sponsored Ads Reporting API v3 request semantics and Unified Reporting context. Re-discovered Amazon Ads MCP/downloader projects and high-adoption Agent Skills/evaluation projects; forks, archived projects and already-reviewed runtime ideas were de-duplicated. No external code, schema, prompt, workflow or request template was imported.

## v1.8.0 — 2026-09-22

### Added

- Bounded `measurement_comparison` audit evidence on optimization events, preserving comparator identity, classification, changed fields, deterministic reasons, and baseline/post evidence snapshot IDs.
- Stable `measurement-composition@1` comparator identity plus snapshot-lineage passthrough in `compare_measurement_composition.py`.

### Changed

- `post-change-review` now preserves the machine comparison result on `evaluated` / `corrected` structured events when that comparison materially gates the outcome.
- Optimization-memory guidance now treats comparator output as append-first audit lineage rather than a transient LLM judgment; missing snapshot identities remain unknown and are never reconstructed.

### Research

- Re-verified Amazon Ads conversion-attribution, modeled-conversion and Unified Reporting semantics and reviewed OpenLIT and Arize Phoenix for agent-evaluation/trace auditability. Langfuse was de-duplicated from prior review. No external trace schema, observability backend, evaluator or runtime was imported.

## v1.7.0 — 2026-09-22

### Added

- Dependency-free `scripts/compare_measurement_composition.py` for deterministic baseline/post comparison of modeled/direct inclusion, split availability, allocation coverage, `Unallocated` state and allocation grain.
- Regression coverage for fail-closed unknown evidence, hard semantic/grain incompatibility and lower-grain directional allocation drift.

### Changed

- `post-change-review` now routes machine-readable baseline/post composition states through the comparator before affected conversion outcomes can be promoted to causal `Worked` / `Failed`.
- Shared data-lineage guidance now defines the machine classifications `Comparable`, `Directional`, `Not Comparable` and `Unknown` for the bounded composition contract.

### Research

- Re-verified Amazon official modeled-conversion reporting semantics and reviewed Great Expectations and Soda Core as data-quality/data-contract references. No third-party validator, framework, contract syntax, workflow or implementation was imported.

## v1.6.0 — 2026-09-22

### Added

- Post-change measurement-composition comparability gate covering modeled/direct inclusion, lower-grain allocation coverage, `Unallocated` rows and allocation grain.
- A replay fixture for a confirmed bid action whose apparent conversion/ROAS improvement coincides with changed lower-grain allocation coverage.

### Changed

- Post-change outcome review now treats material unreconciled measurement-composition drift as a measurement confounder and caps affected conclusions at `Inconclusive` / directional / Hold / Manual Review rather than promoting them directly to causal `Worked` or `Failed`.
- Weekly change-memory review now checks measurement-composition drift before attributing recent conversion movement to a prior optimization action.

### Research

- Re-verified Amazon official modeled-conversion/`Unallocated` reporting semantics and reviewed OpenLineage, OpenMetadata and DataHub as high-adoption lineage/context projects. No external lineage framework, schema, client, workflow or runtime was imported.

## v1.5.0 — 2026-09-22

### Added

- Optional `measurement_composition` schema parity at both optimization-event evidence and derived entity-history measurement boundaries, matching the existing read-only projector.
- A deterministic unittest-discovery guard that prevents top-level pytest-style tests from being silently skipped by the repository's `unittest discover` CI runner.

### Changed

- Measurement-composition persistence now explicitly keeps modeled/direct inclusion, split availability, allocation coverage, unallocated-row presence and allocation grain nullable/unknown when evidence is absent.
- The schema-parity regression is now a real `unittest.TestCase`, so CI exercises the contract instead of returning a false green.

### Research

- Re-verified Amazon official modeled-conversion reporting semantics and reviewed `microsoft/skills`, `alibaba/skill-up`, and `SalesforceAIResearch/MCPEval` for evaluation/test-harness practices. No external runtime, harness, schema, prompt or workflow was imported.

## v1.4.0 — 2026-09-21

### Added

- Campaign-objective decision lineage across optimization memory and post-change review, including explicit action-time objective preservation and objective-drift handling.
- Regression/eval coverage for a Growth action reviewed after the campaign later switches to a Profit objective.

### Changed

- Derived `entity-history.latest_action` can preserve the source action's `campaign_objective` without treating it as current truth.
- Post-change review now separates historical outcome evaluation from the current campaign objective and forbids retroactive KPI/guardrail substitution.
- Weekly review now checks action-time objective vs current objective before classifying prior actions.

### Research

- Re-reviewed Amazon official goal/KPI guidance and high-adoption agent/evaluation projects including `mozilla-ai/any-agent`, `google/adk-go`, and `mlflow/mlflow`; no external runtime or implementation was imported.

## v1.3.0 — 2026-09-21

### Changed

- Bid and placement optimization now load the shared campaign-objective contract before turning local efficiency into objective-dependent action or sizing.
- `Unknown` campaign objective explicitly caps mission-dependent bid/placement decisions to conservative hold/directional/shadow/experiment/manual-review outcomes rather than inventing action authority.
- Existing connector-capability, sample-sufficiency, realized-exposure, control-interaction, confounder, action-sizing and platform-capability safeguards remain additive and unchanged.

### Research

- Recorded `evalstate/fast-agent` as a high-adoption Apache-2.0 runtime/evaluation reference and rejected importing its runtime machinery because connector attachment, execution and orchestration remain external to this decision library.

## v1.2.0 — 2026-09-21

### Added

- User-facing documentation hierarchy with `docs/README.md`, `docs/CAPABILITIES.md`, `docs/ARCHITECTURE.md`, research/archive boundaries and a much smaller product-entry README.
- Campaign-objective context contract with bounded `Discovery`, `Control`, `Growth`, `Profit`, `Defense`, `Experiment`, and safe `Unknown` roles.
- Operator/community research boundary: practitioner evidence can expose failure modes, but anecdotes and fixed percentages do not become repository defaults.

### Changed

- Superseded 2026-09-07 bootstrap plan/design moved out of active documentation so obsolete 11-Skill/direct-to-main guidance no longer competes with current repository governance.
- Optimization action proposals can preserve campaign-objective context when it materially changes a recommendation.

## v1.1.0 — 2026-09-21

### Added

- Deterministic SHA-256 and byte-size content identities for the selected Skill package and directly referenced shared resources returned by the custom-host context resolver.
- Explicit platform-integration guidance separating the repository-local resource manifest from the normative MCP Skills wire protocol.
- Repository-wide semantic-version governance with `VERSION` as the canonical source and CI coverage for README/runtime-manifest synchronization.

### Changed

- Release-readiness tests no longer hardcode `1.0.0`; they validate the active semantic version dynamically.
- Pull requests now classify version impact so substantial backward-compatible improvements advance MINOR versions and breaking public contracts advance MAJOR versions.

## v1.0.0

Initial public v1 release of the 15-Skill Amazon Ads decision library.
