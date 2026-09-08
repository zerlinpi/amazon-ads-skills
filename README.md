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
  → Readback → Post-change Review
  → Keep / Monitor / Rollback Candidate
  → Append event → Refresh entity history
         ↓
Historical Replay / Eval Fixtures
  → detect decision regressions
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

`evals/` 仅用于测试和历史回放，普通账户分析不应加载，以免浪费 token 或污染决策上下文。

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

当前保持 **15 个 Skills**。如果一个新能力只是“把已有 Skills 按固定运营节奏组合起来”，优先增加 `playbooks/`；如果目的是验证现有决策是否可靠，优先增加 `evals/`，而不是继续拆新 Skill。

## Historical Replay / Evals

`evals/README.md` 定义历史回放和回归测试合同。

评估拆成两层：

```text
Contract checks
→ schema / path / enum / mode / structure

Capability replay
→ same fixture through matching Skill
→ score decision behavior, not wording
```

Capability Eval 使用三态：`met / not_met / insufficient_evidence`。`insufficient_evidence` 不会被强行算作通过或失败。

当前 regression pack 已覆盖 **15 类关键安全风险**，包括：Mixed-ASIN 误否词、Negative attachment 错层级、Pending Change 反复调参、Bid×Placement 联动、Featured Offer / Buy Box 冲击、Stockout 转化冲击、Promotion baseline 假异常、Attribution Lag 假失败、Unknown Application 错误归因、Partial Application、stale entity identity memory、Executor retry/idempotency 风险、Experiment contamination、Proven Winner 合理扩量、Budget exhausted 但无 marginal headroom。

其中新增的执行完整性原则是：**timeout ≠ failed write**。当外部 Executor 写入结果为 `Unknown` 且没有 trusted readback / idempotency evidence 时，Skill 只能 Hold / Manual Review / Blocked，不能盲目重复写入。实体经过 Campaign/Ad Group restructure 重新创建后，也不能因为 keyword text 相同就自动继承旧实体的 optimization memory。

结构：

```text
evals/
├── README.md
└── fixtures/
    ├── mixed-asin-negative-blocked.json
    ├── negative-attachment-scope-mismatch.json
    ├── pending-bid-change-hold.json
    ├── bid-placement-interaction-hold.json
    ├── post-change-attribution-lag.json
    ├── application-status-unknown.json
    ├── partial-application-manual-review.json
    ├── stale-entity-identity-memory.json
    ├── executor-retry-idempotency.json
    ├── retail-readiness-conversion-shock.json
    ├── stockout-conversion-shock.json
    ├── promotion-period-false-positive.json
    ├── experiment-contamination-hold.json
    ├── proven-winner-budget-growth.json
    └── budget-exhausted-no-headroom.json

schemas/eval-case.json
```

Fixture 使用合成数据，不提交真实客户、账户或第三方私有导出。

## Weekly Review Playbook

`playbooks/weekly-review.md` 用于周期性账户复盘。它不是固定阈值表，而是从 Comparable windows、Business-first scorecard、Recent-action / memory checkpoint、Contribution triage、Campaign + ASIN review、Search term / target review、Budget / bid / placement review、Retail / event confounders，最终输出 Protect / Recover / Optimize / Grow / Experiment / Hold 与 P0-P4 action packet。

核心原则：不使用固定 ACOS/CTR/CVR 阈值强制打标；不因预算跑满自动加预算；不因 Search Term 暂时 0 单自动否定；不在上一动作未成熟时叠加反向动作；复杂根因交给专业 Skill；输出必须允许明确 Hold。

## Optimization Memory

`references/optimization-memory.md` 采用：

```text
Append-first event ledger
→ schemas/optimization-event.json
→ derived compact entity history
→ schemas/entity-history.json
→ read-before-recommend gate
```

