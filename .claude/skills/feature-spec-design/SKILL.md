---
name: feature-spec-design
type: chain
description: |
  Phase 3 · 功能规格设计（核心产出） — CEO 审查 → 设计评审 → 设计系统 → 实施计划 → PRD → 指标仪表盘。

  当用户说"功能规格"、"写PRD"、"设计评审"、"feature spec"、"design review"时触发。

  节点序列: plan-ceo-review → plan-design-review → design-consultation → writing-plans → create-prd → ai-workflow[验证] → metrics-dashboard
steps: plan-ceo-review → plan-design-review → design-consultation → writing-plans → create-prd → ai-workflow → metrics-dashboard
---

# Phase 3 · Feature Spec Design（功能规格设计）

三个仓库协作最紧密的阶段 — 从战略审查到设计系统，从实施计划到完整 PRD。

## 触发条件

- 用户说"功能规格"、"feature spec"
- 用户说"写PRD"、"create PRD"
- 用户说"设计评审"、"design review"
- 战略对齐阶段（Phase 2）完成后的自然衔接

## 节点序列

```
┌──────────────────────┐
│ 1. PLAN-CEO-REVIEW   │  CEO 视角：挑战前提，扩展范围，找到 10 星产品
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│2. PLAN-DESIGN-REVIEW │  设计评审：多维度 0-10 分，明确改进方向
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│3. DESIGN-CONSULTATION│  从零构建完整设计系统（美学/排版/色彩/布局/动效）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. WRITING-PLANS     │  将设计转化为结构化实施计划（精确到文件路径）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. CREATE-PRD        │  生成完整 PRD（问题/目标/用户/方案/指标/范围/技术）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 6. AI-WORKFLOW [验证] │  验证 PRD/Story/Card 三层文档完整性
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 7. METRICS-DASHBOARD │  设计产品指标仪表盘（北极星/输入/健康/告警）
└──────────────────────┘
```

## 各节点说明

### Step 1: plan-ceo-review

```
Skill("plan-ceo-review")
```

**目的**: CEO/创始人模式的方案审查 — 重新思考问题，挑战前提假设，在保守和大胆之间找到最优产品形态。

**产出**:
- 方案审查报告
- 范围调整建议（扩展/收缩/精选扩展）

### Step 2: plan-design-review

```
Skill("plan-design-review")
```

**目的**: 设计师视角的多维度评审，对每个设计维度打 0-10 分，说明 10 分标准，然后修正方案。

**产出**:
- 多维度设计评分
- 具体改进方案

### Step 3: design-consultation

```
Skill("design-consultation")
```

**目的**: 从零构建完整设计系统 — 美学风格、排版方案、色彩系统、布局规则、间距规范、动效设计。

**产出**:
- `DESIGN.md` 设计系统文档
- 字体 + 色彩预览页面

### Step 4: writing-plans

```
Skill("writing-plans")
```

**目的**: 将设计方案转化为工程可执行的实施计划 — 精确到文件路径、逐步步骤和预期输出。

**产出**:
- 结构化实施计划文件

### Step 5: create-prd

```
Skill("create-prd")
```

**目的**: 生成包含 8 个核心章节的完整 PRD — 问题陈述、成功指标、用户故事、范围定义、技术考量。

**产出**:
- `docs/prds/PRD-XXX.md`

### Step 6: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 验证 create-prd 产出的 PRD 文档符合三层标准 — frontmatter 完整、Story/Card 关联正确、@card 引用就位。

**产出**:
- PRD 格式验证通过
- Story/Card 层级关联确认

### Step 7: metrics-dashboard

```
Skill("metrics-dashboard")
```

**目的**: 设计产品指标仪表盘 — 北极星指标、输入指标、健康指标、告警阈值。

**产出**:
- 指标仪表盘设计文档
- 数据源和可视化类型定义

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5→6→7 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **设计迭代**: Step 1-2 如果评分过低，可回到上一步迭代
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `strategic-alignment` | 本 chain 承接 Phase 2 的战略产出 |
| `engineering-review` | 本 chain 产出进入 Phase 4 做工程评审 |
| `full-feature-lifecycle` | 简化版：brainstorm → write-plan → dev → qa |
