# Skills Chain 全量重写 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 统一 chain 格式规范，重写现有 2 条 chain（full-feature-lifecycle、bug-fix-to-ship），新增 3 条 chain（refactor-to-ship、deploy-pipeline、code-review-loop），将 gstack 节点嵌入为必经步骤，更新 register.md 和 CLAUDE.md。

**Architecture:** 每条 chain 是独立的 SKILL.md 文件，统一 `type: chain` frontmatter。Chain 之间无代码依赖，Tasks 1-5 可按任意顺序执行。Task 6 最后执行（依赖前 5 个 chain 已写好）。

**Tech Stack:** Markdown, YAML frontmatter, bash (grep 验证)

---

## Chunk 1: 重写现有两条 Chain

### Task 1: 重写 full-feature-lifecycle (CARD-CHAINS-001)

**Files:**
- Modify: `.claude/skills/full-feature-lifecycle/SKILL.md`

- [ ] **Step 1: 确认现有文件**

```bash
cat .claude/skills/full-feature-lifecycle/SKILL.md
```

Expected: 看到旧的 4 节点流程（含独立 tdd 节点）

- [ ] **Step 2: 写入新版 SKILL.md**

完整替换文件内容如下：

```markdown
---
name: full-feature-lifecycle
type: chain
description: |
  完整功能开发生命周期 — 从需求到代码的端到端工作流。

  当用户说"从零开始"、"完整功能"、"新功能开发"、"端到端实现"时触发。

  节点序列: brainstorming → writing-plans → subagent-driven-development → qa[gstack]
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
│ 2. WRITING-PLANS│  创建详细实施计划（含 TDD 步骤）
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

**目的**: 基于 Card 创建详细实施计划，含逐步 TDD 步骤和精确文件路径

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
```

- [ ] **Step 3: 验证 frontmatter 字段**

```bash
grep 'type: chain' .claude/skills/full-feature-lifecycle/SKILL.md
grep 'qa\[gstack\]' .claude/skills/full-feature-lifecycle/SKILL.md
grep '节点序列' .claude/skills/full-feature-lifecycle/SKILL.md
```

Expected: 每条 grep 都返回一行匹配

- [ ] **Step 4: 验证节点序列完整**

```bash
grep -E 'brainstorming|writing-plans|subagent-driven-development|qa' .claude/skills/full-feature-lifecycle/SKILL.md | head -10
```

Expected: 看到 4 个节点名称

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/full-feature-lifecycle/SKILL.md
git commit -m "feat: rewrite full-feature-lifecycle chain with type:chain + qa[gstack] node

@card CARD-CHAINS-001
- Add type:chain frontmatter
- Replace tdd node with qa[gstack] mandatory final step
- subagent-driven-development already requires TDD internally

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 2: 重写 bug-fix-to-ship (CARD-CHAINS-002)

**Files:**
- Modify: `.claude/skills/bug-fix-to-ship/SKILL.md`

- [ ] **Step 1: 确认现有文件**

```bash
cat .claude/skills/bug-fix-to-ship/SKILL.md
```

Expected: 看到旧的 5 节点流程（无 codex 节点）

- [ ] **Step 2: 写入新版 SKILL.md**

完整替换文件内容如下：

```markdown
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

**不可跳过**: codex 独立于 verification，专注安全边界，不替代人工审查。

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
```

- [ ] **Step 3: 验证 frontmatter 和 codex 节点**

```bash
grep 'type: chain' .claude/skills/bug-fix-to-ship/SKILL.md
grep 'codex\[gstack\]' .claude/skills/bug-fix-to-ship/SKILL.md
grep -c '###.*Step' .claude/skills/bug-fix-to-ship/SKILL.md
```

Expected: 前两条各返回一行；第三条返回 6（6 个节点）

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/bug-fix-to-ship/SKILL.md
git commit -m "feat: rewrite bug-fix-to-ship chain with type:chain + codex[gstack] node

