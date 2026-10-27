# Unproven nested SP rule-event collections — 2026-10-28

## Evidence and gap

The main comparator already checks nested collections inside endpoint readbacks using independent JSON-pointer completeness evidence. In v1.111.0 the new optional `rule_collection_evidence` only certifies the *outer* schedule/event/budget rule list of a positive mid-window `control_events` transition. A rule member can contain a second list without an independent collection proof; the comparator previously classified that event as a verified `Confounded` control transition. A declared Complete outer list cannot prove the inner list's pagination, membership or acquisition capability. The extra field is synthetic normalized adapter data, not a documented Amazon Ads native field.

## Minimal safety behavior

Reuse `_deep_extra_collection_problem` on each event before/after rule state with no descendant proof. It permits the registered direct outer lists but returns `Unknown` for deeper arrays, including empty ones, inside schedule/event/active-budget rule members. Do not infer that a nested array is absent or complete, and do not invent a new optional event proof format. Preserve valid flat member data, top-level complete empty rule collections and legacy non-nested events. This is a material MINOR fail-closed decision-safety improvement, not a breaking schema migration.

## Deterministic verification

RED tests-only commit `dfbd5081e706f9e80c06518e2c3a4f3a9a71c497`, [Actions #40562520498](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40562520498): 2107 tests, four expected FAIL on the old comparator; four compatibility cases PASS. Minimal production change `38bc8e2c68150f0472954aa82d2f3cc345f6bd59`, [Actions #40562550569](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40562550569). The latest PR HEAD must independently pass unit, 15-Skill and 55-eval validators before merge. No Amazon Ads mutation or API authentication was performed.

## Primary sources and license boundary

Amazon's [schedule-based bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products) and [Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) explain time-varying controls and why data delivery, restatements and unknowns must be distinguished. They do not define the internal event structure or certify full-window event capture. Reviewed previously documented OpenLineage, OpenEvals, Amazon Ads MCP, Agent Skills and MCP Servers metadata; no external code/prompt/schema/workflow was reused. Source metadata and rejection reasons are in `docs/SOURCES.md`.

## Remaining gap

Externally authenticated full-window event capture, event revision lineage and a versioned independent descendant-proof contract remain unimplemented. A Complete outer collection declaration does not establish any of these.
