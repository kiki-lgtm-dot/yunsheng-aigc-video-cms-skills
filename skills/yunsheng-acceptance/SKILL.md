---
name: yunsheng-acceptance
license: Apache-2.0
description: 对云生脚本、分镜、样片或成片执行内容、品牌、技术与权利质检，记录需求方验收和交付确认；用于生成可追溯验收候选，不得替审核人自动通过。
---

# 云生质检与需求方验收

让“模型能生成”“内部检查通过”“需求方正式验收”成为三个不同状态。默认使用简体中文。

## 何时使用

- 脚本、分镜、样片或最终成片进入阶段审核。
- 需要记录 Needs Changes、通过条件、返工责任人与验收时间。
- 需要生成最终交付清单和重新打开项目的条件。

不用于代替品牌、法务、业务负责人或平台的正式授权。

## 输入

- ProjectID、交付物类型、DeliverableVersion 与父版本。
- Approved Brief 的 ID、版本、审核人和冻结时间。
- 内容、品牌、技术、版权/肖像/素材授权标准。
- 交付文件、技术检测结果、需求方逐条反馈及其来源。
- 审核角色、责任边界、截止时间和约定通过门槛。

输入不完整时，标记待补证，不推断为通过。缺失不等于否决或 0；事实、推算、估算和外部基准分栏。所有数量与耗时附周期、对象范围、分母、公式和 source_id。source_grade 中 A=系统/账单/正式记录，B=带日期可复核截图或人工台账，C=用户陈述，D=外部基准，N=无证据；claim_method 使用 direct/derived/estimated/benchmark/unknown。对外使用默认需人工确认。

## 状态

- candidate：候选，尚未质检。
- needs_changes：存在必须修改项。
- technical_pass：仅技术规格通过。
- internal_qc_pass：内部内容与品牌检查通过。
- accepted：有具名需求方对指定版本的正式验收记录。
- rejected：明确拒绝并保留理由。
- reopened：验收后因新事实或变更重新开启。

状态只能由对应证据推进；导出、下载、交付文件存在都不等于 accepted。

## 工作流

1. 校验交付版本与 Approved Brief 是否对应，发现基线漂移先停止。
2. 分四类检查：内容事实与传播目标、品牌规范、技术规格、权利与合规。
3. 对每个问题记录镜号/时间码/文件位置、严重度、依据、责任人和截止时间。
4. 生成 AcceptanceCandidate，供具名审核人选择 Approved 或 Needs Changes。
5. Needs Changes 只生成修改清单，不静默改稿；新稿必须产生新版本。
6. 收到正式验收后记录 AcceptanceID、验收人、时间、版本与交付范围。
7. 输出最终交付清单和可能触发 reopened 的条件。

## 严重度

- Blocker：事实、品牌、权利、合规或文件损坏导致不可交付。
- Major：影响核心表达、连续性或主要平台规格。
- Minor：不改变核心内容的局部修正。
- Suggestion：非阻断优化，不得冒充必改项。

## 固定输出

1. 验收范围与基线。
2. QC 明细：CheckID、类别、位置、问题、严重度、依据、Owner、状态。
3. 审核决定：Approved/Needs Changes/Rejected/待确认。
4. 修改轮次、已解决与未解决问题。
5. AcceptanceRecord：AcceptanceID、需求方、版本、时间、范围、证据。
6. 最终交付清单及重新打开条件。

ReviewEvent 至少包含 BriefID-Version、submitted_at、reviewed_at、reviewer_role、decision、change_items 和 next_version。文件版本数不能推断修改轮次；一次审核中的多条意见仍计一轮，内部自改不计需求方修改轮次。历史记录缺少真实审核事件时使用 unknown 或 legacy_unverified。

## 停止条件

缺少 Approved Brief、目标版本或具名审核权限时，只输出检查结果和待确认问题，不写 accepted。任何自动改稿、覆盖确认版本或代表需求方签收都需另行明确授权。
