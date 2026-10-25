# Verified connector binding identity integrity — 2026-10-25

## Evidence-based gap
On main `32569d83394918431a130d83bfa67f2419c83424`, `evaluate_connector_capability_gate.py` accepted a `Supported` capability and `Verified` binding even when `binding_id`, `surface_id` or the sole supporting evidence `kind/reference` was a repeated `Unknown` / `Unsupported` / `Partial` label. Non-empty placeholder strings were treated as concrete evidence, permitting `Pass` and high confidence. This is a read-side provenance identity bug, not a claim that Amazon's API uses these labels.

## RED → GREEN
- RED commit `e77e5dd2f37669e878c99dc8bd0e6ad302d0207e`: 17 synthetic deterministic tests, 1353 total, 13 failures (Actions 40177634475).
- GREEN commit `db82411ac448568afc72f8db23ce810693eaa926`: 1353/1353 unit tests plus 15 Skill and 55 eval validations (Actions 40177671009).
- Qualifying Verified bindings now need concrete, unpadded binding/surface IDs and at least one usable supporting evidence kind/reference. A valid secondary binding may independently qualify. Extra unusable evidence does not erase a separate valid supporting record. Matching exact placeholders fail closed; legitimate identifiers containing those words remain accepted.

## Source and reuse boundary
Official Amazon Ads MCP guide (reviewed 2026-10-25): https://advertising.amazon.com/API/docs/en-us/mcp/get-started distinguishes dynamic/fixed account scope, profile/advertiser/manager identities and regional endpoints. Amazon Business exclusive campaign announcement (2025-10-31): https://advertising.amazon.com/resources/whats-new/amazon-business-exclusive-campaign-for-sponsored-product confirms advertiser/marketplace eligibility is separate from connector tool existence. Neither defines this repository's normalized placeholder rule.

Public practitioner anecdotes (e.g. Reddit r/AmazonFBA 2026-09-03, https://www.reddit.com/r/AmazonFBA/comments/1w6hdwl/) are uncontrolled observations, not platform policy or causal proof. Re-reviewed GitHub candidates are recorded in `docs/SOURCES.md`. No third-party code, prompt, schema, template or workflow was copied. No new Skill, live Amazon Ads mutation, retry, idempotency, Executor or HTTP authenticity claim.

## Next gaps
P0 bounded marketplace/advertiser/campaign eligibility and connector capability binding; P1 continuous rule-activation coverage; P2 independently authenticated raw Adapter response provenance; P3 causal interference and marginal profitability.
