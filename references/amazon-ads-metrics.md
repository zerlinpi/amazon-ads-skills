# Amazon Ads 指标参考

本文件定义仓库内 Skills 使用的核心指标。除非用户明确指定，否则不要混合不同 Marketplace、币种、时区、归因窗口或日期范围的数据。

## 基础流量指标

| 指标 | 定义 | 公式/说明 |
|---|---|---|
| Impressions | 展示量 | 广告被展示的次数 |
| Clicks | 点击量 | 广告被点击的次数 |
| CTR | 点击率 | `clicks / impressions` |
| Spend | 广告花费 | 指定周期内广告支出 |
| CPC | 平均点击成本 | `spend / clicks` |

## 转化与销售指标

| 指标 | 定义 | 公式/说明 |
|---|---|---|
| Orders | 广告归因订单 | 以数据源归因窗口为准 |
| Units | 广告归因销量 | 与 Orders 不一定相同 |
| Sales | 广告归因销售额 | 以数据源币种为准 |
| CVR | 点击转化率 | `orders / clicks` |
| CPA | 单次订单获客成本 | `spend / orders` |
| ACOS | 广告投入产出比 | `spend / sales` |
| ROAS | 广告支出回报 | `sales / spend` |

当分母为 0 时，不得输出伪造的百分比或无限值；使用 `N/A` 并解释原因。

## 业务级指标

### TACOS

`TACOS = ad_spend / total_sales`

TACOS 需要广告花费和同周期店铺/ASIN 总销售额。只有广告报表时不得自行推算 TACOS。

### Break-even ACOS

简化情况下：

`break_even_acos = contribution_margin_before_ads / revenue`

贡献毛利应尽量考虑商品成本、Amazon referral fee、FBA/履约费用、折扣、退货、税务/其他可归因成本。缺少成本数据时，只能做广告效率分析，不得声称完成利润优化。

### Profit after ads

`profit_after_ads = sales - product_cost - amazon_fees - fulfillment_cost - discounts - returns_cost - ad_spend - other_variable_costs`

如果输入只有广告归因销售额，该结果仅代表广告归因口径，不等同店铺总利润。

## New-to-Brand (NTB)

Sponsored Brands / Sponsored Display 等支持 NTB 指标时，可使用：
- NTB orders
- NTB sales
- NTB order rate
- NTB sales rate

只有数据源明确提供 NTB 时才能分析，不得从普通订单猜测。

## Placement

常见 Sponsored Products 版位：
- Top of Search (first page)
- Product Pages
- Rest of Search

比较版位时至少检查 spend、clicks、orders、sales、CVR、CPC、ACOS/ROAS，并确认 campaign bidding strategy 与 placement modifier 上下文。

## 诊断派生指标

### Spend share

`entity_spend / parent_spend`

用于识别预算集中度和浪费集中度。

### Sales share

`entity_sales / parent_sales`

用于与 Spend share 对比。

### Efficiency index

可使用：

`efficiency_index = target_acos / actual_acos`

仅在 `actual_acos > 0` 且目标 ACOS 已知时使用。大于 1 表示优于目标，小于 1 表示劣于目标。

### Clicks without order

适合用于候选否词或降价诊断，但不能单凭“0 订单”立即否定。必须结合 CPC、商品价格、历史 CVR、点击样本和业务价值。

## 数据质量检查

在高置信度结论前检查：
1. 日期范围和数据新鲜度；
2. Marketplace、币种、时区；
3. 归因窗口；
4. 广告类型（SP/SB/SD）；
5. campaign/ad group/targeting 状态；
6. 库存、Buy Box、Listing 状态；
7. 价格与促销变化；
8. Prime Day、Best Deal、Lightning Deal、Coupon 等活动；
9. 是否存在预算耗尽、投放受限或广告审核问题。
