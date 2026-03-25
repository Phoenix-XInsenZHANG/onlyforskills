---
name: release-retro
type: chain
description: |
  Phase 6 · 发布与复盘（闭环迭代） — 一键发布 → GTM 发布计划 → 北极星指标 → 团队复盘。

  当用户说"发布上线"、"release"、"上线复盘"、"ship and retro"时触发。

  节点序列: ship → ai-workflow[验证] → gtm-strategy → north-star-metric → retro
steps: ship → ai-workflow → gtm-strategy → north-star-metric → retro
---

# Phase 6 · Release & Retro（发布与复盘）

闭环迭代阶段，从发布到复盘，数据回流驱动下一轮迭代。

## 触发条件

- 用户说"发布上线"、"release"
- 用户说"上线复盘"、"ship and retro"
- 用户说"发版 + 复盘"
- 开发执行阶段（Phase 5）QA 通过后的自然衔接

## 节点序列

```
┌──────────────────────┐
│ 1. SHIP [gstack]     │  一键发布：合并 + 版本号 bump + CHANGELOG + PR
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. AI-WORKFLOW [验证] │  发布后更新文档状态（Card → done, PRD 版本标记）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. GTM-STRATEGY      │  制定 GTM 发布计划（渠道/消息/指标/时间线）
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. NORTH-STAR-METRIC │  定义北极星指标 + 3-5 个输入指标
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. RETRO             │  团队复盘：代码量/测试覆盖/贡献者/改进建议
└──────────────────────┘
          │
          ▼
    数据回流 Phase 1
```

## 各节点说明

### Step 1: ship [gstack] — 必经步骤

```
Skill("ship")
```

**目的**: 一键自动化发布 — 检测 + 合并 base branch、运行测试、bump VERSION、更新 CHANGELOG、commit、push、创建 PR。

**产出**:
- 版本号已 bump
- CHANGELOG 已更新
- PR 已创建或已合并

**不可跳过**: 手动合并绕过 ship 会导致版本号和 CHANGELOG 不一致。

### Step 2: ai-workflow [验证]

```
Skill("ai-workflow")
```

**目的**: 发布后更新三层文档状态 — Card 标记为 done、PRD 标注发布版本、Story 关联发布 commit。

**产出**:
- Card 状态更新
- PRD 版本标记
- 文档闭环确认

### Step 3: gtm-strategy

```
Skill("gtm-strategy")
```

**目的**: 制定 Go-to-Market 发布计划 — 营销渠道、核心消息、成功指标、发布时间线。

**产出**:
- GTM 发布策略文档
- 渠道 + 消息矩阵
- 发布时间线

### Step 4: north-star-metric

```
Skill("north-star-metric")
```

**目的**: 定义北极星指标和 3-5 个支撑输入指标，分类业务游戏（Attention/Transaction/Productivity），验证指标有效性。

**产出**:
- 北极星指标定义
- 输入指标星座图
- 指标验证（7 个有效性标准）

### Step 5: retro

```
Skill("retro")
```

**目的**: 自动生成团队复盘报告 — 分析 commit 历史、工作模式、代码质量指标，包含贡献者分析、改进建议。

**产出**:
- 复盘报告（代码量/测试覆盖/贡献者/趋势）
- 改进建议
- 数据回流到 Phase 1 驱动下一轮迭代

## 执行规则

1. **顺序执行**: 必须按 1→2→3→4→5 顺序，不可跳过
2. **ship 节点必经**: Step 1 不可跳过
3. **闭环**: Step 4 复盘数据应回流到下一轮 Phase 1 (product-discovery)
4. **错误处理**: 任一节点失败 → 报告错误，等待用户指示

## 与其他 Chain 的关系

| Chain | 关系 |
|-------|------|
| `dev-execution` | 本 chain 承接 Phase 5 的 QA 通过产出 |
| `product-discovery` | 本 chain 复盘数据回流到 Phase 1，形成闭环 |
| `deploy-pipeline` | 如果只需部署不需 GTM/复盘，用 deploy-pipeline |

## 完整生命周期闭环

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
  ↑                                                    │
  └────────────── retro 数据回流 ──────────────────────┘
```
