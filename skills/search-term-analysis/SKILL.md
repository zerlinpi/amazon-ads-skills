---
name: search-term-analysis
display_name: 搜索词分析
display_name_en: Search Term Analysis
description: 分析 Amazon Ads Search Term 数据，识别赢家词、扩词/Exact 收割候选、浪费词、否词候选和流量意图偏移。适用于搜索词报告、扩词、否词、流量质量诊断。
description_zh: 从搜索词数据中发现扩词、收割、否词与流量质量机会。
description_en: Analyze Amazon Ads search terms to find winners, harvest candidates, waste, negative-targeting candidates and traffic-intent shifts.
version: 0.1.0
author: zerlinpi
---

# Search Term Analysis

## 核心原则

Search Term 是真实用户查询，不等同 keyword/target。先分析查询表现，再决定是否把它收割、保护、观察或作为否词候选。

## 默认模式

`Suggest`。禁止自动添加 negative keyword/target。

## 输入

需要尽量包含：
- search_term；
- campaign_id / ad_group_id；
- matched_target_id / match_type；
- impressions、clicks、spend、orders、sales；
- 日期、币种、Marketplace；
- Target ACOS/ROAS 或业务目标；
- 可选：历史窗口、品牌词列表、核心类目词、商品价格/利润。

## 分类

### Winner / Harvest candidate

通常具备：
- 有稳定转化；
- 效率达到或优于目标；
- 样本不是一次偶然订单；
- 查询意图与商品高度相关。

建议：考虑 Exact 收割、单独控制 bid/budget、避免重复争抢。

### Growth candidate

表现好但曝光/点击样本偏少。建议增加观察、提高可控性或测试扩量，不急于做大幅调整。

### Explore

相关性合理但样本不足。保留探索，不因为短期无单直接否定。

### Waste candidate

花费/点击样本已足够且长期明显偏离目标，且没有品牌/战略价值。

### Negative candidate

同时满足：
- 查询意图明显不相关，或已有足够证据显示长期低价值；
- 否定不会误伤核心流量；
- 已检查品牌词、历史赢家、归因延迟；
- 已确认合适的 Negative Exact / Phrase 类型。

## 收割工作流

1. 找到高价值 search term；
2. 检查是否已经存在 Exact keyword/target；
3. 如不存在，提出“Exact 收割”建议；
4. 检查原流量入口是否需要保留探索；
5. 只有在流量路由明确时，才考虑对源入口做 Negative Exact 以避免重复；
6. 输出迁移动作顺序，避免先否定导致流量中断。

## 否词保护

在建议 negative 前必须回答：
- 是品牌词吗？
- 是核心产品词/类目词吗？
- 历史是否有订单？
- 是否处于大促或归因延迟窗口？
- 是否只是 CPC 高而非意图错误？
- Negative Phrase 会不会覆盖有价值长尾词？

无法回答时只列为“人工复核候选”。

## 输出格式

### Search-term summary
- spend / sales / orders；
- top winning terms；
- top waste concentration；
- intent shifts。

### Harvest candidates
每项：search term、现有来源、证据、建议目标结构、confidence。

### Negative candidates
每项：search term、建议 negative type、证据、误伤风险、confidence、是否需要人工复核。

### Keep exploring
列出样本不足但相关性合理的词，解释为什么暂不动作。

### Action proposals
使用 `../../schemas/optimization-action.json` 的字段。

## 禁止

- 不以固定“20 clicks 0 orders”之类规则作为唯一否词依据；
- 不把所有高 ACOS search term 都否定；
- 不在不知道品牌/核心词保护清单时批量输出可执行否词。
