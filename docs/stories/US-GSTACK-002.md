---
id: US-GSTACK-002
title: 用户在使用现有 .claude skills 时自动受益于 gstack 的最佳框架
description: gstack 的 Completeness Principle、Status Protocol、时间压缩表、SQL/LLM 检查清单被注入到 brainstorming、code-review、tdd、writing-plans、debugging、verification 等 skills
parent_prd: PRD-GSTACK
cards:
  - CARD-GSTACK-003
  - CARD-GSTACK-004
  - CARD-GSTACK-005
status: backlog
acceptance_criteria:
  - brainstorming skill 包含 Completeness Principle（Boil the Lake）和人力 vs CC 时间压缩表
  - code-review skill 包含 SQL 安全检查项、LLM 信任边界检查项
  - debugging、code-review、verification skills 包含 Completion Status Protocol（DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT）
  - writing-plans skill 包含人力 vs CC 时间压缩参考表
  - tdd skill 包含 Completeness Principle 指导（覆盖率要求）
---
