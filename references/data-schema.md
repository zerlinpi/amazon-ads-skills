# 统一数据模型

本仓库不绑定某个数据源。Amazon Ads API、MCP、领星 MCP、CSV、数据库查询结果应先映射为统一字段，再交给 Skills。

跨来源、跨刷新路径、跨指标语义版本或跨历史快照成熟度比较/回放时，按需加载 `data-lineage.md`；不要仅因为字段名或表路径一致就假设测量定义一致。

## 通用上下文

推荐所有数据批次携带：

```json
{
  "marketplace": "US",
  "profile_scope": "profile-us-01",
  "currency": "USD",
  "timezone": "America/Los_Angeles",
  "date_start": "2026-08-01",
  "date_end": "2026-08-31",
  "attribution_window": "source-defined",
  "ad_type": "SP",
  "mode": "Suggest",
  "promotion_context": [],
  "source_metadata": {
    "source_system": "amazon_ads_api",
    "source_dataset": "campaign-performance",
    "extracted_at": "2026-09-01T08:00:00Z",
    "available_through": "2026-08-31",
    "aggregation_grain": "daily",
    "semantic_version": null,
    "metric_semantics": {
      "orders": {
        "definition_id": "attributed_orders",
        "semantic_version": null
      },
      "sales": {
        "definition_id": "attributed_sales",
        "semantic_version": null
      }
    },
    "snapshot_maturity": {
      "backfill_status": "mature",
      "backfill_age_days": 7,
      "historical_partitions_mutable": true,
      "last_restatement_at": null
    },
    "completeness": "complete"
  }
}
```

`extracted_at` 表示何时获取数据；`available_through` 表示数据实际完整到哪一天。两者不可互相替代。

如果历史分区会因迟到转化、归因、退款、去重或上游修正而回填，建议记录 `snapshot_maturity`：

- `backfill_status`: `provisional / mature / final / unknown`；
- `backfill_age_days` 或等价成熟度；
- `historical_partitions_mutable`；
- `last_restatement_at`（如可用）。

当数据来自 Warehouse、BI、MCP 或派生表时，推荐额外记录 upstream/source lineage、refresh policy、filters、backfill/partial 状态。若同一 dataset 内不同指标可能独立升级定义，使用 `metric_semantics.<metric>.definition_id / semantic_version` 记录，而不要只依赖 dataset-level `semantic_version`。

缺失 lineage 应标记为未知，不得自动假设与另一数据源、语义版本或快照成熟度完全可比。

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

## Source comparability

跨窗口/跨来源/跨语义版本/跨快照成熟度分析时，至少检查：

- marketplace / profile scope；
- timezone / currency；
- date coverage 与 partial-day 状态；
- attribution window / maturity；
- aggregation grain；
- filters / entity inclusion；
- refresh/backfill lag；
- dataset semantic/report version；
- per-metric definition ID / semantic version；
- snapshot/backfill maturity 与 historical-restatement 状态。

可将比较状态标记为：`Comparable`、`Reconcilable`、`Directional`、`Not Comparable`、`Unknown`。

如果 apparent break/lift 与 source switch、metric semantic-version cutover 或不对称 backfill 同期发生，先把 measurement drift 当作 competing explanation，再进入广告优化或 Post-change outcome 判断。

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
  "guardrails": ["bid_change_pct <= account-approved-bound"],
  "validation_window": "7d or until sufficient conversions",
  "rollback_condition": "CVR drops materially while traffic quality remains stable"
}
```

## 缺失值

- 缺少值使用 `null` 或不提供字段，不得用 0 冒充未知值。
- `0` 必须表示真实观测到 0。
- 金额必须带可确定的 currency 上下文。
- 百分比在机器结构中优先使用 0-1 小数，例如 ACOS 30% 表示 `0.30`。
- 来源、刷新时间、完整日期、attribution 定义、metric semantic version 或 snapshot maturity 未知时，应显式标记 unknown；不得通过猜测补齐 lineage。
