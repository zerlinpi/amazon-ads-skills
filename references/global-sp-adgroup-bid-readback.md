# Global SP ad-group marketplace default-bid readback

This is an **independent, read-only, single-item ad-group update** evidence contract. It is not the campaign configured-state/budget gate and not a target-bid verifier. Use `python -m scripts.evaluate_global_sp_adgroup_bid_readback < evidence.json` only after a separately authorized external Executor has attempted a Global Sponsored Products **ad-group** update.

## Official platform facts and scope

The [Amazon Ads Global Sponsored Products API guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) (checked 2026-10-24) describes `/adsApi/v1/update/adGroups` separately from campaign and target updates. Ad groups can carry a `bid.marketplaceSettings` collection with native `currencyCode` and `defaultBid` per marketplace. Create/update/delete use indexed HTTP 207 receipts; query uses HTTP 200 and `nextToken` pagination. The global account ID is distinct from a legacy profile-scope header. A child's marketplaces must be a subset of its parent's. These are platform facts, **not evidence** that a specific connector exposes complete ad-group bid query fields.

The helper consumes **normalized evidence**, not raw Amazon API payloads. A trusted adapter must map raw query `defaultBid` into `amount` as a precision-preserving plain decimal string, normalize the marketplace country-code identity from source-supported evidence, and attest coverage/capability. Never infer ad-group default bid from campaign state, target bid, CPC, delivery status, or an absent value.

## Input contract

- `request`: `resource_type: "ad_group"`, nonempty `request_id` (external Executor correlation), `global_account_id`, `campaign_id`, `ad_group_id`, distinct `marketplaces` (two-letter uppercase country codes), `completed_at` (RFC3339 instant), and `expected_marketplace_default_bids` keyed **exactly** by requested marketplace. Each bid has `currency_code` (three uppercase letters) and `amount` (finite nonnegative plain decimal string). The helper does not assert platform minimums, valid currency-country combinations, or bid eligibility.
- `receipt`: `resource_type: "ad_group"`, matching `request_id`, `global_account_id`, `campaign_id`, `ad_group_id`, integer `http_status: 207`, and all `success`, `error`, `partialSuccess` arrays. Exactly one unique `index: 0` must occur across the arrays. This binding is an **external adapter/Executor assertion**, not a claim that Amazon returns these normalized correlation fields. If an optional normalized `success[0].ad_group` is present, its explicit identity cannot contradict the request.
- `readback`: `resource_type: "ad_group"`, matching global-account/campaign/ad-group identity, `source` with nonempty `source_system`, `acquisition_channel`, `connector_id`, `observed_at` strictly after completion, `coverage_status: "Complete"`, `pagination_status: "Complete"`, `capability_status: "Supported"`, and an explicit `marketplace_default_bids` list with one row per requested marketplace. Each row has `marketplace`, `currency_code`, `amount`, and `evidence_status: "observed"`.

If a row provides optional `global_account_id`, `campaign_id`, `ad_group_id`, `source`, or `observed_at`, it must agree with the request and envelope. Row observation must be after completion and not later than the envelope. Missing optional row lineage inherits the trusted envelope assertion; it does not independently prove row provenance. Conflicting explicit row metadata is never discarded.

## Results and safety

- `Confirmed`: a single ad-group 207 success plus complete, newer, same-identity, native-currency default-bid readback for every marketplace.
- `Partial`: a valid, bound single-item 207 `error` or `partialSuccess`. It is **not** a full success.
- `Drifted`: complete observed bids differ by amount or native currency; no FX conversion.
- `Unknown`: malformed receipt or request, unsupported extra `expected_*` intent, missing/partial/truncated/unsupported capability, incomplete or stale query, missing/duplicate marketplace, invalid amount, or identity/source conflict.

`Confirmed` means configured **ad-group default bid**, not target bid, realized auction bid, effective placement/audience adjustment, performance improvement, or causal lift. The existing campaign helper must continue returning `Unknown` for unsupported ad-group intent; do not splice an ad-group success receipt into a campaign receipt. A combined change requires independent resource-level confirmations and a separately reviewed overall application status. This helper never sends Amazon Ads API requests, writes, retries, executes rollbacks, or handles multi-item batch reconciliation.

## Source and reuse boundary

Only independently paraphrased, publicly verifiable API facts were used. This repository-owned normalized contract and code are not copied from Amazon examples, third-party MCP connectors, prompts, schemas, workflows, or templates. Public practitioner and Reddit cases can motivate experiments but cannot establish API field contracts, fixed bidding formulas, or causal attribution.
