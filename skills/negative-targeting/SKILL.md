---
name: negative-targeting
display_name: 否词与否定投放优化
display_name_en: Negative Targeting
description: 从 Amazon Ads Search Term/Targeting 数据中生成安全的 Negative Exact、Negative Phrase 或否定商品投放候选，重点防止误杀品牌词、核心词和历史赢家。适用于否词、浪费控制和流量净化。
description_zh: 识别否词/否定投放候选，并通过误杀保护规则降低流量损失风险。
description_en: Generate guarded negative keyword/product-targeting candidates while protecting brand terms, strategic traffic and historical winners.
version: 0.1.0
author: zerlinpi
---

# Negative Targeting

## 默认模式

`Suggest`。否词属于可能直接切断流量的高影响动作，默认要求人工复核。

## 输入

需要：
- Search Term 或 product targeting 性能；
- 来源 campaign/ad group/target；
- clicks、spend、orders、sales；
- 日期范围；
- 业务目标。

强烈推荐：
- 品牌词保护表；
- 核心类目词/战略词表；
- 历史赢家；
- 已存在 Exact 收割结构；
- 归因延迟和促销上下文。

## 候选类型

### Negative Exact

适合只屏蔽一个明确查询，误伤范围较小。对于单个低效/不相关 query，优先考虑 Exact 而不是 Phrase。

### Negative Phrase

影响范围更广。只有当一个短语意图整体不相关且已评估长尾误伤时才建议。

### Negative Product Targeting

适用于明确低价值 ASIN/Category traffic，需确认广告类型和 API/控制台是否支持对应否定能力。

## 判断顺序

1. 查询/目标是否相关？
2. 是否已有足够样本？
3. 是否存在历史转化？
4. 是否为品牌、防御、战略或高价值 NTB 流量？
5. 是否可能存在归因延迟？
6. 是否处于大促/价格变化窗口？
7. 是否应该先 Exact 收割赢家再否定源流量？
8. Negative Phrase 是否会覆盖其他有价值 query？

任何关键问题无法确认时，标记 `requires_human_review: true`。

## 0 订单处理

不使用单一固定点击阈值。结合：
- 历史 CVR；
- 当前 CPC；
- 商品价格；
- target CPA/ACOS；
- 点击样本；
- 查询相关性；
- 时间跨度。

如果 query 明显语义不相关，即使样本不大也可以列为“高相关性风险”候选，但仍默认人工复核。

## 收割后否定

当 Search Term 是赢家但来自 Broad/Phrase：
1. 先建议建立 Exact；
2. 确认 Exact 处于 enabled 且可承接流量；
3. 再根据结构目标决定是否对源入口 Negative Exact；
4. 不先否定后创建，避免流量断层。

## 输出

每个候选输出：
- search term / target；
- proposed negative type；
- source entity；
- spend/clicks/orders/sales；
- reason；
- evidence；
- protected-term checks；
- collateral-damage risk；
- confidence；
- mode: Suggest；
- requires_human_review；
- rollback/recovery note。

## 禁止

- 不批量否定品牌词而不提示；
- 不将所有 0 订单词直接否定；
- 不用 Negative Phrase 代替精细诊断；
- 不声称否词一定会降低 ACOS；
- 不在不知道现有 Exact/流量结构时自动做“收割 + 否词”执行计划。
