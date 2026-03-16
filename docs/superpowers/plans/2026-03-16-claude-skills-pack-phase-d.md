# Claude Skills Pack - Phase D: 分发包实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建可分发的技能包，包含完整的 README、安装说明和清理不必要的文件。

**Architecture:** 单一入口 README.md + 分层目录结构，用户只需复制 `.claude/` 目录即可使用。

**Tech Stack:** Markdown 文档，目录结构

**Spec:** `docs/superpowers/specs/2026-03-16-claude-skills-pack-design.md`

---

## Chunk 1: 主 README.md

### Task 1: 创建分发包入口 README

**Files:**
- Create: `.claude/README.md`

- [ ] **Step 1: 创建 README.md**

```markdown
# 🚀 Claude Skills Pack

一套完整的 AI 辅助开发技能包，可直接复制到任何项目使用。

## 特点

- ✅ **完全自包含** — 无需安装任何插件
- ✅ **智能路由** — 自动推荐正确的 skill
- ✅ **新人友好** — `/onboard` 一键引导
- ✅ **E2E 测试** — Playwright + Newman 最佳实践
- ✅ **可分发** — 复制即可分享给团队

## 快速开始

### 安装

```bash
# 复制到你的项目
cp -r .claude/ /path/to/your/project/.claude/
```

### 首次使用

在 Claude Code 中输入：

```
/onboard
```

系统会检测你的项目类型并推荐相关工作流。

## 技能概览

### 🧭 核心系统

| Skill | 说明 |
|-------|------|
| `/router` | 智能路由 — 告诉你该用什么 skill |
| `/onboard` | 新人引导 — 检测项目，推荐工作流 |

### 🔄 开发工作流

| Skill | 说明 |
|-------|------|
| `/brainstorming` | 需求探索 → 设计方案 |
| `/tdd` | 测试驱动开发（RED-GREEN-REFACTOR） |
| `/debugging` | 系统化调试（4 阶段） |
| `/writing-plans` | 编写实现计划 |
| `/executing-plans` | 执行实现计划 |
| `/git-worktrees` | 并行开发分支 |
| `/finishing-branch` | 完成分支（merge/PR） |
| `/code-review` | 代码审查 |
| `/verification` | 完成前验证 |

### 🧪 测试

| Skill | 说明 |
|-------|------|
| `/web-testing` | **E2E + API 测试**（Playwright + Newman） |
| `/api-testing` | Newman/Postman API 测试 |

### 🎨 设计

| Skill | 说明 |
|-------|------|
| `/frontend-design` | 前端页面设计 |
| `/ui-ux-system` | 设计系统（161 调色板、57 字体） |

### 📄 文档

| Skill | 说明 |
|-------|------|
| `/pdf` | PDF 处理 |
| `/pptx` | PPT 演示文稿 |
| `/docx` | Word 文档 |
| `/xlsx` | Excel 表格 |
| `/canvas-design` | 视觉设计 |
| `/theme-factory` | 主题样式 |

### 🔧 工具

| Skill | 说明 |
|-------|------|
| `/mcp-builder` | 构建 MCP 服务器 |
| `/skill-creator` | 创建新 skill |
| `/planning` | 文件规划（Manus 风格） |
| `/claude-api` | Claude API 开发 |

## 文件结构

```
.claude/
├── skills/           # 所有技能
│   ├── core/         # 路由器 + 引导
│   ├── workflow/     # 开发工作流（14 个）
│   ├── testing/      # 测试相关（2 个）
│   ├── design/       # 设计系统（2 个）
│   ├── docs/         # 文档处理（7 个）
│   ├── tools/        # 通用工具（6 个）
│   └── domain/       # 领域特定（可删除）
├── rules/            # 项目规则
├── hooks/            # 钩子脚本
├── settings.json     # 配置
├── SKILL-CATALOG.md  # 技能索引
└── README.md         # 本文件
```

## 自定义

### 移除不需要的 Skills

```bash
# 不需要领域特定的 skills？
rm -rf .claude/skills/domain/

