# Amazon Ads Unified Reporting migration research

Reviewed September 17, 2026.

## Public sources

Amazon Ads public documentation reviewed:

- `Understand unified reporting` — updated August 12, 2026.
- `Data availability in unified reporting` — updated August 17, 2026.
- `Migrate your sponsored ads and Amazon DSP reports` — updated September 1, 2026.
- `Streamline campaign analysis with unified reporting, now generally available` — published June 8, 2026.

These are vendor documentation pages, not source code licensed for redistribution. This repository adopts only factual platform behavior and independently written measurement-safety rules. No Amazon prose, UI assets, report templates, API implementation, or proprietary examples are copied.

## High-value facts retained

Amazon Ads states that Unified Reporting:

- standardizes metric names, definitions and entity terminology across ad products;
- reports conversion metrics on **traffic date** (the date of the ad interaction);
- differs from legacy Amazon DSP and legacy Sponsored Brands reporting that could place conversions on **conversion date**;
- exposes historical data with maximum ranges that vary by time grain and can be shorter for specific dimensions/metrics;
- is replacing the legacy Sponsored Ads and Amazon DSP report centers, which Amazon currently plans to shut down on December 31, 2026;
- will permanently delete remaining saved reports, scheduled reports and historical data from the legacy report-center pages at that shutdown, so post-cutover inability to retrieve legacy history is an availability/lineage state rather than evidence that the historical metric value was zero or that no historical activity occurred.

Amazon's September 1 migration guidance also says net-new report creation and editing on the legacy pages is planned to stop on December 17, 2026 while existing reports remain read-only until shutdown. These dates are vendor migration dates and may change; agents should verify current Amazon documentation when a decision depends on the exact cutoff.

## Independent adaptation

The repository treats reporting-generation migration as a measurement-lineage boundary:

```text
same metric label
+ different reporting generation/date attribution
≠ automatically comparable daily series
```

A safe longitudinal review should preserve reporting generation and date-attribution semantics, verify history availability, and prefer replaying both windows under one compatible definition. When only mixed generations are available, use an overlap bridge and downgrade unresolved conclusions rather than attributing the discontinuity to advertising performance.

A legacy-history retrieval failure after a documented retirement/deletion boundary must be classified as `historical availability unavailable/unknown` (or an equivalent explicit state), not coerced to zero. If a required baseline was not migrated or independently preserved, the correct action is to use a verified alternate source, shorten/reframe the comparison, or downgrade confidence; do not fabricate continuity across a permanently unavailable source.

This adaptation remains connector-neutral and does not require private Amazon Ads interfaces or authorize live mutations.


## 2026-09-19 machine-readable availability gate

The September 1, 2026 Amazon migration guidance makes a generic runtime distinction operationally important: a report surface can still exist while its generation is read-only or scheduled for sunset, and after retirement its historical artifacts can become unavailable. These states must not collapse into a metric value of zero.

The connector-neutral capability contract therefore records, when observed:

- `reporting_generation_status = active | read_only | sunset_scheduled | retired | unknown`;
- optional `sunset_at`;
- `historical_availability_status = available | partial | unavailable | retired | unknown`.

The runtime capability gate accepts per-capability `data_requirements`. It never hard-codes Amazon's migration dates and never advances a state merely because wall-clock time passed; the snapshot must be refreshed from current evidence. For a history-dependent decision, partial/unknown history lowers confidence and unavailable/retired history blocks the dependency without manufacturing zero-valued history.

Current Amazon factual evidence: the old Sponsored Ads and Amazon DSP report centers are scheduled for shutdown on December 31, 2026; Amazon's September 1 migration guidance says net-new creation/editing is disabled on December 17 while existing reports remain read-only, and remaining saved reports/schedules/historical data are deleted at shutdown. Dates remain subject to Amazon change. No Amazon report schema, UI workflow, API implementation, or documentation prose is copied.


## 2026-09-19 profile-owned historical-data routing

Amazon Ads' June 8, 2026 Unified Reporting GA announcement documents history limits that depend on report grain: daily/weekly history is available up to 15 months, while monthly/yearly/summary history can extend up to 6 years. Amazon's September 1 migration guidance separately documents retirement/deletion of legacy report-center history. Therefore a Skill profile that inherently compares pre/post windows should declare the need for historical performance data as part of its machine-readable decision contract, rather than relying on a caller to remember an extra gate input.

