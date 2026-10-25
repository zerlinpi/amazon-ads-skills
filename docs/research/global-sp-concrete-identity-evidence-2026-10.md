# Global SP concrete identity provenance — 2026-10-26

## Verified nonduplicate gap

At main `d84475e40f02cd3ff7a55b04b0c8e82232ba9be6` (v1.64.0), zero open PRs and three relevant Global SP branches behind main, the campaign post-write readback helper accepted a repeated unavailable identity as a verified match. A request, 207 receipt, readback and raw marketplace mapping could echo `Unknown`, `Unsupported` or whitespace-padded values and still return `Confirmed`. Generic connector capability identity guards did not cover this independent readback helper. An unambiguous country code is not proof that a raw marketplace ID or account ID is known.

## Deterministic RED → GREEN

- RED first: `99c1cfdd07bc1befa262c26ba8e7c8ed1c541259`, [Actions 40218402467](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40218402467): 1475 tests, 15 FAIL.
- Minimal source fix: `ba70013601547d7145f0d12651760c09feb1aab1`, [Actions 40218449534](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40218449534): 1475/1475 PASS, 15 Skills and 55 eval fixtures PASS.
- 18 synthetic deterministic tests include account, campaign, optional request ID, source lineage, crosswalk raw ID, crosswalk source and budget crosswalk; legitimate IDs containing `unknown` and legacy index-only receipts still confirm. No live Ads reads/writes.

## Decision examples

| Request/readback evidence | Required classification | Why |
| --- | --- | --- |
| Both account IDs are `Unknown` | `Unknown` | Repeated absence is not shared account identity. |
| A `verified` raw marketplace crosswalk maps US to `Not-Supported`, and state/budget rows echo it | `Unknown` | Crosswalk agreement does not make a placeholder a raw ID. |
| A valid crosswalk and complete per-marketplace configured-state readback match the request | `Confirmed` | Concrete normalized evidence is internally consistent, subject to external adapter trust. |
| A concrete ID contains `unknown` as part of a longer identifier | Unchanged | Reject whole placeholder labels, not arbitrary substrings. |

## Bounded contract

Require concrete unpadded identities in the campaign request, explicit correlation ID, query source and optional raw marketplace crosswalk. Reject only whole-label placeholders after casefold/space/hyphen/underscore normalization, not valid IDs containing the same substring. Return `Unknown`, not `Confirmed`, for unusable provenance. The source adapter still owns raw API authenticity, complete query coverage, advertiser/campaign eligibility, exact marketplace mapping, and application reconciliation. No Amazon-native ID grammar, API retry, bid policy, Executor, new Skill or metric-zero inference is introduced.

## External evidence and reuse limits

Official [Global SP guide](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) documents 207 receipts, independent query, country codes and raw marketplace IDs; it does not define our placeholder vocabulary. [Amazon Ads MCP account-context guide](https://advertising.amazon.com/API/docs/en-us/mcp/get-started) separately scopes account selection. Public candidate review (stars, recent pushes, license, fork status, sampled CI and PRs) is recorded in `docs/SOURCES.md`. No third-party code, prompts, schema, workflows or templates copied. Operator anecdotes on multi-marketplace MCP and low-sample PPC are hypotheses only, not platform specifications or causal evidence.

## Next falsifiable gaps

1. Account-, marketplace-, advertiser- and campaign-specific eligibility proof bound to an exact connector capability and time.
2. Source-supported continuous rule activation history across causal comparison windows.
3. Independent raw adapter HTTP provenance and pagination authenticity.
4. Cross-control interaction and marginal contribution economics before any action sizing.
