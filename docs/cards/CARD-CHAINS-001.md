---
id: CARD-CHAINS-001
title: Rewrite full-feature-lifecycle chain with gstack qa node
description: 按统一 Chain Standard 重写 full-feature-lifecycle SKILL.md，去掉独立 tdd 节点，末尾加必经的 qa[gstack] 节点
parent_story: US-CHAINS-001
parent_prd: PRD-CHAINS
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 读取现有 .claude/skills/full-feature-lifecycle/SKILL.md
  - 更新 frontmatter：添加 type:chain，更新 description 含节点序列
  - 重写工作流图：brainstorming→writing-plans→subagent-driven-development→qa[gstack]
  - 移除独立 tdd 节点（tdd 是 subagent-driven-development 内置要求）
  - 新增 qa 节点说明：目的（真实浏览器冒烟）+ 产出 + 调用方式（Skill "qa"）
  - 所有节点标注为必经步骤
  - 末尾关系表加入 bug-fix-to-ship / deploy-pipeline 引用
files_to_modify:
  - .claude/skills/full-feature-lifecycle/SKILL.md
---
