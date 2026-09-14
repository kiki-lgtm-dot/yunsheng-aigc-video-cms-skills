# 云生 CMS 指标字典

## 对象

- request_count：周期内去重 RequestID 数。
- project_count：周期内去重 ProjectID 数。
- delivered_video_count：完成约定交付动作的视频版本数，不等于验收数。
- accepted_video_count：存在有效 AcceptanceRecord 的视频版本数。
- model_run_count：有效 ModelRunID 数；缓存命中和重试按记录规则区分。
- asset_count：去重 AssetID 数；派生资产与引用次数分列。

## Brief 审核

- external_review_rounds：真实需求方 ReviewEvent 数；内部自改不计。
- change_item_count：所有 Needs Changes 事件中的逐条意见数。
- first_pass_rate：首个外部 ReviewEvent 即 Approved 的终态 Brief 数 ÷ 周期内已有外部终态的 Brief 数。
- review_calendar_hours：reviewed_at - submitted_at 的自然时长。
- review_working_hours：按明确工作日历换算；无日历时不计算。

开放中项目不算首轮失败，也不能从分母中静默删除。

## 工时与成本

- activity_hours：直接完成生产活动的工时。
- coordination_hours：会议、等待反馈之外的协作对齐工时。
- wait_hours：排队、审核等待和外部依赖造成的自然等待。
- headcount：参与的去重人数。
- FTE：按明确周期和标准工时换算的人力当量。
- new_delivery_opex：人工 + 算力/API + 约定工具分摊 + 外部服务。
- transformation_investment：产品开发、接入、迁移和一次性建设投入。
- all_in_cost：new_delivery_opex + transformation_investment。

## 价值

- baseline_delivery_cost：同范围历史交付成本或完成可比性校正的报价。
- gross_savings：baseline_delivery_cost - new_delivery_opex。
- net_benefit：baseline_delivery_cost - all_in_cost。
- savings_rate：net_benefit ÷ baseline_delivery_cost。
- transformation_ROI：net_benefit ÷ transformation_investment，仅在投入完整且分母大于 0 时使用。
- asset_reuse_rate：被后续项目有效引用的可复用资产数 ÷ 同周期具备复用资格的资产数。

市场报价只能作为 source_grade D；必须记录报价日、地域、视频时长、质量、修改轮次、后期、配音、版权和税费范围。
