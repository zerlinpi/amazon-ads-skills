# Explicit rule activation evidence in Sponsored Products — 2026-10-25

## Verified gap
The previous comparator validated unique rule IDs and numeric bid/budget modifiers but did not validate an explicitly supplied activation status. Two snapshots with the same rule and `activation_status: "Unknown"` could return `Treatment Isolated` for an otherwise isolated base-bid or budget change. One-sided optional activation evidence could be treated as a changed control rather than incomplete evidence.

## Sources and limits
Amazon Ads' 2023-11-06 schedule-based bid-rule announcement documents time-of-day, weekday and date-range behavior:
https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products

Amazon Ads' 2025-01-02 event-based bid-rule announcement documents predefined increases around marketplace events:
https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers

These support the narrow claim that configured rule amounts are not the same thing as activation or timing. They do not specify this repository's normalized member fields or guarantee that any connector exposes status or a complete temporal history.

A July 2026 Reddit anecdote about rule-based ROAS and placement losses was considered only as a risk hypothesis, not causal or platform evidence. Open-source candidates KuudoAI/amazon_ads_mcp (MIT), hyperfx-ai/marketing-skills (MIT), promptfoo/promptfoo (MIT), and OpenLineage/OpenLineage (Apache-2.0) were reviewed for metadata, tests and recent public CI. None supplies authenticated Amazon rule activation evidence needed for this deterministic comparator gap; no code, prompts, schemas, templates or workflows were reused. No-license or restricted sources were not copied.

## Independent change and RED→GREEN
Add optional `activation_status` member validation for normalized schedule/event bid rules and active budget rules. Only `active`, `inactive`, and `scheduled` are recognized read-side values. An explicit Unknown, Unsupported, malformed or unmapped status returns Unknown. If the same rule_id appears on both sides, the status field must not appear on only one side. Both-absent legacy fields remain compatible, but cannot prove continuous activation.

RED test-only commit b4bfdb12d5d86b53e7a33be9a5887201e5eaf6f1: 1233 tests, 13 FAIL (Actions 40151792978). Minimal fix commit 0fe79be0651d3e301464bcba6593a04d22b0cbac: 1233/1233 PASS, 15 Skill and 55 eval validations PASS (Actions 40151826044).

No Amazon Ads write, connector auth, retry, idempotency, executor, auction formula, third-party dependency, or additional Skill. This does not establish activation continuously over an interval, campaign eligibility or Amazon API-native status enums.
