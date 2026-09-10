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

当前 regression pack 已覆盖 **42 类关键安全风险**，近期新增：

- Report row-eligibility / selection bias：clicked-only 或 impression-qualified 报表即使完整生成，也不等于完整逻辑总体；禁止把缺失行自动补 0，或把 selected subset 当作全账户 query/target population；
- Placement coupled-control confounding：Base/target bid、placement modifier、dynamic bidding、schedule/event rules 在同一窗口变化时，不把版位 ROAS lift 归因给单一 modifier；
- Upstream budget-cap bottleneck：Campaign 提额前先核对 Sponsored Products account-level / portfolio / business cap；平台 estimated missed sales/clicks 只作为模型机会信号，不当作保证增量；
- Contextual action sizing：禁止在账户没有 sizing policy / calibrated response 时，用仓库默认百分比把方向性 Bid/预算结论伪装成精确动作；
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
successful report completion ≠ complete logical population
clicked-only search-term rows ≠ all query impressions
missing report row ≠ zero unless the report contract proves it
first page + nextToken ≠ complete entity population
raw economic bid/budget anchor ≠ action-safe final magnitude
no account sizing policy ≠ permission to invent a default ±X%
campaign budget headroom ≠ account/portfolio budget headroom
estimated missed sales/clicks ≠ guaranteed incrementality
configured bid controls ≠ realized auction exposure
placement ROAS lift under overlapping control changes ≠ single-modifier causality
profile/campaign/keyword/search-term/placement views ≠ additive spend pools
average(row ACOS/ROAS/CVR) ≠ account ratio
higher ROAS ≠ higher contribution profit
stale retail snapshot ≠ current retail state
campaign-local lift ≠ incremental value when cohorts share demand/resources
campaign-local optimum ≠ portfolio optimum
```

## Data Lineage

统一数据模型见 `references/data-schema.md`。当 baseline/comparison 来自不同 API、MCP、CSV、Warehouse、BI、刷新路径、metric semantic version、report row-inclusion / eligibility contract，或历史快照成熟度不一致时，按需加载 `references/data-lineage.md`；当问题依赖“返回行是否代表完整总体”时，再按需加载 `references/report-coverage.md`。

至少区分：

```text
source system / dataset
extracted_at
available_through
attribution definition / maturity
aggregation grain
filters / scope
row-inclusion / eligibility contract
dataset semantic version
per-metric definition ID / semantic version
completeness / backfill status
snapshot/backfill maturity
```

比较可标记为 `Comparable / Reconcilable / Directional / Not Comparable / Unknown`。如果 apparent break/lift 与 source switch、semantic cutover、row-eligibility switch 或不对称 backfill 同期发生，先 replay/reconcile，再做高置信动作或 Post-change 结论。

## Report Coverage / Row Eligibility

`references/report-coverage.md` 用于处理“报表成功生成，但逻辑总体并不一定全部出现在行中”的情况。

当前 Amazon Ads 公共文档明确给出一些 outcome-based inclusion contract，例如 Sponsored Products Search Term report 只表示至少产生 1 次广告点击的搜索词，而 Targeting report 则面向至少有 impression 的交付目标。仓库因此要求：

```text
report complete under its contract
→ 可以分析 represented population

