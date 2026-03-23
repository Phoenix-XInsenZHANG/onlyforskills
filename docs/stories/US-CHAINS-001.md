---
id: US-CHAINS-001
title: User can trigger a complete feature development workflow via full-feature-lifecycle chain
description: 用户说"从零开始做X"时，自动走完 brainstorming→writing-plans→subagent-dev→qa 完整链路，包含 gstack qa 冒烟测试
parent_prd: PRD-CHAINS
cards:
  - CARD-CHAINS-001
  - CARD-CHAINS-002
status: backlog
acceptance_criteria:
  - full-feature-lifecycle SKILL.md 包含 type:chain frontmatter
  - 节点序列为 brainstorming→writing-plans→subagent-driven-development→qa[gstack]
  - qa 节点是必经步骤，文档中无"可选"字样
  - 与 bug-fix-to-ship 的关系在文档末尾有说明
---
