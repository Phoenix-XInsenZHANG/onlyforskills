---
id: CARD-CHAINS-006
title: Update register.md and CLAUDE.md with Chains table
description: 在 register.md 添加独立 Chains 表，更新 CLAUDE.md Skills Index 使 chains 独立分组显示
parent_story: US-CHAINS-003
parent_prd: PRD-CHAINS
status: backlog
priority: medium
estimate: 0.5h
implementation_checklist:
  - 读取 .claude/skills/general/references/register.md
  - 在 register.md 末尾添加 "## Chains" 表，包含 5 条 chain：
    C01 full-feature-lifecycle / C02 bug-fix-to-ship / C03 refactor-to-ship / C04 deploy-pipeline / C05 code-review-loop
    列：ID | Name | Nodes | Trigger keywords
  - 读取 CLAUDE.md，在 Skills Index 表之后新增 "### Chains" 独立分组
  - 验证：register.md 行数 < 200（MEMORY.md 限制类比）
files_to_modify:
  - .claude/skills/general/references/register.md
  - CLAUDE.md
---
