# Connector read-side access evidence — 2026-10-25

## Observed gap

On main `5438d846f4ca1bf4b171b86dd7912785acefe7f9`, `evaluate_connector_capability_gate.py` returned high-confidence `Pass` for `Supported + Verified` even when the capability declared `access_mode=write`, `mixed`, `unknown`, missing or malformed. A binding's identity and chronology cannot prove read access. The canonical catalog contains only read-side capabilities. This is an internal decision-evidence defect, not an Amazon Ads API enum or remote permission finding.

## RED → GREEN

RED `06dc8d93e11d1c47861881bc59a3f52f0b9e6f35` [Actions 40181875717](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40181875717): 1366 tests, 9 FAIL. GREEN `f81560b145411a20eeb4f8d43913eb130fec4c76` [Actions 40181914834](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40181914834): 1366 PASS, 15 Skills PASS, 55 eval fixtures PASS. No Amazon Ads writes.

## Decision boundary

A `Supported` connector capability with a `Verified` binding still needs a concrete read-side `access_mode`. A `write`-only capability is `Blocked`; `mixed`, `unknown`, missing, malformed or unsupported modes are `Degraded`. Only explicit `read`, `report`, `export` or `stream` access can pass the access-mode preflight, subject to other evidence gates. A second binding or snapshot default mode cannot override write-only access. This repository-owned read-side check does not authenticate remote tool behavior, grant write permission, or replace an authorized external Executor. A `mixed` connector may support legitimate reads, but the per-capability path must explicitly prove read-side behavior before high-confidence use. No account writes, retries, idempotency or Executor functionality added.

## Sources and copyright

Amazon Ads [MCP connection guide](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) (dynamic/fixed account scope) and [eligibility API](https://advertising.amazon.com/API/docs/en-us/mcp/eligibility) (program/product eligibility) are platform context, not definitions of this internal access-mode gate. The [MCP tool annotations analysis](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/) (2026-03-16) cautions that readOnlyHint is advisory and not independently trusted.

GitHub metadata sampled 2026-10-25: [KuudoAI/amazon_ads_mcp](https://github.com/KuudoAI/amazon_ads_mcp) (74 stars, MIT, non-fork, last push 2026-10-14, sampled successful Actions, open PRs #104/#101); [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) (26,398 stars, MIT, non-fork, active 2026-10-25, sampled successful/in-progress Actions, open PRs #11978/#11977); [OpenLineage/OpenLineage](https://github.com/OpenLineage/OpenLineage) (2,721 stars, Apache-2.0, non-fork, active 2026-10-25, sampled successful Actions, open PRs #5105/#5104); [coaxon/amazon-mcp](https://github.com/coaxon/amazon-mcp) (1 star, MIT, non-fork, last push 2026-07-01, sampled June Actions success, no open PRs). All rejected for integration: a local deterministic access-mode guard is sufficient, and no project authenticates the live Ads readback. Sampled CI, issue/PR counts, stars and licenses are not full code/security/license audits. No third-party code, prompts, schemas, templates, workflows or nested assets copied.

## Next gap

P0 independent marketplace/advertiser/campaign eligibility and time-scoped Connector capability evidence; P1 continuous rule activation; P2 raw Adapter authenticity; P3 causal interaction and marginal economics.
