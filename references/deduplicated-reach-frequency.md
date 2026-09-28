# Deduplicated Reach and Frequency

Use this contract when interpreting deduplicated reach and frequency from Amazon Ads or any normalized source.

- **Deduplicated reach** is a non-additive population metric. Do not sum it across overlapping campaigns, accounts, scopes, or time windows.
- **Frequency** depends on the same population definition, time grain, scope, and reporting generation as its reach denominator.
- Keep marketplace/profile/account scope explicit. Cross-account comparisons require compatible population semantics.
- Missing rows, unsupported connector coverage, pagination limits, or truncated exports are **not zero**.
- If time grain or scope differs, mark the comparison `Directional`, `Not Comparable`, or `Unknown` instead of manufacturing an exact delta.
- Only claim `Comparable` when population definition, deduplication semantics, time grain, scope, and reporting generation are reconciled.
