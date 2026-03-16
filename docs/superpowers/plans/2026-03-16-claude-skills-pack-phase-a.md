# Claude Skills Pack - Phase A: 核心层实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建核心层 skills（Router + Onboard + Catalog），为整个技能包提供智能路由和新人引导功能。

**Architecture:** 分层技能架构的核心层，包含 2 个 skill（router、onboard）和 1 个索引文件（SKILL-CATALOG.md）。Router 负责分析用户意图并推荐正确的 skill，Onboard 负责检测项目类型并推荐相关工作流。

**Tech Stack:** Markdown skills, Claude Code skill system

**Spec:** `docs/superpowers/specs/2026-03-16-claude-skills-pack-design.md`

---

## Chunk 1: 目录结构

### Task 1: 创建核心层目录结构

**Files:**
- Create: `.claude/skills/core/router/` (directory)
- Create: `.claude/skills/core/onboard/` (directory)
- Create: `.claude/skills/workflow/` (directory)
- Create: `.claude/skills/testing/` (directory)
- Create: `.claude/skills/design/` (directory)
- Create: `.claude/skills/docs/` (directory)
- Create: `.claude/skills/tools/` (directory)

- [ ] **Step 1: 创建分层目录结构**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills/.claude/skills

# 创建新的分层目录
mkdir -p core/router
mkdir -p core/onboard
mkdir -p workflow
mkdir -p testing/web-testing/references
mkdir -p testing/web-testing/templates
mkdir -p design
mkdir -p docs
mkdir -p tools
```

Run: `ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/`
Expected: 看到 core/, workflow/, testing/, design/, docs/, tools/ 目录

- [ ] **Step 2: 验证目录结构正确**

```bash
tree -L 2 /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/
```

Expected: 显示分层目录结构

---

## Chunk 2: Router Skill

### Task 2: 创建 Router Skill

**Files:**
- Create: `.claude/skills/core/router/SKILL.md`

- [ ] **Step 1: 创建 Router SKILL.md**

```yaml
---
name: router
description: |
  智能技能路由器。分析用户意图，推荐或自动调用正确的 skill。
  当用户不确定用什么 skill，或问题模糊时自动触发。
  触发词：/router, "用什么skill", "帮我", "怎么", "如何"
user-invocable: true
---

# 技能路由器

智能分析你的需求，推荐或自动调用正确的 skill。

## 何时触发

- 用户说"帮我..."但没指定具体 skill
- 用户描述问题但不知道有相关 skill
- 用户问"怎么..."、"如何..."
- 用户输入 `/router`

## 路由逻辑

```
用户输入
    ↓
分析意图（关键词 + 上下文）
    ↓
匹配技能索引表（读取 SKILL-CATALOG.md）
    ↓
┌─ 置信度 > 80% → 自动调用 skill
├─ 置信度 50-80% → 推荐并询问
└─ 置信度 < 50% → 返回候选列表
```

## 技能索引表

路由器读取 `../SKILL-CATALOG.md` 获取所有可用 skills。

### 意图匹配规则

| 意图关键词 | 推荐 Skill | 置信度 |
|-----------|-----------|--------|
| 创建功能、新特性、构建、开发 | brainstorming | 高 |
| 修复 bug、报错、失败、错误 | debugging | 高 |
| 测试、E2E、playwright、newman | web-testing | 高 |
| 写文档、PDF、PPT、Word | pdf / pptx / docx | 中 |
| 设计页面、UI、样式、组件 | frontend-design | 中 |
| 代码审查、PR、review | code-review | 中 |
| Directus、schema、迁移 | directus-schema / migration | 高 |
| 角色权限、RBAC | rbac | 高 |
| 规划、计划、任务分解 | writing-plans | 中 |
| TDD、测试驱动 | tdd | 高 |

## 输出示例

### 高置信度（自动调用）

```
🔍 检测到测试需求，正在调用 web-testing skill...
```

### 中置信度（推荐）

```
💡 你似乎想要创建新功能。推荐使用：

   1. /brainstorming — 先探索需求
   2. /writing-plans — 直接写实现计划

输入数字选择，或描述更多细节。
```

### 低置信度（列表）

```
📚 可用的 Skills：

【核心】
  /router    — 智能路由（当前）
  /onboard   — 新人引导

【工作流】
  /brainstorming    — 探索需求，设计功能
  /tdd              — 测试驱动开发
  /debugging        — 系统化调试
  /writing-plans    — 编写实现计划

【测试】
  /web-testing      — E2E + API 测试

【设计】
  /frontend-design  — 前端页面设计

输入 skill 名称或描述你的需求...
```

