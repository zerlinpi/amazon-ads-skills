# 统一数据模型

本仓库不绑定某个数据源。Amazon Ads API、MCP、领星 MCP、CSV、数据库查询结果应先映射为统一字段，再交给 Skills。

## 通用上下文

推荐所有数据批次携带：

```json
{
  "marketplace": "US",
  "currency": "USD",
  "timezone": "America/Los_Angeles",
  "date_start": "2026-08-01",
  "date_end": "2026-08-31",
  "attribution_window": "source-defined",
  "ad_type": "SP",
  "mode": "Suggest",
  "promotion_context": []
}
```

## Campaign

核心字段：
- `campaign_id`
- `campaign_name`
- `ad_type`
- `state`
- `targeting_type`
- `bidding_strategy`
- `daily_budget`
- `impressions`
- `clicks`
- `spend`
- `orders`
- `sales`
- `currency`
- `date_start`
- `date_end`

可选：`top_of_search_modifier`、`product_pages_modifier`、`rest_of_search_modifier`、`budget_status`。

## Keyword/Target

核心字段：
- `target_id`
- `campaign_id`
- `ad_group_id`
- `target_type`
- `target_text`
- `match_type`
- `state`
- `bid`
- performance metrics

`target_type` 可表示 keyword、product、category、audience 等，具体能力由广告类型决定。

## Search Term

核心字段：
- `search_term`
- `campaign_id`
- `ad_group_id`
- `matched_target_id`
- `match_type`
- performance metrics

搜索词数据和 keyword/targeting 数据不可混为一层；一个 target 可以匹配多个 search term。

## Optimization Action

统一动作结构见 `schemas/optimization-action.json`。

动作示例：

```json
{
  "action_type": "adjust_bid",
  "entity_type": "keyword",
  "entity_id": "kw-123",
  "current_value": 1.2,
  "proposed_value": 1.05,
  "reason": "ACOS 连续两个验证窗口高于目标，且样本充分",
  "evidence": ["28 clicks", "4 orders", "ACOS 42%", "target ACOS 30%"],
  "confidence": 0.82,
  "mode": "Suggest",
  "guardrails": ["bid_change_pct <= 20%"],
  "validation_window": "7d or until sufficient conversions",
  "rollback_condition": "CVR drops materially while traffic quality remains stable"
}
```

## 缺失值

- 缺少值使用 `null` 或不提供字段，不得用 0 冒充未知值。
- `0` 必须表示真实观测到 0。
- 金额必须带可确定的 currency 上下文。
- 百分比在机器结构中优先使用 0-1 小数，例如 ACOS 30% 表示 `0.30`。
