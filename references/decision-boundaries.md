# 决策边界与执行权限

## 四级模式

### Read-only

允许：读取、清洗、解释、比较、诊断。

禁止：生成声称已执行的修改结果。

### Suggest（默认）

允许：生成具体动作建议与标准化 action proposal。

禁止：调用任何真实 Amazon Ads 写接口或声称修改已生效。

### Shadow

允许：对动作进行模拟、回放、对照实验设计、预估影响，并记录“如果执行会怎样”。

禁止：修改真实账户。

### Execute

仅当满足以下全部条件：
1. 用户明确授权执行；
2. 外部 connector/executor 已配置且权限足够；
3. 输入通过数据质量检查；
4. 动作通过 guardrails；
5. 可审计记录当前值、建议值、原因、证据、时间；
6. 定义验证窗口和回滚条件。

Skill 本身仍只输出动作；真实写入由外部执行器完成。

## 动作幅度 Guardrails

仓库不定义通用的固定 bid/budget/placement 单次调整百分比。需要把方向性建议转成具体数值时，按需加载：

- `action-sizing.md`

动作幅度应由当前账户的目标、样本/归因成熟度、可信 current state、历史响应、边际 headroom、业务角色、库存/活动、耦合控制、下行风险、可逆性和显式 caller/account policy 共同约束。

如果缺少能够证明数值幅度安全的账户级约束或校准证据，不要用仓库经验百分比补齐精度；优先输出 Directional、Probe/Experiment、Hold 或 Manual Review。

以下仍属于通用保护原则：

- 不把 campaign budget 降至会立即中断核心品牌/防御投放的水平；
- 不因短周期 0 订单直接否定高价值品牌词、核心类目词或已验证历史赢家；
- 不对同一实体在一个验证窗口内反复调整同一参数；
- 不将不同币种或 Marketplace 的金额直接聚合；
- caller/account 提供的 max change、protected floor、spend-at-risk 等限制只作为约束，不作为性能结论。

以上不是 Amazon 官方限制，而是本仓库的风险控制原则。

## 硬停止条件

出现以下情况时，不输出高置信度执行动作：
- 数据日期/归因窗口未知；
- 大量字段缺失或金额币种不明；
- Listing suppressed、无库存、Buy Box 丢失等商品问题主导转化；
- 大促/Best Deal/Lightning Deal/Coupon 等活动影响明显但无活动上下文；
- 刚发生大幅价格变更；
- 广告刚创建或刚经历重大结构调整，样本不足；
- 用户目标互相冲突且未指定优先级。

## 否词保护

否定前必须检查：
- 是否为品牌核心词；
- 是否为 ASIN/SKU 关键防御词；
- 是否有历史订单或高价值 NTB 表现；
- 是否仅因归因延迟造成暂时 0 单；
- 是否应先 Exact 收割再 Negative Exact/Phrase；
- 是否会影响其他 intended traffic。

## 预算保护

预算不足不等于应该加预算。只有当受限 campaign 的边际效率、业务目标和库存承载都支持扩量时才建议增预算。若存在固定预算池，还必须说明新增预算来源及来源机会成本。

## 审计要求

每个可执行候选至少记录：
- timestamp
- profile/marketplace（非敏感标识可脱敏）
- entity type/id
- before/after（如数值幅度可被证据支持）
- raw/directional anchor 与 sizing basis（如适用）
- reason/evidence
- confidence
- policy/guardrail results
- requester/approval source
- validation window
- rollback condition