明确区分 `proposed ≠ applied`、`applied ≠ readback confirmed`、`readback confirmed ≠ worked`、`rollback proposed ≠ rolled back`。历史是证据，不是当前事实；实体身份也必须连续可验证，不能把旧 entity history 直接迁移到重建后的新 ID。

## Experiment Planner

不确定但可验证的优化优先进入实验，而不是伪装成高置信动作。实验应预声明 decision question、falsifiable hypothesis、treatment、control/holdout、一个 primary metric、guardrails、attribution-mature window、contamination risk、stop/rollback rule。固定点击数、订单数或预算倍数不作为通用实验标准；缺少统计输入时不伪造 power/MDE。

## Safety

| Mode | 行为 |
|---|---|
| `Read-only` | 读取和解释 |
| `Suggest` | 生成建议；默认 |
| `Shadow` | 模拟、回测、实验 |
| `Execute` | 仅显式授权并交给外部 Executor |

建议应尽量携带 evidence、confidence、data quality、sample sufficiency、guardrails、validation window、rollback condition。

## Benchmark Policy

外部 benchmark 不作为自动执行阈值。优先顺序：同账户、同目标、同归因口径历史 → 同账户实验/Holdout → 同实体可比历史 → 方法透明的外部 cohort → 泛行业 benchmark。详见 `references/benchmark-policy.md`。

## Multi-Agent Compatibility

| Runtime | 入口 |
|---|---|
| OpenAI Codex | `.codex-plugin/plugin.json` + `skills/` + `AGENTS.md` |
| Claude Code | `.claude-plugin/plugin.json` + `skills/` + `CLAUDE.md` |
| WorkBuddy | `.workbuddy-plugin/plugin.json` + `skills/` |
| 其他 Agent Skills Runtime | `skills/<name>/SKILL.md` |

三套 Runtime 共用同一个 canonical `skills/` 树，不复制 Amazon Ads 业务逻辑。

## Development Rules

- 一个 Skill 解决一个清晰决策问题；
- 组合型运营节奏优先使用 playbook；
- 回归验证优先使用 synthetic eval fixture，不为测试单独制造 Skill；
- `SKILL.md` 保持薄，详细知识按需加载；
- 区分 Fact / Observation / Hypothesis / Cause / Action / Outcome；
- 不编造缺失数据或历史；
- 不把固定经验阈值伪装成官方规则；
- 对同实体新动作先检查未完成验证的旧动作；
- 事件尽量 append-first，实体摘要可重建；
- stale memory 不等于当前状态，stale identity 也不等于同一实体；
- Executor 的 unknown/timeout 结果必须先 readback/reconcile，再考虑 retry；
- 不确定但可验证的结论优先进入实验；
- Eval 判断行为而不是 exact wording；
- 默认 Suggest/Shadow，不直接写真实账户。

## Sources & Licenses

项目持续研究公开 Amazon Ads / PPC / Agent Skills 项目。采用流程：`discover → license check → extract generic idea → independently rewrite → Amazon Ads adaptation → safety gate → progressive loading`。不会把第三方受版权保护的大段文本、固定阈值或私有接口实现直接搬入仓库。已审阅来源见 `docs/SOURCES.md`。

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
- [x] Historical replay / initial eval fixtures
- [x] 扩展高风险回归覆盖：Retail Readiness、Attribution Lag、Unknown Application、Marginal Headroom
- [x] 扩展高风险回归覆盖：Negative attachment、Bid×Placement、Experiment contamination、Partial Application
- [x] 扩展高风险回归覆盖：Promotion、Stockout、stale entity identity、Executor retry/idempotency
- [ ] Previous Winner suddenly zero-order / profitability conflict / reconciliation disagreement fixtures
- [ ] 继续拆薄旧版较厚 Skills
- [ ] Amazon Ads API / 自研 Connector 示例

## Disclaimer

本项目是独立开源 Amazon Ads AI Agent Skills 项目，与 Amazon 官方无隶属或背书关系。
