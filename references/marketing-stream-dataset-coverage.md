# Amazon Marketing Stream dataset coverage

Load this reference only when a decision uses Amazon Marketing Stream or another dataset-subscription push path for intraday evidence. It complements `data-lineage.md`; it does not replace metric semantics, attribution maturity, connector capability, or report-coverage checks.

## Dataset-level observability

Amazon Marketing Stream is a push-based acquisition channel. Treat each subscribed dataset as its own observation path. A successfully delivered dataset does not prove that a sibling dataset is subscribed, healthy, complete, or semantically available.

Legacy Marketing Stream v1 Amazon reference implementations expose distinct dataset subscriptions for Sponsored Products traffic and conversion streams (and corresponding Sponsored Brands / Sponsored Display streams), alongside budget usage and entity/change datasets. Therefore, **for v1 dataset families**:

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

## Stream v1 versus Stream v2 — separate delivery contracts

Do **not** treat `Amazon Marketing Stream` as a single version-independent ingestion semantic. Resolve `stream_generation` and exact dataset/report identity before interpreting totals, missing rows or restatements.

- **Stream v1** delivers per-hour **delta** values, with `idempotency_id` used to deduplicate delivery retries. Legacy v1 traffic/conversion streams can be separately subscribed; a healthy traffic subscription does not prove conversion coverage.
- **Stream v2** delivers **total values per time window**, not changes since the last delivery. Restated records may arrive again with a replacement total, including older or out-of-order delivery. A resubscription also backfills the dataset's available restatement period. V2 deliveries use S3 Parquet files and SQS notifications.
- For Stream v2, a decision-safe reduced view selects the **highest `streamBatch.version` for each full source-defined record key** before aggregation. A file arrival timestamp, latest notification, report date or highest version globally is not a substitute for version selection **per record**. Do not add successive totals together or retain a late-arriving older version as current.
- Amazon's Stream v2 performance dataset `ads-performance-v1` unifies advertising products; `adProduct.value` distinguishes Sponsored Products, Sponsored Brands, Sponsored Display and DSP performance rows. The v1 **sibling subscription** rule cannot be applied blindly to v2. Establish coverage for the actual v2 dataset plus required metrics, dimensions, profile/marketplace, grain and restatement window instead.
- Stream v1 and v2 are **not interchangeable**: do not deduplicate v2 by the v1 `idempotency_id` contract, and do not treat v1 delta rows as v2 per-window totals. Migration comparison must reconcile compatible windows, grains, event/date semantics, product scopes, backfill and maturity rather than summing both generations as independent performance.

For a decision that **directly sums base metrics from Stream v2 records**, load `../scripts/evaluate_metric_aggregation_gate.py` and supply `acquisition_channel=amazon_marketing_stream_v2` plus a source-supported `stream_record_reconciliation` envelope:

```json
{
  "acquisition_channel": "amazon_marketing_stream_v2",
  "operation": "sum",
  "metric_semantics": {"aggregation_semantics": "additive"},
  "source_relation": "disjoint",
  "stream_record_reconciliation": {
    "record_identity_coverage": "Verified",
    "highest_version_per_record": "Verified"
  }
}
```

Both properties must be verified against the **complete relevant record identity and version history**; unobserved, Partial, Unsupported or Unknown provenance stays `Unknown` and **never becomes permission to sum**. A successful version-reconciliation gate does **not** by itself prove SQS/S3 delivery completeness, metric semantics, campaign/profile identity, full logical population, retention, conversion maturity or causal comparability. Preserve those gates separately.

The gate is a read-only **evidence check**. Parquet ingestion, file/notification handling, record-key design, versioned upserts, SQS retries and idempotent storage belong in an authorized external Connector/warehouse, not inside this Skills repository.

## Missing sibling dataset is not zero

For a v1 dataset family, if traffic is present for an hour but the conversion sibling dataset is absent, unknown, delayed, unsubscribed, or unhealthy, that is an observability gap. It is **not evidence** that orders, sales, or other conversion outcomes are zero. The reverse applies to traffic metrics when only conversion delivery is verified.

Before computing CTR/CVR/ACOS/ROAS or making intraday bid/budget recommendations from joined Stream datasets (or the corresponding required v2 dataset fields):

1. verify every required dataset subscription independently;
2. verify delivery coverage for the same profile, marketplace, entity scope and hour window;
3. verify metric/date-attribution semantics and conversion maturity;
4. reconcile duplicate/replayed/late messages according to the trusted ingestion contract;
5. if any required sibling dataset is `Unknown`, `Partial`, delayed, or unavailable, downgrade to `Directional`, `Missing Data`, `Alternate Source`, `Hold`, or `Manual Review` rather than zero-fill.

A daily or Unified Reporting source may be an alternate source only when its grain, semantics, maturity and requested decision question are compatible. Do not silently replace an intraday question with a coarser daily answer just to avoid a Stream coverage gap.

## Action boundary

This reference is measurement-only. It does not authorize Amazon Ads writes. Keep recommendations in Read-only / Suggest / Shadow unless an external authorized Connector/Executor separately satisfies the repository's execution-safety contract.
