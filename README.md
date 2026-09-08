# amazon-ads-skills

亚马逊广告 AI Agent 技能库，用于广告监控、数据分析、因果诊断、增长机会发现、变更后复盘、安全优化与智能决策。

> 当前版本：`v0.4.0`  
> 默认模式：`Suggest`  
> 真实 Amazon Ads 写入由外部 Connector / Executor 负责，本仓库不直接执行账户修改。

## 核心设计

本仓库不是一组“ACOS 高就降 Bid”的静态规则，而是一套可被 Codex、Claude Code、WorkBuddy 等 Agent 调用的 Amazon Ads 决策知识层。

```text
数据
  ↓
完整性 / 归因 / 时间窗口校验
  ↓
诊断问题 / 发现机会
  ↓
动作候选
  ↓
样本、利润、库存、Mixed-ASIN、促销、增量性等风险检查
  ↓
Suggest / Shadow
  ↓
外部 Executor（可选）
  ↓
Readback → Observe → Evaluate → Keep / Rollback Candidate
  ↓
Optimization Event / History
```

## Progressive Loading：节省 Token

优先采用：

```text
薄 SKILL.md
   ↓
命中具体问题时
   ↓
skill-local references
   ↓
必要时再读取 shared references / schemas
```

例如“这个 ASIN 为什么突然掉量”：

```text
amazon-ads-optimizer
  → performance-drop-diagnosis/SKILL.md
  → references/causal-drop-diagnosis.md
```

“哪里还能继续扩量”：

```text
amazon-ads-optimizer
  → growth-opportunity-finder/SKILL.md
  → references/opportunity-evaluation.md
```

“昨天调了 Bid，现在到底有没有效果”：

```text
amazon-ads-optimizer
  → post-change-review/SKILL.md
  → references/post-change-evaluation.md
  → schemas/optimization-event.json（结构化历史需要时）
```

## Agent 兼容

| Agent / Runtime | 支持方式 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

所有运行时共用同一份核心 Skills，不维护重复业务逻辑。

## Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级体检、结构、浪费与增长机会 |
| `campaign-health-monitor` | Campaign 日常健康监控与告警 |
| `performance-drop-diagnosis` | 业绩突降因果诊断：断点、贡献、Retail、控制变更、Mixed-ASIN 安全 |
| `growth-opportunity-finder` | 增长机会：验证赢家、Headroom、Incrementality、Retail Readiness 与受控扩量 |
| `post-change-review` | 变更后 Readback、效果评估、混杂因素检查、Keep/Monitor/Rollback Candidate |
| `search-term-analysis` | Search Term 赢家、Exact 收割、流量质量与否词候选 |
| `keyword-optimization` | Keyword/Target 生命周期、Match Type 与结构优化 |
| `bid-optimization` | 基于目标、样本和 Guardrail 的 Bid 建议 |
| `budget-optimization` | Budget pacing、预算受限、重分配与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative Exact/Phrase/商品否定与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、广告后利润、TACOS |
| `anomaly-detection` | 历史基线异常检测及促销/库存误报过滤 |
| `amazon-ads-optimizer` | 总调度、意图路由、去重、冲突消解、优先级排序 |

## Post-change 闭环

`post-change-review` 把“提出建议”升级成“知道建议是否真的生效”。

```text
Original Proposal
  ↓
Readback：实际是否应用？
  ↓
Confirmed / Partial / Not Applied / Drifted / Unknown
  ↓
Expected mechanism
  ↓
Comparable baseline + attribution-mature post window
  ↓
Concurrent changes / Promotion / Price / Stock / Buy Box confounders
  ↓
Worked / Likely Worked / Monitoring / Inconclusive /
Likely Failed / Failed / Application Failure / Drifted
  ↓
Keep / Keep Monitoring / Rollback Candidate /
Follow-up Experiment / Fix Application / Manual Review
```

重点原则：

- 未确认 Readback，不评价“优化是否成功”；
- 不把归因未成熟的短期无订单直接判成失败；
- 不只看 ACOS/ROAS，而是检查动作原本应该影响的机制；
- 多个控制项同时改变时，降低单动作因果置信度；
- `Rollback Candidate` 只是建议，不代表仓库直接执行回滚。