## 与 Onboard 的区别

| Router | Onboard |
|--------|---------|
| 分析具体任务意图 | 检测项目环境 |
| 推荐"做什么" | 推荐"用什么工具" |
| 随时触发 | 首次使用时触发 |

## 相关 Skills

- **onboard** — 新人引导，检测项目类型
- **SKILL-CATALOG.md** — 完整技能索引
```

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/router/SKILL.md | head -20`
Expected: 显示 SKILL.md 开头内容

- [ ] **Step 2: 验证 Router skill 可被识别**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/router/
```

Expected: 看到 SKILL.md 文件

---

## Chunk 3: Onboard Skill

### Task 3: 创建 Onboard Skill

**Files:**
- Create: `.claude/skills/core/onboard/SKILL.md`

- [ ] **Step 1: 创建 Onboard SKILL.md**

```yaml
---
name: onboard
description: |
  新人引导系统。检测项目类型，推荐相关 skills 和工作流程。
  触发：/onboard, "我是新手", "怎么开始", "帮助我了解"
user-invocable: true
---

# 新人引导

检测你的项目环境，推荐相关 skills 和工作流程。

## 触发方式

- 用户输入 `/onboard`
- 用户说"我是新手"、"怎么开始"、"帮助我了解"

## 工作流程

```
/onboard
    ↓
Step 1: 检测项目环境
    ↓
Step 2: 识别项目类型
    ↓
Step 3: 推荐相关 Skills
    ↓
Step 4: 生成快速开始指南
```

## Step 1: 检测项目环境

自动检测以下特征：

| 文件/目录 | 检测结果 |
|-----------|----------|
| `package.json` | Node.js 项目 |
| `next.config.js` / `next.config.mjs` | Next.js 项目 |
| `directus/` / `directus.config.js` | Directus 项目 |
| `playwright.config.ts` | 已有 E2E 测试 |
| `*.postman_collection.json` | 已有 API 测试 |
| `tailwind.config.js` | Tailwind CSS |
| `app/` 目录结构 | Next.js App Router |
| `pages/` 目录结构 | Next.js Pages Router |
| `lib/d11/` | Directus 11 集成 |

## Step 2: 识别项目类型

输出示例：

```
🔍 项目检测完成

┌─────────────────────────────────────┐
│  项目类型: Next.js + Directus 全栈  │
│  测试状态: Playwright ✓  Newman ✗   │
│  样式方案: Tailwind CSS              │
│  架构: App Router                    │
└─────────────────────────────────────┘
```

## Step 3: 推荐相关 Skills

基于项目类型推荐：

```
📦 为你的项目推荐的 Skills：

【必装 - 开发流程】
  ✅ /brainstorming   — 开始任何新功能前
  ✅ /tdd             — 测试驱动开发
  ✅ /debugging       — 遇到 bug 时

【必装 - 测试】
  ✅ /web-testing     — E2E + API 测试（Playwright + Newman）

【推荐 - Directus 项目】
  ⭐ /directus-schema — Schema 参考
  ⭐ /migration       — 数据库迁移
  ⭐ /rbac            — 权限管理
  ⭐ /d11-frontend    — D11 前端集成

【可选 - 设计】
  🔹 /frontend-design — 前端页面
  🔹 /ui-ux-system    — 设计系统

输入 skill 名称了解详情，或输入 'all' 查看全部可用 skills。
```

## Step 4: 生成快速开始指南

```markdown
## 快速开始

### 1. 创建新功能
/onboard → 选择"创建功能" → /brainstorming

### 2. 修复 Bug
/debugging

### 3. 运行测试
/web-testing

### 4. 查看所有可用 Skills
/router

### 5. 继续开发
直接描述你想做什么，系统会自动推荐正确的 skill。
```

## 交互式问答模式

如果检测不确定，进入问答：

```
🤔 我检测到这可能是 Next.js 项目，但不确定。

请确认或选择：
1. ✅ 是的，是 Next.js 项目
2. 🔧 是 React 但不是 Next.js
3. 📦 是其他类型（请描述）

你的选择：_
```

## 项目类型与 Skills 映射

| 项目类型 | 推荐 Skills |
|----------|-------------|
| Next.js 全栈 | brainstorming, tdd, debugging, web-testing |
| Next.js + Directus | + directus-schema, migration, rbac, d11-frontend |
| React SPA | brainstorming, tdd, debugging, frontend-design |
| 纯后端 API | brainstorming, tdd, debugging, api-testing |
| 静态网站 | frontend-design, canvas-design |