# 不需要文档处理？
rm -rf .claude/skills/docs/

# 只保留核心？
rm -rf .claude/skills/domain/
rm -rf .claude/skills/docs/
rm -rf .claude/skills/tools/
```

### 添加项目特定规则

编辑 `.claude/rules/` 中的文件，或创建新规则：

```bash
# 创建项目特定规则
echo "# 项目特定规则" > .claude/rules/project.md
```

### 添加项目特定 Skills

```bash
# 创建新 skill
mkdir -p .claude/skills/domain/my-skill
echo "---\nname: my-skill\ndescription: 我的自定义 skill\n---" > .claude/skills/domain/my-skill/SKILL.md
```

## 常见工作流

### 创建新功能

```
1. /brainstorming     — 探索需求
2. /writing-plans     — 写实现计划
3. /tdd               — 测试驱动开发
4. /verification      — 完成前验证
5. /finishing-branch  — 提交/PR
```

### 修复 Bug

```
1. /debugging         — 系统化调试
2. /verification      — 确认修复
```

### 运行测试

```
1. /web-testing       — E2E + API 测试
```

### 设计页面

```
1. /frontend-design   — 前端设计
2. /ui-ux-system      — 设计系统参考
```

## 来源

本技能包整合自：

- [Superpowers](https://github.com/obra/superpowers) by Jesse Vincent
- [Example-skills](https://github.com/anthropics/anthropic-cookbook) by Anthropic
- [UI-UX-Pro-Max](https://github.com/...)
- [Planning-with-files](https://github.com/...)

## License

MIT

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-16 | 初始版本：35+ skills |
```

- [ ] **Step 2: 验证 README.md**

```bash
cat /Users/Zhuanz/Desktop/onlyforskills/.claude/README.md | head -50
```

---

## Chunk 2: INSTALL.md

### Task 2: 创建安装说明

**Files:**
- Create: `.claude/INSTALL.md`

- [ ] **Step 1: 创建 INSTALL.md**

```markdown
# 安装指南

## 系统要求

- Claude Code CLI（最新版本）
- Git（可选，用于版本控制）

## 安装方式

### 方式 1：直接复制

```bash
# 克隆或下载此技能包
git clone <repo-url> skills-pack

# 复制到你的项目
cp -r skills-pack/.claude/ /path/to/your/project/.claude/
```

### 方式 2：作为子模块

```bash
# 在你的项目中添加子模块
cd /path/to/your/project
git submodule add <repo-url> .claude-pack

# 创建符号链接
ln -s .claude-pack/.claude .claude
```

### 方式 3：选择性复制

```bash
# 只复制核心层
cp -r skills-pack/.claude/skills/core/ /path/to/your/project/.claude/skills/

# 只复制测试层
cp -r skills-pack/.claude/skills/testing/ /path/to/your/project/.claude/skills/

# 复制技能索引
cp skills-pack/.claude/skills/SKILL-CATALOG.md /path/to/your/project/.claude/skills/
```

## 验证安装

在 Claude Code 中输入：

```
/onboard
```

如果看到项目检测和技能推荐，说明安装成功。

## 更新

```bash
# 如果是直接复制，重新复制即可
cp -r skills-pack/.claude/ /path/to/your/project/.claude/

# 如果是子模块
cd /path/to/your/project
git submodule update --remote .claude-pack
```

## 卸载

```bash
rm -rf /path/to/your/project/.claude/
```

## 常见问题

### Q: 技能没有被识别？

检查文件结构：
```bash
ls -la /path/to/your/project/.claude/skills/
```

应该看到 `core/`、`workflow/` 等目录。

### Q: Router 不工作？

确保 `SKILL-CATALOG.md` 存在：
```bash
ls /path/to/your/project/.claude/skills/SKILL-CATALOG.md
```

### Q: 想只使用部分技能？

参考"自定义"章节，删除不需要的目录。
```

