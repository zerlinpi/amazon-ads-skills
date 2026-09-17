---
name: search-term-analysis
description: Analyze Amazon Ads Search Term rows for origin, report coverage, query/traffic quality, winner and harvest-candidate evidence. Use when the primary task is interpreting Search Term evidence; route action-safe negative type/scope to negative-targeting and configured keyword/target lifecycle or structure to keyword-optimization.
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "搜索词分析"
  display_name_en: "Search Term Analysis"
  description_zh: "从搜索词数据中发现扩词、收割、否词与流量质量机会。"
  description_en: "Analyze Amazon Ads search terms to find winners, harvest candidates, waste, negative-targeting candidates and traffic-intent shifts."
---

# Search Term Analysis

## Routing boundary

- 本 Skill 负责 **Search Term row 的解释层**：`term_origin`、report/row coverage、query/traffic quality、赢家/浪费证据，以及 harvest / negative 的候选筛选。
- 如果用户的主要目标是选择 action-safe Negative Exact / Negative Phrase / Negative Product Targeting 的类型、scope 与误杀保护，路由到 `../negative-targeting/SKILL.md`；本 Skill 提供证据，不复制否定动作的最终控制决策。
- 如果主要目标是 configured keyword/target 的结构、match type、state、lifecycle 或 traffic ownership，路由到 `../keyword-optimization/SKILL.md`。
- 若同一任务同时需要解释 Search Term row 和选择否定动作，先完成本 Skill 的 origin/coverage/actionability gate，再把结论交给 `negative-targeting`；不要把两个 Skill 当成对同一问题的平行意见。

## 核心原则

Search Term report row 不一定等同于字面意义上的真实用户查询。Amazon 当前 Sponsored Products 文档说明，search term 可以是顾客用于搜索商品的词，也可以是在 non-search context（例如部分站外社交展示）中由系统推断出的 best match。因此先判断 `term_origin`，再决定能否把该 row 当成 literal shopper query 做意图、Exact 收割或 Negative 推理。

建议把 `term_origin` 标记为：
- `literal_query` — 有可靠上下文证明来自 shopper search query；
- `inferred_non_search` — 有可靠证据表明来自 non-search / inferred-best-match context；
- `unknown` — 当前 report/connector 没有提供足够 origin/placement/context 证据。

`unknown` 不自动等于 literal shopper query。

如果结论依赖“报表是否代表完整搜索词总体”、缺失行、impression/CTR coverage、全账户 Top/Bottom 排名或跨报表 reconciliation，按需加载 `../../references/report-coverage.md`。先确认 report 的 `row-inclusion` / eligibility contract，再解释缺失行或总体覆盖。

如果问题涉及 Search Term Impression Share (SIS)、Impression Rank、share-of-voice、竞争可见度或 query growth headroom，按需加载 `../../references/search-term-impression-share.md`。SIS 用作市场可见度/份额证据，不单独证明增量销量或应该提高 bid/budget。

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
- 可选：`term_origin`、placement/context、是否为 on-Amazon search / non-search / off-Amazon context；
- 可选：report_type、row-inclusion / eligibility 规则、分页/完整性状态；
- 可选：Search Term Impression Share、Impression Rank、对应窗口/time unit 和 account scope；
- 可选：历史窗口、品牌词列表、核心类目词、商品价格/利润。

## 覆盖边界

如果数据来自官方 Sponsored Products Search Term report，当前 Amazon Ads 文档说明该报告只包含所选期间至少产生 1 次广告点击的 search-term rows。因此：

- 报表缺失的 search term 不自动等于 `0 impressions` / `0 clicks`；
- 搜索词报表中的 impressions 合计不要求与 Campaign Manager / campaign 总 impressions 完全一致；
- 全账户 query impression coverage、无点击 query 浪费、完整 query CTR denominator 等问题需要兼容的额外来源；
- `top/bottom search terms` 默认只代表当前报表已表示的 clicked population，除非完整总体覆盖另有证明。

另外，row 已出现也不自动证明它是 literal shopper query。对于 inferred non-search rows，点击和转化表现仍然可以用于流量质量/效率分析，但字面 query 意图、Exact keyword 收割和 Negative keyword 动作需要更强的 origin/context 证据。

## 分类

### Winner / Harvest candidate

