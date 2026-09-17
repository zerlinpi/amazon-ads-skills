# Cross-account reporting identity

Load this reference when a report, join, comparison, memory lookup, or optimization candidate can span more than one advertiser account, manager account, country, marketplace, API region, or account-identity generation.

Amazon Ads reporting can aggregate across accounts and countries. Amazon Ads account models can also expose global, regional, and legacy identifiers for the same advertiser relationship. An entity identifier is therefore meaningful only inside its verified account/region/identity-generation scope. `entity_id alone` is not a safe global join key.

## Minimum identity envelope

Preserve the narrowest available composite identity before joining or aggregating rows:

```text
manager_account_id
global_advertiser_account_id
regional_advertiser_account_id
legacy_advertiser_account_id
advertiser_account_id
regional_profile_id
country_code
marketplace
ad_product
entity_type
entity_id
identity_mapping_provenance
```

Fields may be unavailable on a given surface. Missing identity fields are `unknown`, not evidence that two rows belong to the same account. Do not synthesize an identifier from names.

`advertiser_account_id` remains a generic connector-facing slot when the source does not expose which identifier generation it returned. Do not silently relabel it as global, regional, or legacy. When the source distinguishes those identities, preserve the explicit fields instead.

## Global / regional / legacy advertiser identity

Current Amazon Ads account surfaces may preserve an existing legacy advertiser identifier while also exposing a new global advertiser account ID and regional identifiers. Treat these as an identity mapping, not interchangeable strings.

A mapping is action-safe only when its provenance is explicit. Preserve `identity_mapping_provenance` such as the authoritative account-query response, source artifact/reference, retrieval time, and applicable region/country when available. A matching account name, campaign name, billing label, or temporal overlap is not sufficient mapping evidence.

Keep these distinctions explicit:

```text
global_advertiser_account_id
≠ regional_advertiser_account_id
≠ legacy_advertiser_account_id
≠ regional_profile_id
```

A global account can contain or resolve to multiple regional identities. A regional API/profile response does not prove that the returned identifier is the global identity. Likewise, a legacy ID continuing to function does not prove that it is the canonical global join key.

## Identity collision gate

Treat an `identity collision` as unresolved when the same campaign/ad-group/target/entity ID appears in a multi-account dataset but the advertiser/account/country/region envelope is absent or inconsistent, or when old/new advertiser identifiers are mixed without a verified mapping.

Therefore:

```text
same entity_id across rows
≠ same advertising entity
```

Do not deduplicate, sum, join to retail state, retrieve optimization memory, or emit an entity-specific action until the collision is resolved. Safe outcomes include `Missing Data`, `Directional`, `Hold`, or `Manual Review`.

Manager-account membership is context, not entity identity. A manager can contain multiple advertiser accounts; a global or regional account surface can also expose country-specific or regional identifiers. Preserve both parent scope and advertiser-level identity when available.

## Cross-country aggregation

Before aggregating performance across countries, also reconcile currency, timezone/date boundary, marketplace, attribution semantics, reporting generation, metric definition, and row coverage under `data-lineage.md`. Country is not a cosmetic dimension when it changes those semantics.

## Deliberate migrations and upgrades

If an entity or advertiser identity is intentionally migrated, recreated, upgraded, or mapped across profiles/accounts, require an explicit mapping with provenance. Similar names, identical campaign text, coincident dates, or the continued validity of an older identifier do not prove continuity.

When optimization memory spans an account-identity upgrade, preserve both the event-time identity envelope and the verified mapping used to retrieve it. Do not rewrite historical events in place to the newest account ID. Append or project the mapping so audit/replay can distinguish what was known at decision time from what was resolved later.

## Safety boundary

This reference governs read-side identity and decision evidence. It does not authorize Amazon Ads writes, cross-account mutation, or private connector behavior.