- [ ] **Step 2: 验证 INSTALL.md**

```bash
cat /Users/Zhuanz/Desktop/onlyforskills/.claude/INSTALL.md | head -30
```

---

## Chunk 3: CHANGELOG.md

### Task 3: 创建变更日志

**Files:**
- Create: `.claude/CHANGELOG.md`

- [ ] **Step 1: 创建 CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-16

### Added

#### 核心系统
- `core/router` — 智能技能路由器
- `core/onboard` — 新人引导系统
- `SKILL-CATALOG.md` — 完整技能索引

#### 工作流层（13 个 skills）
- `workflow/brainstorming` — 需求探索和设计
- `workflow/tdd` — 测试驱动开发
- `workflow/debugging` — 系统化调试
- `workflow/writing-plans` — 编写实现计划
- `workflow/executing-plans` — 执行实现计划
- `workflow/subagent-driven-development` — 并行 agent 开发
- `workflow/dispatching-parallel-agents` — 分发并行 agent
- `workflow/git-worktrees` — 使用 git worktrees
- `workflow/finishing-branch` — 完成开发分支
- `workflow/requesting-code-review` — 请求代码审查
- `workflow/receiving-code-review` — 处理审查反馈
- `workflow/verification` — 完成前验证
- `workflow/writing-skills` — 编写新 skills

#### 测试层（2 个 skills）
- `testing/web-testing` — 全栈 E2E 测试（Playwright + Newman）
  - 完整的 SKILL.md 主文档
  - playwright-best-practices.md 参考
  - newman-best-practices.md 参考
  - 5 个模板文件
- `testing/api-testing` — Newman API 测试（简化版）

#### 设计层（2 个 skills）
- `design/frontend-design` — 前端页面设计
- `design/ui-ux-system` — 设计系统（161 调色板、57 字体）

#### 文档层（7 个 skills）
- `docs/pdf` — PDF 处理
- `docs/pptx` — PPT 演示文稿
- `docs/docx` — Word 文档
- `docs/xlsx` — Excel 表格
- `docs/canvas-design` — 视觉设计
- `docs/theme-factory` — 主题样式
- `docs/doc-coauthoring` — 文档协作

#### 工具层（6 个 skills）
- `tools/mcp-builder` — 构建 MCP 服务器
- `tools/skill-creator` — 创建新 skill
- `tools/claude-api` — Claude API 开发
- `tools/algorithmic-art` — 算法艺术
- `tools/web-artifacts-builder` — Web artifacts 构建
- `tools/planning` — Manus 风格文件规划

#### 领域层（18 个 skills）
- 保留现有项目特定 skills
- 整理到 `domain/` 目录

#### 文档
- `README.md` — 分发包入口
- `INSTALL.md` — 安装指南
- `CHANGELOG.md` — 变更日志

### Sources

