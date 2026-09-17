# Caller-bound account identity for derived history

Reviewed: 2026-09-17

## Question

The read-only measurement and realization projectors already reject conflicting advertiser identities inside one event slice. The remaining boundary is caller intent: if a caller requests one advertiser account but supplies a slice containing a single event from another advertiser, the legacy marketplace/profile/entity tuple alone cannot prove the requested advertiser identity.

## Public Amazon Ads evidence

Amazon Ads Unified Reporting, generally available June 8, 2026, can include campaigns across multiple manager or advertiser accounts, countries, ad products, metrics and dimensions in one report. Therefore advertiser/account identity is a material retrieval and join boundary.

Amazon's enhanced advertiser-account documentation states that existing advertiser IDs can continue to work while new Global Account IDs and regional identifiers are also available for multi-country API use. These identity generations can coexist and should not be silently substituted for one another.

Amazon's global-seat documentation also states that manager/profile identity is region-specific: Profiles API returns the profile for the regional endpoint being queried rather than all regional profiles together. A profile scope is therefore not a substitute for an explicitly requested advertiser identity.

Sources:

- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting
- https://advertising.amazon.com/library/guides/advertiser-account
- https://advertising.amazon.com/resources/whats-new/register-and-manage-ads-worldwide-with-global-seat

## Repository implication

When `expected_scope` includes an explicit account-identity envelope, the projector should verify the event slice against that requested identity in addition to marketplace/profile/entity scope.

```text
requested marketplace/profile/entity matches
+ requested advertiser identity conflicts or is unavailable
!= verified requested history slice
```

The account-identity request may be partial, but it must contain at least one strong advertiser/profile identifier (`global_advertiser_account_id`, `regional_advertiser_account_id`, `legacy_advertiser_account_id`, `advertiser_account_id`, or `regional_profile_id`). Every explicitly requested identity field must be present and equal in each relevant event; the projector must not infer equivalence across different identity fields or from manager/country alone.

Legacy callers that omit `expected_scope.account_identity` remain backward-compatible and continue to use the existing intra-slice collision gate.

## Copyright / adoption boundary

Amazon Ads pages are public vendor documentation. This repository uses only factual platform behavior and independently written validation logic. No Amazon prose, code, proprietary schema, prompt, workflow, UI or implementation is copied.