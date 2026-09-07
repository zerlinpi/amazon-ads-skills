# Examples

这里给出与具体 Connector 无关的最小示例。真实项目中可将 Amazon Ads API、MCP、领星 MCP、CSV 或数据仓库结果先转换成 `schemas/` 定义的统一结构。

## 示例 1：整体账户诊断

用户：

```text
分析过去 30 天美国站 Sponsored Products，目标 ACOS 30%。找出最值得先处理的 5 个问题，不要直接修改账户。
```

推荐路由：

```text
amazon-ads-optimizer
  -> amazon-ads-audit
  -> campaign-health-monitor
  -> search-term-analysis / bid-optimization / budget-optimization (按诊断结果调用)
```

输出默认 `mode: Suggest`。

## 示例 2：标准 Campaign 输入

```json
{
  "campaign_id": "cmp-001",
  "campaign_name": "SP-Core-Exact",
  "ad_type": "SP",
  "state": "enabled",
  "targeting_type": "manual",
  "bidding_strategy": "dynamic-down-only",
  "daily_budget": 100,
  "currency": "USD",
  "marketplace": "US",
  "date_start": "2026-08-01",
  "date_end": "2026-08-31",
  "impressions": 120000,
  "clicks": 960,
  "spend": 1152.5,
  "orders": 96,
  "sales": 3840
}
```

由此可计算：
- CTR = 0.8%
- CPC ≈ 1.20 USD
- CVR = 10%
- ACOS ≈ 30.0%
- ROAS ≈ 3.33

## 示例 3：竞价建议

输入上下文：

```json
{
  "target_acos": 0.30,
  "keyword": {
    "target_id": "kw-123",
    "current_bid": 1.20,
    "clicks": 80,
    "spend": 104,
    "orders": 8,
    "sales": 240,
    "historical_cvr": 0.10
  }
}
```

可能的 Suggest 输出：

```json
{
  "action_type": "adjust_bid",
  "entity_type": "keyword",
  "entity_id": "kw-123",
  "current_value": 1.2,
  "proposed_value": 1.08,
  "reason": "当前 ACOS 持续高于目标且订单样本可用，建议小步降低竞价后重新观察",
  "evidence": [
    "spend=104",
    "sales=240",
    "ACOS=43.3%",
    "target ACOS=30%",
    "orders=8"
  ],
  "confidence": 0.8,
  "mode": "Suggest",
  "guardrails": ["single bid change <= 20%"],
  "validation_window": "7 days or until another sufficient conversion sample is collected",
  "rollback_condition": "traffic or orders fall materially beyond the expected range"
}
```

这里的 `1.08` 是示例，不是固定算法结果。Skill 需要结合 placement、最近调整、流量和业务阶段重新判断。

## 示例 4：搜索词收割 + 否词保护

用户：

```text
找出过去 45 天应该 Exact 收割的 Search Term 和应该否定的浪费词。品牌词不要误杀。
```

执行顺序：
1. `search-term-analysis` 找 Winner / Harvest candidates；
2. 检查 Exact 是否已经存在；
3. `negative-targeting` 对低价值词做误杀保护检查；
4. 先建立承接流量的 Exact，再考虑源入口 Negative Exact；
5. 默认只输出 Suggest plan。

## 示例 5：Best Deal / 大促期间异常

用户：

```text
昨天 ACOS 突然从 28% 到 45%，是不是要马上降 bid？
```

如果昨天处于 Best Deal、Prime Day、Coupon 或明显价格促销期间：
- 先由 `anomaly-detection` 标记事件上下文；
- 拆解 CPC、CTR、CVR、search-term mix、placement；
- 不将大促日直接与普通日基线机械比较；
- 证据不足时输出 Hold/Watch，不立即降 bid。

## 数据接入建议

```text
Amazon Ads API / MCP / 领星 MCP / CSV / Warehouse
                    ↓
             Normalization Layer
                    ↓
             schemas/*.json
                    ↓
              Agent Skills
                    ↓
        optimization-action proposal
                    ↓
          Guardrails / Approval
                    ↓
        External Executor (optional)
```

本仓库当前不包含真实 Amazon Ads 写入 Executor。
