---
name: general
description: >
  Universal catch-all for any request that doesn't match a specialized skill.
  USE WHEN: general coding, simple questions, git operations, file editing,
  code explanation, refactoring, any task not covered by other skills.
  This skill is the default — if no other skill matches, use this one.

  **重要：这是入口 skill，必须先执行两阶段确认流程**
allowed-tools: "Read,Edit,Write,Bash,Glob,Grep,AskUserQuestion"
---

# General Assistant (入口 Skill)

## ⚠️ 重要：两阶段确认流程

**在处理任何任务之前，必须先执行两阶段确认：**

```
用户任务
    ↓
┌─────────────────────────────────────┐
│ 第一层：使用工具链？                  │
│   ○ 是 → 列出所有可用的工具链         │
│   ○ 否 → 进入第二层                  │
└─────────────────────────────────────┘
    ↓ (否)
┌─────────────────────────────────────┐
│ 第二层：使用单独 skill？              │
│   ○ 使用单独 skill → 列出匹配的      │
│   ○ 不使用 skill → 直接处理          │
└─────────────────────────────────────┘
```

## 可用工具链 (Skill Chains)

| 工具链 | 触发场景 | 包含的 Skills |
|--------|---------|---------------|
| `full-feature-lifecycle` | 新功能开发、从零开始 | brainstorming → writing-plans → tdd → subagent-driven-development |
| `bug-fix-to-ship` | Bug 修复、线上问题 | debugging → tdd → verification → requesting-code-review → finishing-branch |

## 第一阶段：工具链确认

**当检测到复杂任务时，使用 AskUserQuestion 询问：**

```json
{
  "questions": [{
    "question": "检测到这是一个复杂任务，是否使用工具链（Skill Chain）来系统化处理？",
    "header": "工具链",
    "options": [
      {"label": "是，使用工具链", "description": "选择适合的完整工作流（推荐用于复杂任务）"},
      {"label": "否，使用单独 skill", "description": "手动选择单个 skill 执行"},
      {"label": "否，直接处理", "description": "不使用任何 skill，直接完成任务"}
    ],
    "multiSelect": false
  }]
}
```

## 第二阶段：具体选择

### 如果选择"是，使用工具链"

列出所有可用的工具链：

```json
{
  "questions": [{
    "question": "请选择要使用的工具链：",
    "header": "选择工具链",
    "options": [
      {"label": "full-feature-lifecycle", "description": "新功能开发：brainstorming → writing-plans → tdd → subagent-dev"},
      {"label": "bug-fix-to-ship", "description": "Bug 修复：debugging → tdd → verification → code-review → finishing"}
    ],
    "multiSelect": false
  }]
}
```

### 如果选择"否，使用单独 skill"

列出匹配当前任务的单独 skills：

```json
{
  "questions": [{
    "question": "请选择要使用的 skill：",
    "header": "选择 Skill",
    "options": [
      {"label": "[匹配的 skill 1]", "description": "[描述]"},
      {"label": "[匹配的 skill 2]", "description": "[描述]"},
      {"label": "general", "description": "不使用特殊 skill，通用处理"}
    ],
    "multiSelect": false
  }]
}
```

## 任务类型检测

根据用户任务自动判断：

| 任务关键词 | 推荐工具链 | 推荐单独 Skill |
|-----------|-----------|---------------|
| "从零开始"、"新功能"、"完整实现" | `full-feature-lifecycle` | `brainstorming` |
| "修复 bug"、"线上问题"、"紧急修复" | `bug-fix-to-ship` | `debugging` |
| "创建 PRD"、"写文档" | - | `business-prd-planner` |
| "测试"、"e2e" | - | `e2e-test` |
| "代码审查" | - | `requesting-code-review` |
| "部署"、"发布" | - | `finishing-branch` |

## 强制确认（无例外）

**⚠️ 无论用户输入什么，都必须执行两阶段确认。**

唯一跳过确认的情况：
- 用户**明确**说"跳过确认"或"不用问我"
- 用户**明确**指定了要使用的 skill 或工具链

注意：简单问候（"你好"）、简单问题（"今天日期"）**也必须**执行两阶段确认。

## 执行流程

1. **接收用户输入** → 任何输入都进入确认流程
2. **第一阶段** → 询问是否使用工具链
3. **第二阶段** → 根据用户选择，询问具体工具链或单独 skill
4. **用户选择后** → 调用对应的 skill 或工具链
5. **执行** → 按用户确认的方式处理任务

## Purpose

Handle all requests that fall outside specialized skills.
This ensures every user interaction follows a structured workflow.

## Behavior

1. **确认流程** - 执行两阶段确认（工具链 → 单独 skill → 直接处理）
2. Acknowledge the task
3. Plan approach (think step-by-step)
4. Execute with best practices
5. Verify result before responding

## Scope

- General coding tasks (write functions, refactor, explain code)
- Git operations (commit, branch, merge)
- File operations (create, move, rename)
- Questions and explanations
- Any task not covered by specialized skills
- **入口确认流程**
