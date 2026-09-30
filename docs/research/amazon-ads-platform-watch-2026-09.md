# Amazon Ads platform watch — September 2026

Reviewed: 2026-09-30

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

Promoted on 2026-09-29: Amazon's current Sponsored Products bidding help independently documents video as its own bid-adjustment control and states that it combines with other applicable modifiers. The canonical control-state schema/registry therefore treats `video_bid_adjustment` as material for Sponsored Products bid/budget causal review. Exact marketplace/category eligibility remains platform-capability evidence; missing connector support is not a zero boost.

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

## 9. Late-September platform updates

Amazon announced three material platform developments on 2026-09-28 and 2026-09-29:

- Natural-language analytics in Ads Agent is built on Unified Reporting and can answer performance and benchmark questions. Treat the conversational layer as an acquisition/interface path, not a new measurement authority; preserve report source, metric semantics, attribution identity, grain, date coverage and benchmark cohort.
- Ads Agent expanded conversational planning, analysis and campaign optimization, including bid and budget recommendations. This does not change repository write boundaries; exact account/campaign/control availability remains capability evidence.
- Sponsored Services launched for U.S. service providers with CPO bidding, outcome-oriented reporting and Unified API access planned for Q4 2026. Do not map Outcome to existing order/purchase/conversion semantics without an explicit metric contract, and do not treat missing webhook/CRM outcomes as zero without delivery/reconciliation evidence.

Current repository decision: record these as integration/measurement evidence only. Do not add a sixteenth Skill or new canonical control IDs until stable API/report contracts expose a repeatable decision gap.

Sources:
- https://advertising.amazon.com/resources/whats-new/analytics
- https://advertising.amazon.com/resources/whats-new/conversational-experience-amazon-ads-agent
- https://advertising.amazon.com/resources/whats-new/sponsored-services-capture-demand-now

## 10. Full-Funnel Campaigns and DVA+

Amazon announced Full-Funnel Campaigns and DVA+ on 2026-09-29 as part of Amazon Ads Agent. Full-Funnel Campaigns uses one budget and one optimization engine across sponsored ads, display, video and streaming TV; Amazon states that its AI selects formats and reallocates budget across funnel stages in real time. Reporting adds Long-Term Sales (LTS), which includes immediate conversions plus estimated future value from new-to-brand customer actions over a 12-month horizon. DVA+ similarly combines previously separate display/video/audio buying surfaces and can place ads across Amazon properties and the open internet through platform-managed optimization.

Decision implication:

- shared optimization means a channel/format allocation can change without an advertiser making a channel-level budget edit; do not attribute a local before/after effect to one advertiser control when the platform optimizer can reallocate delivery;
- LTS/Long-Term ROAS is not interchangeable with ordinary attributed sales/ROAS: preserve metric definition, modeled/estimated component, horizon, attribution identity, reporting generation and grain before comparison;
- UI/Ads Agent availability does not prove API/MCP/Connector parity. Missing allocation, format, supply, targeting or control-state observability remains Partial/Unsupported/Unknown rather than zero or unchanged;
- do not create a Full-Funnel/DVA+-specific canonical Skill or control type until stable API/report contracts expose a repeatable decision surface that the existing realization/control/measurement contracts cannot represent.

Existing repository coverage:
- measurement comparability and modeled-vs-observed lineage;
- control-state comparability and platform-managed realization confounders;
- connector/platform capability lineage and fail-closed missing-evidence semantics.

Sources:
- https://advertising.amazon.com/resources/whats-new/full-funnel-campaigns-from-discovery-to-sales
- https://advertising.amazon.com/en-us/library/news/amazon-ads-agent/


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
