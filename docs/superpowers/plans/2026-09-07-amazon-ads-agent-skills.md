# Amazon Ads Agent Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `amazon-ads-skills` 初始化为一套同时兼容 Codex、Claude Code 和 WorkBuddy 的 Amazon Ads AI Agent Skills 仓库。

**Architecture:** 核心业务能力只维护在 `skills/<skill-name>/SKILL.md` 中，根目录兼容文件负责发现和使用规则，WorkBuddy 通过插件元数据暴露同一套 Skills。共享指标、决策边界、数据模型和 JSON Schema 独立存放，所有真实账户写入与分析层解耦。

**Tech Stack:** Markdown、YAML frontmatter、JSON/JSON Schema、Agent Skills 目录约定、GitHub。

**Spec:** `docs/superpowers/specs/2026-09-07-amazon-ads-agent-skills-design.md`

## Global Constraints

- 一套核心 Skill，多 Agent 兼容。
- 默认模式为 Suggest，不得未经显式授权修改真实 Amazon Ads 账户。
- 支持 Amazon Ads API、MCP、领星 MCP、CSV 和数据仓库作为数据入口。
- 分析与执行分离；实际写入由外部 Connector/Executor 负责。
- 所有实现直接落到仓库默认 `main`，不创建额外分支。

---

### Task 1: Agent 兼容层与项目入口

**Files:**
- Create: `AGENTS.md`
- Create: `CLAUDE.md`
- Create: `.workbuddy-plugin/plugin.json`

**Interfaces:**
- Consumes: `skills/*/SKILL.md`
- Produces: Codex、Claude Code、WorkBuddy 的统一发现入口和安全规则。

- [ ] **Step 1:** 创建 `AGENTS.md`，声明 Skill 根目录、加载原则、权限模型和禁止未经授权执行真实写入。
- [ ] **Step 2:** 创建 `CLAUDE.md`，引用同一 Skill 根目录，不复制业务规则。
- [ ] **Step 3:** 创建 `.workbuddy-plugin/plugin.json`，将 `skills/` 暴露为 WorkBuddy 插件能力。
- [ ] **Step 4:** 检查三个入口的 Skill 路径和安全边界是否一致。
- [ ] **Step 5:** 提交 `feat: add multi-agent compatibility layer`。

### Task 2: 共享 Amazon Ads 参考资料和数据契约

**Files:**
- Create: `references/amazon-ads-metrics.md`
- Create: `references/optimization-framework.md`
- Create: `references/decision-boundaries.md`
- Create: `references/data-schema.md`
- Create: `schemas/campaign.json`
- Create: `schemas/keyword.json`
- Create: `schemas/search-term.json`
- Create: `schemas/optimization-action.json`

**Interfaces:**
- Consumes: Amazon Ads 常见广告指标和优化场景。
- Produces: 所有 Skills 共用的指标定义、决策规则和标准化输入输出结构。

- [ ] **Step 1:** 定义 impressions、clicks、CTR、CPC、spend、sales、orders、CVR、ACOS、ROAS、TACOS、NTB、placement 等指标及计算方式。
- [ ] **Step 2:** 定义优化框架：目标、样本门槛、基线、诊断、建议、置信度、验证窗口。
- [ ] **Step 3:** 定义 Read-only / Suggest / Shadow / Execute 四级权限以及硬边界。
- [ ] **Step 4:** 定义统一 campaign、keyword、search-term、optimization-action JSON Schema。
- [ ] **Step 5:** 校验所有 JSON 为合法 JSON，字段命名一致。
- [ ] **Step 6:** 提交 `feat: add shared ads references and schemas`。

### Task 3: 核心分析 Skills

**Files:**
- Create: `skills/amazon-ads-audit/SKILL.md`
- Create: `skills/campaign-health-monitor/SKILL.md`
- Create: `skills/search-term-analysis/SKILL.md`
- Create: `skills/profitability-analysis/SKILL.md`
- Create: `skills/anomaly-detection/SKILL.md`

**Interfaces:**
- Consumes: 标准化广告数据、共享 references/schemas。
- Produces: 诊断结果、证据、置信度、风险和建议动作候选。

