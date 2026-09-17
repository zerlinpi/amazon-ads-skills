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

## Routing boundary

- 本 Skill 负责 **configured keyword/target** 的结构、匹配类型、状态、生命周期和流量分工。
- Configured keyword/target analysis does not require treating the displayed Search Term string as a literal shopper query.
- 一旦结论依赖 Search Term row 的显示字符串、query intent、Exact 收割或“这个词是否是真实 shopper query”，先路由到 `../search-term-analysis/SKILL.md`，由它判断 `term_origin` 和 report/context coverage。
- Search Term 相关否定动作继续路由到 `../negative-targeting/SKILL.md`；具体 bid 数值继续路由到 `../bid-optimization/SKILL.md`。
- 不在本 Skill 复制 Search Term origin、report coverage 或 negative safety 的完整规则；复用对应 specialist 的结论。

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

如果动作依赖 Search Term row，额外需要或明确标记缺失：
- `term_origin`: `literal_query` / `inferred_non_search` / `unknown`；
- report / traffic context / placement / matched-target evidence；
- `search-term-analysis` 对该 row 的 origin 与 actionability 结论。

缺少这些 Search Term 语义证据不会阻止纯 configured keyword/target 的结构审查，但会阻止仅凭 displayed string 生成 action-safe `harvest_to_exact`。

## 生命周期分层

将关键词/目标分为：

### Explore
相关性合理但数据不足。目标是获取样本，不急于做强动作。

### Prove
已有初步点击/转化信号，继续验证稳定性。

### Scale
稳定达到目标，可进入扩量/独立控制审查。`Scale` 是生命周期/结构标签，不自动证明存在可盈利 marginal headroom；具体扩量应再核对预算、竞价、零售和增长约束。

### Protect
品牌词、核心防御词、战略词，即便短期效率波动也需要谨慎处理。

### Reduce
样本充分且持续偏离目标，适合进一步评估降 bid、缩流量或拆分；具体金额/幅度交给相应控制 Skill。

### Stop candidate
长期低价值且无战略意义，才考虑暂停/否定；必须保留证据。若结论来自 Search Term displayed string，仍需经过对应 origin/control gate。

## 匹配类型分析

### Broad
用于探索。检查是否持续产生大量低价值 Search Term，以及赢家是否值得进入收割审查；不要把未知 origin 的显示字符串直接当成 shopper query。

### Phrase
用于意图约束和中等探索。检查流量是否被少数长尾 rows 主导；涉及 query intent 时先走 `search-term-analysis`。

### Exact
用于高控制度的已验证 query/target。检查是否因为 bid/budget 不足而失去已验证流量，但不要因为一个 displayed Search Term string 表现好就反推它一定应该成为 Exact keyword。

不要仅因为 Exact ACOS 高于 Broad 就机械调整；不同 match type 承担的流量阶段不同。

## Search Term → Exact 收割门

`harvest_to_exact` 不是 keyword-optimization 根据 displayed string 自行完成的推断。只有当 Search Term 专项分析能支持以下条件时，才把候选升级为 action-safe：

1. `term_origin = literal_query`，或有等价且可审计的 shopper-query 证据；
2. report/traffic context 足以把显示字符串解释为可由 keyword/target 结构控制的 query；
3. 已检查现有 Exact/target，避免重复或错误迁移；
4. 性能/业务证据支持独立控制，而不是一次偶然订单；
5. 收割后原流量入口的处理顺序明确，避免先切断再创建承接结构。

如果 `term_origin = inferred_non_search` 或 `unknown`，该 row 仍可作为 traffic/match/performance signal，但**不能仅依据 displayed string 输出 action-safe `harvest_to_exact`**。保持 `Manual Review`，或请求 `search-term-analysis` 所需的 origin/context 证据。

## 重复与争抢

检查：
- 同一已验证搜索意图在多个 campaign/ad group 重复投放；
- Exact 已验证收割但源 Broad/Phrase 仍存在需要治理的流量；
- 多个关键词争抢导致数据碎片化；
- 同一 ASIN 的品牌/泛词/竞品意图混在一个结构中。

“同一搜索意图”的判断若依赖 Search Term row，需要先满足 origin/context gate；不能把 inferred/unknown row 的 displayed string 当成确定 query identity。

输出“是否真的需要重构”的证据，不以结构整齐为目的过度拆分。

## 优化工作流

1. 先识别用户目标和业务阶段；
2. 按 configured keyword/target 的性能和已知语义给实体分层；
3. 若需要用 Search Term 解释真实流量质量、query intent 或赢家收割，先调用 `search-term-analysis` 获取 `term_origin` / coverage / actionability；
4. 只有 literal-query（或等价可审计）证据成立时，才把 Search Term winner 升级为 `harvest_to_exact` 候选；`inferred_non_search` / `unknown` 保持 traffic signal / Manual Review；
5. 找到长期低效 configured keyword/target，并判断更可能是 bid、query mix、placement 还是 Listing/CVR 问题；
6. 将 bid 数值问题路由给 `bid-optimization`；
7. 将搜索词否定问题路由给 `negative-targeting`；
8. 输出最小必要结构变更，避免一次大范围重构。

## 输出

### Keyword tiers
按 Scale / Protect / Explore / Reduce / Stop candidate 分类。若某个 tier 结论依赖 Search Term 语义，附上 origin/actionability 状态。

### Structural issues
列出重复争抢、匹配类型错位、过度碎片化、流量意图混杂。需要 query identity 的判断必须注明是否经过 Search Term origin gate。

### Recommended actions
动作类型可包括：
- `harvest_to_exact` — 仅在 literal-query/等价 origin evidence 与控制映射充分时；
- `move_to_dedicated_campaign`
- `change_match_strategy`
- `pause_candidate`
- `route_to_search_term_analysis`
- `route_to_bid_optimization`
- `route_to_negative_targeting`

每项必须包含 reason、evidence、confidence、mode、validation_window。Search Term 派生动作还应包含 `term_origin` / origin confidence 或 `Manual Review` 状态。

## 禁止

- 不因短期高 ACOS 自动 pause；
- 不将品牌词与普通泛词用同一阈值判断；
- 不同时建议同一 keyword “扩量”和“暂停”；
- 不为了所谓最佳实践强制重构本来表现稳定的账户；
- 不把 `inferred_non_search` / `unknown` Search Term row 的 displayed string 直接收割成 Exact keyword；
- 不在 keyword-optimization 内绕过 `search-term-analysis` 已有的 Search Term origin / coverage 安全门。