@card CARD-CHAINS-002
- Add type:chain frontmatter
- Insert codex[gstack] as mandatory Step 4 (adversarial review before human review)
- Adjust step numbering (old 4→5, old 5→6)
- Add cross-chain relationship table

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Chunk 2: 新建三条 Chain

### Task 3: 新建 refactor-to-ship (CARD-CHAINS-003)

**Files:**
- Create: `.claude/skills/refactor-to-ship/SKILL.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p .claude/skills/refactor-to-ship
```

- [ ] **Step 2: 写入 SKILL.md**

```markdown
---
name: refactor-to-ship
type: chain
description: |
  重构到上线工作流 — 从对抗性审查到代码合并的端到端流程。

  当用户说"重构"、"技术债清理"、"refactor"、"代码优化"时触发。

  节点序列: codex[gstack] → tdd → verification → requesting-code-review → finishing-branch
---

# Refactor to Ship

重构代码的端到端工作流，确保重构前方向正确、重构后行为不变、经过完整审查后上线。

## 触发条件

- 用户说"重构"、"重写这段代码"
- 用户说"技术债清理"、"clean up"
- 用户说"代码优化"、"refactor"
- 用户识别出耦合过重、文件过大、职责不清的代码

## 节点序列

```
┌─────────────────┐
│1. CODEX [gstack]│  重构前审查，确认方向正确 — 必经步骤
└────────┬────────┘
         ▼
┌─────────────────┐
│     2. TDD      │  先写测试固定当前行为，再重构
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. VERIFICATION │  验证行为未变，所有测试仍然通过
└────────┬────────┘
         ▼
┌─────────────────┐
│4. CODE-REVIEW   │  请求代码审查
└────────┬────────┘
         ▼
┌─────────────────┐
│5. FINISH-BRANCH │  合并/部署
└─────────────────┘
```

## 各节点说明

### Step 1: codex [gstack] — 必经步骤

```
Skill("codex")
```

**目的**: 重构前对抗性审查。确认重构方向正确，识别高风险区域，避免重构到一半发现根本思路有问题。

**产出**:
- codex 审查报告（重构方向 pass/fail）
- 风险清单（若有）

**为什么先 codex**: 重构是高风险操作，开始前的独立审查可防止方向性错误，节省大量返工时间。

### Step 2: tdd

```
Skill("tdd")
```

**目的**: 在重构前先写测试固定当前行为。测试通过后开始重构，测试是重构的安全网。

**产出**:
- 覆盖当前行为的测试套件
- 重构后的代码（测试仍然通过）

**关键原则**: 重构 = 改变代码结构，不改变外部行为。测试证明行为未变。

### Step 3: verification

```
Skill("verification")
```

**目的**: 验证重构后所有测试仍然通过，无回归。

**产出**:
- 所有测试通过的证据（命令输出）
- 无新增警告/错误

### Step 4: requesting-code-review

```
Skill("requesting-code-review")
```

**目的**: 请求代码审查，说明重构动机、范围、codex 审查结论

**产出**:
- PR 或审查请求

### Step 5: finishing-branch

```
Skill("finishing-branch")
```

**目的**: 完成分支，合并到主分支

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5 顺序，不可跳过
2. **codex 节点必经**: 重构前审查不可省略
3. **测试先行**: Step 2 中必须先写测试再重构，不可跳过红绿验证
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `bug-fix-to-ship` | 修 bug 用那个，重构改善代码质量用这个 |
| `full-feature-lifecycle` | 开发新功能用那个，优化现有代码用这个 |
| `code-review-loop` | 若审查有多轮反馈，衔接 code-review-loop |
```

- [ ] **Step 3: 验证文件创建**

```bash
grep 'type: chain' .claude/skills/refactor-to-ship/SKILL.md
grep 'codex\[gstack\]' .claude/skills/refactor-to-ship/SKILL.md
grep -c '###.*Step' .claude/skills/refactor-to-ship/SKILL.md
```

