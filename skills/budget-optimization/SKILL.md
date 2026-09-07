---
name: budget-optimization
display_name: 预算优化
display_name_en: Budget Optimization
description: 分析 Amazon Ads campaign 的预算受限、花费节奏、边际效率和预算分配，生成增预算、降预算、重分配或保持建议。适用于预算不足、预算分配、日预算治理和扩量判断。
description_zh: 在效率、库存和业务目标约束下优化广告预算分配。
description_en: Optimize Amazon Ads budgets using budget constraints, pacing, marginal efficiency, inventory and business goals.
version: 0.1.0
author: zerlinpi
---

# Budget Optimization

## 核心原则

“预算花完”不是自动加预算信号；“预算没花完”也不等于 campaign 有问题。预算动作必须结合边际效率和业务目标。

## 输入

需要：
- daily budget；
- spend；
- budget status / budget utilization（如有）；
- campaign performance；
- 目标 ACOS/ROAS/利润；
- 时间窗口。

推荐：
- 小时级 pacing；
- placement；
- inventory；
- promotion plan；
- campaign priority/role；
- 同账户可调配预算池。

## 诊断

### Efficient and budget constrained

高效且频繁因预算受限停止投放，是优先增预算候选。但还需检查：
- 库存；
- 是否已有足够规模；
- 预算增加后边际流量是否可能明显变差；
- 大促是否即将结束。

### Inefficient and budget constrained

不能因为花完预算就增加。先解决 keyword/search term/bid/placement 效率。

### Efficient and not spending

预算不是瓶颈。检查 bid、流量规模、相关性、排名、广告状态。

### Inefficient and not spending

低优先级；可能需要结构整改而非预算动作。

## Pacing

如有小时数据，检查：
- 是否上午过早耗尽；
- 高转化时段是否没有预算；
- 是否存在大促导致的临时加速；
- 日内波动是否只是单天随机性。

没有小时数据时，不声称可以精确做 dayparting。

## 预算重分配

当总预算固定时：
1. 保护品牌/核心防御和关键业务 campaign；
2. 识别低边际回报预算；
3. 识别高边际回报且受限 campaign；
4. 先小幅重分配；
5. 设验证窗口观察边际 ACOS/ROAS 是否恶化。

## 默认 Guardrail

单次 daily budget 变更建议通常不超过 ±25%，除非用户已有明确大促计划/预算策略。该值是本仓库保守默认，不是 Amazon 官方限制。

## 输出

### Budget map
每个 campaign 标记：
- constrained/not constrained；
- efficient/inefficient；
- role/priority；
- recommended direction。

### Reallocation plan
列出来源 campaign → 目标 campaign，以及：
- 预算前后；
- 证据；
- 预计目的；
- confidence；
- guardrail；
- validation window。

## 禁止

- 不把预算增长当作销售增长保证；
- 不从高效品牌防御 campaign 抽走关键预算而不提示风险；
- 不在库存紧张时建议大幅扩量；
- 不同时大幅改 budget、bid、placement 而没有分阶段验证计划。
