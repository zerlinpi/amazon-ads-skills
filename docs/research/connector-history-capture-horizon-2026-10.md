# Connector historical availability capture horizon — 2026-10-25

## Verified nonduplicate gap

At main `70ee3da739b7e114ee172eb12b061c1e8c540001` (v1.62.0), zero open PRs and five sampled historical/reporting branches had no commits ahead. All 15 Skill files were inspected for safety/domain boundaries; the repository tree and selected references, schema, scripts, tests, evals, playbook and runtime manifests were reviewed (not a line-by-line audit of every file). P0 remains advertiser/campaign/marketplace eligibility tied to Connector evidence; this run addressed a reproducible historical provenance contradiction. P1 rule activation continuity, P2 raw Adapter authenticity, P3 causal/marginal economics remain open.

A Supported/Verified `campaign-performance-read` capability with `historical_availability_status=available` and a per-grain `available_through=2026-10-31` could return high-confidence Pass from a snapshot captured 2026-09-19, even for a requested 2026-10-01–15 history window. A requested earlier window and explicit freshness did not prevent the same false Pass.

## RED→GREEN

- RED `66e09b0a5eee15d1dbfc8f5a226de0bb1988f83b`, [Actions 40208517094](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40208517094): 1449 tests, 3 FAIL; old gate returned Pass where Degraded was expected.
- GREEN `315dac82d12335f219364278da0b439bee0af2f6`, [Actions 40208569404](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40208569404): 1449 PASS, Skill and Eval validators PASS.
- Ten deterministic tests cover future requested history, future observed range with earlier request, explicit freshness, same-day/one-day date-only tolerance, valid past history, no history requirement, unavailable/unknown history and missing windows.

## Minimal fix and boundaries

For an exact requested historical window, compare the matched observed grain's `available_through` date with the snapshot's UTC capture date. More than one calendar day beyond capture yields `data_contract_effect=unknown` and Degraded unless another independent gate blocks. The one-day tolerance avoids assuming an exact marketplace timezone for date-only bounds; it does not prove report completeness, conversion maturity, per-metric retention or raw HTTP authenticity. Out-of-range requested dates and explicit unavailable/retired history remain Blocked. Valid earlier observations and no-history requests remain compatible.

This is a repository-owned read-side evidence rule, **not** an Amazon Ads API retention or data-latency SLA. Never infer missing/unknown/partial as metric zero, account eligibility or causal lift. Actual Ads writes/retries/idempotency/reconciliation remain with an authorized external Executor.

## Sources, licenses and rejected candidates

Official: [Amazon Ads Unified Reporting GA (2026-06-08)](https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting) and [legacy reporting migration help](https://advertising.amazon.com/help/GK3JZZE5QLTF8U8A). Neither defines this internal capture-horizon check.

Public GitHub metadata sampled 2026-10-25: denisneuf/python-amazon-ad-api (MIT, 203 stars), KuudoAI/amazon_ads_mcp (MIT, 74), promptfoo/promptfoo (MIT, 26,412), OpenLineage/OpenLineage (Apache-2.0, 2,721), modelcontextprotocol/servers (NOASSERTION, 91,551). Fork state, recent activity, sampled Actions and open PRs reviewed; no full code/security/issues/transitive-license audit. All rejected as dependencies or copied implementations because none independently proves historical window provenance. NOASSERTION is not reuse permission. No third-party code, prompts, schemas, templates or workflows copied. [Reddit migration discussion](https://www.reddit.com/r/FulfillmentByAmazon/comments/1uklenw/) is a hypothesis, not a platform contract.

## Next gap

P0: independently bound Amazon Business marketplace, advertiser and campaign eligibility with Connector capability identity/time/source. P1: rule activation continuity. P2: Adapter HTTP authenticity. P3: control interactions, retail confounders and marginal economics.
