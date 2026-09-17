---
name: profitability-analysis
description: 将 Amazon Ads 花费、销售与商品成本、Amazon fees、履约、折扣等结合，计算盈亏平衡 ACOS、广告后贡献利润和经济性边界。适用于利润优化、目标 ACOS 设定、ASIN 盈亏分析；不单独认证增长 headroom 或扩量动作。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "广告利润分析"
  display_name_en: "Advertising Profitability Analysis"
  description_zh: "从利润而非单一 ACOS 角度评估亚马逊广告。"
  description_en: "Evaluate Amazon Ads using break-even ACOS, contribution margin and profit-after-ads rather than ACOS alone."
---

# Profitability Analysis

## 什么时候使用

- 用户问“ACOS 多少才不亏”；
- 想设 Target ACOS；
- 想知道哪些 ASIN/campaign 真正赚钱；
- 想判断高 ACOS 是否仍可接受；
- 想做利润最大化而不是销售额最大化。

## Routing boundary

本 Skill 负责 **economic eligibility**：回答当前广告在给定成本口径下是否盈利、接近盈亏平衡、亏损，或在明确战略目标下可以承受怎样的效率区间。

Economic eligibility is not the same as growth qualification. 一个实体历史上盈利或 ACOS 低于 break-even，只能说明当前/历史经济性具备一定承受空间，**不能证明存在 additional demand headroom、incrementality 或正确的 binding control**。

当用户问“该不该加预算 / 加 bid / 扩 Placement / 哪些赢家值得更多投资 / 哪里可以继续放量”时：

1. 本 Skill 提供 break-even、contribution margin、profit-after-ads 等经济输入；
2. 将增长资格交给 `../growth-opportunity-finder/SKILL.md`；
3. 由 growth Skill 再核对 marginal headroom、retail readiness、incrementality/cannibalization、attribution quality 和 binding control；
4. 具体 bid/budget/placement 幅度再交给对应控制 Skill 与 `../../references/action-sizing.md`。

因此“盈利”不是“扩量授权”。

## 所需数据

最低利润模型需要：
- revenue/sales；
- ad spend；
- product cost；
- Amazon referral fee；
- fulfillment/FBA cost。

推荐增加：
- coupons/discounts；
- returns/refunds；
- storage/inbound/other variable costs；
- 总销售额（用于 TACOS）；
- VAT/tax 处理口径（若业务需要）。

缺少成本时必须明确：只能做广告效率分析，不能声称“盈利/亏损”。

## 计算

精确定义参考 `../../references/amazon-ads-metrics.md`。

### Contribution before ads

`revenue - product_cost - amazon_fees - fulfillment - discounts - returns_cost - other_variable_costs`

### Break-even ACOS

`contribution_before_ads / revenue`

### Profit after ads

`contribution_before_ads - ad_spend`

### TACOS

仅当 total sales 已提供：

`ad_spend / total_sales`

## 分析层级

按可用数据分析：
- ASIN；
- campaign；
- ad group；
- keyword/target；
- search term。

不要把 SKU/ASIN 不同毛利的流量混在一起用统一 break-even ACOS 判断，除非用户明确接受近似。

Search Term 级利润视图仍受 Search Term report 的 row eligibility / origin / attribution 范围约束；利润计算不会把缺失或未表示的 row 自动补成 0，也不会把 displayed string 自动解释成 literal shopper query。

## 决策逻辑

### ACOS < break-even ACOS

通常仍有正贡献，但这只建立**经济性资格**，不是 growth headroom 证明。是否增加投资还要交给增长审查，并至少考虑：
- inventory / retail readiness；
- marginal CPC/CVR，而不是只看历史平均 CPC/CVR；
- additional demand / marginal headroom；
- incrementality 与 cannibalization；
- 实际 binding control 是 budget、bid、placement、coverage 还是其它约束；
- 目标利润率；
- 自然销量和 TACOS；
- 新品/排名/防御战略。

### ACOS 接近 break-even

视目标而定。新品、排名、NTB 可接受接近或短期高于 break-even，但要明确这是战略投资，不应表述为“盈利”，也不应仅凭战略标签自动判定增长动作安全。

### ACOS > break-even

先判断是否：
- 暂时大促/价格变化；
- 归因延迟；
- 新品探索；
- 有长期品牌/自然排名价值。

否则优先提出止损和结构优化。若业务明确接受战略性亏损，必须把战略例外与普通盈利流量分开标注。

## 输出格式

### Profitability snapshot
- Revenue
- Contribution before ads
- Break-even ACOS
- Actual ACOS
- Profit after ads
- Profit margin after ads
- TACOS（如可用）

### Entity ranking
按利润贡献而非销售额排序，标记：
- `Profitable — growth review required` — 当前经济性为正；如用户要扩量，继续交给 `growth-opportunity-finder`；
- `Profitable but constrained` — 当前经济性为正，但已知库存、战略、结构或其它约束使增长动作暂不可用；
- `Near break-even`；
- `Loss-making`；
- `Unknown due to missing cost data`。

不要在 profitability-analysis 内使用 `scalable` 作为最终认证标签；只有 growth qualification 完成后才讨论 Action-safe scale。

### Recommended actions

利润 Skill 的动作主要是：
- 调整/校准目标经济边界；
- 标记亏损或接近盈亏平衡实体；
- 为 bid/budget/growth 分析提供可审计的 break-even / contribution inputs；
- 将真正的 scale decision 路由给 `growth-opportunity-finder`。

每项提供数字证据、成本假设、confidence、validation window。若建议需要增加投资，输出 `route_to_growth_opportunity_finder`，而不是直接从历史利润推出加预算/加 bid。

## 保护

- 不要建议为了降低 ACOS 而盲目砍掉能带来高贡献利润的规模。目标是业务利润，不是让 ACOS 数字看起来更漂亮。
- 同样，不要因为当前利润为正就假定下一单位流量仍以相同 CPC/CVR/订单结构获取；historical average profitability ≠ marginal profitability。
- Profitability qualification ≠ headroom ≠ incrementality ≠ binding control。增长动作需要对应 specialist 的额外证据门。
