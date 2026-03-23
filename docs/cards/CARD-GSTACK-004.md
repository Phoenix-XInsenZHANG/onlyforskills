---
id: CARD-GSTACK-004
title: 注入 SQL 安全 + LLM 信任边界检查清单到 code-review skill
description: 从 gstack/review/SKILL.md 提取 SQL 安全检查和 LLM prompt injection 相关的 review 维度，注入 .claude/skills/code-review/SKILL.md
parent_story: US-GSTACK-002
parent_prd: PRD-GSTACK
status: backlog
priority: medium
estimate: 1.5h
implementation_checklist:
  - 通读 gstack/review/SKILL.md 全文，找到 SQL safety 和 LLM trust boundary 相关章节
  - 对比 .claude/skills/code-review/SKILL.md 现有检查项，识别缺失维度
  - 将以下内容注入 code-review skill：SQL 注入安全检查项、LLM 提示词信任边界检查项（用户输入是否直接拼接到 prompt）、条件副作用检查（conditional side effects）
  - 同时注入 gstack/review/SKILL.md 中的时间压缩表（作为 code review 完整性参考）
  - 验证注入后的 checklist 不与现有项重复
files_to_modify:
  - .claude/skills/code-review/SKILL.md
---
