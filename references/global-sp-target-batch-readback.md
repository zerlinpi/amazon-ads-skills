# Global SP positive target batch readback (single update call)

Use `python -m scripts.evaluate_global_sp_target_batch_readback < evidence.json` **only** with a trusted external authorized Executor/adapter's normalized evidence. The tool is read-only and does not send Ads API requests, retry, reconcile, or infer auction bids.

## Platform facts and scope

[Amazon Ads Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) documents target update HTTP 207 with `success`, `error`, `partialSuccess` indexed by request order and separately paginated target queries. This helper supports one homogeneous batch of positive KEYWORD/PRODUCT target bid updates under one Global Account. Each target is one marketplace. Campaign, ad-group, placement, mixed-resource, cross-account, negative, THEME and other unverified intents are not covered.

## Trusted normalized input

- `requests`: nonempty **ordered** list of v1.35.0 single-target `request` objects (see `global-sp-target-bid-readback.md`). Every `request_id` and target identity (global account/campaign/ad group/target/marketplace) must be unique. All requests must share one `global_account_id`. Duplicate updates to the same target in one call are rejected because one later readback cannot prove intermediate states.
- `receipt`: `resource_type: "target"`, integer `http_status: 207`, explicit `success`, `error`, `partialSuccess` arrays. Every entry has a **real integer** `index`; the union must cover exactly `0..len(requests)-1`, with no duplicates. Any optional identity or target attributes explicitly returned by the adapter cannot contradict the indexed request. A receipt is not a readback.
- `readbacks`: list of `{request_id, readback}` entries, exactly one for **each success item** and none for error/partialSuccess items. The `readback` is the complete, independently acquired v1.35.0 target query evidence, including matching identity, source, timestamp strictly after completion, pagination/coverage/capability and native-currency decimal target bid. Array order is irrelevant; `request_id` binds the item. Missing, extra, duplicate or conflicting rows yield `Unknown`.

Normalized correlation fields are external adapter assertions, not claims that Amazon's native API supplies these names. The adapter must preserve the original ordered batch and actual 207 indices; it must not synthesize a success, readback, capability, or missing zero. No FX conversion.

## Classification

The result includes `application_status`, `reasons`, and `items` with `index`, `request_id`, item `application_status` and `reasons`.

- `Confirmed` only when **all** indexed items have complete, independently confirmed target bid readbacks.
- `Unknown` when any item has unverified or contradictory evidence, or the batch structure/index/readback mapping is ambiguous. Unknown outranks Partial/Drifted to prevent false global certainty.
- `Partial` when an otherwise well-formed batch includes an error or partialSuccess 207 item.
- `Drifted` when all items are otherwise known but at least one independently observed bid differs from its expected native-currency amount or currency.

A `Confirmed` configured bid is not proof of auction bid, advertising performance, or causal outcome. Combined multi-resource workflows and retries/idempotency/reconciliation belong to the authorized external Executor. The helper contains no live Amazon Ads write capability.

## Copyright

Independently authored contract and implementation. Only public platform facts and abstract evidence-integrity principles were used; no third-party code, API example payload, schema, prompt, workflow or template was copied.
