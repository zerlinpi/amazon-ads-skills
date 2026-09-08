# amazon-ads-skills

亚马逊广告 AI Agent 技能库，用于广告监控、数据分析、因果诊断、安全优化与智能决策。

> 当前版本：`v0.2.0`  
> 默认模式：`Suggest`  
> 真实 Amazon Ads 写入由外部 Connector / Executor 负责，本仓库不直接执行账户修改。

## 核心设计

本仓库不是一组“ACOS 高就降价”的静态规则，而是一套可被 Codex、Claude Code、WorkBuddy 等 Agent 调用的 Amazon Ads 决策知识层。

核心流程：

```text
数据
  ↓
完整性 / 归因 / 时间窗口校验
  ↓
诊断问题与根因
  ↓
动作候选
  ↓
样本、利润、库存、Mixed-ASIN、促销等风险检查
  ↓
Suggest / Shadow
  ↓
外部 Executor（可选）
  ↓
Observe / Evaluate / Rollback
```

## Progressive Loading：节省 Token

优先采用：

```text
薄 SKILL.md
   ↓
只有在命中具体问题时
   ↓
references / shared references
```

Agent 不应一次加载整个仓库。例如用户问“为什么这个 ASIN 这周突然掉量”：

```text
amazon-ads-optimizer
  ↓
performance-drop-diagnosis/SKILL.md
  ↓
performance-drop-diagnosis/references/causal-drop-diagnosis.md
```

只有涉及外部 benchmark 时，才额外读取 `references/benchmark-policy.md`。

## Agent 兼容

| Agent / Runtime | 支持方式 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

所有 Agent 共用同一份核心 Skills，不维护重复业务逻辑。

## Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级体检、结构、浪费与增长机会 |
| `campaign-health-monitor` | Campaign 日常健康监控与告警 |
| `performance-drop-diagnosis` | 业绩突降因果诊断：断点、贡献、Retail、控制变更、Mixed-ASIN 安全 |
| `search-term-analysis` | Search Term 赢家、Exact 收割、流量质量与否词候选 |
| `keyword-optimization` | Keyword/Target 生命周期、Match Type 与结构优化 |
| `bid-optimization` | 基于目标、样本和 Guardrail 的 Bid 建议 |
| `budget-optimization` | Budget pacing、预算受限、重分配与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative Exact/Phrase/商品否定与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、广告后利润、TACOS |
| `anomaly-detection` | 历史基线异常检测及促销/库存误报过滤 |
| `amazon-ads-optimizer` | 总调度、意图路由、去重、冲突消解、优先级排序 |

## 突降诊断框架

`performance-drop-diagnosis` 不从“哪个 ACOS 最差”开始，而是从业务损失开始：

```text
确认完整窗口
  ↓
定位 break point
  ↓
Account / ASIN 贡献排序
  ↓
Impressions → Clicks → CPC → CVR → Orders → Sales bridge
  ↓
Retail Readiness
  ↓
Bid / Budget / Placement / Negative / State 变更时间线
  ↓
Mixed-ASIN / Halo 风险
  ↓
Confirmed / Likely / Directional / Rejected / Missing Data
  ↓
Action-safe / Directional / Blocked
```

核心目的：避免为了降低 ACOS 误伤销售速度、自然排名、品牌防御或其他 ASIN 的有效流量。

## Benchmark 使用规则

本仓库不把通用 benchmark 当作自动执行阈值。

优先级：

1. 同账户、同目标、同归因口径的可比历史；
2. 同账户实验 / Holdout；
3. 同 ASIN / Campaign 可比历史；
4. 方法透明的外部可比 Cohort；
5. 泛行业 Benchmark，仅作方向参考。

详见：`references/benchmark-policy.md`。

固定的 CTR、CVR、ACOS、点击数、预算比例等规则只能作为显式标注的 heuristic，不能单独授权真实广告动作。

## 安全模式

| Mode | 行为 |
|---|---|
| `Read-only` | 读取与解释 |
| `Suggest` | 输出建议，不修改账户；默认 |
| `Shadow` | 模拟动作、回测、评估 |
| `Execute` | 只有显式授权并经外部 Connector / Executor 才可执行 |

任何动作建议都应尽量携带：

- entity / scope
- reason
- evidence
- confidence
- data quality / sample sufficiency
- guardrails
- validation window
- rollback condition

## 数据接入

Skills 不绑定数据接口，可接：

```text
Amazon Ads API
MCP
领星 MCP
CSV / Excel 导出
Data Warehouse
内部 BI / ETL
```

推荐架构：

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
Executor
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
│   │   └── references/
│   │       └── causal-drop-diagnosis.md
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
├── examples/
└── docs/
    ├── SOURCES.md
    └── superpowers/
```

## Skill 开发规范

新增或重构 Skill 时：

- 一个 Skill 解决一个清晰的运营问题；
- `SKILL.md` 尽量保持精简；
- 复杂算法、判断树、案例、长期知识放到 `references/`；
- 只在命中场景时加载对应 reference；
- 区分 Fact / Observation / Hypothesis / Cause / Action；
- 不编造缺失数据；
- 不把固定经验阈值伪装成 Amazon 官方规则；
- 不直接执行真实账户写入；
- 需要真实写入时，必须经过边界检查和外部 Executor。

## 外部项目借鉴与许可证

本项目会持续研究公开的 Amazon Ads / PPC / Agent Skills 项目，但不会直接大段复制第三方 Skill 文本。

采用流程：

```text
发现优秀方法
  ↓
提炼通用思想
  ↓
检查许可证和适用边界
  ↓
Amazon Ads 化
  ↓
独立重写
  ↓
加入安全边界
  ↓
拆为按需加载 references/playbooks
```

已审阅的重要来源及采用原则见 `docs/SOURCES.md`。

## 当前重点 Roadmap

- [x] Codex / Claude Code / WorkBuddy 统一 Skill 根目录
- [x] 账户审计 / 监控 / Bid / Budget / Placement / Search Term / Negative / Profitability
- [x] 统一安全边界与 action schema
- [x] 业绩突降因果诊断
- [x] Mixed-ASIN action safety
- [x] Contextual benchmark policy
- [ ] 将其余较厚 `SKILL.md` 逐步拆成薄入口 + references
- [ ] Weekly Review playbook
- [ ] Growth Opportunity Finder
- [ ] Experiment Planner
- [ ] Post-change Review
- [ ] Action history / optimization memory schema
- [ ] Historical replay / eval fixtures
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立的开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。Amazon、Amazon Ads、Sponsored Products、Sponsored Brands、Sponsored Display 等名称归其各自权利人所有。
