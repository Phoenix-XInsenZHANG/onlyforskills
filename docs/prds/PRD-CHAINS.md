---
id: "PRD-CHAINS"
title: "Skills Chain 全量重写"
description: "统一 chain 规范，重写现有 2 条 chain，新增 3 条 chain，整合 gstack 节点"
status: "draft"
pattern: requirements-first
keyLearning: "Chain 是 skill 的编排层，gstack 节点是必经步骤而非可选扩展，统一 type:chain frontmatter 让 register 可自动分类"
project: foundation
stories:
  - US-CHAINS-001
  - US-CHAINS-002
  - US-CHAINS-003
cards:
  - CARD-CHAINS-001
  - CARD-CHAINS-002
  - CARD-CHAINS-003
  - CARD-CHAINS-004
  - CARD-CHAINS-005
  - CARD-CHAINS-006
verification:
  codeExists: false
  prdAccurate: unknown
  testsExist: false
  lastVerified: null
---

# PRD-CHAINS: Skills Chain 全量重写

## 背景

当前 .claude 体系有 2 条工作流 chain：`full-feature-lifecycle` 和 `bug-fix-to-ship`。
集成 gstack 后（共 78 个 skills），需要：
1. 统一 chain 格式规范
2. 将 gstack 关键节点（qa、codex、ship）嵌入现有链路
3. 补充缺失的场景链路（refactor、deploy、review-loop）

## 目标

- 5 条 chain 覆盖完整开发生命周期的所有主要场景
- gstack 节点为必经步骤，非可选
- 统一 `type: chain` frontmatter，register.md 自动分类 Chains 表
- general skill 路由从 Chains 表动态读取

## Chain 设计

### 标准格式（Chain Standard）

每条 chain SKILL.md 统一结构：

```
frontmatter:
  name, type: chain, description (含触发词 + 节点序列)

内容:
  # {Name}
  ## 触发条件
  ## 节点序列（ASCII 流程图）
  ## 各节点说明（目的 + 产出）
  ## 执行规则
  ## 与其他 chain 的关系表
```

### 5 条 Chain 节点序列

| Chain | 场景 | 节点序列 |
|-------|------|---------|
| `full-feature-lifecycle` | 新功能开发 | brainstorming → writing-plans → subagent-driven-development → qa[gstack] |
| `bug-fix-to-ship` | Bug 修复 | debugging → tdd → verification → codex[gstack] → requesting-code-review → finishing-branch |
| `refactor-to-ship` | 重构上线 | codex[gstack] → tdd → verification → requesting-code-review → finishing-branch |
| `deploy-pipeline` | 部署上线 | verification → requesting-code-review → ship[gstack] → qa[gstack] → finishing-branch |
| `code-review-loop` | 代码审查循环 | requesting-code-review → receiving-code-review → tdd → verification → requesting-code-review |

### gstack 节点说明

- `qa[gstack]` — 真实浏览器冒烟测试，验证核心路径可用
- `codex[gstack]` — 对抗性代码审查，识别安全漏洞、边界条件
- `ship[gstack]` — 自动化合并 + 版本号 + CHANGELOG 更新

## 成功标准

1. 5 条 chain SKILL.md 全部按标准格式重写/新建
2. register.md 包含独立 Chains 表（手动维护）
3. general skill Phase 2 toolchain 选项来自 register.md Chains 表
4. CLAUDE.md Skills Index 中 chains 独立分组展示
