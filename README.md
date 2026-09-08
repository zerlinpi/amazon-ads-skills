# amazon-ads-skills

Amazon Ads AI Agent 技能库：监控、因果诊断、增长机会、受控实验、变更后复盘、优化记忆与安全优化。

> 当前版本：`v0.7.0`  
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
  → Readback → Post-change Review
  → Keep / Monitor / Rollback Candidate
  → Append event → Refresh entity history
```

## Progressive Loading

目标是只加载当前决策需要的内容：

```text
薄 SKILL.md / playbook
        ↓
命中具体问题
        ↓
skill-local reference
        ↓
必要时 shared reference / schema
        ↓
只读取相关实体的有限历史切片
```

例如：

```text
“为什么突然掉量？”
→ performance-drop-diagnosis
→ causal-drop-diagnosis.md

“哪里还能增长？”
→ growth-opportunity-finder
→ opportunity-evaluation.md

“这个方向有可能，但不确定？”
→ experiment-planner
→ experiment-design.md

“上周调的 Bid 有效果吗？”
→ post-change-review
→ post-change-evaluation.md

“做每周广告复盘”
→ playbooks/weekly-review.md
→ 只按发现的问题调用必要 Skills
```

## Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级体检 |
| `campaign-health-monitor` | Campaign 健康监控 |
| `performance-drop-diagnosis` | 业绩突降因果诊断 |
| `growth-opportunity-finder` | 增长机会与 Headroom |
| `experiment-planner` | 受控实验设计 |
| `post-change-review` | Readback 与优化后效果复盘 |
| `search-term-analysis` | Search Term 赢家、收割、流量质量 |
| `keyword-optimization` | Keyword/Target 生命周期与结构 |
| `bid-optimization` | Bid/CPC 建议 |
| `budget-optimization` | Budget pacing、重分配与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative 与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、TACOS |
| `anomaly-detection` | 历史基线异常检测 |
| `amazon-ads-optimizer` | 总调度、记忆检查、去重与冲突消解 |

当前保持 **15 个 Skills**。如果一个新能力只是“把已有 Skills 按固定运营节奏组合起来”，优先增加 `playbooks/`，而不是继续拆成新的常驻 Skill。

## Weekly Review Playbook

`playbooks/weekly-review.md` 用于周期性账户复盘。

它不是固定阈值表，而是：

```text
Comparable windows
→ Business-first scorecard
→ Recent-action / memory checkpoint
→ Contribution triage
→ Campaign + ASIN review
→ Search term / target review
→ Budget / bid / placement review
→ Retail / event confounders
→ Protect / Recover / Optimize / Grow / Experiment / Hold
→ P0-P4 action packet
→ Next-review contract
```

核心原则：

- 不用固定 ACOS/CTR/CVR 阈值给 Campaign 强行红黄绿；
- 不因预算跑满就自动加预算；
- 不因 Search Term 暂时 0 单就自动否定；
- 不在上一动作尚未成熟时反向叠加新动作；
- Weekly Review 只识别和排序问题，复杂根因交给专业 Skill；
- 输出必须包含 `Hold` 列表，而不是每周强行改所有实体。

## Optimization Memory

`references/optimization-memory.md` 采用：

```text
Append-first event ledger
→ schemas/optimization-event.json
→ derived compact entity history
→ schemas/entity-history.json
→ read-before-recommend gate
```

明确区分：

```text
proposed ≠ applied
applied ≠ readback confirmed
readback confirmed ≠ worked
rollback proposed ≠ rolled back
```

历史是证据，不是当前事实。当前 Bid/Budget/State 等状态仍应从可信数据源 Readback。

## Experiment Planner

不确定但可验证的优化优先进入实验，而不是伪装成高置信动作。

实验应预声明：decision question、falsifiable hypothesis、treatment、control/holdout 设计、一个 primary metric、guardrails、attribution-mature window、contamination risk、stop/rollback rule。

固定点击数、订单数或预算倍数不作为通用实验标准；缺少统计输入时不伪造 power/MDE。

结构化合同：`schemas/experiment-plan.json`。

## Safety

| Mode | 行为 |
|---|---|
| `Read-only` | 读取和解释 |
| `Suggest` | 生成建议；默认 |
| `Shadow` | 模拟、回测、实验 |
| `Execute` | 仅显式授权并交给外部 Executor |

建议应尽量携带：evidence、confidence、data quality、sample sufficiency、guardrails、validation window、rollback condition。

## Benchmark Policy

外部 benchmark 不作为自动执行阈值。优先顺序：

1. 同账户、同目标、同归因口径历史；
2. 同账户实验 / Holdout；
3. 同实体可比历史；
4. 方法透明的外部 cohort；
5. 泛行业 benchmark，仅作方向参考。

详见 `references/benchmark-policy.md`。

## Multi-Agent Compatibility

| Runtime | 入口 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

三套 Runtime 共用同一个 canonical `skills/` 树，不复制 Amazon Ads 业务逻辑。

## Structure

```text
amazon-ads-skills/
├── skills/
│   ├── amazon-ads-optimizer/
│   ├── performance-drop-diagnosis/
│   ├── growth-opportunity-finder/
│   ├── experiment-planner/
│   ├── post-change-review/
│   └── ...
├── playbooks/
│   └── weekly-review.md
├── references/
│   ├── optimization-memory.md
│   ├── benchmark-policy.md
│   └── ...
├── schemas/
│   ├── optimization-action.json
│   ├── optimization-event.json
│   ├── entity-history.json
│   └── experiment-plan.json
├── docs/SOURCES.md
├── AGENTS.md
├── CLAUDE.md
├── .codex-plugin/
├── .claude-plugin/
└── .workbuddy-plugin/
```

## Development Rules

- 一个 Skill 解决一个清晰决策问题；
- 组合型运营节奏优先使用 playbook；
- `SKILL.md` 保持薄，详细知识按需加载；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 不编造缺失数据或历史；
- 不把固定经验阈值伪装成官方规则；
- 对同实体新动作先检查未完成验证的旧动作；
- 事件尽量 append-first，实体摘要可重建；
- stale memory 不等于当前状态；
- 不确定但可验证的结论优先进入实验；
- 默认 Suggest/Shadow，不直接写真实账户。

## Sources & Licenses

项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目。采用流程：

```text
discover → license check → extract generic idea
→ independently rewrite → Amazon Ads adaptation
→ safety gate → progressive loading
```

不会把第三方受版权保护的大段文本、固定阈值或私有接口实现直接搬入仓库。已审阅来源见 `docs/SOURCES.md`。

## Roadmap

- [x] Codex / Claude Code / WorkBuddy 共用 Skill 根目录
- [x] 基础 Audit / Monitor / Search Term / Bid / Budget / Placement / Negative / Profitability
- [x] Performance Drop Diagnosis + Mixed-ASIN safety
- [x] Growth Opportunity Finder
- [x] Experiment Planner
- [x] Post-change Review
- [x] Optimization Memory + Entity History
- [x] Contextual Benchmark Policy
- [x] Weekly Review Playbook
- [ ] Historical replay / eval fixtures
- [ ] 继续拆薄旧版较厚 Skills
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
