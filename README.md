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
| `budget-optimization` | Budget pacing、重分配与扩量 |
| `placement-optimization` | Top of Search / Product Pages / Rest of Search |
| `negative-targeting` | Negative 与误杀保护 |
| `profitability-analysis` | Break-even ACOS、贡献利润、TACOS |
| `anomaly-detection` | 历史基线异常检测 |
| `amazon-ads-optimizer` | 总调度、记忆检查、去重与冲突消解 |

当前保持 **15 个 Skills**。组合型运营流程优先进入 `playbooks/`；可靠性验证优先进入 `evals/`，而不是继续拆新 Skill。

## Historical Replay / Evals

`evals/README.md` 定义 Contract checks + Capability replay。Capability Eval 使用 `met / not_met / insufficient_evidence`，比较决策行为而不是 exact wording。

当前 regression pack 已覆盖 **19 类关键安全风险**：Mixed-ASIN 误否词、Negative attachment 错层级、Previous Winner 短期 0 单、Pending Change 反复调参、Bid×Placement 联动、Featured Offer / Buy Box 冲击、Stockout 转化冲击、Promotion baseline 假异常、Attribution Lag 假失败、Unknown Application 错误归因、Partial Application、stale entity identity memory、blind retry、显式 idempotency safe retry、readback 与 intended state 不一致、Experiment contamination、Proven Winner 合理扩量、Budget exhausted 但无 marginal headroom、ROAS 增长但贡献利润恶化。

执行完整性原则：

```text
timeout ≠ failed write
executor success ≠ trusted current state
same intended value ≠ retry is automatically safe
same idempotency key + same stable intent + explicit dedup contract → transport retry may be safe
safe retry ≠ application confirmed
same keyword text ≠ same optimization identity
higher ROAS ≠ higher contribution profit
recent zero orders ≠ irrelevant query
```

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

明确区分 `proposed ≠ applied`、`applied ≠ readback confirmed`、`readback confirmed ≠ worked`。历史是证据，不是当前事实。

## Experiment Planner

证据不足但可验证的优化优先进入 Experiment / Shadow。实验应预声明 decision question、hypothesis、treatment、control/holdout、primary metric、guardrails、attribution-mature window、contamination risk 与 stop/rollback rule；缺少统计输入时不伪造 power/MDE。

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
- 不把固定经验阈值伪装成官方规则；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 同实体新动作先检查未完成验证和可信 readback；
- stale memory / stale identity 不等于当前状态；
- Executor 的 unknown/timeout 结果先 reconcile，再决定 retry；
- 幂等重试必须保持 stable intent、相同 key 与相同 mutation payload；
- ROAS/ACoS 不能替代贡献利润和业务目标；
- 历史赢家短期 0 单先诊断 conversion break，不自动否定；
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
- [x] Previous Winner zero-order / profitability conflict / reconciliation disagreement / explicit idempotency retry fixtures
- [ ] 继续拆薄旧版较厚 Skills
- [ ] 扩展 portfolio-level conflict 与 deliberate entity migration evals
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
