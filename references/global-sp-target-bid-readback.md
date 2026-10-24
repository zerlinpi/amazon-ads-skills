# Global SP positive target bid readback (single marketplace)

Use `python -m scripts.evaluate_global_sp_target_bid_readback < evidence.json` only after an **external authorized Executor** has attempted one Global Sponsored Products target bid update. The helper is read-only and accepts trusted connector-normalized evidence, not raw Amazon API responses.

## Official facts and explicit limits

The [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) (checked 2026-10-24) describes `/adsApi/v1/update/targets` and `/adsApi/v1/query/targets` separately from campaigns and ad groups. Targets apply to **one marketplace**, while ad groups may span multiple. Manual positive keyword/product targets may have a `bid.marketplaceSettings` entry with native `currencyCode` and target `bid`. Create/update/delete return indexed HTTP 207; query uses HTTP 200 and `nextToken` pagination. Target bid is **not** the ad-group `defaultBid`, a realized auction bid, or a campaign/placement adjustment.

This narrow helper accepts only positive `KEYWORD` and `PRODUCT` targets with an explicit configured target bid. Negative targets, automatically generated `THEME` targets without an explicit bid, `PRODUCT_CATEGORY` targets, multi-item batches and any other unverified intent return `Unknown`. These limits describe **helper coverage**, not universal Amazon Ads eligibility. A connector must establish that the queried target bid field is actually supported.

## Trusted normalized input

- `request`: `resource_type: "target"`, nonempty `request_id` (external correlation), `global_account_id`, `campaign_id`, `ad_group_id`, `target_id`, single `marketplace` country code, `target_type: "KEYWORD" | "PRODUCT"`, `negative: false`, `completed_at` RFC3339, and `expected_target_bid: {currency_code, amount}`. `amount` is a precision-preserving, finite nonnegative plain decimal **string**; no JSON floats or implicit FX.
- `receipt`: matching `resource_type`, `request_id` and all four resource identities, integer `http_status: 207`, explicit `success`, `error`, `partialSuccess` arrays with exactly one unique `index: 0`. A normalized `success[0].target`, if supplied, cannot contradict target identity, type, negative status or marketplace. A success receipt is not independent readback.
- `readback`: `resource_type: "target"`, exact global account/campaign/ad group/target and single-marketplace identity, matching `target_type`, `negative: false`, nonempty `source.source_system`, `source.acquisition_channel`, `source.connector_id`, `observed_at` strictly after request completion, `coverage_status: "Complete"`, `pagination_status: "Complete"`, `capability_status: "Supported"`, and `target_bid` with the same `marketplace`, `currency_code`, `amount`, `evidence_status: "observed"`.
- If the bid row provides optional account/campaign/ad-group/target IDs, `target_type`, `negative`, `source` or `observed_at`, those values must agree with request/envelope. A row timestamp must be strictly after completion and no later than the envelope timestamp. Missing optional row metadata inherits the trusted envelope assertion; explicit conflicts are never ignored.

All normalized IDs and `request_id` correlation are repository/Executor assertions, **not** claims that Amazon's raw API supplies these exact field names. A trusted adapter must map the raw API's native bid without loss of precision and prove query pagination/coverage/capability; the helper cannot independently authenticate an adapter.

## Result meanings

- `Confirmed`: bound single-item target 207 success and complete newer independent configured target bid query agree in native currency.
- `Partial`: valid bound 207 `error` or `partialSuccess` item.
- `Drifted`: complete observed target bid differs in native currency or amount.
- `Unknown`: missing/partial/unsupported evidence, identity or type conflict, wrong marketplace, invalid monetary value, stale query, extra `expected_*` intent, malformed or multi-item receipt.

`Confirmed` is only a **configured target bid** confirmation. It is not a guarantee of campaign state, ad-group default bid, actual auction price, attribution, performance improvement, or causal effect. Combined multi-resource changes require independent confirmations and separate review. No Ads writes, retries, rollback, idempotency implementation, or reconciliation are performed here.

## Source and copyright boundary

The contract and implementation are repository-owned, independently authored. Only publicly verifiable Amazon platform facts and abstract evidence-integrity principles were used. No vendor/third-party code, API example payload, schema, prompt, workflow, template or practitioner bidding formula was copied.
