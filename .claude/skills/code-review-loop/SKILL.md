---
name: code-review-loop
type: chain
description: |
  代码审查循环 — 从请求审查到审查通过的完整迭代流程。

  当用户说"代码审查循环"、"review loop"、"审查有反馈需要处理"时触发。

  节点序列: requesting-code-review → receiving-code-review → tdd → verification → requesting-code-review (循环，最多 3 轮)
steps: requesting-code-review → receiving-code-review → tdd → verification
---

# Code Review Loop

代码审查的完整循环工作流，确保每轮反馈都经过 TDD 修复和验证，直到审查通过。

## 触发条件

- 用户说"代码审查循环"、"review loop"
- 用户说"审查有反馈，帮我处理"
- 需要多轮审查迭代的场景

## 节点序列（循环结构）

```
┌─────────────────────┐
│1. REQUESTING-REVIEW │  发起代码审查请求
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│2. RECEIVING-REVIEW  │  接收并分析审查反馈
└──────────┬──────────┘
           ▼
      有反馈? ──── 无 ────▶ 审查通过，结束
           │
           ▼ 是
┌─────────────────────┐
│       3. TDD        │  TDD 方式修复审查反馈
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  4. VERIFICATION    │  验证修复，所有测试通过
└──────────┬──────────┘
           ▼
      轮次 < 3? ──── 否 ──▶ BLOCKED，人工介入
           │
           ▼ 是
   返回 Step 1（下一轮）
```

## 各节点说明

### Step 1: requesting-code-review

```
Skill("requesting-code-review")
```

**目的**: 发起或重新发起代码审查。每轮循环都重新请求，附上本轮修改说明。

**产出**:
- 审查请求（PR comment / review request）

### Step 2: receiving-code-review

```
Skill("receiving-code-review")
```

**目的**: 接收审查反馈，分类处理：must-fix / suggested / nitpick

**产出**:
- 反馈分类清单
- 若无 must-fix 反馈 → 审查通过，循环结束

**循环终止条件**: receiving-code-review 返回"无 must-fix 反馈"时，循环结束，chain 完成。

### Step 3: tdd（仅当有反馈时执行）

```
Skill("tdd")
```

**目的**: 用 TDD 方式修复 must-fix 反馈。先写失败测试，再修复，再验绿。

**产出**:
- 修复代码（针对每条 must-fix）
- 对应测试通过

### Step 4: verification（仅当有反馈时执行）

```
Skill("verification")
```

**目的**: 验证本轮修复后，所有测试仍然通过，无回归。

**产出**:
- 所有测试通过证据

## 执行规则

1. **最多 3 轮**: 超过 3 轮未通过 → STATUS: BLOCKED，等待人工介入
2. **循环终止**: receiving-code-review 报告无 must-fix 反馈 → 立即结束
3. **每轮独立 commit**: 每次 Step 3+4 完成后提交，保持修复历史可追溯
4. **BLOCKED 格式**:
   ```
   STATUS: BLOCKED
   REASON: 代码审查第 3 轮仍有未解决反馈
   ATTEMPTED: [3 轮修复记录]
   RECOMMENDATION: 人工介入，重新讨论设计方案
   ```

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `bug-fix-to-ship` | bug 修复后的审查反馈处理用这个 |
| `refactor-to-ship` | 重构审查有多轮反馈时衔接这个 |
| `deploy-pipeline` | 审查通过后衔接 deploy-pipeline 上线 |