report complete under its contract
≠ 可以自动推断 omitted rows = 0
≠ 可以自动声称 full account/query/target population coverage
```

Search Term harvest / negative / clicked-query efficiency 仍可使用已表示的 clicked population；但 zero-click query identification、完整 query-impression coverage、全账户 query CTR denominator 或完整 population ranking 需要兼容的额外来源。不同报告之间做 reconciliation 时，要把 row-inclusion / eligibility 视为 measurement identity，而不只看列名或来源系统。

## Account Audit Integrity

`amazon-ads-audit` 已改为薄入口，详细流程按需加载：

`skills/amazon-ads-audit/references/account-audit-framework.md`

账户体检现在明确：

```text
选择一个 canonical additive grain
耗尽 nextToken/cursor 或使用可信完整导出
记录 pages/rows/continuation/truncation 状态
确认 report row-inclusion / eligibility 是否支持所需总体结论
profile total ↔ complete campaign aggregate 做 reconciliation
keyword / search term / placement 等用于分解，不重复累加
先汇总 impressions/clicks/spend/orders/sales，再重新计算 CTR/CPC/CVR/ACOS/ROAS
```

缺失行不自动等于 0；未耗尽分页的结果只能做明确标注的局部/Directional 观察，clicked-only / delivered-only subset 也只能支持其 represented population 范围内的结论。profile/campaign 总量不一致时先查 coverage、pagination、row eligibility、truncation、filters、freshness 或 lineage，而不是直接评分。

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

当多个 Campaign 竞争固定业务预算、portfolio cap、Sponsored Products account-level daily budget cap 或外部 pacing pool 时，`budget-optimization` 按需加载 `skills/budget-optimization/references/portfolio-budget-conflicts.md`。

核心约束：

```text
平均历史 ROAS ≠ 下一单位预算的边际回报
campaign budget increase ≠ deliverable extra spend when an upstream cap is binding
estimated missed opportunity = modeled directional evidence, not guaranteed incrementality
固定总预算 → destination gain 必须同时计算 source opportunity cost
protected spend / business role → 不能被局部效率排序静默覆盖
```

预算诊断现在区分 observed serving evidence（spend、budget、average time in budget、cap utilization）与 modeled opportunity evidence（estimated missed impressions/clicks/sales、recommended budget）。上游 cap 无足够 headroom 时，要么给出 source → destination 的平衡重分配，要么把上游 cap 变更作为单独业务预算决策；不能只提高 Campaign 数值后假定 delivery 会增加。

## Contextual Action Sizing

当 `bid-optimization`、`budget-optimization` 或其他 monetary-control Skill 需要把方向性结论转成具体金额/百分比时，按需加载 `references/action-sizing.md`。

核心顺序：

```text
raw economic / directional anchor
→ evidence strength + current-state confidence
→ downside exposure + reversibility + coupled controls
→ explicit account/caller policy or calibrated response
→ proposed value / Probe / Hold / Experiment
```

仓库不再提供全账户通用的单次 Bid/预算调整百分比。公开案例、平台 UI 示例、第三方 Skill 阈值和其他账户历史都不能直接成为当前账户的默认幅度。没有账户策略、校准响应、边际 headroom 或明确实验约束时，允许保留方向而不制造 `proposed_value` 的假精度。

## Placement Control Interaction

`placement-optimization` 在 base/target bid、placement adjustment、dynamic bidding、schedule/event bid rules 等可能同时影响版位曝光时，按需加载：

`skills/placement-optimization/references/realized-bid-exposure.md`

核心区分：

```text
configured controls = intent
placement delivery / CPC / traffic mix = realized evidence
```

仓库不会把配置值拼成未经平台行为证实的精确 auction-level effective-bid 公式。多个 material bidding controls 在同一 measurement window 变化时，版位效果应标记为 `Directional / Confounded`，优先重建 control timeline，再选择单一可解释控制、Hold 或 Shadow/Experiment。

历史 Top of Search / Product Pages / Rest of Search ROAS/CVR 只是过去 realized traffic 的证据，不自动证明继续提高 modifier 后仍有同等 marginal efficiency。

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

建议应尽量携带 evidence、confidence、data quality、sample sufficiency、guardrails、validation window、rollback condition。数值动作还应携带 raw/directional anchor、sizing basis 和 applied constraints；缺少可靠 sizing basis 时不强制输出精确动作幅度。

## Multi-Agent Compatibility

| Runtime | 入口 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

三套 Runtime 共用同一个 canonical `skills/` 树，不复制 Amazon Ads 业务逻辑。`SKILL.md` frontmatter 对齐 Agent Skills 规范：顶层仅使用 `name`、`description` 及规范允许的可选字段；作者、版本、双语显示名等仓库自定义信息统一放入 `metadata`，避免在严格 validator/runtime 下因未知顶层字段加载失败。

## Deterministic Repository Validation

为避免后续吸收第三方方法时引入“某个 Runtime 能读、另一个 Runtime 加载失败”或“Eval 索引存在但 fixture contract 已损坏”的静默漂移，仓库提供纯 Python 标准库校验器：

```bash
python -m unittest discover -s tests -v
python scripts/validate_skills.py .
python scripts/validate_evals.py .
```

`validate_skills.py` 检查：`skills/*/SKILL.md` 必须存在、`name/description` 必填、顶层 frontmatter 字段白名单、`name` 与目录一致、禁止 nested `SKILL.md`、以及 `SKILL.md` 中相对 Markdown 引用必须留在仓库内且真实存在。

`validate_evals.py` 检查全部 `evals/fixtures/*.json`：JSON 可解析、字段/enum 符合 closed-world contract、fixture ID 与文件名一致且不冲突、entrypoint 在仓库内真实存在、rubric/required observation 不得正向要求 live mutation。

`.github/workflows/validate-skills.yml` 对相关 Push/PR 运行 unit tests + 两个 validator。Deterministic pass 只证明 packaging/fixture contract integrity；Amazon Ads 决策质量仍由 capability replay 验证，二者不能互相替代。

## Development Rules

- `SKILL.md` 保持薄，详细知识按需加载；
- `SKILL.md` 顶层 frontmatter 保持 Agent Skills spec-compatible，自定义字段进入 `metadata`；
- 修改 Skill/reference/schema/playbook/eval 后运行 unit tests + Skill/Eval deterministic validators；
- 不把固定经验阈值伪装成官方规则或默认动作幅度；
- monetary-control 建议必须区分 raw anchor 与 final magnitude；无账户级 sizing basis 时不制造默认百分比；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 跨来源/语义版本/快照成熟度/row-inclusion contract 趋势先检查 lineage comparability；
- 报表行缺失先检查 row-inclusion / eligibility；除非 report contract 明确支持，否则不自动补 0、不声称完整总体；
- 可变历史的重要 evaluation 保存 decision-time evidence identity；restatement 用 append-only correction，不 hindsight overwrite；
- 账户级排名/覆盖结论先验证 pagination/truncation completeness 与 population-selection contract；
- 聚合 base metrics 后再重算 ratio，禁止把重叠 entity grains 累加为账户总量；
- placement optimization 必须区分 configured controls 与 realized exposure；多个 material bidding controls 同窗变化时不做单一 modifier 因果归因；
- 同实体新动作先检查未完成验证和可信 readback；
- memory 检索先匹配 marketplace/profile scope，scope 不完整或冲突时 fail closed；
- deliberate migration 需要显式 lineage mapping；跨 Marketplace 性能证据默认不直接迁移；
- stale memory / stale identity / stale retail snapshot 不等于当前状态；
- Executor 的 unknown/timeout 结果先 reconcile，再决定 retry；
- ROAS/ACoS 不能替代贡献利润和业务目标；
- 预算优化先解析 campaign → portfolio → account/business/external constraint hierarchy；平台 missed-opportunity estimate 不当作保证增量；
- 固定预算池先做 portfolio reconciliation，再给单 Campaign 预算动作；
- 实验先验证 allocation、control integrity、leakage/interference；
- Eval 判断行为而不是 exact wording；
- 默认 Suggest/Shadow，不直接写真实账户。

## Sources & Licenses

项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目。采用流程：`discover → license check → extract generic idea → independently rewrite → Amazon Ads adaptation → safety gate → progressive loading`。已审阅来源见 `docs/SOURCES.md`，单轮专项研究可放在 `docs/research/` 并保持来源与采用边界可追溯。

## Roadmap

- [x] Codex / Claude Code / WorkBuddy 共用 Skill 根目录
- [x] Agent Skills strict frontmatter compatibility（custom metadata nested under `metadata`）
- [x] Deterministic Skill validator + unit tests + CI gate
- [x] Deterministic Eval fixture validator + CI gate
- [x] Audit / Monitor / Search Term / Bid / Budget / Placement / Negative / Profitability
- [x] Performance Drop Diagnosis + Mixed-ASIN safety
- [x] Growth Opportunity Finder
- [x] Experiment Planner
- [x] Post-change Review + Reconciliation
- [x] Optimization Memory + Entity History
- [x] Contextual Benchmark Policy
- [x] Contextual action sizing / no universal default change percentage
- [x] Weekly Review Playbook
- [x] Historical replay / regression fixtures
- [x] Source lineage + semantic metric-version drift
- [x] Report row-inclusion / eligibility coverage safety
- [x] Cross-profile + cross-marketplace migration safety
- [x] Asymmetric backfill measurement-parity eval
- [x] Slim `performance-drop-diagnosis` and `amazon-ads-audit` entrypoints
- [x] Audit aggregation-integrity eval
- [x] Historical-restatement-after-decision eval
- [x] Truncated/paginated audit coverage eval
- [x] Upstream account/portfolio budget-cap feasibility eval
- [x] Placement realized-exposure / coupled-control attribution eval
- [ ] 继续拆薄其他旧版较厚 Skills
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
