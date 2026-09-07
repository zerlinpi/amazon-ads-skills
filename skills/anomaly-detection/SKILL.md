---
name: anomaly-detection
display_name: 亚马逊广告异常检测
display_name_en: Amazon Ads Anomaly Detection
description: 基于历史基线检测 Amazon Ads 的展示、点击、CPC、CVR、花费、订单、销售、ACOS/ROAS 和预算异常，并区分真实异常、业务事件与正常波动。适用于自动监控、告警和根因排查。
description_zh: 用历史基线检测广告异常并减少大促、价格和库存事件造成的误报。
description_en: Detect Amazon Ads anomalies against historical baselines while separating true issues from promotions, inventory, pricing events and normal variance.
version: 0.1.0
author: zerlinpi
---

# Anomaly Detection

## 目标

检测“值得行动”的变化，而不是简单比较今天和昨天。

## 输入

最低要求：
- 当前观察窗口；
- 历史基线窗口；
- impressions、clicks、spend、orders、sales；
- date/marketplace/currency。

推荐：
- CPC/CTR/CVR/ACOS/ROAS；
- budget status；
- placement/search term；
- price、promotion、inventory、Buy Box、Listing 状态；
- 近期优化动作日志。

## 基线选择

优先：
1. 同一实体过去 4-8 周滚动分布；
2. 同星期/同 daypart 可比窗口；
3. 同季节历史；
4. 相似实体代理基线。

流量很低时不要使用过度精确的统计结论。

## 检测维度

- Delivery anomaly：impressions/clicks 突降；
- Cost anomaly：CPC/spend 激增；
- Conversion anomaly：CVR/orders/sales 异常下滑；
- Efficiency anomaly：ACOS 恶化或 ROAS 下滑；
- Budget anomaly：过早耗尽或意外不花费；
- Mix anomaly：placement/search-term 流量结构改变。

## 去误报检查

发现异常后，先检查：
- Prime Day / Best Deal / Lightning Deal / Coupon；
- 价格变化；
- 库存/Buy Box/Listing；
- campaign/bid/budget 最近刚调整；
- 新品刚上线；
- 归因延迟；
- 周末/节假日/季节性；
- 数据管道缺数。

如果变化能被事件解释，标记 `explained_event`，而不是 `Critical anomaly`。

## Severity

### Info
偏离较小或样本低，只记录趋势。

### Watch
偏离值得关注，但需更多数据确认。

### Critical
满足：
- 偏离显著；
- 业务影响较大；
- 样本充分或持续多个窗口；
- 无已知合理事件解释。

## 根因树

例如 sales 下降：

```text
Sales ↓
├─ Traffic ↓ ?
│  ├─ Impressions ↓
│  └─ CTR ↓
└─ Conversion ↓ ?
   ├─ CPC ↑ → clicks 减少
   ├─ CVR ↓
   ├─ Price/Promotion changed
   ├─ Inventory/Buy Box issue
   └─ Search term / placement mix changed
```

## 输出格式

每个异常：
- entity；
- severity；
- metric；
- current vs baseline；
- duration；
- estimated business impact；
- possible causes；
- event/confounder checks；
- confidence；
- recommended investigation/action；
- next validation time/window。

## 自动化约束

异常检测可以触发其他 Skills，但不直接触发真实账户写入。即便 severity=Critical，也先生成 Suggest/Shadow 动作并通过 `../../references/decision-boundaries.md`。