通常具备：
- 有稳定转化；
- 效率达到或优于目标；
- 样本不是一次偶然订单；
- `term_origin` 足以支持把该字符串解释为 literal shopper query；
- 查询意图与商品高度相关。

若 `term_origin = inferred_non_search` 或 `unknown`，可保留为高价值 traffic/match signal，但不要仅凭字符串自动升级为 Exact keyword。优先输出 `Manual Review` 或请求可解释的 search-context / placement / targeting evidence。

建议：在 literal-query 证据成立时考虑 Exact 收割、单独控制 bid/budget、避免重复争抢。

### Growth candidate

表现好但曝光/点击样本偏少。建议增加观察、提高可控性或测试扩量，不急于做大幅调整。若同时存在 SIS，则先判断 share headroom 与实际 binding constraint，再决定是 bid、budget、placement、routing 还是仅继续观察。

### Explore

相关性合理但样本不足，或 row origin 尚不足以支持 literal-query interpretation。保留探索，不因为短期无单直接否定。

### Waste candidate

花费/点击样本已足够且长期明显偏离目标，且没有品牌/战略价值。若 row 可能来自 inferred non-search context，优先检查实际 targeting/placement/traffic source，不把字面字符串直接当成应该屏蔽的 shopper query。

### Negative candidate

同时满足：
- `term_origin` / traffic context 足以证明 Negative keyword/target 与实际可控流量语义匹配；
- 查询意图明显不相关，或已有足够证据显示长期低价值；
- 否定不会误伤核心流量；
- 已检查品牌词、历史赢家、归因延迟；
- 已确认合适的 Negative Exact / Phrase / product-target 类型。

如果 row 为 `inferred_non_search` 或 `unknown`，不要仅根据显示字符串生成 action-safe Negative keyword。应先确认真正可控的 target/placement/context；证据不足时输出 `Manual Review`。

## 收割工作流

1. 找到高价值 search-term row；
2. 判定 `term_origin`；
3. 只有 literal shopper query 证据足够时，检查是否已经存在 Exact keyword/target；
4. 如不存在，再提出“Exact 收割”建议；
5. 检查原流量入口是否需要保留探索；
6. 只有在流量路由明确时，才考虑对源入口做 Negative Exact 以避免重复；
7. 输出迁移动作顺序，避免先否定导致流量中断。

## 否词保护

在建议 negative 前必须回答：
- 这是 literal shopper query，还是 inferred non-search match / unknown origin？
- 是品牌词吗？
- 是核心产品词/类目词吗？
- 历史是否有订单？
- 是否处于大促或归因延迟窗口？
- 是否只是 CPC 高而非意图错误？
- Negative Phrase 会不会覆盖有价值长尾词？
- 实际可控对象究竟是 keyword、product target、placement/context，还是当前证据不足？

无法回答时只列为 `Manual Review` / 人工复核候选。

## 输出格式

### Search-term summary
- report coverage / row-inclusion status（当影响结论时）；
- `term_origin` / origin confidence（当影响意图解释或动作时）；
- spend / sales / orders；
- top winning terms；
- top waste concentration；
- intent shifts；
- SIS / Impression Rank 与 share-headroom classification（如果提供）。

### Harvest candidates
每项：search term、`term_origin`、现有来源、证据、建议目标结构、confidence。

### Negative candidates
每项：search term、`term_origin`、建议 negative type、证据、误伤风险、confidence、是否需要人工复核。需要形成 action-safe negative type/scope 时交给 `negative-targeting` 完成最终控制决策。

### Keep exploring
列出样本不足、origin 不确定或相关性合理的词，解释为什么暂不动作。

### Action proposals
使用 `../../schemas/optimization-action.json` 的字段。

## 禁止

- 不把所有 Search Term report rows 默认描述成 literal shopper queries；
- 不把 inferred non-search / unknown-origin row 仅按显示字符串机械转成 Exact harvest 或 Negative keyword；
- 不以固定“20 clicks 0 orders”之类规则作为唯一否词依据；
- 不把所有高 ACOS search term 都否定；
- 不在不知道品牌/核心词保护清单时批量输出可执行否词；
- 不把 clicked-only / delivered-only 报表的缺失行自动补成 0；
- 不把 selected report subset 无标注地描述成完整账户搜索词总体；
- 不把低 impression share 单独解释为保证存在可盈利增量，也不从 SIS 直接推导固定 bid/budget 增幅。