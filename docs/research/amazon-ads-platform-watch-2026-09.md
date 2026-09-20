# Amazon Ads platform watch — September 2026

Reviewed: 2026-09-20

Purpose: keep fast-moving Amazon Ads surfaces visible to maintainers without copying volatile launch details into the 15 canonical Skills. A feature listed here is **not** automatically an optimization recommendation, eligibility guarantee, or permission to execute.

## 1. Amazon Ads MCP Server — open beta

Amazon announced the Amazon Ads MCP Server in open beta on 2026-02-02 for Amazon Ads partners with active API credentials. Amazon describes connectivity for reporting and account workflows, including capabilities that may create, update, or delete campaign objects.

Repository impact:

- high-value future Connector candidate for the user's planned advertising-platform integration;
- do not bind Skills to transient tool names/workflow names;
- map observed server abilities into the repository-owned connector capability catalog/snapshot;
- write-capable connector exposure does not change the repository default from Suggest or grant mutation authority;
- retry, idempotency, authorization, reconciliation and secrets stay in the external platform.

Source:
- https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta

## 2. Sponsored Products off-Amazon expansion

Amazon's Sponsored Products help documentation, updated 2026-08-27, states that Sponsored Products can extend to premium sites/apps outside Amazon in supported markets, using existing targeting, bid and budget settings. Amazon also notes that formats may include image, video or text and that text may contain AI-generated content based on product/landing-page information.

Decision implication:

- a traffic/CVR/CPC shift can reflect realized supply/surface mix rather than a manual bid/keyword change;
- causal diagnosis should preserve realized surface/source evidence where available;
- an empty advertiser change log does not prove delivery conditions stayed constant;
- do not manufacture an "off-Amazon = bad/good" rule from launch documentation.

Existing repository coverage:
- `realization-state-read`;
- platform-capability lineage;
- platform-managed-surface confounder evals.

Source:
- https://advertising.amazon.com/help/GYTD2Z3SYMAAMVXA

## 3. Sponsored Products video

Amazon currently documents Sponsored Products video as integrated into existing Sponsored Products campaign targeting and budget, with separate video performance reporting and a video-specific bid adjustment. Amazon documentation also states that the video bid boost can stack with other placement adjustments.

Decision implication:

- video exposure is a distinct realized creative/surface variable even when base targeting/budget are unchanged;
- base-bid or placement causal review should not assume image/video mix is stable;
- when a video bid adjustment is active, it is a candidate material control rather than ordinary creative metadata;
- video engagement metrics should not be mixed with click/conversion metrics without metric-semantic identity.

This may justify a future extension to the material-control registry if current connector/account evidence proves that the video adjustment is exposed as an independently mutable control for the target decision surface. Do **not** add a permanent control type solely from a guide example.

Sources:
- https://advertising.amazon.com/library/guides/sponsored-products-video
- https://advertising.amazon.com/resources/whats-new/unboxed-2025-sponsored-products-video

## 4. Sponsored Products / Sponsored Brands prompts

Amazon announced Sponsored Products prompts and Sponsored Brands prompts/reporting as generally available in the U.S. from 2026-03-25. The enhancement can automatically surface product information and may route shopper interaction through conversational experiences.

Decision implication:

- prompt exposure is another possible platform-managed realization variable;
- post-change review should distinguish advertiser controls from platform-managed message/surface realization;
- prompt reporting can become useful evidence, but absence of prompt rows is not zero exposure unless the report contract proves that.

Source:
- https://advertising.amazon.com/resources/whats-new/unboxed-2025-sponsored-products-and-sponsored-brands-prompts

## 5. Unified Reporting — GA

Unified Reporting became generally available on 2026-06-08 and can combine multiple accounts, ad products, countries, metrics and dimensions such as campaign, placement and audience.

Decision implication:

- easier cross-surface querying does not remove lineage requirements;
- standardized labels do not prove identical historical availability, row eligibility, attribution semantics or control state;
- a platform integration can use Unified Reporting as an acquisition path, but must still populate source/reporting-generation/metric/grain/coverage evidence.

Source:
- https://advertising.amazon.com/resources/whats-new/streamline-campaign-analysis-with-unified-reporting

## 6. Audience bid adjustments continue to expand

Current Sponsored Products help documentation (updated 2026-09-14) describes dynamic/fixed/rule-based bidding plus independent audience bid adjustments. Earlier Amazon releases introduced both AMC and Amazon-built audiences for bid boosting.

Decision implication:

- audience controls remain material to bid causal review;
- connector/platform integrations should expose audience adjustment state and audience identity where action safety depends on it;
- audience performance lift claims from Amazon launch materials are vendor-reported aggregate evidence, not a default bid percentage for an individual account.

Sources:
- https://advertising.amazon.com/help/GCU2BUWJH2W3A8Z7
- https://advertising.amazon.com/resources/whats-new/amazon-built-audience-in-sp
- https://advertising.amazon.com/resources/whats-new/audience-bid-boosting-in-sponsored-products

## 7. Ads Agent and agentic workflows

Amazon's Ads Agent product can assist with campaign creation, pacing/budget changes, targeting recommendations and AMC SQL/audience workflows. Amazon's positioning reinforces that agentic execution is becoming native to the ad platform.

Repository decision:

- do not compete with Ads Agent by duplicating execution/orchestration inside these Skills;
- keep this repository focused on evidence discipline, causal reasoning, economic gates, action safety, evaluation and portable strategy;
- a future platform may use Ads Agent/Amazon MCP as an execution/acquisition surface while these Skills provide independent decision policy.

Sources:
- https://advertising.amazon.com/solutions/products/ads-agent
- https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta

## 8. ChatGPT Ads integration pilot

Amazon announced on 2026-09-10 that select U.S. advertisers are testing an integration that extends Amazon Ads campaigns into ChatGPT conversational advertising experiences.

Current repository decision:

- record as an emerging surface only;
- do not modify Sponsored Products rules or claim account eligibility from the announcement;
- wait for stable campaign/report/control semantics before adding a canonical capability or decision surface.

Source:
- https://advertising.amazon.com/library/news/amazon-ads-chat-gpt-advertising-integration

## Promotion rule

A platform update moves from this watch file into a canonical Skill/reference/registry only when at least one of these is true:

1. it changes a repeatable decision boundary;
2. it introduces a separately mutable material control;
3. it changes measurement/report semantics;
4. it creates a new acquisition/realization path that can materially confound diagnosis;
5. it changes connector capability requirements.

Even then, require current scope/marketplace/eligibility evidence and deterministic regression coverage before changing behavior.

## Token policy

This watch file is maintenance context. Do not load it during ordinary optimization runs.

Load only when:
- the user explicitly asks for latest Amazon Ads tactics/features;
- a platform capability may explain an observed break;
- a connector integration is being designed or updated;
- a regression requires verifying a recent platform behavior.

This keeps volatile product news out of normal Skill context while preserving a path to adopt useful changes quickly.
