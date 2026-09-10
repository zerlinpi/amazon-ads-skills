---
name: keyword-optimization
description: 优化 Amazon Ads keyword/target 的结构、匹配类型、状态和流量分工，识别扩量、收割、观察、降权或暂停候选。适用于关键词复盘、匹配类型治理、重复争抢和关键词分层。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "关键词优化"
  display_name_en: "Keyword Optimization"
  description_zh: "优化关键词和投放目标的结构、匹配类型与生命周期管理。"
  description_en: "Optimize Amazon Ads keywords and targets across structure, match types, lifecycle, traffic ownership and performance tiers."
---

# Keyword Optimization

## 默认模式

`Suggest`。本 Skill 只生成结构与状态建议；具体 bid 数值优先交给 `bid-optimization`。

## 输入

推荐提供：
- keyword/target 级性能；
- campaign/ad group；
- match type；
- state、bid；
- 对应 search term；
- 目标 ACOS/ROAS 或业务阶段；
- 品牌词、核心类目词、竞品词等语义标签；
- 历史窗口。

## 生命周期分层

将关键词/目标分为：

### Explore
相关性合理但数据不足。目标是获取样本，不急于做强动作。

### Prove
已有初步点击/转化信号，继续验证稳定性。

### Scale
稳定达到目标，考虑扩量、独立控制和预算保障。

### Protect
品牌词、核心防御词、战略词，即便短期效率波动也需要谨慎处理。

### Reduce
样本充分且持续偏离目标，适合降 bid、缩流量或拆分。

### Stop candidate
长期低价值且无战略意义，才考虑暂停/否定；必须保留证据。

## 匹配类型分析

### Broad
用于探索。检查是否持续产生大量不相关 Search Term，以及赢家是否被收割。

### Phrase
用于意图约束和中等探索。检查流量是否被少数长尾查询主导。

### Exact
用于高控制度收割。检查是否因为 bid/budget 不足而失去已验证流量。

不要仅因为 Exact ACOS 高于 Broad 就机械调整；不同 match type 承担的流量阶段不同。

## 重复与争抢

检查：
- 同一搜索意图在多个 campaign/ad group 重复投放；
- Exact 已收割但源 Broad/Phrase 未做流量治理；
- 多个关键词争抢导致数据碎片化；
- 同一 ASIN 的品牌/泛词/竞品意图混在一个结构中。

输出“是否真的需要重构”的证据，不以结构整齐为目的过度拆分。

## 优化工作流

1. 先识别用户目标和业务阶段；
2. 按性能和语义给 keyword/target 分层；
3. 关联 Search Term，判断真实流量质量；
4. 找到赢家并检查是否需要独立控制；
5. 找到长期低效实体并判断是 bid、query mix、placement 还是 Listing/CVR 问题；
6. 将 bid 数值问题路由给 `bid-optimization`；
7. 将搜索词否定问题路由给 `negative-targeting`；
8. 输出最小必要结构变更，避免一次大范围重构。

## 输出

### Keyword tiers
按 Scale / Protect / Explore / Reduce / Stop candidate 分类。

### Structural issues
列出重复争抢、匹配类型错位、过度碎片化、流量意图混杂。

### Recommended actions
动作类型可包括：
- `harvest_to_exact`
- `move_to_dedicated_campaign`
- `change_match_strategy`
- `pause_candidate`
- `route_to_bid_optimization`
- `route_to_negative_targeting`

每项必须包含 reason、evidence、confidence、mode、validation_window。

## 禁止

- 不因短期高 ACOS 自动 pause；
- 不将品牌词与普通泛词用同一阈值判断；
- 不同时建议同一 keyword “扩量”和“暂停”；
- 不为了所谓最佳实践强制重构本来表现稳定的账户。
