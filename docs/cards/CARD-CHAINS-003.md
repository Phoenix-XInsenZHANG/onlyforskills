---
id: CARD-CHAINS-003
title: Create refactor-to-ship chain
description: 新建 .claude/skills/refactor-to-ship/SKILL.md，节点序列：codex[gstack]→tdd→verification→requesting-code-review→finishing-branch
parent_story: US-CHAINS-002
parent_prd: PRD-CHAINS
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 创建目录 .claude/skills/refactor-to-ship/
  - 写 SKILL.md，frontmatter 含 type:chain
  - 触发条件：用户说"重构"、"技术债清理"、"refactor"
  - 工作流图：codex[gstack]→tdd→verification→requesting-code-review→finishing-branch
  - 节点说明：
    - codex：重构前审查，确认方向正确，识别风险
    - tdd：先写测试固定行为，再重构
    - verification：验证行为未改变，所有测试通过
    - requesting-code-review：请求审查
    - finishing-branch：合并/部署
  - 执行规则：顺序执行，所有节点必经
  - 关系表：与 bug-fix-to-ship / full-feature-lifecycle 区别
files_to_modify:
  - .claude/skills/refactor-to-ship/SKILL.md (新建)
---
