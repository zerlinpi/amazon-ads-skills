# amazon-ads-skills

Amazon Ads AI Agent 技能库：监控、因果诊断、增长机会、受控实验、变更后复盘、优化记忆、安全优化与历史回放 Eval。

> 当前版本：`v0.9.0`  
> 默认模式：`Suggest`  
> 本仓库不直接修改真实 Amazon Ads 账户；写入由外部 Connector / Executor 负责。

## 核心闭环

```text
Data → Validate → Read relevant history
  → Diagnose / Find Opportunity
  → Action-safe? ─ yes → Suggest
         │
         no
         ↓
      Experiment / Shadow
         ↓
External Executor (optional, authorized)
  → Readback → Reconcile → Post-change Review
  → Keep / Monitor / Rollback Candidate
  → Append event → Refresh entity history
         ↓
Historical Replay / Eval Fixtures
  → detect decision regressions
```

## Progressive Loading

只加载当前决策需要的内容：

```text
薄 SKILL.md / playbook
→ skill-local reference
→ 必要时 shared reference / schema
→ 只读取相关实体的有限历史切片
```

`evals/` 仅用于测试和历史回放，普通账户分析不应加载。

## Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级体检 |
| `campaign-health-monitor` | Campaign 健康监控 |
| `performance-drop-diagnosis` | 业绩突降因果诊断 |
| `growth-opportunity-finder` | 增长机会与 Headroom |
| `experiment-planner` | 受控实验设计 |
| `post-change-review` | Readback、Reconciliation 与优化后效果复盘 |
| `search-term-analysis` | Search Term 赢家、收割、流量质量 |
| `keyword-optimization` | Keyword/Target 生命周期与结构 |
| `bid-optimization` | Bid/CPC 建议 |
| `budget-optimization` | Budget pacing、边际分配、预算池冲突与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative 与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、TACOS |
| `anomaly-detection` | 历史基线异常检测 |
| `amazon-ads-optimizer` | 总调度、记忆检查、去重与冲突消解 |

当前保持 **15 个 Skills**。组合型运营流程优先进入 `playbooks/`；复杂细节优先进入按需 `references/`；可靠性验证优先进入 `evals/`，而不是继续拆新 Skill。

## Historical Replay / Evals

`evals/README.md` 定义 Contract checks + Capability replay。Capability Eval 使用 `met / not_met / insufficient_evidence`，比较决策行为而不是 exact wording。

当前 regression pack 已覆盖 **38 类关键安全风险**，本轮新增：

- Historical restatement after decision：保留 decision-time evidence snapshot，并用 correction/re-evaluation 追加最新解释；
- Audit pagination/truncation：未耗尽 `nextToken/cursor` 的实体结果不得伪装成完整账户覆盖或用于全量排名。

其余覆盖继续包括 Mixed-ASIN、Negative scope、Previous Winner、source/semantic/backfill drift、aggregation integrity、retail shock、application/readback/retry、experiment leakage/interference、portfolio conflict、profitability conflict 等关键风险。

关键原则：

```text
timeout ≠ failed write
executor success ≠ trusted current state
safe retry ≠ application confirmed
same entity id/name across profiles ≠ same optimization identity
verified cross-profile migration → bounded predecessor context, not state cloning
verified cross-marketplace mapping ≠ portable bid/performance conclusion
same metric name/table path ≠ same measurement definition
same source + same semantic version ≠ same backfill maturity
latest restated history ≠ evidence that was available at decision time
extracted_at ≠ available_through
first page + nextToken ≠ complete entity population
profile/campaign/keyword/search-term/placement views ≠ additive spend pools
average(row ACOS/ROAS/CVR) ≠ account ratio
higher ROAS ≠ higher contribution profit
stale retail snapshot ≠ current retail state
campaign-local lift ≠ incremental value when cohorts share demand/resources
campaign-local optimum ≠ portfolio optimum
```

