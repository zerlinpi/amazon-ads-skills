# Global Sponsored Products 207 receipt and readback evidence

This is a **read-only, single-item campaign-update** evidence contract. Use it in post-change review when an external, separately authorized Executor has already attempted a Global Sponsored Products campaign update. The helper `scripts/evaluate_global_sp_readback.py` never calls Amazon Ads, mutates accounts, retries requests, or reconciles Executor idempotency.

## Platform facts and scope

Amazon Ads' [Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) documents HTTP **207** multi-status receipts for create/update/delete with per-request-index `success`, `error`, and `partialSuccess`. Query returns HTTP **200** with `nextToken` pagination. A global campaign may override `state` for individual marketplaces via `marketplaceConfigurations`; the top-level state is not every marketplace's configured state. Query `status.deliveryStatus` is delivery health, not the configured state. Some query status marketplace identifiers are marketplace IDs rather than ISO country codes.

Those facts are platform behavior, **not proof** that a particular connector can expose all required fields. A trusted external adapter must produce source-supported, identity-verified **effective configured state per marketplace**, resolving top-level state and any overrides using the actual query evidence. It must not guess from delivery status, infer unsupported marketplaces, or treat a missing override as evidence without the complete global query context.

## Normalized input

Call `python -m scripts.evaluate_global_sp_readback < normalized-evidence.json`. This tool consumes one **single request item** only; batch receipts with additional indices return `Unknown` rather than a false batch-wide confirmation.

The normalized JSON envelope contains:

- `request`: nonempty `global_account_id`, `campaign_id`, unique `marketplaces` (one consistent country-code namespace), `expected_effective_states` keyed exactly by those marketplaces, and RFC3339 `completed_at`.
- `receipt`: integer `http_status: 207` and all three `success`, `error`, `partialSuccess` arrays, with exactly one unique `index: 0` across the arrays. Receipt status alone never proves readback.
- `readback`: matching global-account/campaign identity, source-system/acquisition-channel/connector identity, RFC3339 `observed_at` strictly later than request completion, `coverage_status: Complete`, `pagination_status: Complete`, `capability_status: Supported`, and `marketplace_states` with one source-observed `effective_state` for **every** requested marketplace. A trusted adapter must prove that normalized country codes map to the source's marketplace identifiers.

`effective_state` is the source-supported configured `ENABLED`, `PAUSED`, or `ARCHIVED` state, not delivery status or performance. `Unknown`, missing, partial, unsupported, and unverified observations are not zero or paused.

## Conservative classifications

- `Confirmed`: only an unambiguous single-item 207 success plus complete, newer, same-identity query readback with every marketplace configured as intended. **Not** proof of campaign delivery, performance, or causal lift.
- `Partial`: a valid 207 receipt contains an `error` or `partialSuccess`; no batch-wide success inference, even if a later snapshot appears to match.
- `Drifted`: the successful receipt has complete, source-supported readback but one or more marketplace effective configured states differ.
- `Unknown`: malformed/ambiguous receipt, unsupported status, missing or incomplete query, stale evidence, source or account identity mismatch, duplicate/missing marketplace, or invalid configured state.

This helper is not a generic Global SP request/response validator, not a multi-item reconciliation engine, and not a replacement for the versioned material-control comparator. Preserve the raw receipt and query evidence externally. The normalized envelope is an input assertion by the trusted connector/adapter, not cryptographic verification of that adapter.

## Copyright and adoption boundary

Only independently expressed, verifiable API facts from Amazon's copyrighted guide informed this repository-owned implementation. No Amazon source code, API schema, request/response examples, prompt, template, or workflow was copied. No third-party MCP dependency or Amazon Ads write capability was added.
