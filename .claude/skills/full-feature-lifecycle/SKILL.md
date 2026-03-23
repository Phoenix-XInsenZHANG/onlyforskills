---
name: full-feature-lifecycle
type: chain
description: |
  完整功能开发生命周期 — 从需求到代码的端到端工作流。

  当用户说"从零开始"、"完整功能"、"新功能开发"、"端到端实现"时触发。

  节点序列: brainstorming → writing-plans → subagent-driven-development → qa[gstack]
steps: brainstorming → writing-plans → subagent-driven-development → qa
---

# Full Feature Lifecycle

端到端功能开发工作流，确保从需求到代码、从代码到验证的完整链路。

## 触发条件

- 用户说"从零开始做..."
- 用户说"完整功能开发"
- 用户说"端到端实现"
- 用户描述新业务需求，没有现有 PRD/Card

## 节点序列

```
┌─────────────────┐
│  1. BRAINSTORM  │  需求探索，输出 PRD/Story/Card
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. WRITING-PLANS│  创建详细实施计划（含精确步骤和文件路径）
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. SUBAGENT-DEV │  并行执行独立任务（内置 TDD + 两阶段审查）
└────────┬────────┘
         ▼
┌─────────────────┐
│  4. QA [gstack] │  真实浏览器冒烟测试 — 必经步骤
└─────────────────┘
```

## 各节点说明

### Step 1: brainstorming

```
Skill("brainstorming")
```

**目的**: 探索用户意图，输出 PRD → Story → Card 三层文档

**产出**:
- `docs/prds/PRD-XXX.md`
- `docs/stories/US-XXX.md`
- `docs/cards/CARD-XXX.md`

### Step 2: writing-plans

```
Skill("writing-plans")
```

**目的**: 基于 Card 创建详细实施计划，含精确文件路径、逐步步骤和预期输出

**产出**:
- `docs/superpowers/plans/YYYY-MM-DD-feature.md`

### Step 3: subagent-driven-development

```
Skill("subagent-driven-development")
```

**目的**: Fresh subagent per task + 两阶段审查（spec compliance → code quality）

**产出**:
- 完成的功能代码，所有测试通过，每个 task 有 commit

**注意**: subagent-driven-development 内置 TDD 要求。不需要额外调用 tdd skill。

### Step 4: qa [gstack] — 必经步骤

```
Skill("qa")
```

**目的**: 真实浏览器冒烟测试，验证核心用户路径在真实环境中可用

**产出**:
- QA 测试报告，核心路径通过

**不可跳过**: 即使 Step 3 所有单元测试通过，qa 仍然必须执行。单元测试无法替代真实浏览器验证。

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **错误处理**: 任一节点失败 → 报告错误，等待用户指示
4. **gstack 节点必经**: Step 4 不可标记为"可选"

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `bug-fix-to-ship` | 修 bug 用那个，新功能用这个 |
| `deploy-pipeline` | 本 chain 的 qa 节点通过后可衔接 deploy-pipeline 上线 |
| `refactor-to-ship` | 重构现有功能用那个，开发全新功能用这个 |
| `code-review-loop` | subagent-dev 内置了两阶段审查，通常不需要额外调用 |
