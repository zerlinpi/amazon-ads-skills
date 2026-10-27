# N/A and Not Applicable are not control scope/source identities — 2026-10-27

## Fresh baseline and verified gap

Initial main `679f5d3a1b7fe9a04ae3984ab956a228e0e22795`, main Actions #40445755084 SUCCESS, no open PR; three sampled older branches zero ahead. Read all 15 canonical Skills, runtime manifests, comparator/schema, existing placeholder tests and research inventory. `scripts/compare_control_state.py` rejected Unknown/Missing/Not Available but did not reserve whole-label `N/A` or `Not Applicable` for control scope/source. Identical placeholder values in baseline/post incorrectly counted as shared real identity; a synthetic bid change returned `Treatment Isolated`.

## Deterministic RED → GREEN

Tests-only `e9712f65c70c15521cf41c06d0c898f6474988ef`, [RED Actions #40451514757](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40451514757): 1938 tests, 14 FAIL, 3 compatibility cases PASS. Cases cover marketplace, profile, campaign, entity ID/type, global/manager/country account identity, source system, acquisition channel and connector, with tabs, repeated spaces, hyphen and underscore variants.

Minimal code `98bcb0eb97a30616aef90c1ec53c0dd34467d1da`, [GREEN Actions #40451585223](https://github.com/zerlinpi/amazon-ads-skills/actions/runs/40451585223): 1938/1938 PASS, Skill/Eval validators PASS. Add only `not_applicable` and `n/a` to the existing whole-label reserved identity set. Genuine opaque IDs containing these words remain valid. No new Skill, schema, dependency, Ads write, retries or external executor changes.

## Sources, license and decision boundary

Amazon [Global Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/guides/campaign-management/global-campaigns) distinguishes advertiser and marketplace identities. [Marketing Stream v2](https://advertising.amazon.com/API/docs/en-us/guides/amazon-marketing-stream/v2/overview) explains record versions and restatements. [Budget/bidding rules](https://advertising.amazon.com/library/guides/budget-rules/) shows time-varying control states. [DSP bid adjustment testing](https://advertising.amazon.com/API/docs/en-us/guides/dsp/bid-adjustments/testing) warns against uncontrolled before/after inference, but DSP-specific instructions are not a Sponsored Products requirement. These sources do **not** define the repository's reserved identity tokens or authenticate connector responses. [October 2026 Reddit PPC launch case](https://www.reddit.com/r/AmazonFBA/comments/1wva243/) is a hypothesis generator, not policy.

GitHub metadata sampled October 27: OpenLineage (2726 stars, Apache-2.0, nonfork, Oct 25 push), MetricFlow (1848, Apache-2.0, nonfork, Oct 13), OpenEvals (1232, MIT, nonfork, Oct 22), KuudoAI amazon_ads_mcp (74, MIT, nonfork, Oct 14), Agent Skills (26674, Apache-2.0, nonfork, Aug 9). Some Actions/PRs sampled; prior SOURCES reviews exist. Reject imports: this deterministic guard needs no external dependency and none authenticates Amazon Ads observations. No comprehensive security/issue/dependency-license audit; no external code, prompts, schemas, templates or workflows reused. No blanket license inference.

## Next real gaps

P0: continuous Schedule/Event/Budget Rules history with gaps, activation and source identity; P1: externally authenticated source/metric/date/grain/identity and connector capability; P2: marginal contribution-profit and cross-campaign control interference. Default Read-only/Suggest/Shadow; authorized Executor owns writes, retries, idempotency and reconciliation.
