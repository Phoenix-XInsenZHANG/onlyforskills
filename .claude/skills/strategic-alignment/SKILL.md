---
name: strategic-alignment
type: chain
description: |
  Phase 2 · 战略对齐（收敛评估） — 价值主张定义 → 功能优先级排序 → 竞品格局分析。

  当用户说"战略对齐"、"优先级排序"、"竞品分析"、"strategic alignment"时触发。

  节点序列: value-proposition → prioritize-features → competitor-analysis → ai-workflow[验证]
steps: value-proposition → prioritize-features → competitor-analysis → ai-workflow
---

# Phase 2 · Strategic Alignment（战略对齐）

收敛评估阶段，从发散创意中提炼价值主张，排列优先级，定位竞争格局。

## 触发条件

- 用户说"战略对齐"、"strategic alignment"
- 用户说"优先级排序"、"prioritize"
- 用户说"竞品分析"、"competitive analysis"
- 产品发现阶段（Phase 1）完成后的自然衔接

## 节点序列

```
┌──────────────────────┐
│ 1. VALUE-PROPOSITION │  基于 JTBD 定义六部分价值主张
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│2. PRIORITIZE-FEATURES│  RICE/ICE/Kano 等 9 种框架排列功能优先级
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│3. COMPETITOR-ANALYSIS│  竞品格局分析，发现差异化机会
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. AI-WORKFLOW [验证] │  验证战略产出落入 PRD/Story/Card 文档体系
└──────────────────────┘
```

## 各节点说明

### Step 1: value-proposition

```
Skill("value-proposition")
```

**目的**: 基于 JTBD 框架定义完整价值主张 — Who、Why、What before、How、What after、Alternatives。

**产出**:
- 六部分价值主张文档
- 目标用户画像与核心需求

### Step 2: prioritize-features

```
Skill("prioritize-features")
```

**目的**: 对候选功能做多维度优先级排序，支持 RICE、ICE、MoSCoW、Kano 等 9 种框架。

**产出**:
- 功能优先级排序表
- Top 5 推荐功能及理由
- 影响力/工作量/风险评估

### Step 3: competitor-analysis

```
Skill("competitor-analysis")
```

**目的**: 分析竞争格局 — 识别直接竞品、对比优劣势、发现差异化机会。

**产出**:
- 竞品分析矩阵
- 差异化定位建议
- 竞争优势/劣势清单

### Step 4: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 验证战略分析产出已反映到 PRD/Story/Card 三层文档 — 价值主张更新到 PRD、优先级排序落入 Story、竞品洞察记录到 Card。

**产出**:
- 文档更新确认
- 缺失关联已补全

## 测试验证层

| 验证点 | 工具 | 验证内容 |
|--------|------|---------|
| 功能 ROI 分析 | `prioritize-features` | 每个功能有 Impact/Effort/Risk 评分 |
| 竞品差异化 | `competitor-analysis` | 差异化定位有数据支撑 |
| 文档同步 | `ai-workflow` | 战略产出已反映到 PRD/Story/Card |

## Gate Checklist（出口质量关卡）

进入 Phase 3 前必须全部通过：

- [ ] 价值主张 6 部分完整（Who/Why/What before/How/What after/Alternatives）
- [ ] Top 5 功能已排序，每个有 Impact/Effort/Risk 评分
- [ ] 竞品分析覆盖至少 3 个直接竞品
- [ ] 差异化定位明确（vs 竞品的独特优势）
- [ ] 战略产出已通过 ai-workflow 同步到文档体系

## Timeline

**预估耗时: 2-3 个工作日**

```
Day 1              │ Day 2                │ Day 3
value-proposition  │ competitor-analysis  │ ai-workflow
prioritize-features│                      │ Gate Review
```

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4 顺序，不可跳过
2. **自动流转**: 每个节点完成后立即调用下一个
3. **输入依赖**: 建议在 Phase 1 (product-discovery) 之后执行，以获得充分的创意输入
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `product-discovery` | 本 chain 承接 Phase 1 的发散创意，做收敛 |
| `feature-spec-design` | 本 chain 产出进入 Phase 3 做功能规格设计 |
| `full-feature-lifecycle` | 如果已有明确需求，可跳过本 chain |
