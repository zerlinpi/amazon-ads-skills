---
name: budget-optimization
description: 分析 Amazon Ads campaign 的预算受限、花费节奏、边际效率和预算分配，生成增预算、降预算、重分配或保持建议。适用于预算不足、预算分配、日预算治理和扩量判断。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "预算优化"
  display_name_en: "Budget Optimization"
  description_zh: "在效率、库存和业务目标约束下优化广告预算分配。"
  description_en: "Optimize Amazon Ads budgets using budget constraints, pacing, marginal efficiency, inventory and business goals."
---

# Budget Optimization

## 核心原则

“预算花完”不是自动加预算信号；“预算没花完”也不等于 campaign 有问题。预算动作必须结合边际效率、业务目标和预算池约束。

## Progressive loading

只有多个 Campaign 竞争同一个业务预算、portfolio cap 或外部 pacing pool 时，再加载：

- `references/portfolio-budget-conflicts.md`

只有方向性预算结论需要转成具体金额时，再加载：

- `../../references/action-sizing.md`

普通单 Campaign 预算诊断若不需要具体动作幅度，不加载这些 reference。

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
- 同账户可调配预算池、protected floor 或外部 pacing 约束。

## 诊断

### Efficient and budget constrained

高效且频繁因预算受限停止投放，是优先增预算候选。但还需检查：
- 库存；
- 是否已有足够规模；
- 预算增加后边际流量是否可能明显变差；
- 大促是否即将结束；
- 如果总预算固定，新增预算从哪里来以及来源 Campaign 的机会成本。

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
1. 明确总预算池、业务目标和不可随意移动的 protected spend；
2. 识别低边际回报预算；
3. 识别高边际回报且存在真实 headroom 的 Campaign；
4. 把建议写成来源 Campaign → 目标 Campaign 的平衡转移，而不是彼此冲突的独立增预算建议；
5. 同时估计目标收益与来源机会成本；
6. 采用与证据质量、风险和可逆性匹配的变更幅度；
7. 设验证窗口观察 pool-level 结果与边际效率。

## 变更幅度 Guardrail

不使用通用固定百分比作为默认预算调整幅度。需要给出具体预算金额时，使用 `../../references/action-sizing.md`，并让建议幅度受以下因素共同约束：

- 可用的 marginal headroom 证据；
- 数据量和归因成熟度；
- 库存与促销窗口；
- 预算池可移动空间；
- Campaign 的业务角色和 protected floor；
- 最近是否存在未完成验证的 Bid / Placement / Budget / Structure 变更；
- 动作可逆性与潜在损失上限；
- caller/account 显式提供的 max change、spend-at-risk 或其他政策限制。

证据弱时优先 Directional、Probe/Shadow、Experiment 或 Hold，而不是套用固定比例。无法证明具体 `proposed_value` 时保留方向和缺失约束，不制造精确金额。

## 输出

### Budget map
每个 campaign 标记：
- constrained/not constrained；
- efficient/inefficient；
- role/priority；
- marginal headroom；
- pool constraint / protected floor（如适用）；
- recommended direction。

### Reallocation plan
列出来源 campaign → 目标 campaign，以及：
- 预算前后（仅当具体幅度可被证据支持）；
- action class / sizing basis；
- pool total reconciliation；
- 证据；
- 来源机会成本；
- 预计目的；
- confidence；
- guardrail；
- validation window。

## 禁止

- 不把预算增长当作销售增长保证；
- 不把平均 ROAS/ACOS 当作下一单位预算的边际回报；
- 不在固定总预算池下对所有受限 Campaign 同时给出无法调和的增预算建议；
- 不从高效品牌防御或其他 protected Campaign 抽走关键预算而不提示风险；
- 不在库存紧张时建议大幅扩量；
- 不同时大幅改 budget、bid、placement 而没有分阶段验证计划；
- 不把第三方/平台示例百分比直接当作本账户默认预算动作幅度；
- 不引入未经授权的真实账户写入。
