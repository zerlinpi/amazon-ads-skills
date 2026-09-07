# amazon-ads-skills

亚马逊广告 AI Agent 技能库，用于广告监控、数据分析、自动优化与智能决策。

本仓库将 Amazon Ads 运营经验封装为可复用的 **Agent Skills**，核心业务逻辑只维护一份 `SKILL.md`，同时面向 **OpenAI Codex、Claude Code、WorkBuddy** 等支持 Agent Skills 的 Agent 环境。

> 当前版本：`v0.1.0`  
> 默认运行模式：`Suggest`  
> 当前仓库不会直接修改真实 Amazon Ads 账户；真实写入由未来的 Connector / Executor 层负责。

## 为什么做这个仓库

普通广告自动化经常把优化简化成：

```text
ACOS 高 -> 降 bid
ACOS 低 -> 加 bid
0 订单 -> 否词
预算跑完 -> 加预算
```

真实 Amazon Ads 优化远比这复杂。一个结果指标可能同时受到 Search Term、CPC、CVR、Placement、Budget、价格、库存、Buy Box、Listing、大促、归因延迟和业务目标影响。

这个仓库的目标是把广告运营方法拆成可组合 Skills，让 Agent 遵循：

```text
数据 -> 校验 -> 诊断 -> 根因 -> 动作候选 -> 风险边界 -> 验证 -> 执行层
```

而不是直接做机械调价。

---

## Agent 兼容

| Agent / 平台 | 支持方式 | 入口 |
|---|---|---|
| OpenAI Codex | Skill-only Codex Plugin + Agent Skills | `.codex-plugin/plugin.json`、`skills/`、`AGENTS.md` |
| Claude Code | Claude Code Plugin + Agent Skills | `.claude-plugin/plugin.json`、`skills/`、`CLAUDE.md` |
| WorkBuddy | WorkBuddy Skill / Plugin 结构 | `.workbuddy-plugin/plugin.json`、`skills/` |
| 其他 Agent Skills Runtime | 标准 `SKILL.md` | `skills/<name>/SKILL.md` |

三套兼容层都指向同一个 `skills/` 目录，**不维护三份重复广告逻辑**。

---

## 已封装 Skills

| Skill | 用途 |
|---|---|
| `amazon-ads-audit` | 账户级广告体检、结构审计、浪费与增长机会 |
| `campaign-health-monitor` | Campaign 健康监控、异常与根因方向 |
| `search-term-analysis` | Search Term 分析、赢家识别、Exact 收割、否词候选 |
| `keyword-optimization` | Keyword/Target 生命周期、匹配类型和结构优化 |
| `bid-optimization` | 基于目标、样本和风险边界生成 bid 建议 |
| `budget-optimization` | 预算受限、pacing、预算重分配和扩量判断 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search 优化 |
| `negative-targeting` | Negative Exact/Phrase/商品否定候选与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、广告后利润与 TACOS |
| `anomaly-detection` | 历史基线异常检测与大促/库存/价格误报过滤 |
| `amazon-ads-optimizer` | 总调度、意图路由、去重、冲突消解、优先级排序 |

如果用户没有明确指定某个问题域，而是说“帮我整体优化广告”，优先使用 `amazon-ads-optimizer`。

---

## 架构

```text
Amazon Ads API / MCP / 领星 MCP / CSV / Data Warehouse
                         |
                         v
                 Normalization Layer
                         |
                         v
                 schemas/*.json
                         |
                         v
              amazon-ads-optimizer
                         |
       +-----------------+-----------------+
       |                 |                 |
       v                 v                 v
    Audit            Monitoring         Analysis
       |                 |                 |
       +--------+--------+--------+--------+
                |                 |
                v                 v
          Optimization Skills   Profit/Risk
                |                 |
                +--------+--------+
                         |
                         v
             Optimization Action Proposal
                         |
                         v
              Guardrails / Approval
                         |
           +-------------+-------------+
           |                           |
           v                           v
      Suggest/Shadow            External Executor
                                   (optional)
```

---

## 仓库结构

```text
amazon-ads-skills/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
├── .codex-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── plugin.json
├── .workbuddy-plugin/
│   └── plugin.json
├── skills/
│   ├── amazon-ads-audit/SKILL.md
│   ├── campaign-health-monitor/SKILL.md
│   ├── search-term-analysis/SKILL.md
│   ├── keyword-optimization/SKILL.md
│   ├── bid-optimization/SKILL.md
│   ├── budget-optimization/SKILL.md
│   ├── placement-optimization/SKILL.md
│   ├── negative-targeting/SKILL.md
│   ├── profitability-analysis/SKILL.md
│   ├── anomaly-detection/SKILL.md
│   └── amazon-ads-optimizer/SKILL.md
├── references/
│   ├── amazon-ads-metrics.md
│   ├── optimization-framework.md
│   ├── decision-boundaries.md
│   └── data-schema.md
├── schemas/
│   ├── campaign.json
│   ├── keyword.json
│   ├── search-term.json
│   └── optimization-action.json
├── examples/
│   └── README.md
└── docs/superpowers/
    ├── specs/
    └── plans/
```

