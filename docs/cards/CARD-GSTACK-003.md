---
id: CARD-GSTACK-003
title: 注入 Completeness Principle 到 brainstorming 和 tdd skills
description: 将 gstack 的 "Boil the Lake" 完整性原则和人力 vs CC 时间压缩表注入 brainstorming 和 tdd skill，在方案评估和测试覆盖率决策时给 AI 更强的完整性指引
parent_story: US-GSTACK-002
parent_prd: PRD-GSTACK
status: backlog
priority: medium
estimate: 2h
implementation_checklist:
  - 读取 gstack/review/SKILL.md 中 "Completeness Principle — Boil the Lake" 完整章节内容
  - 读取 gstack/review/SKILL.md 中的时间压缩参考表（boilerplate/test/feature/bugfix/architecture/research）
  - 在 .claude/skills/brainstorming/SKILL.md 的"Exploring approaches"章节后注入 Completeness Principle
  - 在 .claude/skills/brainstorming/SKILL.md 注入时间压缩表（作为方案评估参考）
  - 在 .claude/skills/tdd/SKILL.md 注入 Completeness Principle（强调测试覆盖不可妥协）
  - 验证注入后的 skill 逻辑连贯，不破坏现有流程
files_to_modify:
  - .claude/skills/brainstorming/SKILL.md
  - .claude/skills/tdd/SKILL.md
---
