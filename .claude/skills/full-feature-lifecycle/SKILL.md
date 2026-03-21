---
name: full-feature-lifecycle
description: |
  完整功能开发生命周期 — 从需求到代码的端到端工作流。

  当用户说"从零开始"、"完整功能"、"新功能开发"、"端到端实现"时触发。

  自动按顺序调用 4 个 skill：
  1. brainstorming → 需求探索，输出 PRD/Story/Card
  2. writing-plans → 创建实施计划
  3. tdd → 测试驱动开发
  4. subagent-driven-development → 并行执行任务
---

# Full Feature Lifecycle

端到端功能开发工作流，确保从需求到代码的完整链路。

## 触发条件

- 用户说"从零开始做..."
- 用户说"完整功能开发"
- 用户说"端到端实现"
- 用户描述新业务需求，没有现有 PRD/Card

## 工作流程

```
┌─────────────────┐
│  1. BRAINSTORM  │  需求探索，输出 PRD/Story/Card
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. WRITING-PLANS│  创建详细实施计划
└────────┬────────┘
         ▼
┌─────────────────┐
│     3. TDD      │  先写测试，再写实现
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. SUBAGENT-DEV │  并行执行独立任务
└─────────────────┘
```

## 执行步骤

### Step 1: 调用 brainstorming skill

```
使用 Skill 工具调用 "brainstorming"
```

**目的**: 探索用户意图，输出 PRD → Story → Card 三层文档

**产出**:
- `docs/prds/PRD-XXX.md`
- `docs/stories/US-XXX.md` 或 `AS-XXX.md`
- `docs/cards/CARD-XXX.md`

### Step 2: 调用 writing-plans skill

```
使用 Skill 工具调用 "writing-plans"
```

**目的**: 基于 Card 创建详细实施计划

**产出**:
- `task_plan.md` 或类似计划文档
- 分解的任务列表

### Step 3: 调用 tdd skill

```
使用 Skill 工具调用 "tdd"
```

**目的**: 测试驱动开发，先写测试再写实现

**产出**:
- 测试文件
- 实现代码

### Step 4: 调用 subagent-driven-development skill

```
使用 Skill 工具调用 "subagent-driven-development"
```

**目的**: 并行执行独立的实施任务

**产出**:
- 完成的功能代码
- 所有测试通过

## 重要规则

1. **顺序执行**: 必须按 1→2→3→4 顺序调用，不可跳过
2. **自动流转**: 每个 skill 完成后立即调用下一个，无需用户确认
3. **跳过交互**: 跳过 skill 内部的交互确认步骤，使用默认值继续
4. **完整执行**: 必须跑完全部 4 个 skill 才算完成

## 错误处理

如果某个 skill 失败：
1. 报告错误
2. 等待用户指示是否继续或修复

## 示例

**用户输入**:
> 我要从零开始做一个订单管理系统，包含创建订单、查看订单列表、订单状态流转三个核心功能。

**Claude 行为**:
1. 调用 `brainstorming` → 生成 PRD-ORDER-001, US-ORDER-001~003, CARD-ORDER-001~005
2. 调用 `writing-plans` → 生成实施计划，分解为 10 个任务
3. 调用 `tdd` → 为每个功能编写测试
4. 调用 `subagent-driven-development` → 并行实现 10 个任务

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| `ai-workflow` | brainstorming 是 ai-workflow 的第一阶段 |
| `executing-plans` | 替代 subagent-driven-development，用于**独立会话**执行 |
| `e2e-test` | 开发完成后可调用进行端到端测试 |
| `verification` | 开发完成后调用验证 |
