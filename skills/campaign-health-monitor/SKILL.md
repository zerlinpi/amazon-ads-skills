---
name: campaign-health-monitor
description: 监控 Amazon Ads campaign 的流量、花费、转化、预算和效率变化，基于历史基线识别 Healthy、Watch、Critical 状态并给出根因方向。适用于日常巡检、异常告警、周趋势监控。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "广告活动健康监控"
  display_name_en: "Campaign Health Monitor"
  description_zh: "基于历史基线监控广告活动健康度和异常变化。"
  description_en: "Monitor Amazon Ads campaign health across traffic, spend, conversion, budget and efficiency using historical baselines."
---

# Campaign Health Monitor

## 目标

发现“真正需要运营人员注意”的 campaign，而不是对正常波动产生告警疲劳。

## 默认模式

`Suggest`。只输出状态、证据和动作候选。

## 输入

至少需要：
- campaign 当前窗口数据；
- 一个可比较历史窗口或滚动基线；
- 日期、Marketplace、币种；
- campaign state、budget；
- impressions、clicks、spend、orders、sales。

最好额外提供：placement、budget status、bid strategy、库存/促销/价格变化。

## 健康维度

### Traffic
- impressions 是否异常下降/上升；
- clicks/CTR 是否偏离基线；
- campaign 是否突然失去流量。

### Cost
- CPC 是否突增；
- spend 增长是否由流量增加还是 CPC 增加驱动。

### Conversion
- CVR 是否显著低于自己的历史基线；
- orders/sales 下滑是否只是流量下滑导致。

### Efficiency
- ACOS/ROAS 相对目标与历史变化；
- 不在 sales=0 时计算伪 ACOS。

### Budget
- 是否频繁预算耗尽；
- 预算受限 campaign 是否本身高效；
- 是否存在低效 campaign 占用大量预算。

### Delivery
- state/eligibility 是否异常；
- 是否存在 Listing/Buy Box/库存影响。

## 状态规则

不要依赖固定百分比阈值作为唯一依据。结合：
- 历史波动区间；
- 流量体量；
- 目标；
- 业务事件；
- 连续性。

状态含义：
- `Healthy`：核心指标在合理区间，无明确阻塞；
- `Watch`：出现值得观察的偏离，但证据不足以做强动作；
- `Critical`：持续、显著且有业务影响的问题，或 delivery/数据层硬故障。

## 根因拆解

当 sales/ROAS 下降时按顺序拆：
1. impressions 是否下降；
2. CTR 是否下降；
3. CPC 是否上升；
4. clicks 是否不足；
5. CVR 是否下降；
6. price/promotion/inventory/Buy Box 是否改变；
7. search term 或 placement mix 是否变化。

不要把结果指标当根因。

## 输出格式

对每个需要关注的 campaign 输出：

```text
Campaign: <name/id>
Status: Healthy | Watch | Critical
Primary signal: <主要异常>
Evidence: <当前值 vs 基线>
Likely causes: <按可能性排序>
Business impact: <影响>
Confidence: 0-1
Next action: <调查或优化建议>
Validation window: <再次观察条件>
```

然后给出：
- Critical campaigns；
- Watch list；
- Healthy but scalable campaigns；
- Account-wide pattern。

## 特殊事件保护

如果窗口覆盖 Prime Day、Best Deal、LD、Coupon、价格促销或断货，先标记事件，再解释相对基线偏差，避免将正常活动波动误报。

## 安全

任何 bid/budget/placement 变化只作为 `Suggest` action proposal。实际执行交给外部 executor，并遵守 `../../references/decision-boundaries.md`。
