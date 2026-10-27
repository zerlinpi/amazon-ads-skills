# Intervening event observation identity collisions — 2026-10-27

## Verified gap and priority

Starting main `ea0f3daed46f44a9eef17fd7d4fa71d3e4f5b79a` had successful main CI, no open PR and 15 Skills. Five relevant historical branches were behind main. The comparator's optional positive `control_events` path enforced unique event IDs, event time within the observation window, source/scope identity, and valid material states. It did not cross-check a concrete `source.readback_id` reused by two event rows, nor incompatible before/after transitions for one material control at the exact same instant.

Two independently asserted rows can each look well-formed while contradicting the identity of one source observation or the value of one simultaneous control transition. Classifying their apparent change as `Confounded` gives stronger evidence than the inputs support. This is a narrow internal contradiction, not an assertion that the optional event log is exhaustive.

Gap ranking: P0 external authenticated full-window event coverage (not implementable from synthetic endpoints); P1 **confirmed event identity/time contradiction** (this patch); P2 cross-control interactions and connector capability lineage; P3 profitability/retail confounders. The patch does not claim to solve P0.

## RED → GREEN

- RED tests-only `f2002b28626e99194e2b333d7932c57bf0eb7fab`, [Actions #40506427213](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40506427213): **2061 tests / 4 FAIL**, seven new compatibility cases passed.
- Minimal production fix `d0ee5795c0aab844a7dcfc090519b20918227106`, [Actions #40506525853](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40506525853): **2061/2061 PASS**, Skill and Eval validators PASS.
- Eleven synthetic deterministic tests: same ID/different time, nanosecond mismatch, conflicting same-control same-instant before/after, offset-equivalent UTC, distinct IDs, omitted IDs, valid multi-control same-time, identical duplicate transitions, and non-exhaustive discontinuous event chains.
- Implementation keeps per-readback exact UTC event instant and per-(control, instant) normalized before/after pair. For SP rule/budget lists, comparison uses the existing identity-keyed rule-member equality, not adapter row order.

## Official evidence and what it does not prove

Amazon Ads [schedule-based Sponsored Products bid rules (2023-11-06)](https://advertising.amazon.com/resources/whats-new/schedule-based-bid-rules-available-for-sponsored-products), [event-based bid rules (2025-01-02)](https://advertising.amazon.com/resources/whats-new/event-based-bid-rules-for-sponsored-products-advertisers), and [budget rules (2021-08-12)](https://advertising.amazon.com/resources/whats-new/dynamic-budget-control) establish that controls may change with schedules/events. [Amazon Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq) documents restated totals, record-level deduplication, cadence versus grain, and multi-part delivery. These sources do not define this repository's normalized event/readback identity, prove complete event capture, or establish causal lift. The new check is an independently implemented conservative evidence rule.

## External candidate and copyright boundary

Sampled GitHub metadata on Oct 27: OpenLineage 2727 stars / Apache-2.0 / nonfork / pushed Oct 25; OpenEvals 1233 / MIT / nonfork / Oct 22; KuudoAI amazon_ads_mcp 74 / MIT / nonfork / Oct 14; Agent Skills 26691 / Apache-2.0 / nonfork / Aug 9; MCP Servers 91598 / NOASSERTION / nonfork / Oct 27. OpenLineage had mixed recent CI, OpenEvals sampled PR runs were action_required, and KuudoAI had successful scheduled runs; selected open PRs were inspected. No exhaustive security/code/issue/mirror/transitive-license review was performed. Existing stdlib is sufficient and no external project authenticates this event stream, so all are rejected for integration. NOASSERTION grants no reuse rights; no third-party code, prompt, schema, workflow, template or protected prose was copied. [Reddit automation anecdote, Sep 18 2026](https://www.reddit.com/r/AmazonFBA/comments/1wjcgd4/) is an unverified operator hypothesis only.

## Safety and remaining work

No Skill, schema, dependency or live Amazon Ads write was added. Valid zero/false, absent optional event readback, distinct observation IDs, offset-equivalent instants, identical duplicate transitions and simultaneous different-control changes remain compatible. Non-adjacent event states are not treated as contradictions because the log is non-exhaustive. Missing/unsupported/partial/unknown are not zero; causal conclusions require separate retail, attribution, account/connector identity and marginal-profit evidence. Read-only/Suggest/Shadow default; authorized external Executor owns live writes/retries/idempotency/reconciliation.

Next genuine gap: an externally verifiable, time-bounded event capture and restatement/coverage attestation (including missed windows and source authenticity), rather than treating empty `control_events` as continuity.
