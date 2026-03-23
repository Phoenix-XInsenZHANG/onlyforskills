---
id: CARD-GSTACK-005
title: 注入 Completion Status Protocol 到 debugging、code-review、verification skills
description: 将 gstack 的标准化完成状态报告协议（DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT）注入关键 skills，统一 AI 输出的结束信号格式
parent_story: US-GSTACK-002
parent_prd: PRD-GSTACK
status: backlog
priority: medium
estimate: 1.5h
implementation_checklist:
  - 读取 gstack/review/SKILL.md 中 "Completion Status Protocol" 完整章节
  - 在 .claude/skills/debugging/SKILL.md 末尾注入 Status Protocol
  - 在 .claude/skills/code-review/SKILL.md 末尾注入 Status Protocol（与 CARD-GSTACK-004 同批修改）
  - 在 .claude/skills/verification/SKILL.md 末尾注入 Status Protocol
  - 同时注入 Escalation 规则（3次失败即停止、安全敏感操作即停止）
  - 验证三个 skill 中的 Protocol 格式一致
files_to_modify:
  - .claude/skills/debugging/SKILL.md
  - .claude/skills/code-review/SKILL.md
  - .claude/skills/verification/SKILL.md
---
