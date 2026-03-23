---
id: "PRD-GSTACK"
title: "gstack 融合进 .claude 体系"
description: "将 Garry Tan 的 gstack 开源工具集以精选合并+内容提炼方式整合进现有 .claude skill 体系，引入浏览器 QA、安全模式、对抗审查等独有能力，同时将 gstack 的 Completeness Principle、Status Protocol、时间压缩框架注入现有 skills。"
status: "in-progress"
pattern: requirements-first
keyLearning: "gstack 最大价值不在替代现有 skills，而在于补充独有工具链（browse/qa/careful/freeze/codex）+ 将其思维框架（Boil the Lake、Status Protocol）提炼进全体系"
project: foundation
stories:
  - US-GSTACK-001
  - US-GSTACK-002
cards:
  - CARD-GSTACK-001
  - CARD-GSTACK-002
  - CARD-GSTACK-003
  - CARD-GSTACK-004
  - CARD-GSTACK-005
verification:
  codeExists: false
  prdAccurate: unknown
  testsExist: false
  lastVerified: null
---

# PRD-GSTACK: gstack 融合进 .claude 体系

## 背景

当前 .claude 体系拥有 61 个 skills，覆盖产品规划（PRD/Story/Card）、开发工作流、测试、代码审查等领域。

gstack 是 Garry Tan（YC CEO）开源的 21 个 slash command 集合，核心亮点：
- **独有工具**：headless 浏览器 (`/browse`)、真实浏览器 QA (`/qa`)、安全守卫模式 (`/careful`/`/freeze`/`/guard`)、对抗性审查 (`/codex`)、周报统计 (`/retro`)
- **优质思维框架**：Completeness Principle（Boil the Lake）、Completion Status Protocol、人力 vs AI 时间压缩表、标准化 AskUserQuestion 格式

## 目标

采用**精选合并 + 内容提炼**策略（方案 C）：

1. **结构引入**：将 gstack 独有的 11 个 skills 纳入 `.claude/skills/gstack/` 命名空间
2. **内容提炼**：将 gstack 的最佳框架注入现有 .claude skills，全体系受益

## 重叠 skill 路由规则

| 意图 | 路由 |
|---|---|
| brainstorm / 需求探索 | `.claude/brainstorming`（3 层文档更完整） |
| "YC 风格逼问" / office hours | `gstack/office-hours` |
| code review / PR 审查 | `.claude/code-review`（已注入 SQL/LLM 检查） |
| browse / QA / 点击测试 | `gstack/qa` or `gstack/browse` |
| production / 生产操作 | `gstack/careful` |
| ship / deploy / create PR | `gstack/ship` |

## 成功指标

- gstack 11 个独有 skills 在 register.md 中可被路由
- 5 个现有 .claude skills 注入了 gstack 的框架内容
- CLAUDE.md 中有清晰的 gstack 触发关键词映射
- `./setup` 构建完成，`/browse` 和 `/qa` 可运行
