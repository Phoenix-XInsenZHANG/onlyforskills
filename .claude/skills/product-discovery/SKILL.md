---
name: product-discovery
type: chain
description: |
  Phase 1 · 产品发现（发散创意） — CEO 视角审视 → 苏格拉底式追问 → 多角色发散 → 风险假设 → 验证实验。

  当用户说"产品发现"、"discovery"、"探索需求"、"新想法"、"validate idea"时触发。

  节点序列: office-hours → brainstorming → ai-workflow[验证] → brainstorm-ideas-existing → identify-assumptions-existing → brainstorm-experiments-existing
steps: office-hours → brainstorming → ai-workflow → brainstorm-ideas-existing → identify-assumptions-existing → brainstorm-experiments-existing
---

# Phase 1 · Product Discovery（产品发现）

发散创意阶段，从 CEO 视角审视到多角色发散，最终输出可验证的实验方案。

## 触发条件

- 用户说"产品发现"、"discovery"
- 用户说"探索需求"、"新想法"
- 用户说"validate idea"、"验证想法"
- 用户有一个模糊的产品方向，需要系统化探索

## 节点序列

```
┌──────────────────────┐
│ 1. OFFICE-HOURS      │  CEO 视角：六个关键问题重新审视产品假设
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. BRAINSTORMING     │  苏格拉底式追问，打磨需求，输出 PRD/Story/Card
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. AI-WORKFLOW [验证] │  验证 PRD/Story/Card 三层文档符合标准
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. BRAINSTORM-IDEAS  │  PM / 设计师 / 工程师三视角发散创意
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. IDENTIFY-ASSUMPT. │  识别 Value/Usability/Viability/Feasibility 风险假设
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 6. BRAINSTORM-EXPER. │  设计低成本验证实验（A/B test、原型、spike）
└──────────────────────┘
```

## 各节点说明

### Step 1: office-hours

```
Skill("office-hours")
```

**目的**: 以 CEO/创始人视角，通过六个强迫性问题（需求真实性、现状替代方案、极致具体性、最窄楔子、观察洞察、未来适配）重新审视产品方向。

**产出**:
- 对产品假设的深度质疑
- 明确的方向判断：值得做 / 需要调整 / 放弃

### Step 2: brainstorming

```
Skill("brainstorming")
```

**目的**: 苏格拉底式追问，在用户想清楚之前不急于动手。输出三层文档。

**产出**:
- `docs/prds/PRD-XXX.md`
- `docs/stories/US-XXX.md`
- `docs/cards/CARD-XXX.md`

### Step 3: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 验证 Step 2 brainstorming 产出的 PRD/Story/Card 三层文档符合 ai-workflow 规范 — frontmatter 完整、层级关联正确、@card 引用就位。

**产出**:
- 文档格式验证通过
- 缺失字段已补全

**不可跳过**: 确保后续阶段有可追溯的文档基础。

### Step 4: brainstorm-ideas-existing

```
Skill("brainstorm-ideas-existing")
```

**目的**: 从 PM、设计师、工程师三个视角发散功能创意，拓宽解决方案空间。

**产出**:
- 多视角功能创意列表
- 每个创意的可行性初步评估

**注意**: 如果是全新产品（无现有用户），改用 `brainstorm-ideas-new`。

### Step 5: identify-assumptions-existing

```
Skill("identify-assumptions-existing")
```

**目的**: 对功能创意进行魔鬼代言人式的假设识别，覆盖 Value、Usability、Viability、Feasibility 四维度。

**产出**:
- 分类的风险假设清单
- 每个假设的风险等级

**注意**: 如果是全新产品，改用 `identify-assumptions-new`（覆盖 8 个风险类别含 GTM 和团队）。

### Step 6: brainstorm-experiments-existing

```
Skill("brainstorm-experiments-existing")
```

**目的**: 为高风险假设设计低成本验证实验 — 原型、A/B test、spike 等。

**产出**:
- 每个高风险假设对应的验证实验方案
- 实验优先级排序

**注意**: 如果是全新产品，改用 `brainstorm-experiments-new`（侧重 pretotype 和 MVP 实验）。

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5→6 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **新产品变体**: 如果是全新产品，Step 3/4/5 自动替换为 `-new` 后缀版本
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `strategic-alignment` | 本 chain 产出进入 Phase 2 做收敛评估 |
| `full-feature-lifecycle` | 如果不需要深度发现，可直接走 full-feature-lifecycle |
| `feature-spec-design` | 发现阶段结束后，跳过战略对齐直接进入规格设计 |
