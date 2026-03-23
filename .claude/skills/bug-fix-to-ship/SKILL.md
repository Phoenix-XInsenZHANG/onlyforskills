---
name: bug-fix-to-ship
type: chain
description: |
  Bug 修复到上线完整流程 — 从问题诊断到代码合并的端到端工作流。

  当用户说"修复bug"、"生产环境问题"、"线上故障"、"紧急修复"时触发。

  节点序列: debugging → tdd → verification → codex[gstack] → requesting-code-review → finishing-branch
---

# Bug Fix to Ship

从 Bug 报告到生产环境修复的完整工作流，确保修复质量可追溯、可验证、经过对抗性审查。

## 触发条件

- 用户说"修复bug"、"修一下这个bug"
- 用户说"生产环境有问题"、"线上故障"
- 用户说"紧急修复"、"hotfix"
- 用户报告错误信息、异常行为

## 节点序列

```
┌─────────────────┐
│  1. DEBUGGING   │  分析根因，定位问题
└────────┬────────┘
         ▼
┌─────────────────┐
│     2. TDD      │  先写失败测试，再写修复
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. VERIFICATION │  验证修复有效，所有测试通过
└────────┬────────┘
         ▼
┌─────────────────┐
│4. CODEX [gstack]│  对抗性审查，识别安全漏洞 — 必经步骤
└────────┬────────┘
         ▼
┌─────────────────┐
│5. CODE-REVIEW   │  请求人工代码审查
└────────┬────────┘
         ▼
┌─────────────────┐
│6. FINISH-BRANCH │  合并/PR/部署
└─────────────────┘
```

## 各节点说明

### Step 1: debugging

```
Skill("debugging")
```

**目的**: 系统性分析 Bug 根因（四阶段：根因调查→模式分析→假设测试→实施）

**产出**:
- 根因分析报告
- 问题定位（文件、行号、函数）
- 复现步骤

### Step 2: tdd

```
Skill("tdd")
```

**目的**: 先写复现 bug 的失败测试，再写修复代码

**产出**:
- 失败的测试用例（精确复现 bug）
- 修复代码
- 测试通过（红→绿已验证）

### Step 3: verification

```
Skill("verification")
```

**目的**: 验证修复有效，确保没有引入新问题

**产出**:
- 所有测试通过（含新写的回归测试）
- 验证命令输出证据

### Step 4: codex [gstack] — 必经步骤

```
Skill("codex")
```

**目的**: 对抗性代码审查，在人工审查前发现 AI 可能遗漏的安全漏洞、边界条件、并发问题

**产出**:
- codex 审查报告（pass/fail）
- 若 fail：需修复后重新运行 Step 3 → Step 4

**不可跳过**: codex 独立于 verification，专注安全边界，不替代人工审查。AI 修复容易引入新的安全盲点，codex 是第二层防线。

### Step 5: requesting-code-review

```
Skill("requesting-code-review")
```

**目的**: 请求人工代码审查，附上根因分析和 codex 审查通过证明

**产出**:
- PR 或审查请求
- 审查反馈（若有反馈，调用 receiving-code-review 处理）

### Step 6: finishing-branch

```
Skill("finishing-branch")
```

**目的**: 完成分支工作，合并到主分支

**产出**:
- 合并/PR/部署决策完成

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5→6 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **codex 节点必经**: Step 4 不可跳过，即使你对修复很有把握
4. **证据优先**: Step 3 必须有测试通过的输出截图/日志
5. **错误处理**: 任一节点失败 → 报告错误详情，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `full-feature-lifecycle` | 新功能开发用那个，bug 修复用这个 |
| `refactor-to-ship` | 重构技术债用那个，修 bug 用这个 |
| `code-review-loop` | 若 Step 5 审查有反馈，衔接 code-review-loop |
| `receiving-code-review` | 审查有具体反馈时调用这个单独 skill |