## 与 Router 的区别

| Onboard | Router |
|---------|--------|
| 检测项目环境 | 分析具体任务意图 |
| 推荐"用什么工具" | 推荐"做什么" |
| 首次使用时触发 | 随时触发 |

## 相关 Skills

- **router** — 智能路由，分析任务意图
- **SKILL-CATALOG.md** — 完整技能索引
```

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/onboard/SKILL.md | head -20`
Expected: 显示 SKILL.md 开头内容

- [ ] **Step 2: 验证 Onboard skill 可被识别**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/onboard/
```

Expected: 看到 SKILL.md 文件

---

## Chunk 4: SKILL-CATALOG.md

### Task 4: 创建技能索引表

**Files:**
- Create: `.claude/skills/SKILL-CATALOG.md`

- [ ] **Step 1: 创建 SKILL-CATALOG.md**

```markdown
# Skills Catalog

技能索引表，供 Router 和 Onboard 读取。

---

## 核心层 (Core)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `router` | /router, 用什么skill, 帮我 | 智能路由，分析意图推荐 skill |
| `onboard` | /onboard, 新手, 怎么开始 | 新人引导，检测项目推荐工作流 |

---

## 工作流层 (Workflow)

### 需求与设计

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `brainstorming` | /brainstorm, 创建功能, 新特性 | 需求探索，设计方案 |
| `writing-plans` | /plan, 规划, 计划 | 编写实现计划 |

### 开发流程

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `tdd` | /tdd, 测试驱动 | 测试驱动开发（RED-GREEN-REFACTOR） |
| `debugging` | /debug, bug, 报错, 失败 | 系统化调试（4 阶段） |
| `executing-plans` | /execute, 执行计划 | 执行实现计划 |

### 代码审查

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `code-review` | /review, PR, 代码审查 | 代码审查 |
| `requesting-code-review` | 请求审查 | 请求代码审查 |
| `receiving-code-review` | 处理反馈 | 处理审查反馈 |

### Git 与分支

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `git-worktrees` | /worktree, 并行开发 | 使用 git worktrees |
| `finishing-branch` | 完成分支, merge, PR | 完成开发分支 |

### Agent 相关

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `subagent-driven` | 并行 agent | 并行 agent 开发 |
| `dispatching-agents` | 分发 agent | 分发并行 agents |

### 其他

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `verification` | 验证, 确认 | 完成前验证 |
| `writing-skills` | 创建 skill | 编写新 skills |

---

## 测试层 (Testing)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `web-testing` | /e2e, playwright, newman, 测试 | E2E + API 测试（Playwright + Newman） |
| `api-testing` | /api-test, newman | Newman/Postman API 测试 |

---

## 设计层 (Design)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `frontend-design` | /design, UI, 页面设计 | 前端页面设计 |
| `ui-ux-system` | 调色板, 字体, UX | 设计系统（161 调色板、57 字体） |

---

## 文档层 (Docs)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `pdf` | /pdf, PDF | PDF 文档处理 |
| `pptx` | /ppt, PPT, 演示文稿 | PPT 演示文稿 |
| `docx` | /doc, Word, 文档 | Word 文档 |
| `xlsx` | /xlsx, Excel, 表格 | Excel 表格 |
| `canvas-design` | 设计, 海报 | 视觉设计 |
| `doc-coauthoring` | 协作文档 | 文档协作 |
| `theme-factory` | 主题, 样式 | 主题样式 |

---

## 工具层 (Tools)

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `mcp-builder` | /mcp, MCP 服务器 | 构建 MCP 服务器 |
| `skill-creator` | /create-skill | 创建新 skill |
| `claude-api` | Claude API, SDK | Claude API 开发 |
| `planning-with-files` | /planning, Manus | Manus 风格文件规划 |
| `algorithmic-art` | 算法艺术, p5.js | 算法艺术 |
| `web-artifacts` | artifacts | Web artifacts 构建 |

---

## 领域层 (Domain)

> 这些 skills 是项目特定的，分发给其他团队时可以移除。

### Directus 相关

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `directus-schema` | /schema, seed, 数据库 | Directus schema 参考 |
| `d11-frontend` | /d11, D11 前端 | D11 前端集成 |
| `rbac` | /rbac, 权限, 角色 | RBAC 权限管理 |
| `backend-extension` | /extension, 后端扩展 | 后端扩展开发 |
| `migration` | /migration, 迁移 | 数据迁移 |