Expected: 前两条各一行匹配；第三条返回 5（5 个节点）

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/refactor-to-ship/SKILL.md
git commit -m "feat: add refactor-to-ship chain

@card CARD-CHAINS-003
- New chain: codex[gstack] → tdd → verification → code-review → finish
- codex first: validates refactor direction before implementation
- tdd: tests lock current behavior before refactoring begins

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 4: 新建 deploy-pipeline (CARD-CHAINS-004)

**Files:**
- Create: `.claude/skills/deploy-pipeline/SKILL.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p .claude/skills/deploy-pipeline
```

- [ ] **Step 2: 写入 SKILL.md**

```markdown
---
name: deploy-pipeline
type: chain
description: |
  部署上线流水线 — 从最终验证到生产环境的端到端流程。

  当用户说"部署"、"上线"、"deploy"、"发版"、"发布"时触发。

  节点序列: verification → requesting-code-review → ship[gstack] → qa[gstack] → finishing-branch
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
```

- [ ] **Step 3: 验证文件**

```bash
grep 'type: chain' .claude/skills/deploy-pipeline/SKILL.md
grep 'ship\[gstack\]' .claude/skills/deploy-pipeline/SKILL.md
grep 'qa\[gstack\]' .claude/skills/deploy-pipeline/SKILL.md
grep -c '###.*Step' .claude/skills/deploy-pipeline/SKILL.md
```

Expected: 前三条各一行匹配；第四条返回 5

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/deploy-pipeline/SKILL.md
git commit -m "feat: add deploy-pipeline chain

@card CARD-CHAINS-004
- New chain: verification → code-review → ship[gstack] → qa[gstack] → finish
- ship[gstack]: automated merge + version bump + CHANGELOG
- qa[gstack]: post-deploy browser smoke test (mandatory)

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

### Task 5: 新建 code-review-loop (CARD-CHAINS-005)

**Files:**
- Create: `.claude/skills/code-review-loop/SKILL.md`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p .claude/skills/code-review-loop
```

- [ ] **Step 2: 写入 SKILL.md**

```markdown
---
name: code-review-loop
type: chain
description: |
  代码审查循环 — 从请求审查到审查通过的完整迭代流程。

  当用户说"代码审查循环"、"review loop"、"审查有反馈需要处理"时触发。

  节点序列: requesting-code-review → receiving-code-review → tdd → verification → requesting-code-review (循环，最多 3 轮)
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
```

- [ ] **Step 3: 验证文件**

```bash
grep 'type: chain' .claude/skills/code-review-loop/SKILL.md
grep 'BLOCKED' .claude/skills/code-review-loop/SKILL.md
grep -c '###.*Step' .claude/skills/code-review-loop/SKILL.md
```

Expected: 前两条各一行匹配；第三条返回 4（4 个节点）

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/code-review-loop/SKILL.md
git commit -m "feat: add code-review-loop chain

@card CARD-CHAINS-005
- New chain: requesting-review → receiving-review → tdd → verification → loop
- Max 3 rounds, BLOCKED status if exceeded
- Termination: receiving-review reports no must-fix feedback

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Chunk 3: 更新 Registry 和文档

### Task 6: 更新 register.md 和 CLAUDE.md (CARD-CHAINS-006)

**Files:**
- Modify: `.claude/skills/general/references/register.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: 确认所有 5 条 chain 文件存在**

```bash
ls .claude/skills/full-feature-lifecycle/SKILL.md \
   .claude/skills/bug-fix-to-ship/SKILL.md \
   .claude/skills/refactor-to-ship/SKILL.md \
   .claude/skills/deploy-pipeline/SKILL.md \
   .claude/skills/code-review-loop/SKILL.md
```

Expected: 5 行，无 "No such file"

- [ ] **Step 2: 在 register.md 末尾追加 Chains 表**

在文件末尾（`## Individual Skills` 表之后）添加：

