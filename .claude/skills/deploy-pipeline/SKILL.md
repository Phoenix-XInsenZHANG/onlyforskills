---
name: deploy-pipeline
type: chain
description: |
  部署上线流水线 — 从最终验证到生产环境的端到端流程。

  当用户说"部署"、"上线"、"deploy"、"发版"、"发布"时触发。

  节点序列: verification → requesting-code-review → ship[gstack] → qa[gstack] → finishing-branch
steps: verification → requesting-code-review → ship → qa → finishing-branch
---

# Deploy Pipeline

从准备上线到生产验证的完整部署工作流，确保每次发布经过验证、审查、自动化打包和上线后冒烟测试。

## 触发条件

- 用户说"部署"、"上线"
- 用户说"deploy"、"发版"、"发布"
- 功能开发完成，准备合并到主分支

## 节点序列

```
┌─────────────────┐
│ 1. VERIFICATION │  确认测试全部通过，构建成功
└────────┬────────┘
         ▼
┌─────────────────┐
│2. CODE-REVIEW   │  最终代码审查
└────────┬────────┘
         ▼
┌─────────────────┐
│3. SHIP [gstack] │  自动合并 + 版本号 bump + CHANGELOG — 必经步骤
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. QA [gstack]  │  上线后真实浏览器冒烟测试 — 必经步骤
└────────┬────────┘
         ▼
┌─────────────────┐
│5. FINISH-BRANCH │  清理分支
└─────────────────┘
```

## 各节点说明

### Step 1: verification

```
Skill("verification")
```

**目的**: 上线前最终确认 — 所有测试通过，构建成功，无遗留警告

**产出**:
- 测试通过证据
- 构建成功证据（exit 0）

### Step 2: requesting-code-review

```
Skill("requesting-code-review")
```

**目的**: 最终人工代码审查。若已有审查通过记录，确认无新增改动即可。

**产出**:
- 审查通过确认

### Step 3: ship [gstack] — 必经步骤

```
Skill("ship")
```

**目的**: 自动化发布流程 — 合并 base branch、运行测试、bump VERSION、更新 CHANGELOG、创建 PR

**产出**:
- 版本号已 bump
- CHANGELOG 已更新
- PR 已创建

**不可跳过**: 手动合并绕过 ship 会导致版本号和 CHANGELOG 不一致。

### Step 4: qa [gstack] — 必经步骤

```
Skill("qa")
```

**目的**: 上线后真实浏览器冒烟测试，验证核心用户路径在生产环境中可用

**产出**:
- QA 测试报告
- 核心路径通过确认

**时机**: 在 ship 之后执行，测试的是合并后的生产/staging 环境。

### Step 5: finishing-branch

```
Skill("finishing-branch")
```

**目的**: 清理功能分支，关闭相关 issues

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5 顺序，不可跳过
2. **ship 和 qa 节点必经**: 两个 gstack 节点都不可跳过
3. **qa 失败处理**: 若 qa 发现问题 → hotfix → 重走 deploy-pipeline（从 Step 1 开始）
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `full-feature-lifecycle` | 功能开发完成后，可衔接本 chain 上线 |
| `bug-fix-to-ship` | bug 修复完成后，可衔接本 chain 上线 |
| `refactor-to-ship` | 重构完成后，可衔接本 chain 上线 |
