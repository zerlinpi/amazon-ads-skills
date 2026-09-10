---
name: profitability-analysis
description: 将 Amazon Ads 花费、销售与商品成本、Amazon fees、履约、折扣等结合，计算盈亏平衡 ACOS、广告后贡献利润和可扩量空间。适用于利润优化、目标 ACOS 设定、ASIN 盈亏分析。
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

## 决策逻辑

### ACOS < break-even ACOS

通常仍有正贡献，但是否扩量还要看：
- 库存；
- 边际 CPC/CVR；
- 目标利润率；
- 自然销量和 TACOS；
- 新品/排名战略。

### ACOS 接近 break-even

视目标而定。新品、排名、NTB 可接受接近或短期高于 break-even，但要明确这是战略投资，不应表述为“盈利”。

### ACOS > break-even

先判断是否：
- 暂时大促/价格变化；
- 归因延迟；
- 新品探索；
- 有长期品牌/自然排名价值。

否则优先提出止损和结构优化。

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
- Profitable & scalable
- Profitable but constrained
- Near break-even
- Loss-making
- Unknown due to missing cost data

### Recommended actions
每项提供数字证据、假设、confidence、validation window。

## 保护

不要建议为了降低 ACOS 而盲目砍掉能带来高贡献利润的规模。目标是业务利润，不是让 ACOS 数字看起来更漂亮。
