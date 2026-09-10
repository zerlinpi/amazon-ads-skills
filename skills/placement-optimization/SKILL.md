---
name: placement-optimization
description: 分析 Amazon Ads Sponsored Products 等广告的 Top of Search、Product Pages、Rest of Search 版位表现与 modifier，识别高效版位、浪费和竞价放大风险。适用于 placement 调整和流量结构优化。
license: MIT
metadata:
  author: "zerlinpi"
  version: "0.1.0"
  display_name_zh: "广告版位优化"
  display_name_en: "Placement Optimization"
  description_zh: "分析不同广告版位效率并生成安全的 placement modifier 建议。"
  description_en: "Analyze Amazon Ads placement performance and modifiers across Top of Search, Product Pages and Rest of Search."
---

# Placement Optimization

## 默认模式

`Suggest`。输出 placement modifier 候选，不直接修改 campaign。

## 输入

需要尽量包含：
- placement name；
- impressions、clicks、spend、orders、sales；
- CPC、CVR、ACOS/ROAS；
- current base/target bid；
- current placement modifier；
- campaign bidding strategy；
- active schedule/event bid rules or other material modifiers；
- material control-change timestamps；
- 日期窗口和目标。

当 recommendation 依赖 base bid、placement modifier、dynamic bidding、schedule/event rules 等控制的交互时，按需加载：

`references/realized-bid-exposure.md`

## 分析思路

### 1. 看效率，不只看销售额

高销售额版位可能只是获得更多流量。比较：
- spend share vs sales share；
- CPC；
- CVR；
- ACOS/ROAS；
- 样本量；
- query/target/product mix 是否可比。

### 2. 区分配置控制与 realized exposure

Base/target bid、placement adjustment、campaign bidding strategy、schedule/event rule 都是配置控制；placement report 中的实际流量、CPC、CVR 和效率是 realized outcome。

不要从配置值自行发明一个精确 auction-level effective bid。控制组合与 Amazon 的 auction-time logic 共同影响实际 exposure，应该通过控制时间线 + placement delivery/CPC 来诊断。

### 3. 看增量潜力

高效 Top of Search 不代表应该立即大幅提高 modifier。需要判断：
- 当前 impression/click 规模；
- base bid 是否本身偏低/偏高；
- modifier 提升可能带来的边际 CPC；
- dynamic bidding / bid rules 是否已经改变 exposure；
- 目标是否偏增长还是利润；
- 是否存在可解释的 marginal headroom，而不只是历史平均 ROAS/ACOS 好看。

### 4. 识别放大与归因风险

Base bid、dynamic bidding、placement modifier、schedule/event rules 可能共同影响实际竞价。不要把 modifier 当作独立旋钮。

如果多个 material controls 在同一 attribution/measurement window 内变化，placement 结果只能 `Directional / Confounded`，除非有额外设计能分离影响。

## 常见状态

### High-efficiency / underexposed

可考虑提高 modifier、调整 base bid 或设计实验，但需判断哪一个控制最可解释，并确认没有重叠的 pending control change。

### High-efficiency / already dominant

继续扩量可能边际效率下降，先观察，不追涨。

### Low-efficiency / high-spend

检查 query mix、CVR、retail state 和 coupled controls 后，再判断降低 modifier、base bid 或其他控制。

### Low-volume

样本不足，不做强结论。

### Coupled / confounded

多个竞价控制或规则同时变化，或当前 control state 不完整。优先 `Hold / Shadow / Experiment`，不要输出假精度 modifier。

## 变更原则

- 一次只做可归因的单一/最小控制变化，除非实验明确设计组合 treatment；
- 若同时需要改 base bid 和 placement，优先分阶段；
- 已有 base bid / placement / bidding-strategy / bid-rule 变化 pending evaluation 时，不叠加同一路由上的另一个 material change；
- 数值幅度需要账户策略、校准响应或明确实验约束；必要时加载 `../../references/action-sizing.md`；
- 设验证窗口，避免短期反向调整；
- 大促、event rule active window、零售状态变化需要单独解释。

## 输出

每个 placement：
- current modifier；
- current base/target bid；
- bidding strategy / active bid-rule state；
- control state as-of / material change timeline；
- spend share / sales share；
- CPC/CVR/ACOS；
- baseline comparison；
- interaction risk；
- causal attribution: Supported / Directional / Confounded / Unknown；
- recommendation: increase/decrease/hold/investigate/experiment；
- recommended control；
- proposed modifier（仅证据和 sizing basis 充分时）；
- confidence；
- evidence；
- guardrails；
- validation window；
- rollback condition。

## 禁止

- 不因为 Top of Search CVR/ROAS 高就默认提高 modifier；
- 不忽略 dynamic bids strategy、schedule/event rules 或其他 material bidding controls；
- 不把配置值拼成未经平台行为证实的精确 effective-bid 公式；
- 不把历史 placement 平均效率当成增加 modifier 后的保证边际效率；
- 不在 placement 样本很小的时候做大幅动作；
- 不同时大改多个竞价层造成无法归因；
- 不在 material control state 缺失/过期时输出 action-safe 精确 modifier。