---

## Codex 使用

Codex 当前支持以 Agent Skills / skill-only plugin 的方式加载 `SKILL.md`。

本仓库已经提供：

```text
.codex-plugin/plugin.json
skills/<skill-name>/SKILL.md
AGENTS.md
```

`.codex-plugin/plugin.json` 的 `skills` 指向 `./skills/`。

如果只需要安装一个 Skill，也可以在 Codex 中使用 `$skill-installer`，让它从本仓库具体 Skill 的 GitHub 目录安装，例如 `skills/amazon-ads-optimizer`。

在仓库内直接让 Codex 工作时，`AGENTS.md` 还会提供默认 Suggest、安全边界和共享 references 规则。

示例请求：

```text
使用 amazon-ads-optimizer 分析这份过去 30 天广告数据，目标 ACOS 30%，给出优先级最高的优化动作，不要真实执行。
```

---

## Claude Code 使用

Claude Code 的 Skill-focused Plugin 采用：

```text
.claude-plugin/plugin.json
skills/<skill-name>/SKILL.md
```

本仓库已经按该结构提供 manifest，并显式声明 `skills: ./skills/`。

安装/启用该插件后，Claude Code 可根据 `SKILL.md` 的 `name` 与 `description` 自动发现匹配 Skill。`CLAUDE.md` 只保存仓库级规则，业务逻辑仍然来自 `skills/`。

示例：

```text
检查这些 campaign 为什么本周 ROAS 突然下降，并区分流量、CPC、CVR 和促销因素。
```

典型路由：

```text
anomaly-detection -> campaign-health-monitor -> 对应优化 Skill
```

---

## WorkBuddy 使用

WorkBuddy 原生 Skill 基础结构为：

```text
skills/
└── <skill-name>/
    ├── SKILL.md
    ├── references/   # optional
    ├── scripts/      # optional
    └── templates/    # optional
```

本仓库所有 Skills 都使用 YAML frontmatter + Markdown，并补充 WorkBuddy 常用的：
- `description_zh`
- `description_en`
- `version`
- `author`

同时提供 `.workbuddy-plugin/plugin.json`，将 11 个 Skills 作为统一插件能力暴露。

可以直接按 WorkBuddy Skill/Plugin 的导入方式使用本仓库，或者只打包所需 `skills/<name>`。

---

## 数据源

Skills 不绑定某一种数据获取技术。

支持的设计入口包括：

### Amazon Ads API

最适合未来自研正式 Connector：

```text
Amazon Ads API
   -> OAuth / Profiles
   -> Reporting / Campaign Management
   -> Normalizer
   -> Skills
```

### MCP

可以让 Agent 通过 MCP 获取 campaign、keyword、search term、placement、budget 等数据，再统一映射给 Skills。

### 领星 MCP

如果你已经有领星 MCP，可将它作为第一阶段数据 Connector：

```text
领星 MCP -> 广告数据 -> Normalizer -> amazon-ads-skills
```

这样未来替换成自研 Amazon Ads API Connector 时，不需要重写广告决策 Skills。

### CSV / Excel / Data Warehouse

离线报表、BI 或数据仓库也可以，只要先标准化成 `schemas/` 对应的数据模型。

---

## 标准数据模型

共享定义位于：

- `references/data-schema.md`
- `schemas/campaign.json`
- `schemas/keyword.json`
- `schemas/search-term.json`
- `schemas/optimization-action.json`

机器字段中百分比统一优先使用 0-1 小数，例如：

```text
30% ACOS -> 0.30
10% CVR  -> 0.10
```

未知值使用 `null`/缺失字段，不允许用 0 冒充未知值。

---

## 核心广告指标

完整定义见 `references/amazon-ads-metrics.md`。

常用公式：

```text
CTR   = Clicks / Impressions
CPC   = Spend / Clicks
CVR   = Orders / Clicks
ACOS  = Spend / Ad Sales
ROAS  = Ad Sales / Spend
TACOS = Ad Spend / Total Sales
```

利润相关：

```text
Break-even ACOS = Contribution Before Ads / Revenue
Profit After Ads = Contribution Before Ads - Ad Spend
```

如果没有成本数据，Agent 必须明确它只能做广告效率分析，而不是利润分析。

---

## 四级权限模型

### 1. Read-only

只读取、计算、解释、诊断。

### 2. Suggest — 默认

输出明确优化建议，但不修改真实账户。

### 3. Shadow

模拟“如果执行会怎样”，可用于回测和内部自动化验证。

### 4. Execute

只有满足以下条件才能进入：
- 用户明确授权；
- 外部 Connector / Executor 可用；
- 数据质量检查通过；
- guardrails 通过；
- before/after 可审计；
- 有 validation window；
- 有 rollback condition。

**即使在 Execute 模式，Skill 负责生成动作，真正 API 写入仍由执行层负责。**

完整规则见 `references/decision-boundaries.md`。

---

## 为什么分析和执行要分开

后续你可以把系统拆成：

