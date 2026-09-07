# Amazon Ads Agent Skills 设计

## 目标

将本仓库建设为 Amazon Ads AI Agent 技能库。所有业务技能只维护一份 `SKILL.md`，通过轻量兼容层同时服务 Codex、Claude Code 和 WorkBuddy。

## 核心原则

- 一套核心 Skill，多 Agent 兼容。
- 分析与真实广告账户执行解耦。
- 默认只读或建议模式，执行需要显式授权与边界检查。
- 详细规则、指标和数据结构按需从 references/schemas 加载。
- 数据入口可来自 Amazon Ads API、MCP、领星 MCP、CSV 或数据仓库。

## 目录

```text
amazon-ads-skills/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── .workbuddy-plugin/plugin.json
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
└── examples/README.md
```

## Skills

1. `amazon-ads-audit`：账户级广告体检。
2. `campaign-health-monitor`：广告活动健康监控与异常识别。
3. `search-term-analysis`：搜索词效率、扩词和否词候选分析。
4. `keyword-optimization`：关键词与匹配类型优化。
5. `bid-optimization`：基于目标和样本量生成竞价建议。
6. `budget-optimization`：预算受限和预算分配分析。
7. `placement-optimization`：广告版位效率分析。
8. `negative-targeting`：否定关键词/商品投放候选。
9. `profitability-analysis`：结合利润和盈亏平衡指标分析广告。
10. `anomaly-detection`：相对历史基线检测异常。
11. `amazon-ads-optimizer`：总调度、合并和冲突消解。

## Agent 兼容

### Codex
根目录 `AGENTS.md` 声明 Skills 位置、加载方式和安全规则。核心技能仍使用标准 `SKILL.md`。

### Claude Code
根目录 `CLAUDE.md` 负责仓库规则和技能发现，不复制 Skill 业务内容。

### WorkBuddy
通过 `.workbuddy-plugin/plugin.json` 暴露 `skills/`，核心 Skill 保持单一来源。

## 数据流

```text
数据源
  ↓
统一数据模型
  ↓
amazon-ads-optimizer
  ↓
一个或多个子 Skill
  ↓
分析/诊断
  ↓
标准化 Action Proposal
  ↓
边界检查
  ↓
Read-only / Suggest / Shadow / Execute
  ↓
外部 Connector 或执行器
```

## 权限模型

- `Read-only`：只读取和解释数据。
- `Suggest`：生成建议，不修改广告账户；默认模式。
- `Shadow`：生成模拟动作供回测和人工审阅。
- `Execute`：显式授权后输出可执行动作；实际写入由外部执行器负责。

## 错误与安全处理

当数据缺失、样本不足、归因窗口不一致、Marketplace/货币/时区不明确、数据延迟明显，或处于 Prime Day、Best Deal、Coupon 等特殊活动但缺少上下文时，Skill 不得强行给出高置信度执行建议。

## 测试

第一阶段检查：

- SKILL frontmatter 有效。
- Skill 和目录命名唯一。
- references/schemas 相对引用有效。
- JSON Schema 语法有效。
- 示例输入输出契约有效。
- 默认不会生成未经授权的真实账户修改动作。
- Codex、Claude Code、WorkBuddy 能发现同一核心 Skill。

## README 范围

README 需要包含项目定位、Skills 列表、目录、Codex/Claude/WorkBuddy 安装使用、数据接入、权限模型、新增 Skill 规范、安全说明与 Roadmap。

## 第一阶段非目标

本仓库暂不承载 OAuth 服务、长期数据库、调度器、广告 API 写入 SDK、Web 控制台或多租户系统；这些属于未来 Agent Runtime/Data/Connector 层。

## 验收标准

- 11 个核心 Skills 职责清晰。
- 三类 Agent 共用同一份 Skill 内容。
- README 提供完整使用说明。
- 分析与执行解耦。
- 默认安全，不在未授权状态修改真实广告账户。