Repository adaptation:

- `post-change-review:outcome-review` now requires `campaign-performance-read` in addition to historical-availability observation;
- the same profile owns `data_requirements.campaign-performance-read.requires_historical_data = true`;
- `resolve_skill_capabilities.py` validates and emits profile-owned data requirements so callers can pass them unchanged into the connector runtime gate;
- no specific Amazon reporting generation is hard-coded because a valid outcome review may use any verified compatible generation/source.

No Amazon documentation prose, report schema, API implementation, or UI workflow is copied.


## 2026-09-19 exact history window + grain gate

Unified Reporting's published retention differs by grain: Amazon states that daily/weekly reporting can reach up to 15 months, while monthly/yearly/summary reporting can reach up to 6 years. Therefore `historical_availability_status = available` is insufficient to prove that a specific request is retrievable.

Independent repository adaptation:

- connector snapshots may expose `historical_windows[]` with exact `grain / available_from / available_through`;
- a task-level `data_requirements.history_window` identifies the requested date range and grain;
- the runtime gate requires an exact grain match and blocks a requested range outside the verified boundaries;
- an unobserved grain, missing boundaries, or ambiguous duplicate grain windows is `Unknown/Degraded`, not Unsupported and not zero;
- no Amazon retention constant is hard-coded into the evaluator. The connector snapshot carries the currently observed boundaries so platform changes can be represented without code changes.

Source facts are used only to justify the generic safety rule. No Amazon report schema, UI, API implementation, or prose is copied.


## 2026-09-19 task-level requirement merge

Exact history windows are task-specific and should not be frozen into a static Skill profile. Conversely, allowing each caller to hand-merge task constraints with profile policy creates a relaxation risk: a caller can accidentally omit `requires_historical_data=true` or overwrite a profile-owned reporting constraint.

The repository now treats profile policy and task intent as separate provenance layers:

- the profile owns stable minimum requirements;
- the task may explicitly add `required_reporting_generation`, `requires_historical_data=true`, or an exact `history_window`;
- task requirements must target a capability already required by the selected profile;
- task constraints can only strengthen the profile and cannot turn required history off or replace a conflicting profile reporting generation;
- the resolver emits a single merged gate envelope plus the profile/task provenance used to build it.

This is repository-owned control-plane logic. It does not infer requirements from natural-language task text, call Amazon Ads, or authorize writes.


## 2026-10-22 official migration-tool limitations (2026-10-12 update)

Amazon Ads' official *Migrate your scheduled reports to unified reporting* help article,
updated 2026-10-12, identifies limits that must not be conflated with a measured
zero or with the availability of all alternative reporting routes:

- The self-service migration tool covers active saved/scheduled report
  configurations from the last 24 months. This is **not** a promise that the
  underlying historical metric rows or requested date grains are retrievable.
- Some legacy configurations are not yet supported by that migration tool,
  including conversion-path, Amazon Attribution, benchmark, Sponsored Products
  budget, prompts, video, and certain retailer/placement reports. A failed
  configuration migration does **not** establish that the same business metric
  is absent from every other report/API/export.
- Fields without equivalents can be omitted. In particular,
  `topOfSearchImpressionShare` was available at keyword, targeting and campaign
  grains in legacy reports, but the migration documentation currently describes
  campaign-grain support in unified reporting. Never substitute a campaign-grain
  value for a missing keyword/targeting-grain observation.
- The vendor currently lists 2026-12-17 as the legacy creation/edit cutoff
  and 2026-12-31 as shutdown/deletion. These are vendor-maintained dates, not
  constants for a runtime decision gate.

**Decision boundary:** preserve report generation, metric definition, source,
requested grain, time/date semantics, connector capability, and historical
availability separately. A dropped field, unsupported migration configuration,
or unavailable historical artifact remains `Unsupported`/`Unknown` evidence,
not zero. Verify an alternative source and its comparability before using it.

**Scope and rights:** documentation-only factual clarification; existing
lineage, capability and report-coverage gates already express the general
fail-closed rule. No new Skill, provider schema, migration automation, live
write, vendor code, prompt, template or workflow is imported.

Source (official vendor help, updated 2026-10-12):
https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A
