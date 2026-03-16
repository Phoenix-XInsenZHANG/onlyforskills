# Skills Repository

AI 辅助开发工具集，包含 Skills、Rules、Hooks 等配置，用于提升 Claude Code、Gemini CLI 等 AI 编程助手的开发效率。

## 仓库结构

```
onlyforskills/
├── .claude/                    # Claude Code 配置
│   ├── skills/                 # 技能模块（50+ skills）
│   │   ├── SKILL-CATALOG.md    # 技能索引
│   │   ├── brainstorming/      # 需求探索
│   │   ├── tdd/                # 测试驱动开发
│   │   ├── debugging/          # 系统化调试
│   │   ├── web-testing/        # E2E 测试（Playwright + Newman）
│   │   ├── frontend-design/    # 前端设计
│   │   ├── directus-schema/    # Directus Schema 参考
│   │   └── ...                 # 更多 skills
│   ├── rules/                  # 开发规则
│   │   ├── core.md             # 核心规则（Rules 0-9）
│   │   ├── api-patterns.md     # API 模式
│   │   ├── auth.md             # 认证规范
│   │   └── ...                 # 更多规则
│   ├── hooks/                  # Git hooks
│   │   ├── lint-card.sh        # Card 格式检查
│   │   ├── lint-prd.sh         # PRD 格式检查
│   │   └── ...                 # 更多 hooks
│   └── settings.json           # Claude Code 设置
│
├── superpowers/                # Superpowers 技能包
│   ├── skills/                 # 核心技能
│   │   ├── brainstorming/      # 头脑风暴
│   │   ├── systematic-debugging/  # 系统化调试
│   │   ├── test-driven-development/  # TDD
│   │   ├── writing-plans/      # 计划编写
│   │   └── ...                 # 更多
│   ├── agents/                 # Agent 配置
│   └── commands/               # 命令定义
│
├── planning-with-files/        # 多平台规划技能
│   ├── .cursor/skills/         # Cursor 支持
│   ├── .gemini/skills/         # Gemini 支持
│   ├── .codex/skills/          # Codex 支持
│   ├── .continue/skills/       # Continue 支持
│   └── templates/              # 模板文件
│
├── ui-ux-pro-max-skill/        # UI/UX 设计技能
│   └── cli/                    # CLI 工具
│
└── docs/                       # 文档
```

## 核心 Skills 分类

### 工作流层
| Skill | 用途 |
|-------|------|
| `brainstorming` | 需求探索，设计方案 |
| `writing-plans` | 编写实现计划 |
| `tdd` | 测试驱动开发（RED-GREEN-REFACTOR） |
| `debugging` | 系统化调试（4 阶段） |
| `executing-plans` | 执行实现计划 |

### 代码审查
| Skill | 用途 |
|-------|------|
| `code-review` | 代码审查 |
| `requesting-code-review` | 请求代码审查 |
| `receiving-code-review` | 处理审查反馈 |

### 测试层
| Skill | 用途 |
|-------|------|
| `web-testing` | 全栈 E2E 测试（Playwright UI + Newman API） |
| `api-testing` | Newman/Postman API 测试 |
| `e2e-test` | E2E 测试 |

### 设计层
| Skill | 用途 |
|-------|------|
| `frontend-design` | 前端页面设计 |
| `ui-ux-system` | 设计系统（161 调色板、57 字体） |

### 文档层
| Skill | 用途 |
|-------|------|
| `pdf` | PDF 文档处理 |
| `pptx` | PPT 演示文稿 |
| `docx` | Word 文档 |
| `xlsx` | Excel 表格 |

### Directus 领域
| Skill | 用途 |
|-------|------|
| `directus-schema` | Directus schema 参考 |
| `d11-frontend` | D11 前端集成 |
| `rbac` | RBAC 权限管理 |
| `migration` | 数据迁移 |

## 核心规则 (Rules 0-9)

```
0. PAUSE BEFORE CODE — 先检查现有 cards，论证后再创建
1. CARD FIRST — 每个代码变更都需要 card（可追溯性）
2. ATOMIC COMMITS — 代码 + card 一起提交
3. @card IN CODE — 在代码中链接 card
4. USE AGENT TEAMS — 非平凡任务使用 agent teams（7.5x 效率提升）
5. USE useOrgStore for ORQ — 不要手动解析 localStorage
6. COLLECTION VIEWER FIRST — DB 工作前先建 `/collection/[name]`
7. REDIRECT to /app not /** — 所有"首页"按钮指向 `/app`
8. ARGUE AGAINST FIRST — 提议新字段/文件/模式前先解释为什么不要
9. DOCS FIRST — 探索代码前先 glob `docs/**/`
```

## 快速开始

### 1. 了解项目
```
/onboard
```

### 2. 创建新功能
```
/brainstorming → /writing-plans → /tdd
```

### 3. 修复 Bug
```
/debugging
```

### 4. 运行测试
```
/web-testing
```

### 5. 找正确的 skill
```
/router
```

## 平台支持

- Claude Code (`.claude/`)
- Cursor (`.cursor/`)
- Gemini (`.gemini/`)
- Codex (`.codex/`)
- Continue (`.continue/`)
- And more...

## 仓库信息

- **GitHub**: https://github.com/Phoenix-XInsenZHANG/onlyforskills
- **可见性**: 私有
- **创建时间**: 2026-03-16
- **初始提交**: 496 files, 135990 insertions

---

*此仓库为 AI 辅助开发工具集，持续更新中。*
