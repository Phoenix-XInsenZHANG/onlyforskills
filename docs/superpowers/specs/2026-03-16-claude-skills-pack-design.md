    # Claude Skills Pack 设计文档

> 日期：2026-03-16
> 状态：待审核
> 作者：Claude + 用户协作

---

## 1. 概述

### 1.1 目标

构建一个**可分发的 Claude Skills 技能包**，具有以下特点：

1. **完全自包含** — 所有 skills 都在 `.claude/skills/` 中，不依赖外部插件系统
2. **新人友好** — 提供交互式引导和智能路由器
3. **E2E 测试为重点** — 基于 E2E 最佳实践重写 `web-testing` skill
4. **可分发** — 可直接复制到任何项目分享给其他团队

### 1.2 设计决策

| 需求 | 决策 |
|------|------|
| Web-testing | 完全重写，基于 E2E 最佳实践（Playwright + Newman） |
| 新人引导 | 交互式 `/onboard` + 智能路由器 `router` |
| 插件整合 | 全部复制到 `.claude/skills/`，自包含 |
| 分发目标 | 可分发的技能包，分享给其他团队 |

---

## 2. 架构设计

### 2.1 分层技能架构

```
.claude/
├── skills/
│   │
│   ├── core/                          # 核心层（始终加载）
│   │   ├── router/SKILL.md            # 智能路由器
│   │   └── onboard/SKILL.md           # 新人引导
│   │
│   ├── workflow/                      # 开发工作流层
│   │   ├── brainstorming/             # 需求探索
│   │   ├── tdd/                       # 测试驱动开发
│   │   ├── debugging/                 # 系统化调试
│   │   ├── writing-plans/             # 编写实现计划
│   │   ├── executing-plans/           # 执行实现计划
│   │   ├── subagent-driven-development/  # 并行 agent
│   │   ├── using-git-worktrees/       # 并行开发分支
│   │   ├── finishing-a-development-branch/  # 完成分支
│   │   ├── requesting-code-review/    # 请求代码审查
│   │   ├── receiving-code-review/     # 处理审查反馈
│   │   ├── verification-before-completion/  # 完成前验证
│   │   ├── writing-skills/            # 编写新 skills
│   │   └── dispatching-parallel-agents/  # 分发并行 agent
│   │
│   ├── testing/                       # 测试层 ★ 重点升级
│   │   ├── web-testing/               # 新的 E2E skill
│   │   │   ├── SKILL.md               # 主文档
│   │   │   ├── references/
│   │   │   │   ├── playwright-best-practices.md
│   │   │   │   └── newman-best-practices.md
│   │   │   └── templates/
│   │   │       ├── playwright.config.ts
│   │   │       ├── base-page.ts
│   │   │       └── newman-collection.json
│   │   │
│   │   └── api-testing/               # Newman 简化版
│   │
│   ├── design/                        # 设计层
│   │   ├── frontend-design/           # 前端页面设计
│   │   └── ui-ux-system/              # 设计系统
│   │
│   ├── docs/                          # 文档层
│   │   ├── pdf/
│   │   ├── pptx/
│   │   ├── docx/
│   │   ├── xlsx/
│   │   ├── canvas-design/
│   │   ├── doc-coauthoring/
│   │   └── theme-factory/
│   │
│   ├── tools/                         # 工具层
│   │   ├── mcp-builder/               # 构建 MCP 服务器
│   │   ├── skill-creator/             # 创建新 skill
│   │   ├── claude-api/                # Claude API 开发
│   │   ├── planning-with-files/       # Manus 风格规划
│   │   ├── algorithmic-art/           # 算法艺术
│   │   └── web-artifacts-builder/     # Web artifacts
│   │
│   └── domain/                        # 领域层（可选）
│       ├── directus-schema/           # Directus schema
│       ├── d11-frontend/              # D11 前端
│       ├── rbac/                      # RBAC 权限
│       ├── backend-extension/         # 后端扩展
│       ├── migration/                 # 数据迁移
│       ├── ai-workflow/               # AI 工作流
│       ├── pm-comments/               # PM 评论同步
│       └── ...                        # 其他现有 skills
│
├── rules/                             # 保持现有
├── hooks/                             # 保持现有
├── settings.json
└── README.md                          # 分发包入口
```