## Data Lineage

统一数据模型见 `references/data-schema.md`。当 baseline/comparison 来自不同 API、MCP、CSV、Warehouse、BI、刷新路径、metric semantic version，或历史快照成熟度不一致时，按需加载 `references/data-lineage.md`。

至少区分：

```text
source system / dataset
extracted_at
available_through
attribution definition / maturity
aggregation grain
filters / scope
dataset semantic version
per-metric definition ID / semantic version
completeness / backfill status
snapshot/backfill maturity
```

比较可标记为 `Comparable / Reconcilable / Directional / Not Comparable / Unknown`。如果 apparent break/lift 与 source switch、semantic cutover 或不对称 backfill 同期发生，先 replay/reconcile，再做高置信动作或 Post-change 结论。

## Account Audit Integrity

`amazon-ads-audit` 已改为薄入口，详细流程按需加载：

`skills/amazon-ads-audit/references/account-audit-framework.md`

账户体检现在明确：

```text
选择一个 canonical additive grain
耗尽 nextToken/cursor 或使用可信完整导出
记录 pages/rows/continuation/truncation 状态
profile total ↔ complete campaign aggregate 做 reconciliation
keyword / search term / placement 等用于分解，不重复累加
先汇总 impressions/clicks/spend/orders/sales，再重新计算 CTR/CPC/CVR/ACOS/ROAS
```

缺失行不自动等于 0；未耗尽分页的结果只能做明确标注的局部/Directional 观察。profile/campaign 总量不一致时先查 coverage、pagination、truncation、filters、freshness 或 lineage，而不是直接评分。

## Weekly Review Playbook

`playbooks/weekly-review.md` 用于周期性账户复盘，并按发现的问题再调用必要 Skills。它不会把固定 ACoS/CTR/CVR 或点击/订单阈值当作自动执行规则，也允许明确输出 Hold。

## Optimization Memory

`references/optimization-memory.md` 采用 append-first event ledger + derived entity history：

```text
schemas/optimization-event.json
→ compact entity history
→ schemas/entity-history.json
→ read-before-recommend gate
```

Memory identity：

```text
marketplace + profile/account scope + entity type + entity id + control dimension
```

对于会 restate 的历史数据，material `evaluated` event 应尽量保存 decision-time `evidence_snapshot`（snapshot/report/export identity、capture time、available-through、maturity 等）。后续 restatement 如果改变结论，不覆盖旧事件，而是追加 `corrected/evaluated` 事件并链接原事件；derived summary 同时区分当时结论与 latest-data interpretation。

Deliberate migration 区分：

```text
same_scope
cross_profile_same_marketplace
cross_marketplace
```

Verified 同 Marketplace 跨 Profile 迁移可以继承 bounded mature evidence，但 successor 当前 Bid/Budget/State/Readback 必须独立读取。

跨 Marketplace 默认 `Partial / Directional Only`：相关性、业务意图、失败模式可以作为假设；Bid、CPC、CVR、ACOS/ROAS、预算、版位倍率、利润阈值和验证时钟不能直接迁移为 action-safe 证据。

## Budget Pool / Portfolio Conflicts

当多个 Campaign 竞争固定业务预算、portfolio cap 或外部 pacing pool 时，`budget-optimization` 按需加载 `skills/budget-optimization/references/portfolio-budget-conflicts.md`。

核心约束：

```text
平均历史 ROAS ≠ 下一单位预算的边际回报
固定总预算 → destination gain 必须同时计算 source opportunity cost
protected spend / business role → 不能被局部效率排序静默覆盖
```

## Experiment Planner

证据不足但可验证的优化优先进入 Experiment / Shadow。实验应预声明 decision question、hypothesis、treatment、control/holdout、primary metric、guardrails、attribution-mature window、contamination risk、allocation integrity、control integrity 与 stop/rollback rule。

