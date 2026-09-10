---
name: bid-optimization
description: 基于目标 ACOS/ROAS、历史 CVR、CPC、样本量、placement 与业务阶段，为 Amazon Ads keyword/target 生成保守可验证的 bid 调整建议。适用于降 ACOS、扩量、竞价治理和批量出价建议。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "竞价优化"
  display_name_en: "Bid Optimization"
  description_zh: "在样本和风险边界约束下生成亚马逊广告竞价调整建议。"
  description_en: "Generate guarded Amazon Ads bid recommendations using targets, conversion data, CPC, sample sufficiency, placement and business context."
---

# Bid Optimization

## 默认模式

`Suggest`。任何 bid 变化均为 proposal，不直接写入账户。

## Progressive loading

只有当方向性结论需要转成具体 bid 数值时，再加载：

- `../../references/action-sizing.md`

不要为了普通诊断预加载该 reference。

## 必需上下文

尽量获取：
- current bid；
- clicks、spend、orders、sales；
- 当前 ACOS/ROAS；
- target ACOS/ROAS；
- 历史 CVR；
- CPC；
- campaign bidding strategy；
- placement modifiers；
- 最近一次 bid 变更时间；
- 日期范围和业务阶段。

缺 target 时只做相对诊断，不自行编造“标准 ACOS”。

## 样本检查

先判断当前样本是否足以改变 bid：
- 有多少 clicks/orders；
- 当前窗口是否覆盖合理转化周期；
- 是否存在归因延迟；
- 是否刚调整 bid；
- 历史 CVR 能否支持当前 0 单判断。

样本不足时输出 `hold_bid` 或较低 confidence，而不是强行算新 bid。

## 常用估算

### 基于 ACOS 的方向性调整

当订单样本充分、sales > 0 且 target ACOS 已知时，可用：

`raw_bid = current_bid * target_acos / actual_acos`

这只是方向性/经济性基准，不能直接执行。必须：
- 将 `raw_bid` 与最终 `proposed_value` 分开记录；
- 检查 placement modifier 和 dynamic bidding；
- 检查业务阶段、历史变更和可逆性；
- 只有账户策略、校准历史响应、实验设计或其他可信约束支持时才做数值 damping/截断；
- 数值幅度按 `../../references/action-sizing.md`，不使用仓库级固定百分比。

### 基于 CVR 的可承受 CPC

有目标 ACOS、预期订单价值和 CVR 时：

`max_cpc ≈ average_order_value * cvr * target_acos`

该值是经济性参考，不等于 Amazon auction 中一定应该设置的 bid。

## 调整逻辑

### Increase candidate

满足多数条件：
- 稳定优于目标；
- 有足够样本；
- 流量/预算存在扩量空间；
- 库存允许；
- 最近没有刚做大幅调整。

### Decrease candidate

满足：
- 样本充分；
- 持续高于目标；
- 主要问题确实与流量成本/流量质量有关；
- 不是 Listing、价格、库存、促销造成的临时 CVR 问题。

### Hold

适用于：
- 样本不足；
- 刚调整；
- 大促/促销扰动；
- 指标在目标附近正常波动；
- placement/budget 等其他因素更值得先处理。

## 与 Placement 的关系

如果 Top of Search modifier 很高，base bid 的实际竞价效果可能被放大。调整 bid 前读取 placement 数据；避免同时大幅改变 base bid 和 placement modifier，否则无法判断因果。

## 输出格式

每个候选：

```json
{
  "action_type": "adjust_bid",
  "entity_type": "keyword",
  "entity_id": "...",
  "current_value": 1.20,
  "raw_value": 1.00,
  "proposed_value": 1.10,
  "action_class": "Bounded Adjust",
  "sizing_basis": "account policy + mature same-entity history",
  "reason": "...",
  "evidence": ["..."],
  "confidence": 0.0,
  "mode": "Suggest",
  "constraints_applied": ["..."],
  "validation_window": "...",
  "rollback_condition": "..."
}
```

如果无法证明具体 `proposed_value` 的幅度合理，保留 `raw_value`/方向，说明缺失的 sizing constraint，输出 `Probe`、`Hold` 或 `Manual Review`，不要伪造精确 bid。

## 排序

优先：
1. 高花费且高置信度的明显低效；
2. 高利润、受竞价限制的已验证赢家；
3. 中等置信度调整；
4. 样本不足实体只观察。

## 禁止

- 不用一次大幅降 bid 代替 Search Term/Listing 根因分析；
- 不连续短周期调整同一实体；
- 不在不知道币种/业务目标时输出“最优 bid”；
- 不把第三方示例百分比、其他账户动作幅度或平台 UI 示例直接当作本账户默认调整幅度；
- 不声称算法可以保证排名、销售或 ACOS。
