# Amazon Marketing Stream dataset coverage

Load this reference only when a decision uses Amazon Marketing Stream or another dataset-subscription push path for intraday evidence. It complements `data-lineage.md`; it does not replace metric semantics, attribution maturity, connector capability, or report-coverage checks.

## Dataset-level observability

Amazon Marketing Stream is a push-based acquisition channel. Treat each subscribed dataset as its own observation path. A successfully delivered dataset does not prove that a sibling dataset is subscribed, healthy, complete, or semantically available.

Current Amazon reference implementations expose distinct dataset subscriptions for Sponsored Products traffic and conversion streams (and corresponding Sponsored Brands / Sponsored Display streams), alongside budget usage and entity/change datasets. Therefore:

```text
traffic dataset delivered
!= conversion dataset delivered
!= conversion metric is zero
```

Likewise, conversion messages arriving does not prove traffic coverage for the same entity/hour.

For decision-relevant Stream evidence, preserve when available:

- `stream_dataset` — exact dataset identity, not merely `Amazon Marketing Stream`;
- `subscription_status` — verified active, inactive, unknown, or equivalent source state;
- `delivery_status` — observed delivery health/completeness for the requested window;
- destination/consumer identity when multiple SQS/Firehose or downstream paths exist;
- profile/marketplace/region and entity scope;
- event hour/timezone and ingestion/receipt time;
- latest observed event hour / `available_through`;
- duplicate/deduplication and replay handling when relevant;
- backfill or attribution-maturity state for conversion outcomes.

Do not infer `subscription_status=active` merely because another Stream dataset is flowing. Do not infer `delivery_status=complete` from a healthy destination alone.

## Missing sibling dataset is not zero

If traffic is present for an hour but the conversion sibling dataset is absent, unknown, delayed, unsubscribed, or unhealthy, that is an observability gap. It is **not evidence** that orders, sales, or other conversion outcomes are zero. The reverse applies to traffic metrics when only conversion delivery is verified.

Before computing CTR/CVR/ACOS/ROAS or making intraday bid/budget recommendations from joined Stream datasets:

1. verify every required dataset subscription independently;
2. verify delivery coverage for the same profile, marketplace, entity scope and hour window;
3. verify metric/date-attribution semantics and conversion maturity;
4. reconcile duplicate/replayed/late messages according to the trusted ingestion contract;
5. if any required sibling dataset is `Unknown`, `Partial`, delayed, or unavailable, downgrade to `Directional`, `Missing Data`, `Alternate Source`, `Hold`, or `Manual Review` rather than zero-fill.

A daily or Unified Reporting source may be an alternate source only when its grain, semantics, maturity and requested decision question are compatible. Do not silently replace an intraday question with a coarser daily answer just to avoid a Stream coverage gap.

## Action boundary

This reference is measurement-only. It does not authorize Amazon Ads writes. Keep recommendations in Read-only / Suggest / Shadow unless an external authorized Connector/Executor separately satisfies the repository's execution-safety contract.
