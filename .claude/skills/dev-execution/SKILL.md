---
name: dev-execution
type: chain
description: |
  Phase 5 · 开发执行（质量保障） — 子代理并行开发(TDD) → 结构化代码审查 → 真实浏览器 QA。

  当用户说"开始开发"、"执行计划"、"start coding"、"execute plan"时触发。

  节点序列: ai-workflow[验证] → executing-plans → review → qa
steps: ai-workflow → executing-plans → review → qa
---

# Phase 5 · Dev Execution（开发执行）

质量保障阶段，通过子代理并行开发、结构化审查和真实浏览器测试确保交付质量。

## 触发条件

- 用户说"开始开发"、"start coding"
- 用户说"执行计划"、"execute plan"
- 用户说"开始写代码"
- 工程评审阶段（Phase 4）完成后的自然衔接

## 节点序列

```
┌──────────────────────┐
│ 1. AI-WORKFLOW [验证] │  开发前确认 Card 存在，PRD/Story/Card 齐全
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. EXECUTING-PLANS   │  子代理驱动开发，严格 TDD 红-绿-重构循环
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. REVIEW            │  结构化代码审查（SQL 安全/LLM 信任边界/条件副作用）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. QA [gstack]       │  真实浏览器端到端 QA 测试 — 必经步骤
└──────────────────────┘
```

## 各节点说明

### Step 1: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 开发前确认 CARD-XXX 存在且关联到 PRD/Story，确保每行代码都有可追溯的文档基础。遵循 Rule 0（PAUSE BEFORE CODE）。

**产出**:
- Card 存在确认
- PRD → Story → Card 层级完整

**不可跳过**: 没有 Card 的代码 = 无法追溯的代码。

### Step 2: executing-plans

```
Skill("executing-plans")
```

**目的**: 启动子代理驱动的开发流程 — 每个独立任务分配 fresh subagent，严格遵循 TDD 红-绿-重构循环，内置两阶段审查（spec compliance + code quality）。

**产出**:
- 功能代码实现
- 所有测试通过
- 每个 task 有独立 commit

**注意**: executing-plans 内置 TDD 和审查，不需要额外调用 tdd skill。

### Step 3: review

```
Skill("review")
```

**目的**: Pre-landing 结构化代码审查 — 检查 SQL 安全、LLM 信任边界违规、条件副作用等结构性问题。

**产出**:
- 代码审查报告
- 问题清单（按严重程度排序）
- 通过/不通过判定

**修复流程**: 如果审查不通过 → 修复问题 → 重新执行 Step 2

### Step 4: qa [gstack] — 必经步骤

```
Skill("qa")
```

**目的**: 真实浏览器端到端 QA 测试 — 实际登录、导航页面、填写表单、截图验证核心用户路径。

**产出**:
- QA 测试报告
- 核心路径通过确认
- 截图证据

**不可跳过**: 即使 Step 1 所有单元测试通过，qa 仍然必须执行。单元测试无法替代真实浏览器验证。

## 测试验证层

| 验证点 | 工具 | 验证内容 |
|--------|------|---------|
| 浏览器 E2E 测试 | `qa` [gstack] | 真实浏览器核心用户路径验证 |
| 单元测试覆盖 | `executing-plans` (内置 TDD) | 红-绿-重构循环，每个 task 有测试 |
| 代码结构审查 | `review` | SQL 安全、LLM 信任边界、条件副作用 |
| 文档追溯性 | `ai-workflow` | 每行代码有 @card 引用 |

## Gate Checklist（出口质量关卡）

进入 Phase 6 前必须全部通过：

- [ ] Card 存在且关联到 PRD/Story（ai-workflow 验证通过）
- [ ] 所有单元测试通过（TDD 红-绿-重构完成）
- [ ] 代码审查通过（无 Critical/High 级别问题）
- [ ] 真实浏览器 QA 测试通过（核心路径 + 截图证据）
- [ ] 每个 commit 有 @card 引用
- [ ] 无安全漏洞（SQL 注入、XSS、信任边界）

## Timeline

**预估耗时: 3-7 个工作日**（视复杂度）

```
Day 1          │ Day 2-5           │ Day 6-7
ai-workflow    │ executing-plans   │ qa [gstack]
               │ (TDD per task)    │ Gate Review
               │ review            │
```

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4 顺序，不可跳过
2. **审查迭代**: Step 3 不通过 → 修复 → 重新审查（最多 3 轮）
3. **gstack 节点必经**: Step 4 不可标记为"可选"
4. **QA 失败处理**: 若 QA 发现 bug → 修复 → 从 Step 3 重新开始
5. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `engineering-review` | 本 chain 承接 Phase 4 的任务拆解 |
| `release-retro` | 本 chain QA 通过后进入 Phase 6 发布 |
| `full-feature-lifecycle` | 简化版：subagent-dev → qa |
| `code-review-loop` | 如果需要更多轮审查迭代，可切换到 code-review-loop |