```markdown

---

## Chains

> 手动维护。每条 chain 是端到端工作流，由多个 skill 按顺序组合而成。

| ID | Name | Nodes | Trigger Keywords |
|----|------|-------|-----------------|
| C01 | `full-feature-lifecycle` | brainstorming → writing-plans → subagent-driven-development → qa[gstack] | 从零开始, 新功能, 完整功能, 端到端实现 |
| C02 | `bug-fix-to-ship` | debugging → tdd → verification → codex[gstack] → requesting-code-review → finishing-branch | 修复bug, 线上故障, hotfix, 紧急修复 |
| C03 | `refactor-to-ship` | codex[gstack] → tdd → verification → requesting-code-review → finishing-branch | 重构, 技术债, refactor, 代码优化 |
| C04 | `deploy-pipeline` | verification → requesting-code-review → ship[gstack] → qa[gstack] → finishing-branch | 部署, 上线, deploy, 发版, 发布 |
| C05 | `code-review-loop` | requesting-code-review → receiving-code-review → tdd → verification → loop | 代码审查循环, review loop, 审查反馈 |
```

- [ ] **Step 3: 验证 register.md 更新**

```bash
grep -A 10 '## Chains' .claude/skills/general/references/register.md
```

Expected: 看到 Chains 表格，含 5 行数据（C01~C05）

- [ ] **Step 4: 在 CLAUDE.md Skills Index 中新增 Chains 分组**

在 CLAUDE.md 的 `## Skills Index` 表格之后，找到表格结束位置，新增：

```markdown

### Chains（工作流链路）

> 每条 chain 按顺序自动调用多个 skill，覆盖完整开发场景。

| 触发场景 | Chain | 节点序列 |
|---------|-------|---------|
| 新功能开发 | `full-feature-lifecycle` | brainstorming→writing-plans→subagent-dev→qa |
| Bug 修复 | `bug-fix-to-ship` | debugging→tdd→verification→codex→review→finish |
| 重构上线 | `refactor-to-ship` | codex→tdd→verification→review→finish |
| 部署上线 | `deploy-pipeline` | verification→review→ship→qa→finish |
| 审查循环 | `code-review-loop` | request-review→receive-review→tdd→verify→loop |
```

- [ ] **Step 5: 验证 CLAUDE.md 更新**

```bash
grep -A 8 'Chains（工作流链路）' CLAUDE.md
```

Expected: 看到 5 行 chain 数据

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/general/references/register.md CLAUDE.md
git commit -m "docs: add Chains table to register.md and CLAUDE.md

@card CARD-CHAINS-006
- register.md: new ## Chains section with C01-C05
- CLAUDE.md: new Chains group in Skills Index

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## 最终验证

- [ ] **验证所有 chain 有 type:chain frontmatter**

```bash
for f in full-feature-lifecycle bug-fix-to-ship refactor-to-ship deploy-pipeline code-review-loop; do
  echo -n "$f: "
  grep 'type: chain' .claude/skills/$f/SKILL.md && echo "✅" || echo "❌ MISSING"
done
```

Expected: 5 行全部 ✅

- [ ] **验证 gstack 节点分布**

```bash
echo "=== qa[gstack] ==="
grep -l 'qa\[gstack\]' .claude/skills/*/SKILL.md
echo "=== codex[gstack] ==="
grep -l 'codex\[gstack\]' .claude/skills/*/SKILL.md
echo "=== ship[gstack] ==="
grep -l 'ship\[gstack\]' .claude/skills/*/SKILL.md
```

Expected:
- qa[gstack]: full-feature-lifecycle, deploy-pipeline
- codex[gstack]: bug-fix-to-ship, refactor-to-ship
- ship[gstack]: deploy-pipeline

- [ ] **验证 register.md 行数合理**

```bash
wc -l .claude/skills/general/references/register.md
```

Expected: < 300 行（当前约 200 行 + 新增 ~20 行）

- [ ] **验证 git log**

```bash
git log --oneline -8
```

Expected: 看到 6 条新 commit（Tasks 1-6）
