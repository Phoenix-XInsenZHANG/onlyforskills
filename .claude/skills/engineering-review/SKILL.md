---
name: engineering-review
type: chain
description: |
  Phase 4 · 工程评审（技术落地） — 架构/数据流/边界评审 → 微任务拆解 → 用户故事卡。

  当用户说"工程评审"、"技术评审"、"eng review"、"architecture review"时触发。

  节点序列: plan-eng-review → writing-plans → user-stories → ai-workflow[验证]
steps: plan-eng-review → writing-plans → user-stories → ai-workflow
---

# Phase 4 · Engineering Review（工程评审）

技术落地阶段，锁定架构决策，将方案拆解到工程师可直接执行的粒度。

## 触发条件

- 用户说"工程评审"、"eng review"
- 用户说"技术评审"、"architecture review"
- 用户说"拆解任务"、"break down tasks"
- 功能规格设计阶段（Phase 3）完成后的自然衔接

## 节点序列

```
┌──────────────────────┐
│ 1. PLAN-ENG-REVIEW   │  锁定架构、数据流、边界条件、测试方案
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. WRITING-PLANS     │  拆解为 2-5 分钟微任务，精确到文件和函数
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. USER-STORIES      │  输出带验收标准的用户故事卡
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. AI-WORKFLOW [验证] │  验证 Story/Card 关联到 PRD，@card 引用就位
└──────────────────────┘
```

## 各节点说明

### Step 1: plan-eng-review

```
Skill("plan-eng-review")
```

**目的**: 工程经理模式的方案审查 — 锁定架构选型、数据流设计、边界条件处理、测试覆盖策略、性能预期。把隐藏的技术假设全部暴露出来。

**产出**:
- 架构审查报告
- 技术风险清单
- 建议修改项

### Step 2: writing-plans

```
Skill("writing-plans")
```

**目的**: 将架构决策转化为微粒度实施计划 — 每个任务 2-5 分钟，精确到文件路径和函数签名，足够清晰到一个「没有判断力的初级工程师」也能执行。

**产出**:
- 微任务清单（含文件路径、预期输出、验收标准）

### Step 3: user-stories

```
Skill("user-stories")
```

**目的**: 输出符合 3C 原则（Card/Conversation/Confirmation）和 INVEST 准则的用户故事，带完整验收标准。

**产出**:
- 用户故事列表
- 每个故事的验收标准
- 依赖关系说明

### Step 4: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 验证 user-stories 产出的故事卡已正确关联到 Card 层，@card 引用就位，验收标准完整。

**产出**:
- Story → Card 关联验证通过
- @card 引用确认

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **迭代允许**: Step 1 发现重大架构问题可回退到 Phase 3 修改设计
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `feature-spec-design` | 本 chain 承接 Phase 3 的规格产出 |
| `dev-execution` | 本 chain 产出进入 Phase 5 做开发执行 |
| `full-feature-lifecycle` | 简化版将 brainstorm + write-plan 合并 |