### 2.2 层级说明

| 层级 | 用途 | 加载策略 |
|------|------|----------|
| `core/` | 路由 + 引导 | 始终加载 |
| `workflow/` | 开发流程 | 按需加载 |
| `testing/` | 测试相关 | 按需加载 |
| `design/` | 设计相关 | 按需加载 |
| `docs/` | 文档处理 | 按需加载 |
| `tools/` | 通用工具 | 按需加载 |
| `domain/` | 特定领域 | 可选/可删除 |

---

## 3. 核心 Skills 设计

### 3.1 Router Skill（智能路由器）

**文件**：`skills/core/router/SKILL.md`

**功能**：
- 分析用户意图，推荐或自动调用正确的 skill
- 维护技能索引表（从 `SKILL-CATALOG.md` 读取）
- 根据置信度决定：自动调用 / 推荐 / 列出候选

**路由逻辑**：

```
用户输入
    ↓
分析意图（关键词 + 上下文）
    ↓
匹配技能索引表
    ↓
┌─ 置信度 > 80% → 自动调用 skill
├─ 置信度 50-80% → 推荐并询问
└─ 置信度 < 50% → 返回候选列表
```

**触发条件**：
- 用户说"帮我..."但没指定具体 skill
- 用户描述问题但不知道有相关 skill
- 用户问"怎么..."、"如何..."

### 3.2 Onboard Skill（新人引导）

**文件**：`skills/core/onboard/SKILL.md`

**功能**：
- 检测项目类型（Next.js、Directus、React 等）
- 推荐相关的 skills
- 生成本项目的快速开始指南

**工作流程**：

```
/onboard
    ↓
Step 1: 检测项目环境
    ↓
Step 2: 识别项目类型
    ↓
Step 3: 推荐相关 skills
    ↓
Step 4: 生成快速开始指南
```

**触发条件**：
- 用户输入 `/onboard`
- 用户说"我是新手"、"怎么开始"、"帮助我了解"

---

## 4. Web-Testing Skill 设计（重点）

### 4.1 设计原则

基于 `E2E测试最佳实践-Playwright与Newman完整指南.md`：

1. **测试金字塔**：单元 ~70% | API ~20% | UI ~10%
2. **执行顺序**：API 测试先跑，UI 测试后跑
3. **定位器优先级**：`getByRole` → `getByLabel` → `getByText` → `getByTestId`
4. **消除 Flaky**：使用 web-first 断言，避免硬编码等待

### 4.2 文件结构

```
skills/testing/web-testing/
├── SKILL.md                          # 主文档
├── references/
│   ├── playwright-best-practices.md  # Playwright 最佳实践
│   ├── newman-best-practices.md      # Newman 最佳实践
│   └── ci-integration.md             # CI/CD 集成（可选）
└── templates/
    ├── playwright.config.ts          # Playwright 配置模板
    ├── base-page.ts                  # Page Object 基类
    ├── auth.setup.ts                 # 认证 setup 模板
    ├── fixtures.ts                   # Fixtures 模板
    └── newman-collection.json        # Newman collection 模板
```

### 4.3 SKILL.md 核心内容

```yaml
---
name: web-testing
description: |
  全栈 E2E 测试系统：Playwright (UI) + Newman (API)。
  遵循测试金字塔：API 测试先行，UI 测试关键路径。
  触发："run e2e", "playwright test", "api test", "newman", "e2e测试"
user-invocable: true
---
```

**主要章节**：
- 测试策略（金字塔原则）
- 执行顺序（API 先行）
- Playwright UI 测试
  - 项目结构
  - Page Object Model + Fixtures
  - 认证状态复用
  - 定位器优先级
  - 消除 Flaky 测试
  - 视觉回归测试
- Newman API 测试
  - Collection 组织
  - 变量管理
  - 脚本执行流程
  - JSON Schema 验证
- 诊断命令

---

## 5. Skills 整合清单

### 5.1 从 Superpowers 复制（14 个）

