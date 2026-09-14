# 贡献指南

感谢你改进 Yunsheng AIGC Video CMS Skills。

## 提交内容

- 修正文档、事实口径或边界条件；
- 改善既有 Skill 的触发范围和输出质量；
- 增加有明确使用场景的新 Skill；
- 提交能够暴露真实决策错误的评测用例。

请勿提交真实客户名、人名、群聊原文、内部链接、密钥、账单、未脱敏报价或未获授权的素材。

## 修改要求

1. 保持每个 Skill 可独立运行，必需规则不能只存在于 `shared/`。
2. 不把缺失数据补成 `0`，不把估算包装成实际结果。
3. 涉及批准、验收或对外发布时，保留人工决策门禁。
4. 新增 Skill 时同步更新 `manifest.json`、`CATALOG.md` 和 `evals/cases.jsonl`。
5. 测试材料必须是合成数据或已完成不可逆脱敏的数据。

## 本地校验

```bash
python3 evals/validate_pack.py
```

如果本地安装了 Codex `skill-creator`，还应对每个 Skill 运行其 `quick_validate.py` 结构校验。

提交 Pull Request 时，请说明：解决的问题、变更的 Skill、行为边界是否改变，以及对应测试结果。

