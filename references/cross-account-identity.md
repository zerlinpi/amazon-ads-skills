# Cross-account reporting identity

Load this reference when a report, join, comparison, memory lookup, or optimization candidate can span more than one advertiser account, manager account, country, marketplace, or API region.

Amazon Ads reporting can aggregate across accounts and countries. That makes an entity identifier meaningful only inside its verified account/region scope. `entity_id alone` is not a safe global join key.

## Minimum identity envelope

Preserve the narrowest available composite identity before joining or aggregating rows:

```text
manager_account_id
advertiser_account_id
regional_profile_id
country_code
marketplace
ad_product
entity_type
entity_id
```

Fields may be unavailable on a given surface. Missing identity fields are `unknown`, not evidence that two rows belong to the same account. Do not synthesize an identifier from names.

## Identity collision gate

Treat an `identity collision` as unresolved when the same campaign/ad-group/target/entity ID appears in a multi-account dataset but the advertiser/account/country/region envelope is absent or inconsistent.

Therefore:

```text
same entity_id across rows
≠ same advertising entity
```

Do not deduplicate, sum, join to retail state, retrieve optimization memory, or emit an entity-specific action until the collision is resolved. Safe outcomes include `Missing Data`, `Directional`, `Hold`, or `Manual Review`.

Manager-account membership is context, not entity identity. A manager can contain multiple advertiser accounts; a global or regional account surface can also expose country-specific or regional identifiers. Preserve both parent scope and advertiser-level identity when available.

## Cross-country aggregation

Before aggregating performance across countries, also reconcile currency, timezone/date boundary, marketplace, attribution semantics, reporting generation, metric definition, and row coverage under `data-lineage.md`. Country is not a cosmetic dimension when it changes those semantics.

## Deliberate migrations

If an entity is intentionally migrated, recreated, or mapped across profiles/accounts, require an explicit mapping with provenance. Similar names, identical campaign text, or coincident dates do not prove continuity.

## Safety boundary

This reference governs read-side identity and decision evidence. It does not authorize Amazon Ads writes, cross-account mutation, or private connector behavior.
