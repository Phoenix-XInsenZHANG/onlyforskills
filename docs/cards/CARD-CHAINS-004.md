---
id: CARD-CHAINS-004
title: Create deploy-pipeline chain
description: 新建 .claude/skills/deploy-pipeline/SKILL.md，节点序列：verification→requesting-code-review→ship[gstack]→qa[gstack]→finishing-branch
parent_story: US-CHAINS-002
parent_prd: PRD-CHAINS
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 创建目录 .claude/skills/deploy-pipeline/
  - 写 SKILL.md，frontmatter 含 type:chain
  - 触发条件：用户说"部署"、"上线"、"deploy"、"发版"
  - 工作流图：verification→requesting-code-review→ship[gstack]→qa[gstack]→finishing-branch
  - 节点说明：
    - verification：确认测试全部通过，构建成功
    - requesting-code-review：最终代码审查
    - ship[gstack]：自动合并 + 版本号 bump + CHANGELOG 更新
    - qa[gstack]：上线后真实浏览器冒烟，验证核心路径
    - finishing-branch：清理分支
  - 执行规则：顺序执行，所有节点必经
  - 关系表：与 full-feature-lifecycle 末尾衔接关系
files_to_modify:
  - .claude/skills/deploy-pipeline/SKILL.md (新建)
---
