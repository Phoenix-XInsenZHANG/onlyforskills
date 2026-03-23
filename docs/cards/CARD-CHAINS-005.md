---
id: CARD-CHAINS-005
title: Create code-review-loop chain
description: 新建 .claude/skills/code-review-loop/SKILL.md，循环链：requesting-code-review→receiving-code-review→tdd→verification→requesting-code-review
parent_story: US-CHAINS-003
parent_prd: PRD-CHAINS
status: backlog
priority: medium
estimate: 1h
implementation_checklist:
  - 创建目录 .claude/skills/code-review-loop/
  - 写 SKILL.md，frontmatter 含 type:chain
  - 触发条件：用户说"代码审查"、"review loop"、"审查循环"
  - 工作流图（循环结构）：
    requesting-code-review → receiving-code-review
    → [有反馈?] → tdd → verification → requesting-code-review (循环)
    → [通过?] → 结束
  - 节点说明（含循环终止条件）
  - 终止条件：reviewer 通过审查，无需更多改动
  - 执行规则：循环最多 3 轮，第 3 轮未通过 → BLOCKED 状态，等待人工介入
  - 关系表：与 bug-fix-to-ship / refactor-to-ship 的衔接
files_to_modify:
  - .claude/skills/code-review-loop/SKILL.md (新建)
---