整合自以下项目：
- [Superpowers](https://github.com/obra/superpowers) v5.0.2
- [Example-skills](https://github.com/anthropics/anthropic-cookbook)
- [UI-UX-Pro-Max](https://github.com/...) v2.0.1
- [Planning-with-files](https://github.com/...) v2.23.0
```

---

## Chunk 4: 清理不必要的文件

### Task 4: 清理临时和缓存文件

**Files:**
- Delete: 临时文件、缓存、备份

- [ ] **Step 1: 检查需要清理的文件**

```bash
# 检查可能需要清理的文件
find /Users/Zhuanz/Desktop/onlyforskills/.claude -name "*.bak" -o -name "*.tmp" -o -name ".DS_Store"
```

- [ ] **Step 2: 清理备份文件**

```bash
# 如果有备份文件，删除
find /Users/Zhuanz/Desktop/onlyforskills/.claude -name "*.bak" -delete
find /Users/Zhuanz/Desktop/onlyforskills/.claude -name "*.tmp" -delete
find /Users/Zhuanz/Desktop/onlyforskills/.claude -name ".DS_Store" -delete
```

- [ ] **Step 3: 确保 .gitignore 正确**

```bash
# 检查 .gitignore 是否包含敏感路径
cat /Users/Zhuanz/Desktop/onlyforskills/.gitignore | grep -E "playwright|auth|\.env"
```

Expected: 应该包含 `playwright/.auth/` 等敏感路径

---

## Chunk 5: 验证完整性

### Task 5: 最终验证

- [ ] **Step 1: 验证文件数量**

```bash
# 统计各层文件数
echo "=== 目录结构 ===" && tree -L 2 /Users/Zhuanz/Desktop/onlyforskills/.claude/
echo ""
echo "=== Skills 数量 ===" && find /Users/Zhuanz/Desktop/onlyforskills/.claude/skills -name "SKILL.md" | wc -l
echo ""
echo "=== Rules 数量 ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/rules/ | wc -l
echo ""
echo "=== Hooks 数量 ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/hooks/ | wc -l
```

- [ ] **Step 2: 验证必需文件存在**

```bash
# 检查必需文件
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/README.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/INSTALL.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/CHANGELOG.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/SKILL-CATALOG.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/router/SKILL.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/onboard/SKILL.md
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/web-testing/SKILL.md
```

Expected: 所有文件都存在

- [ ] **Step 3: 创建最终统计**

```bash
echo "# Skills Pack 统计" > /tmp/skills-stats.txt
echo "" >> /tmp/skills-stats.txt
echo "## 各层 Skills 数量" >> /tmp/skills-stats.txt
echo "| 层级 | 数量 |" >> /tmp/skills-stats.txt
echo "|------|------|" >> /tmp/skills-stats.txt
echo "| Core | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/core/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Workflow | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Testing | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Design | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Docs | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/docs/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Tools | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| Domain | $(ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/domain/ | wc -l) |" >> /tmp/skills-stats.txt
echo "| **Total** | **$(find /Users/Zhuanz/Desktop/onlyforskills/.claude/skills -name "SKILL.md" | wc -l)** |" >> /tmp/skills-stats.txt
cat /tmp/skills-stats.txt
```

---

## Chunk 6: 最终提交

### Task 6: 提交 Phase D 完成

- [ ] **Step 1: 添加所有新文件**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/README.md
git add .claude/INSTALL.md
git add .claude/CHANGELOG.md
```

- [ ] **Step 2: 提交 Phase D**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git commit -m "feat(skills): create distributable package

- Add README.md as package entry point
- Add INSTALL.md with installation guide
- Add CHANGELOG.md documenting all skills
- Clean up temporary files

Phase D of Claude Skills Pack implementation.

Total skills: 35+"
```

- [ ] **Step 3: 创建版本标签**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git tag -a v1.0.0 -m "Claude Skills Pack v1.0.0

- Core layer: router + onboard
- Workflow layer: 13 skills
- Testing layer: web-testing + api-testing
- Design layer: 2 skills
- Docs layer: 7 skills
- Tools layer: 6 skills
- Domain layer: 18 skills

Total: 48+ skills"
```

---

## 完成检查

- [ ] README.md 包含完整的使用说明
- [ ] INSTALL.md 包含安装指南
- [ ] CHANGELOG.md 记录所有变更
- [ ] 临时文件已清理
- [ ] 所有必需文件存在
- [ ] Git 提交完成
- [ ] 版本标签已创建

---

## 项目完成！

恭喜！Claude Skills Pack 已完成。

### 成果总结

| 项目 | 数量 |
|------|------|
| **总 Skills 数** | 48+ |
| 核心层 | 2 |
| 工作流层 | 13 |
| 测试层 | 2 |
| 设计层 | 2 |
| 文档层 | 7 |
| 工具层 | 6 |
| 领域层 | 18+ |

### 下一步

1. 测试安装流程
2. 分享给团队成员
3. 收集反馈并迭代
