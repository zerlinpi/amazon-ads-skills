# Global SP ad-group default-bid batch readback (one update call)

Use `python -m scripts.evaluate_global_sp_adgroup_batch_readback < evidence.json` with a **trusted, normalized** external Executor/adapter evidence envelope only. This is a read-only classifier, not an Amazon Ads client or an execution/retry/reconciliation service.

## Platform basis and limits

The [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) describes indexed HTTP 207 `success`, `error`, and `partialSuccess` entries for update calls, independent paginated ad-group queries, and marketplace-specific native-currency default bids. These are public API facts; the `request_id`, source, capability, coverage, and timing fields below are **external normalized evidence assertions**, not native Amazon API field guarantees.

This gate supports one homogeneous Global SP **ad-group** update call with multiple distinct ad groups under one Global Account. A single ad-group request can cover multiple marketplaces. It does not support repeated updates to the same ad group within a batch (one later readback cannot prove intermediate states), mixed resource types, target bid changes, campaign/placement controls, cross-account batches, or retry reconciliation.

## Input contract

- `requests`: nonempty **ordered** array of the same single-ad-group request objects required by [global-sp-adgroup-bid-readback.md](global-sp-adgroup-bid-readback.md). Each has a unique external `request_id` and unique global-account/campaign/ad-group identity; all share one `global_account_id`. Each request's `expected_marketplace_default_bids` covers exactly its declared `marketplaces`, with finite nonnegative **plain decimal strings** and native currency codes.
- `receipt`: `resource_type: "ad_group"`, integer `http_status: 207`, explicit `success`, `error`, and `partialSuccess` arrays. Each entry has an integer `index` identifying the original ordered request; their union covers every index exactly once. Optional returned index-level identity, marketplace list, or `ad_group` object cannot contradict the bound request. Optional batch-level `global_account_id` must match the one Global Account.
- `readbacks`: array of `{ "request_id": "...", "readback": { ... } }` exactly once for **each successful item** and none for error/partialSuccess items. The nested `readback` is independently acquired, post-completion, fully paginated, source-identified, capability-supported single-ad-group query evidence with **all requested marketplaces**. Readback array order is irrelevant. Missing, extra, duplicate, stale, partial, unsupported, or identity-conflicting evidence returns `Unknown`.

Each successful item is evaluated by the existing `evaluate_global_sp_adgroup_bid_readback` single-item gate. The batch gate cannot replace it with a campaign state or target bid proof, infer zero from missing fields, or perform FX conversion.

## Conservative classification

Results contain `application_status`, `reasons`, and indexed `items` with `request_id`, per-item status, and reasons.

- `Confirmed`: **every** item is independently confirmed with complete matching native-currency marketplace default bids.
- `Unknown`: malformed/ambiguous batch or any item with unknown, unsupported, stale, incomplete, or conflicting evidence. Unknown takes precedence over Partial/Drifted.
- `Partial`: a well-formed batch with one or more indexed `error` or `partialSuccess` items and no Unknown.
- `Drifted`: all items otherwise known, but at least one independently observed default bid differs from intended amount/currency, with no Partial/Unknown.

This conservative precedence is repository policy, **not** an Amazon Ads status precedence rule. A configured default-bid confirmation is not proof of auction bids, spend, profitability, incrementality, or causal lift. Real writes, retries, idempotency, reconciliation and cross-resource workflow status remain with the separately authorized external Executor.

## Copyright boundary

This repository-owned normalized evidence contract and implementation are independently authored. No third-party code, API sample payloads, prompts, schemas, workflows or templates were copied.