结构化事件使用 `schemas/optimization-event.json`，为后续 Action History / Optimization Memory 提供稳定数据合同。

## Benchmark 使用规则

外部 Benchmark 不作为自动执行阈值。优先级：

1. 同账户、同目标、同归因口径的历史；
2. 同账户实验 / Holdout；
3. 同实体可比历史；
4. 方法透明的外部可比 Cohort；
5. 泛行业 Benchmark，仅作方向参考。

详见 `references/benchmark-policy.md`。

## 安全模式

| Mode | 行为 |
|---|---|
| `Read-only` | 读取与解释 |
| `Suggest` | 输出建议，不修改账户；默认 |
| `Shadow` | 模拟动作、回测、评估 |
| `Execute` | 只有显式授权并经外部 Connector / Executor 才可执行 |

任何动作建议都应尽量携带：entity/scope、reason、evidence、confidence、data quality、sample sufficiency、guardrails、validation window、rollback condition。

## 数据接入

Skills 不绑定接口，可接 Amazon Ads API、MCP、领星 MCP、CSV/Excel、Data Warehouse 或内部 BI/ETL。

```text
Data Sources
   ↓
Normalizer
   ↓
schemas/*.json
   ↓
Amazon Ads Skills
   ↓
Action Proposal
   ↓
Policy / Approval
   ↓
External Executor
   ↓
Optimization Event
```

## 仓库结构

```text
amazon-ads-skills/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── .codex-plugin/
├── .claude-plugin/
├── .workbuddy-plugin/
├── skills/
│   ├── amazon-ads-audit/
│   ├── campaign-health-monitor/
│   ├── performance-drop-diagnosis/
│   │   ├── SKILL.md
│   │   └── references/causal-drop-diagnosis.md
│   ├── growth-opportunity-finder/
│   │   ├── SKILL.md
│   │   └── references/opportunity-evaluation.md
│   ├── post-change-review/
│   │   ├── SKILL.md
│   │   └── references/post-change-evaluation.md
│   ├── search-term-analysis/
│   ├── keyword-optimization/
│   ├── bid-optimization/
│   ├── budget-optimization/
│   ├── placement-optimization/
│   ├── negative-targeting/
│   ├── profitability-analysis/
│   ├── anomaly-detection/
│   └── amazon-ads-optimizer/
├── references/
│   ├── amazon-ads-metrics.md
│   ├── optimization-framework.md
│   ├── decision-boundaries.md
│   ├── benchmark-policy.md
│   └── data-schema.md
├── schemas/
│   ├── optimization-action.json
│   └── optimization-event.json
├── examples/
└── docs/SOURCES.md
```

## Skill 开发规范

- 一个 Skill 解决一个清晰运营问题；
- `SKILL.md` 尽量精简，复杂判断放 `references/`；
- 只在命中场景时加载对应 reference；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 不编造缺失数据；
- 不把固定经验阈值伪装成 Amazon 官方规则；
- 不直接执行真实账户写入；
- 对同实体的新动作，优先检查最近尚未完成验证的旧动作；
- 需要真实写入时必须经过边界检查和外部 Executor。

## 外部项目借鉴与许可证

本项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目，但不直接大段复制第三方文本。采用流程：发现优秀方法 → 提炼通用思想 → 检查许可证 → Amazon Ads 化 → 独立重写 → 加安全边界 → 拆成按需加载 references/playbooks。

已审阅来源及采用原则见 `docs/SOURCES.md`。

## Roadmap

- [x] Codex / Claude Code / WorkBuddy 统一 Skill 根目录
- [x] 基础 Audit / Monitor / Search Term / Bid / Budget / Placement / Negative / Profitability
- [x] 业绩突降因果诊断 + Mixed-ASIN safety
- [x] Contextual benchmark policy
- [x] Growth Opportunity Finder
- [x] Post-change Review
- [x] Optimization Event schema
- [ ] 将其余较厚 `SKILL.md` 继续拆成薄入口 + references
- [ ] Weekly Review playbook
- [ ] Experiment Planner
- [ ] Optimization Memory / entity history reference
- [ ] Historical replay / eval fixtures
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。Amazon、Amazon Ads、Sponsored Products、Sponsored Brands、Sponsored Display 等名称归其各自权利人所有。
