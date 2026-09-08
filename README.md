# amazon-ads-skills

亚马逊广告 AI Agent 技能库，用于广告监控、因果诊断、增长机会发现、受控实验、变更后复盘与安全优化。

> 当前版本：`v0.5.0`  
> 默认模式：`Suggest`  
> 真实 Amazon Ads 写入由外部 Connector / Executor 负责，本仓库不直接修改账户。

## 决策闭环

```text
Data
  ↓
Validate freshness / attribution / scope / economics
  ↓
Diagnose problem or find opportunity
  ↓
Evidence strong? ── yes ─→ Action proposal
  │
  no / uncertain
  ↓
Experiment Planner → Suggest / Shadow
  ↓
External Executor (optional, authorized)
  ↓
Readback → Observe → Post-change Review
  ↓
Keep / Monitor / Rollback Candidate / Repeat
  ↓
Optimization Event / History
```

这套结构避免把“ACOS 高就降 Bid”“预算跑满就加预算”当成自动规则。

## Progressive Loading：节省 Token

```text
薄 SKILL.md
   ↓
只在命中具体问题时
   ↓
skill-local references
   ↓
必要时 shared references / schemas
```

示例：

```text
“为什么突然掉量？”
→ performance-drop-diagnosis
→ references/causal-drop-diagnosis.md

“哪里还能增长？”
→ growth-opportunity-finder
→ references/opportunity-evaluation.md

“这个机会证据不够，怎么安全验证？”
→ experiment-planner
→ references/experiment-design.md
→ schemas/experiment-plan.json

“昨天改的 Bid 到底有没有效果？”
→ post-change-review
→ references/post-change-evaluation.md
→ schemas/optimization-event.json
```

## Agent 兼容

| Runtime | 入口 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

所有 Runtime 共用一份 canonical Skills，不复制业务逻辑。

## Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级体检 |
| `campaign-health-monitor` | Campaign 健康监控 |
| `performance-drop-diagnosis` | 业绩突降因果诊断 |
| `growth-opportunity-finder` | 增长机会与 Headroom |
| `experiment-planner` | 假设、Control/Holdout、Primary Metric、Guardrail、验证窗口 |
| `post-change-review` | Readback 与优化后效果复盘 |
| `search-term-analysis` | Search Term 赢家、收割与流量质量 |
| `keyword-optimization` | Keyword/Target 生命周期与结构 |
| `bid-optimization` | Bid/CPC 建议 |
| `budget-optimization` | Budget pacing、重分配与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative 与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、TACOS |
| `anomaly-detection` | 历史基线异常检测 |
| `amazon-ads-optimizer` | 总调度、去重、冲突消解与优先级 |

## Experiment Planner

`experiment-planner` 用于“有合理假设，但证据不足以直接修改”的场景。

它要求预先定义：

- decision question；
- falsifiable hypothesis；
- treatment scope；
- holdout / matched control / phased rollout / switchback / historical baseline；
- **一个** primary metric；
- diagnostic metrics；
- profitability / volume / inventory / Buy Box 等 guardrails；
- attribution-mature observation window；
- contamination / Mixed-ASIN / concurrent-change risk；
- stop / rollback rules。

固定点击数、订单数或百分比不会被当成 Amazon 通用实验标准。若缺少 variance、baseline rate、allocation 等统计输入，不会伪造 power/MDE 精度。

结构化实验计划使用 `schemas/experiment-plan.json`。

## 安全模式

| Mode | 行为 |
|---|---|
| `Read-only` | 读取与解释 |
| `Suggest` | 生成建议；默认 |
| `Shadow` | 模拟、回测、实验设计 |
| `Execute` | 仅显式授权并交给外部 Executor |

任何可操作建议都应尽量携带 evidence、confidence、data quality、sample sufficiency、guardrails、validation window 与 rollback condition。

## Benchmark 原则

外部 Benchmark 不作为自动执行阈值。优先使用：

1. 同账户、同目标、同归因口径历史；
2. 同账户实验 / Holdout；
3. 同实体可比历史；
4. 方法透明的外部 Cohort；
5. 泛行业 Benchmark，仅作方向参考。

详见 `references/benchmark-policy.md`。

## 结构

```text
amazon-ads-skills/
├── skills/
│   ├── performance-drop-diagnosis/
│   ├── growth-opportunity-finder/
│   ├── experiment-planner/
│   │   ├── SKILL.md
│   │   └── references/experiment-design.md
│   ├── post-change-review/
│   └── ...
├── references/
├── schemas/
│   ├── optimization-action.json
│   ├── optimization-event.json
│   └── experiment-plan.json
├── docs/SOURCES.md
├── AGENTS.md
├── CLAUDE.md
├── .codex-plugin/
├── .claude-plugin/
└── .workbuddy-plugin/
```

## 开发规范

- 一个 Skill 解决一个清晰运营问题；
- `SKILL.md` 尽量薄，复杂知识进入按需 references；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 不编造缺失数据；
- 不把固定经验阈值伪装成官方规则；
- 不直接执行真实账户写入；
- 对同实体的新动作，先检查尚未完成验证的旧动作；
- 不确定但可验证的结论优先变成受控实验，而不是高置信动作。

## 外部资料与许可证

项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目，但不直接大段复制第三方文本。流程：方法发现 → License 检查 → 通用思想提炼 → Amazon Ads 化 → 独立重写 → Safety Gate → Progressive Loading。

已审阅来源见 `docs/SOURCES.md`。

## Roadmap

- [x] Codex / Claude Code / WorkBuddy 共用 Skill 根目录
- [x] 基础 Audit / Monitor / Search Term / Bid / Budget / Placement / Negative / Profitability
- [x] Performance Drop Diagnosis + Mixed-ASIN safety
- [x] Growth Opportunity Finder
- [x] Experiment Planner + experiment schema
- [x] Post-change Review + optimization event schema
- [x] Contextual benchmark policy
- [ ] Weekly Review playbook
- [ ] Optimization Memory / entity history reference
- [ ] Historical replay / eval fixtures
- [ ] 继续拆薄旧版较厚 Skills
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