| Skill | 用途 |
|-------|------|
| `brainstorming` | 需求探索、设计 |
| `test-driven-development` | TDD 红-绿-重构 |
| `systematic-debugging` | 4 阶段调试 |
| `writing-plans` | 编写实现计划 |
| `executing-plans` | 执行实现计划 |
| `subagent-driven-development` | 并行 agent 开发 |
| `dispatching-parallel-agents` | 分发并行 agent |
| `using-git-worktrees` | 并行开发分支 |
| `finishing-a-development-branch` | 完成开发分支 |
| `requesting-code-review` | 请求代码审查 |
| `receiving-code-review` | 处理审查反馈 |
| `verification-before-completion` | 完成前验证 |
| `writing-skills` | 编写新 skills |
| `using-superpowers` | 技能系统介绍 |

### 5.2 从 Example-skills 复制（17 个）

| Skill | 用途 |
|-------|------|
| `frontend-design` | 前端页面设计 |
| `mcp-builder` | 构建 MCP 服务器 |
| `webapp-testing` | 原有测试（合并到 web-testing） |
| `pdf` | PDF 文档处理 |
| `pptx` | PPT 演示文稿 |
| `docx` | Word 文档 |
| `xlsx` | Excel 表格 |
| `skill-creator` | 创建新 skill |
| `algorithmic-art` | 算法艺术 |
| `brand-guidelines` | 品牌指南 |
| `canvas-design` | 视觉设计 |
| `claude-api` | Claude API 开发 |
| `doc-coauthoring` | 文档协作 |
| `internal-comms` | 内部沟通 |
| `slack-gif-creator` | Slack GIF |
| `theme-factory` | 主题样式 |
| `web-artifacts-builder` | Web artifacts |

### 5.3 从 UI-UX-Pro-Max 复制（1 个）

| Skill | 内容 |
|-------|------|
| `ui-ux-system` | 设计系统（161 调色板、57 字体、99 UX 指南） |

### 5.4 从 Planning-with-files 复制（1 个）

| Skill | 用途 |
|-------|------|
| `planning-with-files` | Manus 风格文件规划 |

### 5.5 保留现有 Domain Skills（6+ 个）

- `directus-schema`
- `d11-frontend`
- `rbac`
- `backend-extension`
- `migration`
- `ai-workflow`
- `pm-comments`
- `progress`
- `visualizer`
- `landing-page`
- `landing-audit`
- `agent-teams`
- `team-health`
- `meta-evaluation`
- `context-review`
- `business-prd-planner`
- `business-report`
- `user-journey-mapper`

---

## 6. 分发包设计

### 6.1 README.md 结构

```markdown
# 🚀 Claude Skills Pack

## 快速开始
## 技能概览
## 文件结构
## 自定义
## 来源
## License
```

### 6.2 SKILL-CATALOG.md

作为技能索引表，供 Router 读取：

```markdown
# Skills Catalog

## Core
| Skill | 触发词 | 用途 |
|-------|--------|------|

## Workflow
...

## Testing
...

## Design
...

## Docs
...

## Tools
...

## Domain
...
```

---

## 7. 实现计划概要

### Phase 1：核心架构
1. 创建分层目录结构
2. 实现 Router skill
3. 实现 Onboard skill
4. 创建 SKILL-CATALOG.md

### Phase 2：Web-Testing 重写
1. 编写 web-testing/SKILL.md
2. 创建 references 文件
3. 创建 templates 文件

### Phase 3：Skills 整合
1. 从 Superpowers 复制 14 个 skills
2. 从 Example-skills 复制 17 个 skills
3. 从 UI-UX-Pro-Max 复制 1 个 skill
4. 从 Planning-with-files 复制 1 个 skill
5. 迁移现有 domain skills

### Phase 4：分发包
1. 编写 README.md
2. 测试安装流程
3. 清理不必要的文件

---

## 8. 预期成果

| 项目 | 数量 |
|------|------|
| 总 Skills 数 | 35+ |
| 核心层 | 2 |
| 工作流层 | 14 |
| 测试层 | 2 |
| 设计层 | 2 |
| 文档层 | 7 |
| 工具层 | 6 |
| 领域层 | 6+ |

---

## 附录

### A. 来源项目

- [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent
- [Example-skills](https://github.com/anthropics/anthropic-cookbook) by Anthropic
- [UI-UX-Pro-Max](https://github.com/...)
- [Planning-with-files](https://github.com/...)

### B. 参考文档

- `E2E测试最佳实践-Playwright与Newman完整指南.md`
