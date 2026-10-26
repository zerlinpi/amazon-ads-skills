# Feature eligibility capability-level source-reference collision — 2026-10-26

## Fresh-read and non-duplicate defect

Base main `1113f21eb588da2083a8fe9e73aaee939e5157ea` (v1.73.0), no open PR. The previous source-independence fix checked all observed connector *bindings* and their evidence references, but `schemas/connector-capability-snapshot.json` also supports `capabilities[].evidence[].reference`. A normalized feature-specific eligibility record reusing a capability-level reference could be misclassified as independent Eligible (Pass) or Ineligible (Blocked). This is not a remote Amazon API authenticity claim. Historical related branches had no commits ahead of main.

## Deterministic RED → GREEN

- Branch `fix/feature-eligibility-capability-evidence-reference-20261026`, PR #187. RED `47520eb3787d75c0d75a9e5435bb5c610c3f91f1`: [Actions #40261027113](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40261027113), 1580 tests, 4 FAIL. Cases: required/non-required/Unsupported capability evidence, and self-referential Ineligible. Three compatibility controls passed.
- Minimal repair `17b798291ba143d779c077eb4248e2a7293ad027`: [Actions #40261080915](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40261080915), 1580/1580 PASS, 15 Skill directories and 55 eval fixtures PASS.
- Read-only source-reference equality check expanded to capability-level evidence. Existing binding-level checks, feature identity/time, capability requirements, scope, source and metric lineage remain unchanged. Seven tests; no new Skill, dependency, schema, Amazon Ads write/retry/idempotency or Executor behavior.

## Evidence, license and rejection

Amazon Ads [MCP account context](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) and [Ads API overview](https://advertising.amazon.com/about-api) distinguish authorized account access and API read/report/manage operations, but do not define the repository-owned evidence collision rule or independently authenticate raw responses.

GitHub candidates (2026-10-26 mutable observations): KuudoAI/amazon_ads_mcp (74 stars, MIT, non-fork, recent sampled CI success); promptfoo/promptfoo (26,424, MIT, non-fork, recent sampled CI success); OpenLineage/OpenLineage (2,722, Apache-2.0, non-fork, recent sampled CI success); agentskills/agentskills (26,624, Apache-2.0, non-fork, older sampled CI failure). Sampled PRs, actions and license metadata do not constitute complete code/security or dependency audits. All rejected as imports because no external runtime is needed. No third-party code, prompts, schemas, templates or workflows copied; abstract principles only. [PPC discussion of unchanged bids and CPC drift, 2026-09-20](https://www.reddit.com/r/FulfillmentByAmazon/comments/1wl9jki/) is a hypothesis source, not Amazon policy or causal evidence.

## Remaining real gaps

P0: normalized reference distinctness does not authenticate raw HTTP or establish actual feature entitlement; needs externally authorized source readback/reconciliation.
P1: rule activation at two instants and last transition do not establish continuous Schedule/Event/Budget Rule execution over the full causal comparison window.
P2: cross-campaign control interaction and retail/profitability confounders require separately evidenced marginal economics and experimental identification.
