---
name: amazon-ads-audit
display_name: 亚马逊广告账户体检
display_name_en: Amazon Ads Audit
description: 对 Amazon Ads 账户、广告活动与投放结构进行系统体检，识别数据质量、浪费、预算、转化、结构和增长机会。适用于广告体检、账户诊断、周/月复盘、接手新账户等场景。
description_zh: 系统审计亚马逊广告账户，输出问题、证据、优先级和优化建议。
description_en: Audit Amazon Ads accounts for data quality, structure, efficiency, waste, budget constraints, conversion issues and growth opportunities.
version: 0.1.0
author: zerlinpi
---

# Amazon Ads Audit

## 什么时候使用

当用户表达以下意图时使用：
- “帮我体检这个广告账户”
- “这个月广告有什么问题”
- “接手这个账户先看哪里”
- “找出浪费和增长机会”
- “做周报/月报广告诊断”

跨多个优化领域时，本 Skill 可由 `amazon-ads-optimizer` 调用。

## 默认模式

`Suggest`。本 Skill 只分析和生成建议，不直接修改真实 Amazon Ads 账户。

## 输入

尽量收集：
- Marketplace、币种、时区、日期范围、归因窗口；
- campaign / ad group / keyword or target / search term 性能；
- budget、bid、placement；
- 广告类型 SP/SB/SD；
- 业务目标（Target ACOS/ROAS、利润、增长、新品等）；
- 可选：总销售额、商品成本、Amazon fees、库存、价格、促销、Buy Box/Listing 状态。

缺失输入不得自行编造。需要精确指标定义时读取 `../../references/amazon-ads-metrics.md`。

## 工作流

### 1. 数据完整性检查

先判断数据是否可比：
- 是否混合 Marketplace/币种；
- 日期范围是否一致；
- 归因窗口是否明确；
- 是否存在最近 1-3 天归因延迟；
- 是否有 Prime Day、Best Deal、Lightning Deal、Coupon 或大幅价格变化；
- 是否缺 campaign/keyword/search term 某一关键层级。

发现严重数据问题时，把它列为最高优先级，并降低后续结论置信度。

### 2. 账户总览

计算或读取：
- spend、sales、orders；
- ACOS、ROAS、CTR、CPC、CVR；
- 如有总销售额：TACOS；
- 如有成本：break-even ACOS、profit after ads。

对比用户目标和历史基线，不只看单一绝对值。

### 3. 结构审计

检查：
- 广告类型是否覆盖当前业务需要；
- 自动/手动、品牌/泛词、竞品/类目等意图是否混杂；
- 一个 campaign 是否承担过多互相冲突的目标；
- 搜索词是否能被追溯到 target/keyword；
- 是否存在重复争抢、过度碎片化或长期无流量实体；
- 是否存在明显的预算集中风险。

### 4. 浪费识别

优先发现：
- 花费集中但销售贡献低的实体；
- 长期高 CPC + 低 CVR；
- 已有足够样本仍持续偏离目标的关键词/搜索词/目标；
- 无效版位放大；
- 高花费 0 订单候选。

0 订单不等于立即否定；必须结合历史 CVR、CPC、点击样本、品牌价值和归因延迟。

### 5. 增长机会

寻找：
- ACOS/ROAS 明显优于目标但预算受限；
- 高 CVR、低曝光或低 impression share 的已验证目标；
- Search Term 中可收割为 Exact 的赢家；
- 高效 placement；
- 有销量但出价/预算限制明显的 campaign。

增长建议必须同时检查库存和业务目标。

### 6. 优先级排序

按以下顺序：
1. 数据/商品层硬问题；
2. 严重浪费与账户风险；
3. 预算阻塞；
4. 高置信度效率优化；
5. 增长机会；
6. 结构性长期改造。

## 输出格式

输出：

### 账户结论
一句话说明健康状态和最重要问题。

### 健康评分
按 `Data / Structure / Efficiency / Conversion / Budget / Growth` 给出 `Healthy / Watch / Critical`，并说明证据。

### Top issues
每项包含：
- 问题；
- 影响范围；
- 证据；
- 可能原因；
- confidence；
- 优先级。

### Recommended actions
按 `optimization-action` 结构输出建议动作；默认 `mode: Suggest`。

### Need more data
列出会显著提高结论质量但当前缺失的数据。

## 停止条件

遇到以下情况不要输出高置信度动作：
- Marketplace/币种/日期口径无法确定；
- 主要转化问题来自断货、Buy Box、Listing suppression；
- 大促波动但缺少活动上下文；
- 样本量明显不足。

执行边界读取 `../../references/decision-boundaries.md`。
