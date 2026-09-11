# Search Term Impression Share evidence policy

Load this shared reference when Amazon Ads query growth, share-of-voice, competitive visibility, or headroom reasoning uses Search Term Impression Share (SIS) / Impression Rank data.

The purpose is to use SIS as **market-visibility evidence** without turning it into guaranteed incremental sales or a mechanical bid/budget instruction.

## 1. What SIS can establish

For supported Sponsored Products / Sponsored Brands reporting, Amazon describes Search Term Impression Share as the account-level share of eligible ad impressions captured for a search term relative to other advertisers, with a numeric impression rank for the same term.

Treat these fields as useful for questions such as:

- Is the account already capturing a large or small share of ad impressions on a commercially important query?
- Did share/rank move after a bidding, targeting, or budget change?
- Which proven high-value queries appear to have additional visibility headroom?
- Which queries are strategically important enough to monitor for defensive share loss?

SIS is not the same thing as conversion rate, profitability, total consumer demand, organic share, sales share, or incrementality.

## 2. Scope and acquisition contract

Before joining SIS to search-term performance, capture when available:

- ad product;
- marketplace and profile/account scope;
- search term text / normalized identity;
- report window and time unit;
- report lookback availability;
- account scope represented by the SIS report;
- search-term report row-inclusion / eligibility contract;
- source/reporting generation and extraction timestamp;
- `acquisition_channel` — advertising console download, Amazon Ads API, MCP/connector, warehouse import, manual export, or another concrete path;
- `channel_capability_status` — verified available, unavailable, unsupported, unknown, or transformed downstream.

Amazon's current public Sponsored Products help documentation describes SIS as an **account-wide** search-term measure and documents a 90-day lookback with summary or daily time units. Treat those limits as source/report characteristics, not universal constants for every ad product, marketplace, API version, connector, or future reporting generation.

A metric being available in the Amazon Ads product or report center does not prove that the active API, MCP, connector, or warehouse path exposes the same field. Conversely, a field missing from the active connector is not evidence that SIS is zero, unavailable to the advertiser, or absent from Amazon Ads entirely.

When SIS is decision-relevant but the current acquisition path does not expose it:

1. record the metric as `Unavailable via active channel` or `Capability unknown`;
2. do not coerce missing SIS/rank to zero;
3. do not infer `100% remaining share` from a null/missing value;
4. use other evidence only for claims it can actually support;
5. request or route to a verified compatible acquisition path if the decision materially depends on SIS.

## 3. Join safety

Do not assume that a row in a clicked-only Search Term performance report has the same population contract as a SIS row.

Before combining the two, verify:

1. same marketplace/profile/account scope;
2. compatible ad product;
3. same normalized search term identity;
4. compatible date window/time grain;
5. compatible reporting generation/date semantics;
6. no unresolved row-eligibility or truncation issue;
7. acquisition channels preserve compatible metric semantics and scope.

A successful string join is not evidence that the measurements describe the same population.

## 4. Headroom interpretation

Low SIS can support a **visibility-headroom hypothesis** only when the query is also commercially valuable and the account is not already blocked by another constraint.

Useful supporting evidence includes:

- mature conversions / profitable economics for the query or its routed target;
- stable retail readiness and inventory;
- campaign/portfolio/account budget headroom;
- bid/placement controls that plausibly constrain delivery;
- sufficient query relevance and strategic importance;
- evidence that increasing paid visibility would not merely displace another profitable route inside the same account.

Prefer classifications such as:

- `share-headroom-candidate` — valuable query with credible room to capture more paid impressions;
- `share-defense` — strategically important query whose share/rank deterioration deserves monitoring or controlled response;
- `share-saturated-or-constrained` — high share or another binding control limits plausible incremental reach;
- `directional-only` — SIS is informative but economics, routing, or comparability is incomplete.

## 5. What SIS does not prove

Do not infer any of the following from low SIS alone:

- guaranteed incremental clicks, sales, or profit;
- that raising bid is the correct control;
- that raising campaign budget is the correct control;
- that competitors are the only reason for low share;
- that the account has profitable marginal demand;
- that the query deserves Exact harvesting or protection;
- that a higher SIS target is always better.

Likewise, high SIS does not automatically mean a query is fully saturated: available demand, auction dynamics, placement mix, retail state, bid strategy, budget caps and query-routing overlap can still matter.

## 6. Change interpretation

When SIS/share rank changes after an optimization, do not call the action successful from share movement alone.

Check:

- spend, CPC, clicks and conversion economics;
- query/target routing and duplication;
- budget and pacing constraints;
- placement/base-bid/dynamic-bidding changes;
- promotion, retail readiness and seasonality;
- whether the reporting windows are comparable;
- whether both windows were acquired through channels with equivalent SIS semantics and coverage.

A share increase that reduces contribution economics, steals traffic from another profitable route, or occurs during a confounded control window is not automatically a positive outcome.

## 7. Action gate

When a query has low SIS but action-driving evidence is incomplete:

- keep the conclusion at `Directional` / `Experiment` / `Hold`;
- request the missing economics, routing, budget/headroom, retail, or acquisition-path evidence;
- do not output a repository-default bid/budget percentage;
- if sizing becomes appropriate, use `action-sizing.md` and the relevant bid/budget/placement Skill.

When SIS is missing from the active connector, do not convert absence into a low-share signal. Treat it as a data-capability limitation until another verified source supplies the metric.

This reference never authorizes a live Amazon Ads write.

## 8. Output fields when SIS materially affects a decision

Include when useful:

- `search_term`;
- `sis_window` / time unit;
- `impression_share`;
- `impression_rank`;
- `acquisition_channel`;
- `channel_capability_status`;
- `scope_status`;
- `join/comparability_status`;
- `commercial_value_evidence`;
- `binding_constraint` or `unknown`;
- `headroom_classification`;
- `confidence`;
- `next_measurement`;
- `actionability`: `Action-safe`, `Directional`, `Experiment`, `Hold`, or `Manual Review`.