- [ ] **Step 1:** 实现账户审计 Skill，覆盖数据质量、结构、效率、预算、浪费和机会。
- [ ] **Step 2:** 实现 Campaign 健康监控 Skill，定义正常/警告/严重状态。
- [ ] **Step 3:** 实现 Search Term 分析 Skill，输出扩词和否词候选但不直接执行。
- [ ] **Step 4:** 实现利润分析 Skill，支持盈亏平衡 ACOS 和贡献利润视角。
- [ ] **Step 5:** 实现异常检测 Skill，要求使用历史基线且避免将促销波动误报为异常。
- [ ] **Step 6:** 检查每个 `SKILL.md` frontmatter 包含唯一 `name` 和明确 `description`。
- [ ] **Step 7:** 提交 `feat: add core Amazon Ads analysis skills`。

### Task 4: 优化动作 Skills

**Files:**
- Create: `skills/keyword-optimization/SKILL.md`
- Create: `skills/bid-optimization/SKILL.md`
- Create: `skills/budget-optimization/SKILL.md`
- Create: `skills/placement-optimization/SKILL.md`
- Create: `skills/negative-targeting/SKILL.md`

**Interfaces:**
- Consumes: 诊断结果、目标 KPI、样本量和共享决策边界。
- Produces: 标准 `optimization-action` 候选，不直接写入 Amazon Ads。

- [ ] **Step 1:** 实现关键词优化 Skill，覆盖匹配类型、状态、效率和收割策略。
- [ ] **Step 2:** 实现 bid 优化 Skill，要求样本量、上下限和单次变更幅度约束。
- [ ] **Step 3:** 实现 budget 优化 Skill，区分预算受限与效率低下。
- [ ] **Step 4:** 实现 placement 优化 Skill，对 Top of Search / Product Pages / Rest of Search 分析。
- [ ] **Step 5:** 实现 negative targeting Skill，增加误杀保护与品牌词/高价值词保护。
- [ ] **Step 6:** 检查所有优化输出都要求 `mode`、`evidence`、`confidence` 和 `rollback`/验证条件。
- [ ] **Step 7:** 提交 `feat: add Amazon Ads optimization skills`。

### Task 5: 总调度 Skill

**Files:**
- Create: `skills/amazon-ads-optimizer/SKILL.md`

**Interfaces:**
- Consumes: 其余 10 个 Skills 的分析或动作候选。
- Produces: 去重、冲突消解、优先级排序后的优化计划。

- [ ] **Step 1:** 定义意图路由：审计、监控、搜索词、关键词、竞价、预算、版位、否词、利润、异常。
- [ ] **Step 2:** 定义冲突消解，例如同一目标不可同时建议升 bid 和降 bid。
- [ ] **Step 3:** 定义动作排序：保护性动作 > 浪费控制 > 预算释放 > 增长动作。
- [ ] **Step 4:** 强制继承权限模型，默认 Suggest。
- [ ] **Step 5:** 提交 `feat: add Amazon Ads optimizer orchestrator skill`。

### Task 6: 示例和中文 README

**Files:**
- Create: `examples/README.md`
- Create: `README.md`

**Interfaces:**
- Consumes: 已实现的目录和 Skills。
- Produces: 用户可以直接理解、安装和扩展仓库的中文文档。

- [ ] **Step 1:** 创建示例，展示自然语言触发、标准数据输入和建议输出。
- [ ] **Step 2:** README 写明项目定位、能力矩阵、目录和 11 个 Skills。
- [ ] **Step 3:** README 增加 Codex、Claude Code、WorkBuddy 使用方式。
- [ ] **Step 4:** README 增加 Amazon Ads API / MCP / 领星 MCP / CSV / Warehouse 数据接入说明。
- [ ] **Step 5:** README 增加四级权限、安全边界、如何新增 Skill、Roadmap。
- [ ] **Step 6:** 提交 `docs: add usage guide and examples`。

### Task 7: 仓库级验证

**Files:**
- Verify: all created files

**Interfaces:**
- Consumes: Tasks 1-6 输出。
- Produces: 可发布的 v0.1 仓库状态。

- [ ] **Step 1:** 列出仓库树，确认 11 个 `SKILL.md` 均存在且无重复名称。
- [ ] **Step 2:** 抽查所有 JSON 文件可解析，路径引用一致。
- [ ] **Step 3:** 搜索 `TODO`、`TBD`、占位符和未定义路径并清理。
- [ ] **Step 4:** 确认 README 与实际文件结构一致。
- [ ] **Step 5:** 确认默认模式始终为 Suggest，真实执行需显式授权并交给外部 Executor。
- [ ] **Step 6:** 提交必要修正并记录最终提交 SHA。
