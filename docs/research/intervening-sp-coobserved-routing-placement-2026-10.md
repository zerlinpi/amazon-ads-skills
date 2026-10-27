# Co-observed Sponsored Products routing/placement event coherence — 2026-10-27

## Verified gap and priority

At initial main `7bc6e2bf97898039cda469ee36f8b7bff66301d9`, required push CI was successful, no PR was open, and four sampled historical branches were behind main. The comparator already rejects an endpoint Sponsored Products state combining `ACROSS_RETAILERS` routing and `amazon_business` placement. The positive mid-window `control_events` validator checked each control independently but did not join different control types sharing the same concrete `source.readback_id`. A single readback could thus assert incompatible placement/routing before or after states yet produce `Confounded` instead of `Unknown`.

Priority: P1, internal cross-control evidence contradiction; not a substitute for P0 complete event-window coverage, authenticated source, or realized marginal profit analysis.

## Deterministic RED → GREEN

Synthetic event fixtures use an observed SP base-bid endpoint change plus two mid-window positive control transitions at the same event time. A shared concrete event readback asserts across-retailer routing and an Amazon Business placement modifier in the same phase. RED `ea99994252628a83800a341113dac2310846e166` ([Actions #40515556189](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515556189)) had 2066 tests with 1 FAIL: old classifier returned `Confounded` instead of `Unknown`. The initial production fix `2821101d95f24551f458a48b649909e8cd346635` ([Actions #40515691037](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515691037)) uncovered a pre-existing empty-event compatibility test ERROR due to a newly unbound variable. Corrected `54d03a4035a4abbc299d8f2bff14c7b6d316ccc8` ([Actions #40515711043](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40515711043)) passed all 2066 tests and both validators. Additional pre-transition contradiction test `5c94bc61efa108ec468b4fcf65586b19a550fdeb` was added before final PR validation.

The minimal fix groups only positive events with the same concrete source readback and checks the incompatible routing/placement combination independently for before/after phases. Separate/missing readbacks remain compatible; coincident timestamps do not create an inferred join. Valid Amazon Store and no-business-placement cases remain confounders. No new Skill, schema field, dependency or Amazon Ads write.

## Sources and copyright

Official Amazon Ads pages: [Amazon Business exclusive Sponsored Products](https://advertising.amazon.com/en-gb/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product), [Sponsored Products across retailers](https://advertising.amazon.com/solutions/products/sponsored-products-across-retailers), [Amazon Business advertising](https://advertising.amazon.com/channels/amazon-business), [Marketing Stream v2 FAQ](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/faq). They distinguish control surfaces and delivery semantics, but do not specify this repository's normalized event structure or authenticate event logs.

Sampled OpenLineage (Apache-2.0), OpenEvals (MIT), KuudoAI Amazon Ads MCP (MIT), Agent Skills (Apache-2.0), MCP Servers (NOASSERTION); prior SOURCES reviews already cover them. No dependency added or external code/prompt/schema/workflow/template copied. Reddit operator experience is hypothesis-only.

## Remaining gaps

P0: independently authenticated full-window event coverage and versioned restatement reconciliation; P1: additional cross-control consistency and eligibility evidence; P2: source/metric/date/grain/currency/attribution identity; P3: cross-campaign interference and marginal profit. Missing/unsupported/partial/unknown never become zero. Read-only/Suggest/Shadow default, external authorized Executor for writes/retries/idempotency/reconciliation.
