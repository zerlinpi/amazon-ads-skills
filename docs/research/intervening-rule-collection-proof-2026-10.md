# Optional paired completeness evidence for mid-window SP rule collections — 2026-10-28

## Gap and evidence boundary

The v1.110.0 comparator validated endpoint nested rule-list completeness but its positive mid-window `control_events` had no way to carry separate before/after enumeration, pagination and capability evidence. A valid observed rule transition could still originate from a truncated adapter listing. The event list itself is optional and non-exhaustive. Endpoint snapshots cannot certify uninterrupted rule execution.

## Decision

Add an **optional** `rule_collection_evidence` envelope on positive normalized SP rule/budget events. Each of `before` and `after` must independently cover `schedule_rules` plus `event_rules`, or `active_budget_rules`, with Complete enumeration, Complete pagination and Supported capability. Explicit incomplete, malformed, one-sided or unmapped evidence is `Unknown`; complete proof preserves a valid observed confounder. Omitted legacy proof remains accepted for compatibility, **not** as proof of complete collection enumeration. No full-window capture, source authentication, rule execution, retail attribution or causality is inferred.

The source mapping and the proof values are adapter-owned claims, not Amazon API-native event fields. Before asserting full-window stability, an external authorized acquisition system must independently verify source lineage, pagination, missing time intervals, restatement/deduplication and relevant control scope. Do not convert Unknown/Partial/Unsupported/Missing to zero.

## RED→GREEN

- Initial main: `3c0ae4f70455a375714b8fb3ccf2a49427e232ee`; latest main CI SUCCESS, open PRs zero. Related sampled branches were all behind main.
- RED tests-only: `fa2c5e5d034ff5858fc5dd4cf58e68feef702815`; [Actions #40553399677](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40553399677): 2099 tests, 2 FAIL, 1 ERROR. Old validator rejected valid new proof and schema lacked its property.
- GREEN: comparator `224a7e0252a39ddfdb725c419c8fb9b4d327a7db` and schema `7e5842eadff32ed6c88b981d55f05cb7fd175b1a`; [Actions #40553566614](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40553566614): 2099 unit tests PASS, 15 Skills PASS, 55 Evals PASS.
- Thirteen deterministic synthetic tests cover accepted complete proof, rejected partial/truncated/unsupported/missing/unmapped proof, legacy compatibility and schema. No Amazon Ads account access or write.

## Primary sources, candidates and copyright

Amazon's [schedule-based bid rules](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [event-based bid rules](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers) and [hours-of-day budget rules](https://advertising.amazon.com/resources/whats-new/hours-of-day-available-for-schedule-based-budget-rules) demonstrate temporal control changes. The [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) discusses delivery, per-record versions, restatement, and null/zero distinction. None specifies this normalized event proof structure or proves complete historical capture.

Reviewed GitHub repository metadata Oct 28: OpenLineage Apache-2.0 2728 stars; OpenEvals MIT 1233; KuudoAI Amazon Ads MCP MIT 74; Agent Skills Apache-2.0 26700; MCP Servers NOASSERTION 91604. All nonfork; sampled activity but not full source/security/dependency/issue/PR/CI audits. Adopt abstract provenance and deterministic eval principles only; reject importing frameworks because they do not provide authenticated Ads history and existing Python logic suffices. No third-party code, schema, prompt, workflow or template copied. Anecdotal operator/Reddit strategies are hypotheses, not platform rules.

## Next gap

External full-window event coverage and revision-proof collection membership. Opt-in per-event proof is not a substitute for a verified event-source capture horizon. A future integration must explicitly bind batches, time windows, account/campaign identity, revisions and pagination to observed source records before making continuous-stability claims.