```text
Data Plane
  Amazon Ads API / MCP / Warehouse

Decision Plane
  amazon-ads-skills

Execution Plane
  Policy Engine
  Approval
  Amazon Ads Executor
  Audit Log

Control Plane
  Scheduler
  Monitoring
  Web Console
  Multi-tenant / RBAC
```

这样更适合从“公司内部 AI 广告助手”逐步升级为商业 SaaS。

---

## 特殊活动保护

以下场景必须作为上下文进入分析：
- Prime Day
- Best Deal (BD)
- Lightning Deal (LD)
- Coupon
- Prime Exclusive Discount
- 大幅价格变化
- 断货 / 补货
- Buy Box 丢失
- Listing suppression

例如 Best Deal 期间 ACOS 突然升高，不能直接按普通周基线判断并立刻砍 bid；需要先拆 CPC、CVR、流量结构和促销影响。

---

## Optimization Action

所有优化 Skill 尽量归一输出：

```json
{
  "action_type": "adjust_bid",
  "entity_type": "keyword",
  "entity_id": "kw-123",
  "current_value": 1.20,
  "proposed_value": 1.05,
  "reason": "样本充分且 ACOS 持续高于目标",
  "evidence": ["ACOS=42%", "target=30%", "orders=8"],
  "confidence": 0.82,
  "mode": "Suggest",
  "guardrails": ["single bid change <= 20%"],
  "validation_window": "7d",
  "rollback_condition": "conversion volume falls materially"
}
```

这让未来 Policy Engine / Executor 可以消费同一动作协议。

---

## 新增 Skill 规范

目录：

```text
skills/<kebab-case-name>/SKILL.md
```

推荐 frontmatter：

```yaml
---
name: your-skill-name
display_name: 中文名
display_name_en: English Name
description: 写清楚能力、使用场景和触发意图
description_zh: 中文简述
description_en: English description
version: 0.1.0
author: zerlinpi
---
```

正文至少包含：
1. 什么时候使用；
2. 输入；
3. 数据校验；
4. 工作流；
5. 输出契约；
6. 风险边界；
7. 停止条件。

原则：**Progressive Disclosure**。不要把全部 Amazon Ads 知识塞进每个 Skill；通用内容放 `references/`，机器契约放 `schemas/`。

新增 Skill 后记得同步：
- `.workbuddy-plugin/plugin.json`；
- README Skills 表；
- 必要时 orchestrator 路由表。

Codex/Claude manifest 已指向整个 `./skills/`，新增目录通常无需逐项添加。

---

## 推荐开发路线

### v0.1 — Skills Foundation（当前）

- [x] 多 Agent 统一 Skill 架构
- [x] Codex Plugin manifest
- [x] Claude Code Plugin manifest
- [x] WorkBuddy plugin manifest
- [x] 广告指标与数据模型
- [x] 账户审计
- [x] Campaign 健康监控
- [x] Search Term 分析
- [x] Keyword 优化
- [x] Bid 优化
- [x] Budget 优化
- [x] Placement 优化
- [x] Negative Targeting
- [x] Profitability
- [x] Anomaly Detection
- [x] Optimizer Orchestrator

### v0.2 — Data Connector

- [ ] Amazon Ads API Connector
- [ ] Reporting ingestion
- [ ] Profile / Marketplace normalization
- [ ] 领星 MCP Adapter
- [ ] CSV importer

### v0.3 — Evaluation

- [ ] 历史广告数据回测
- [ ] Action precision / recall
- [ ] Guardrail evals
- [ ] Promotion-aware eval set
- [ ] Human approval feedback loop

### v0.4 — Shadow Automation

- [ ] Scheduler
- [ ] Daily monitor
- [ ] Action queue
- [ ] Shadow mode
- [ ] Audit log
- [ ] Slack/企业微信告警

### v1.0 — Controlled Execution

- [ ] Amazon Ads write executor
- [ ] Policy engine
- [ ] RBAC
- [ ] Approval workflow
- [ ] Rollback
- [ ] Multi-account / multi-tenant
- [ ] Web console

---

## 示例

查看 `examples/README.md`：
- 整体账户诊断
- Campaign 标准输入
- Bid Suggest action
- Search Term 收割 + 否词
- Best Deal / 大促异常处理

---

## 参考标准

本仓库的跨 Agent 结构参考：
- OpenAI Codex Plugin / Agent Skills：`SKILL.md` + `.codex-plugin/plugin.json` + `skills/`
- Anthropic Claude Code Plugin / Agent Skills：`.claude-plugin/plugin.json` + `skills/<name>/SKILL.md`
- WorkBuddy Skill：`skills/<name>/SKILL.md`，YAML frontmatter + Markdown，可带 references/scripts/templates

---

## License

MIT License，见 `LICENSE`。

## Disclaimer

本项目是独立的开源 Agent Skills 项目，与 Amazon、Amazon Ads、OpenAI、Anthropic 或 WorkBuddy 不存在官方隶属关系。广告建议应结合实际账户权限、Marketplace 规则、业务目标和最新平台能力进行验证。
