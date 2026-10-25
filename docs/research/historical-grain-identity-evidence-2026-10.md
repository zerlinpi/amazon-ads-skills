# Historical reporting grain identity evidence — 2026-10-25

## Verified gap

At main `01b3f57c2ac74c6be3f67fc7dc7b9bbd7513a14d` (v1.61.0), with zero open PRs and no sampled history branch ahead, the connector history gate could accept requested `grain=Unknown` matched to observed `Unknown`, or trim an observed padded ` daily ` to match `daily`. Both could yield high-confidence Pass for a claimed retention range. This differs from reporting-generation identity.

## RED→GREEN

- RED `0f1195bef1c2d509f7cd332edbb96f0345b58f96` [Actions 40203462802](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40203462802): 1439 tests, 8 FAIL.
- GREEN `6f1a632f255ce3a4b6a58c84182f12b29f675da0` [Actions 40203519607](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40203519607): 1439 PASS, 15 Skill and 55 eval fixture validators PASS.
- Fourteen synthetic deterministic tests cover requested placeholders, padded observed matching grain, valid-plus-padded duplicate ambiguity, valid case-insensitive match, concrete mismatch and no history requirement.

## Minimal behavior and boundary

Reuse the existing concrete-identity predicate for requested grain. An observed padded apparent match is not a verified historical window, even when another concrete entry matches. Preserve valid grain/date bounds and no-requirement behavior. This repository-owned read-side rule does not certify per-metric or per-dimension availability, report completion, account/campaign eligibility, API authenticity or actual causal lift. Missing/partial/unknown are not metric zero; no live account writes.

## Sources and reuse

[Amazon Ads 2025 Unified Reporting](https://advertising.amazon.com/resources/whats-new/unboxed-2025-campaign-analysis-with-unified-reporting) separates hourly/daily/weekly/monthly history; [GA 2026-06-08](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) confirms grain-specific reporting; [migration help updated 2026-10-12](https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A) warns of 2026-12-31 legacy retirement and incompatible report types. None specifies internal placeholder labels.

Public metadata sampled: denisneuf/python-amazon-ad-api (MIT, 203 stars), KuudoAI/amazon_ads_mcp (MIT, 74), promptfoo/promptfoo (MIT, 26,408), OpenLineage/OpenLineage (Apache-2.0, 2,721), modelcontextprotocol/servers (NOASSERTION, 91,549). All rejected for integration because they do not independently prove a historical grain match; no third-party code, prompt, schema, workflow or template copied. Sampled Actions and repository metadata are not a full security/issue/PR/license audit. [Reddit reporting-delay discussion](https://www.reddit.com/r/PPC/comments/z9a1zb) is a hypothesis only, not a platform rule.

## Next gaps

P0 account/campaign/marketplace eligibility with independently bound Connector capability; P1 rule activation continuity; P2 external Adapter raw-response authenticity; P3 control interactions and marginal economics.