当 treatment/control 可能共享 query、target、ASIN、variation family、budget pool、routing、placement、auction 或 automation 时，按需加载 `skills/experiment-planner/references/interference-and-leakage.md`。

长周期实验发生 Keyword/Target、Negative、Automation、Migration、Budget Pool 或 Variation Scope 变化后，需要重新验证 Control Boundary。

## Post-change Review

`post-change-review` 现在除 Readback/Attribution 外，还检查 measurement parity：

```text
baseline D+1 frozen
post window D+7 mature
historical rows mutable
→ 不可直接把差异归因给优化动作
```

优先重新抽取同成熟度 baseline/post、使用一致 snapshot policy，或对 backfill revision 做 reconciliation。若历史在评估落账后发生 material restatement，则同时保留 decision-time snapshot 与 latest restated snapshot，避免 hindsight rewrite。

## Safety

| Mode | 行为 |
|---|---|
| `Read-only` | 读取和解释 |
| `Suggest` | 生成建议；默认 |
| `Shadow` | 模拟、回测、实验 |
| `Execute` | 仅显式授权并交给外部 Executor |

建议应尽量携带 evidence、confidence、data quality、sample sufficiency、guardrails、validation window、rollback condition。

## Multi-Agent Compatibility

| Runtime | 入口 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

三套 Runtime 共用同一个 canonical `skills/` 树，不复制 Amazon Ads 业务逻辑。

## Development Rules

- `SKILL.md` 保持薄，详细知识按需加载；
- 不把固定经验阈值伪装成官方规则或默认动作幅度；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 跨来源/语义版本/快照成熟度趋势先检查 lineage comparability；
- 可变历史的重要 evaluation 保存 decision-time evidence identity；restatement 用 append-only correction，不 hindsight overwrite；
- 账户级排名/覆盖结论先验证 pagination/truncation completeness；
- 聚合 base metrics 后再重算 ratio，禁止把重叠 entity grains 累加为账户总量；
- 同实体新动作先检查未完成验证和可信 readback；
- memory 检索先匹配 marketplace/profile scope，scope 不完整或冲突时 fail closed；
- deliberate migration 需要显式 lineage mapping；跨 Marketplace 性能证据默认不直接迁移；
- stale memory / stale identity / stale retail snapshot 不等于当前状态；
- Executor 的 unknown/timeout 结果先 reconcile，再决定 retry；
- ROAS/ACoS 不能替代贡献利润和业务目标；
- 固定预算池先做 portfolio reconciliation，再给单 Campaign 预算动作；
- 实验先验证 allocation、control integrity、leakage/interference；
- Eval 判断行为而不是 exact wording；
- 默认 Suggest/Shadow，不直接写真实账户。

## Sources & Licenses

项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目。采用流程：`discover → license check → extract generic idea → independently rewrite → Amazon Ads adaptation → safety gate → progressive loading`。已审阅来源见 `docs/SOURCES.md`。

## Roadmap

- [x] Codex / Claude Code / WorkBuddy 共用 Skill 根目录
- [x] Audit / Monitor / Search Term / Bid / Budget / Placement / Negative / Profitability
- [x] Performance Drop Diagnosis + Mixed-ASIN safety
- [x] Growth Opportunity Finder
- [x] Experiment Planner
- [x] Post-change Review + Reconciliation
- [x] Optimization Memory + Entity History
- [x] Contextual Benchmark Policy
- [x] Weekly Review Playbook
- [x] Historical replay / regression fixtures
- [x] Source lineage + semantic metric-version drift
- [x] Cross-profile + cross-marketplace migration safety
- [x] Asymmetric backfill measurement-parity eval
- [x] Slim `performance-drop-diagnosis` and `amazon-ads-audit` entrypoints
- [x] Audit aggregation-integrity eval
- [x] Historical-restatement-after-decision eval
- [x] Truncated/paginated audit coverage eval
- [ ] 继续拆薄其他旧版较厚 Skills
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
