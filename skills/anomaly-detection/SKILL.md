---
name: anomaly-detection
description: Detect unexplained anomaly signals and alert-worthy Amazon Ads metric movements against historical baselines, separating true anomalies from promotions, inventory, pricing events and normal variance before escalation. 中文：用于异常信号识别、告警分级和误报过滤，不替代深度根因诊断。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "亚马逊广告异常检测"
  display_name_en: "Amazon Ads Anomaly Detection"
  description_zh: "用历史基线检测广告异常并减少大促、价格和库存事件造成的误报。"
  description_en: "Detect Amazon Ads anomalies against historical baselines while separating true issues from promotions, inventory, pricing events and normal variance."
---

# Anomaly Detection

## 目标

检测“值得行动”的变化，而不是简单比较今天和昨天。

## Routing boundary

- 这是**异常信号判定 / 告警 triage** Skill：回答“这个变化是否真的异常，还是活动、库存、价格、季节或数据问题可以解释”。
- 如果任务只是例行扫描多个 Campaign 的健康状态、Watch/Critical watchlist 或周趋势监控，交给 `../campaign-health-monitor/SKILL.md`。
- 如果异常已经表现为 sustained business-impact decline，而且用户要知道“为什么下降、损失从哪里来、哪一个原因最有证据”，升级到 `../performance-drop-diagnosis/SKILL.md`。
- 异常本身不是动作授权；即使 severity 为 `Critical`，也不直接推导 bid/budget/negative/placement 变更。

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

`Critical` 只表示值得优先升级调查，不等于已经完成 sustained decline 的因果归因。需要深度损失桥接、控制变更、零售状态与证据强度判断时交给 `performance-drop-diagnosis`。

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

该树用于 anomaly triage 和下一步路由，不把“possible cause”自动升级成确认根因。

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

如果异常已经 sustained 且业务影响明确，输出中应标记 `escalate_to: performance-drop-diagnosis`，而不是在 anomaly Skill 内继续扩展为完整深度诊断。

## 自动化约束

异常检测可以触发其他 Skills，但不直接触发真实账户写入。即便 severity=Critical，也先生成 Suggest/Shadow 动作并通过 `../../references/decision-boundaries.md`。
