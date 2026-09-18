---
name: negative-targeting
description: Generate action-safe Amazon Ads negative keyword or negative product-targeting candidates with protected-term, origin/context and collateral-damage checks. Use when the primary task is choosing negative type/scope; route Search Term row interpretation to search-term-analysis.
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "否词与否定投放优化"
  display_name_en: "Negative Targeting"
  description_zh: "识别否词/否定投放候选，并通过误杀保护规则降低流量损失风险。"
  description_en: "Generate guarded negative keyword/product-targeting candidates while protecting brand terms, strategic traffic and historical winners."
---

# Negative Targeting

## Connector capability gate

When a conclusion depends on live MCP/API/connector data, load `../../references/connector-capability.md` before interpreting missing or empty fields. If a machine-readable capability snapshot is available, identify the exact required capability IDs and run `../../scripts/evaluate_connector_capability_gate.py` **before metric interpretation**.

- `Pass` — continue with the Skill's normal evidence, sufficiency, lineage and safety checks.
- `Degraded` — do not make a high-confidence dependent recommendation; keep the result to `Directional`, `Hold`, `Alternate Source`, `Missing Data`, or `Manual Review`.
- `Blocked` — do not treat the dependent observation as action-safe until the capability is resolved or an allowed alternate source is verified.
- `missing_evidence_policy = never_zero` — `Partial`, `Unsupported`, `Unknown`, or absent connector capability is never a numeric zero, unchanged state, or proof that the platform lacks the feature.

This gate is read-only and does not authorize live Amazon Ads mutation.

## 默认模式

`Suggest`。否词属于可能直接切断流量的高影响动作，默认要求人工复核。

## Routing boundary

- 本 Skill 负责 **negative control decision**：选择 Negative Exact / Negative Phrase / Negative Product Targeting 的类型与 scope，并检查 protected terms、origin/context、历史赢家、归因延迟和 collateral-damage risk。
- 如果主要任务是解释 Search Term report row、判断 `term_origin`、report coverage、query/traffic quality、winner/waste evidence，先路由到 `../search-term-analysis/SKILL.md`；本 Skill 消费该证据，不复制 Search Term 解释层。
- 如果主要任务是 configured keyword/target 的结构、match type、state 或 lifecycle，而不是否定控制，路由到 `../keyword-optimization/SKILL.md`。
- Search Term row 缺少 origin/context/control mapping 时，不因为用户说“否词”就跳过解释层；先补证据或保持 `Manual Review`。

## 输入

需要：
- Search Term 或 product targeting 性能；
- 来源 campaign/ad group/target；
- clicks、spend、orders、sales；
- 日期范围；
- 业务目标。

强烈推荐：
- `term_origin`：`literal_query` / `inferred_non_search` / `unknown`；
- placement / traffic context / matched targeting evidence；
- 品牌词保护表；
- 核心类目词/战略词表；
- 历史赢家；
- 已存在 Exact 收割结构；
- 归因延迟和促销上下文。

Amazon 当前 Sponsored Products Search Term report 可能包含 shopper search query，也可能包含 non-search context 中由系统推断出的 best match。因此 Search Term row 的显示字符串不自动等于 literal shopper query。

## 候选类型

### Negative Exact

适合只屏蔽一个明确查询，误伤范围较小。对于单个低效/不相关 query，优先考虑 Exact 而不是 Phrase，但前提是 `term_origin` / context 足以证明显示字符串确实对应可由 Negative keyword 控制的 literal shopper query。

### Negative Phrase

影响范围更广。只有当一个短语意图整体不相关、origin/context 明确且已评估长尾误伤时才建议。

### Negative Product Targeting

适用于明确低价值 ASIN/Category traffic，需确认广告类型和 API/控制台是否支持对应否定能力。

## 判断顺序

1. 该 row 是 literal shopper query、inferred non-search match，还是 `unknown` origin？
2. 实际可控对象是 keyword、product target、placement/context，还是尚不明确？
3. 查询/目标是否相关？
4. 是否已有足够样本？
5. 是否存在历史转化？
6. 是否为品牌、防御、战略或高价值 NTB 流量？
7. 是否可能存在归因延迟？
8. 是否处于大促/价格变化窗口？
9. 是否应该先 Exact 收割赢家再否定源流量？
10. Negative Phrase 是否会覆盖其他有价值 query？

任何关键问题无法确认时，标记 `requires_human_review: true`。

如果 `term_origin = inferred_non_search` 或 `unknown`，不要仅依据显示字符串输出 action-safe Negative keyword。先寻找 matched target / placement / traffic-context 证据；无法建立控制映射时保持 `Manual Review`。

## 0 订单处理

不使用单一固定点击阈值。结合：
- 历史 CVR；
- 当前 CPC；
- 商品价格；
- target CPA/ACOS；
- 点击样本；
- 查询相关性；
- `term_origin` 与 traffic context；
- 时间跨度。

如果 literal query 明显语义不相关，即使样本不大也可以列为“高相关性风险”候选，但仍默认人工复核。对于 inferred non-search / unknown-origin rows，字面语义不相关本身不足以证明 Negative keyword 是正确控制。

## 收割后否定

当 Search Term 是赢家但来自 Broad/Phrase：
1. 先确认 `term_origin` 足以支持 literal-query interpretation；
2. 再建议建立 Exact；
3. 确认 Exact 处于 enabled 且可承接流量；
4. 再根据结构目标决定是否对源入口 Negative Exact；
5. 不先否定后创建，避免流量断层。

## 输出

每个候选输出：
- search term / target；
- `term_origin` / origin confidence；
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

- 不把 inferred non-search / unknown-origin Search Term row 仅按显示字符串自动转成 Negative keyword；
- 不批量否定品牌词而不提示；
- 不将所有 0 订单词直接否定；
- 不用 Negative Phrase 代替精细诊断；
- 不声称否词一定会降低 ACOS；
- 不在不知道现有 Exact/流量结构时自动做“收割 + 否词”执行计划。