---
id: CARD-CHAINS-002
title: Rewrite bug-fix-to-ship chain with codex[gstack] node
description: 按统一 Chain Standard 重写 bug-fix-to-ship SKILL.md，在 requesting-code-review 前插入必经的 codex[gstack] 对抗性审查节点
parent_story: US-CHAINS-002
parent_prd: PRD-CHAINS
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 读取现有 .claude/skills/bug-fix-to-ship/SKILL.md
  - 更新 frontmatter：添加 type:chain，更新 description 含完整节点序列
  - 重写工作流图：debugging→tdd→verification→codex[gstack]→requesting-code-review→finishing-branch
  - 在 Step 4 位置插入 codex 节点说明：目的（对抗性审查，找安全漏洞）+ 调用方式
  - 调整 Step 编号（原 4→5，原 5→6）
  - 末尾关系表加入 refactor-to-ship / code-review-loop 引用
files_to_modify:
  - .claude/skills/bug-fix-to-ship/SKILL.md
---
