---
id: US-CHAINS-003
title: User can see all available chains in register.md and CLAUDE.md for easy routing
description: register.md 有独立 Chains 表，CLAUDE.md Skills Index 中 chains 独立分组，general skill 路由选项从 Chains 表动态读取
parent_prd: PRD-CHAINS
cards:
  - CARD-CHAINS-005
  - CARD-CHAINS-006
status: backlog
acceptance_criteria:
  - register.md 包含 "## Chains" 独立表格，列出 5 条 chain 的 ID/名称/节点/触发词
  - code-review-loop chain 新建，包含循环结构说明
  - CLAUDE.md Skills Index 中新增 Chains 独立分组（区别于 Skills 行）
  - general skill SKILL.md Phase 2 toolchain 说明引用 register.md Chains 表
---
