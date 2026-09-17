# Account identity in derived optimization memory

Reviewed: 2026-09-17

## Why this matters

Amazon Ads can expose performance and account context across multiple advertiser or manager accounts, countries, regions and identifier generations. A compact optimization-memory projection therefore cannot assume that the same marketplace/profile/entity tuple proves the same advertiser identity when explicit account identity evidence says otherwise.

This note records the public platform facts motivating the repository's derived-memory identity gate. It does not add a live connector, private Amazon interface or mutation authority.

## Public Amazon Ads evidence reviewed

### Unified reporting

Amazon Ads, `Streamline campaign analysis with unified reporting, now generally available`, published June 8, 2026:

https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

Amazon states that one unified report can include campaigns across multiple manager or advertiser accounts, ad products, countries, metrics and dimensions. This makes advertiser/account identity a material join and aggregation boundary rather than a cosmetic reporting field.

### Enhanced advertiser account

Amazon Ads, `A guide to the enhanced Amazon Ads advertiser account`:

https://advertising.amazon.com/library/guides/advertiser-account

Amazon states that existing DSP advertisers are automatically upgraded, existing integrations continue to work, and new Global Account IDs plus regional identifiers are available for multi-country API use. The existing advertiser identifier and newer identity surfaces can therefore coexist.

### Global seat / regional profiles

Amazon Ads, `Register once and manage ads worldwide with a global seat`, published February 20, 2025:

https://advertising.amazon.com/resources/whats-new/register-and-manage-ads-worldwide-with-global-seat

Amazon documents region-specific profile IDs and API endpoints for global manager accounts; the Profiles API returns the profile for the regional endpoint being queried rather than all regional profiles at once. A profile identifier is therefore not interchangeable with a global advertiser identity.

## Repository adaptation

The repository independently applies these platform facts to optimization-memory safety:

```text
same marketplace/profile/entity tuple
+ conflicting explicit advertiser identity
!= one verified optimization history
```

`schemas/optimization-event.json` remains the append-first source of event-time account identity. Derived history may preserve a compatible identity envelope for retrieval, but it must not manufacture mappings or collapse conflicting identities.

For the read-only measurement and realization projectors:

- explicit conflicting values for the same account-identity field fail closed;
- compatible envelopes must share at least one strong advertiser/profile identity before they are merged;
- manager account or country alone is not sufficient proof of advertiser identity;
- known and missing account identity are not silently treated as the same account within one projected event slice;
- all-legacy slices with no account identity remain backward-compatible, but no account identity is invented;
- `identity_mapping_provenance` is preserved when provided but is not used to manufacture an identifier relationship by itself.

The append-first event ledger remains authoritative. A derived `account_identity` is a bounded retrieval aid, not proof that every historical event was observed under identical account semantics.

## Copyright / adoption boundary

Amazon Ads pages are public vendor documentation, not code or schemas licensed into this repository. No Amazon prose, API implementation, proprietary schema, prompt, workflow, screenshot or template is copied. The repository uses only factual platform behavior and independently written identity-lineage and fail-closed projection rules.
