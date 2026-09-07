---
name: placement-optimization
display_name: 广告版位优化
display_name_en: Placement Optimization
description: 分析 Amazon Ads Sponsored Products 等广告的 Top of Search、Product Pages、Rest of Search 版位表现与 modifier，识别高效版位、浪费和竞价放大风险。适用于 placement 调整和流量结构优化。
description_zh: 分析不同广告版位效率并生成安全的 placement modifier 建议。
description_en: Analyze Amazon Ads placement performance and modifiers across Top of Search, Product Pages and Rest of Search.
version: 0.1.0
author: zerlinpi
---

# Placement Optimization

## 默认模式

`Suggest`。输出 placement modifier 候选，不直接修改 campaign。

## 输入

需要尽量包含：
- placement name；
- impressions、clicks、spend、orders、sales；
- CPC、CVR、ACOS/ROAS；
- current base bid；
- current placement modifier；
- campaign bidding strategy；
- 日期窗口和目标。

## 分析思路

### 1. 看效率，不只看销售额

高销售额版位可能只是获得更多流量。比较：
- spend share vs sales share；
- CPC；
- CVR；
- ACOS/ROAS；
- 样本量。

### 2. 看增量潜力

高效 Top of Search 不代表应该立即大幅提高 modifier。需要判断：
- 当前 impression/click 规模；
- base bid 是否本身偏低/偏高；
- modifier 提升可能带来的边际 CPC；
- 目标是否偏增长还是利润。

### 3. 识别放大风险

base bid、dynamic bidding 和 placement modifier 共同影响实际竞价。不要把 modifier 当作独立旋钮。

## 常见状态

### High-efficiency / underexposed

可考虑小幅提高 modifier 或保持 modifier、先优化 base bid，需判断哪一个更可解释。

### High-efficiency / already dominant

继续扩量可能边际效率下降，先观察，不追涨。

### Low-efficiency / high-spend

检查 query mix 和 CVR 根因后，可建议降低 modifier。

### Low-volume

样本不足，不做强结论。

## 变更原则

- 一次只做可归因的小步调整；
- 若同时需要改 base bid 和 placement，优先分阶段；
- 设验证窗口，避免一天后再反向调整；
- 大促期单独解释。

## 输出

每个 placement：
- current modifier；
- spend share / sales share；
- CPC/CVR/ACOS；
- baseline comparison；
- recommendation: increase/decrease/hold/investigate；
- proposed modifier（如证据充分）；
- confidence；
- evidence；
- guardrails；
- validation window；
- rollback condition。

## 禁止

- 不因为 Top of Search CVR 高就默认提高到极端 modifier；
- 不忽略 dynamic bids strategy；
- 不在 placement 样本很小的时候做大幅动作；
- 不同时大改多个竞价层造成无法归因。