### 项目管理

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `ai-workflow` | /workflow | AI 开发工作流 |
| `pm-comments` | /synque, sync | PM 评论同步 |
| `progress` | /progress | 进度跟踪 |
| `visualizer` | /visualize | 数据可视化 |

### 其他

| Skill | 触发词 | 用途 |
|-------|--------|------|
| `landing-page` | /landing | Landing page 管理 |
| `landing-audit` | /audit | Landing page 审计 |
| `agent-teams` | /teams | Agent 团队编排 |
| `team-health` | /health | 团队健康检查 |
| `business-prd` | /prd | PRD 规划 |
| `user-journey` | /journey | 用户旅程地图 |

---

## 快速查找

### 按任务类型

| 我想... | 使用 Skill |
|---------|-----------|
| 创建新功能 | brainstorming → writing-plans → tdd |
| 修复 bug | debugging |
| 写测试 | web-testing 或 tdd |
| 设计页面 | frontend-design |
| 写文档 | pdf / pptx / docx |
| 代码审查 | code-review |
| 了解项目 | onboard |
| 找正确的 skill | router |

### 按项目类型

| 项目类型 | 推荐 Skills |
|----------|-------------|
| 全栈 Web | brainstorming, tdd, debugging, web-testing, frontend-design |
| 后端 API | brainstorming, tdd, debugging, api-testing |
| Directus | + directus-schema, migration, rbac, d11-frontend |
| 前端 SPA | brainstorming, tdd, debugging, frontend-design, ui-ux-system |
```

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/SKILL-CATALOG.md | head -30`
Expected: 显示 SKILL-CATALOG.md 开头内容

- [ ] **Step 2: 验证 SKILL-CATALOG.md 创建成功**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/SKILL-CATALOG.md
```

Expected: 文件存在

---

## Chunk 5: 更新 README.md

### Task 5: 更新 skills/README.md

**Files:**
- Modify: `.claude/skills/README.md`

- [ ] **Step 1: 读取现有 README.md**

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/README.md | head -50`

- [ ] **Step 2: 在 README.md 顶部添加核心层说明**

在现有的 `## Available Skills` 之前添加：

```markdown
## 核心系统

**[core/router](core/router/SKILL.md)** - 智能技能路由器
- **Purpose**: 分析用户意图，推荐或自动调用正确的 skill
- **Auto-invokes**: 当用户不确定用什么 skill 时
- **Handles**: 意图分析、技能推荐、自动调用

**[core/onboard](core/onboard/SKILL.md)** - 新人引导系统
- **Purpose**: 检测项目类型，推荐相关 skills 和工作流程
- **Triggers**: `/onboard`, "我是新手", "怎么开始"
- **Handles**: 项目检测、技能推荐、快速开始指南

## 技能索引

完整的技能索引请查看 [SKILL-CATALOG.md](SKILL-CATALOG.md)

---
```

- [ ] **Step 3: 验证 README.md 更新**

Run: `cat /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/README.md | head -30`
Expected: 看到新增的核心系统说明

---

## Chunk 6: 验证与提交

### Task 6: 验证核心层完整性

- [ ] **Step 1: 验证目录结构**

```bash
tree /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/
```

Expected:
```
core/
├── router/
│   └── SKILL.md
└── onboard/
    └── SKILL.md
```

- [ ] **Step 2: 验证所有文件存在**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/
```

Expected: 看到 SKILL-CATALOG.md 和 core/ 目录

- [ ] **Step 3: 提交 Phase A 完成**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/core/
git add .claude/skills/SKILL-CATALOG.md
git add .claude/skills/README.md
git commit -m "feat(skills): add core layer - router + onboard + catalog

- Add router skill for intelligent skill routing
- Add onboard skill for new user onboarding
- Add SKILL-CATALOG.md as skill index
- Update README.md with core layer docs

Phase A of Claude Skills Pack implementation."
```

---

## 完成检查

- [ ] Router skill 可以被 `/router` 触发
- [ ] Onboard skill 可以被 `/onboard` 触发
- [ ] SKILL-CATALOG.md 包含完整的技能索引
- [ ] README.md 已更新核心层说明
- [ ] Git 提交完成

---

## 下一步

Phase A 完成后，继续执行：
- **Phase B**: Web-Testing Skill（E2E 测试重写）
- **Phase C**: Skills 整合（从插件复制）
- **Phase D**: 分发包（README + 清理）
