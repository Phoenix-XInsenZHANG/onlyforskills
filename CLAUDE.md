# CLAUDE.md

Monorepo: Next.js frontend + Directus 11 backend. Domain-specific rules in `.claude/rules/`. Skills in `.claude/skills/`.

## CRITICAL RULES - READ FIRST

```
0. PAUSE BEFORE CODE - check existing cards, argue against, then create card
1. CARD FIRST - every code change needs a card (traceability)
2. ATOMIC COMMITS - Code + Card together
3. @card IN CODE - link implementation to card for searchability
4. USE AGENT TEAMS - For any non-trivial task (7.5x proven)
5. USE useOrgStore for ORQ - never parse localStorage manually (frontend)
6. COLLECTION VIEWER FIRST - /collection/[name] before any DB work
7. REDIRECT to /app not / - all "home" buttons go to /app (frontend)
8. ARGUE AGAINST FIRST - before proposing new fields/files/patterns, explain why NOT to
9. DOCS FIRST - glob docs/**/ for existing knowledge before exploring code
```

**Rule 0 Process (HARD GATE — no code without this):**
1. `grep docs/cards/` for existing card covering this work
2. If found → state which CARD-XXX you're updating
3. If not found → "Arguments against: [reasons]", then create CARD-XXX
4. Only after card identified → write code with `@card CARD-XXX` references

**Enforcement hierarchy:** types > guards > lints > hooks > rules files > docs

---

## Context Initialization (Start Here)

1. **Check docs/cards/** for current working context
2. **Run `/progress`** for strategic intelligence
3. **Ask**: "What patterns are we currently testing?"

---

## Monorepo Structure

```
/
├── .claude/                    # Skills, rules, hooks (shared)
├── docs/                       # Cross-cutting documentation
│   ├── prds/PRD-*.md           # Product Requirements
│   ├── stories/{US,AS}-*.md    # User Stories
│   ├── cards/CARD-*.md         # Technical Cards
│   └── integration/            # Integration Runbooks
├── frontend/                   # Next.js app
│   ├── app/                    # App router pages
│   ├── components/             # UI components
│   ├── lib/                    # Utilities, API clients, hooks
│   ├── stores/                 # Zustand stores (org-store.ts)
│   ├── public/                 # Static assets, locales
│   └── package.json
├── backend/                    # Directus 11
│   ├── extensions/             # Custom extensions
│   │   └── directus-extension-*/
│   ├── migrations/             # Schema migration registry
│   │   └── REGISTRY.md
│   ├── snapshots/              # Schema snapshots (before/after)
│   ├── scripts/                # Seed data, collection creation
│   ├── uploads/                # User files (gitignored)
│   ├── .env                    # Backend env (gitignored)
│   └── package.json
├── scripts/                    # Cross-cutting (sync, deploy)
├── docker-compose.yml          # Orchestrates Postgres + D11 + Next.js
├── package.json                # Workspace root (yarn workspaces)
├── CLAUDE.md
└── .gitignore
```

---

## Quick Reference

### Commands

| Command | Location | Purpose |
|---------|----------|---------|
| `yarn dev` | `frontend/` | Start Next.js dev server |
| `yarn build` | `frontend/` | Build frontend for production |
| `yarn lint` | `frontend/` | Run ESLint |
| `yarn dev` | `backend/` | Start Directus dev mode |
| `yarn start` | `backend/` | Start Directus |
| `yarn bootstrap` | `backend/` | First-time Directus setup |

### Key Endpoints (Frontend)

| Endpoint | Purpose |
|----------|---------|
| `/app` | SaaS application homepage |
| `/prd` | Knowledge Hub — browse PRDs, progress |
| `/collection/{name}` | Schema discovery with "Copy Collection Data" |
| `/api/ai-context` | Machine-readable project state |

### File Locations

| Type | Location |
|------|----------|
| PRDs | `docs/prds/PRD-*.md` |
| Stories | `docs/stories/{US,AS}-*.md` |
| Cards | `docs/cards/CARD-*.md` |
| Frontend pages | `frontend/app/` |
| Frontend components | `frontend/components/` |
| Org store | `frontend/stores/org-store.ts` |
| Backend extensions | `backend/extensions/directus-extension-*` |
| Migrations | `backend/migrations/REGISTRY.md` |
| Snapshots | `backend/snapshots/` |
| Seed/collection scripts | `backend/scripts/` |
| Cross-cutting scripts | `scripts/` |
| Lint scripts | `.claude/hooks/lint-*.sh` |
| Rules | `.claude/rules/*.md` |

### Lint Pipeline

PostToolUse hook auto-runs lint after Edit/Write. Manual:

| Script | Validates |
|--------|-----------|
| `bash .claude/hooks/lint-prd.sh` | PRD frontmatter |
| `bash .claude/hooks/lint-card.sh` | Card frontmatter |
| `bash .claude/hooks/lint-story.sh` | Story frontmatter |
| `bash .claude/hooks/lint-d11.sh` | D11 collection names |
| `bash .claude/hooks/lint-loaders.sh` | TypeScript scope in critical files |

---

## Agent Era Philosophy

> "AI agents generate code faster than humans can review. Knowledge lives in context windows — close the session, it's gone."

**Solution:** Every code change has a Card. Local markdown = source of truth.

```
Prompt → Card → Code → Commit
  ↓        ↓      ↓       ↓
Context  Tracks  @card   Atomic
captured  task  reference (all 3)
```

### Document Hierarchy
```
PRD (Why — business context)     → docs/prds/
  └── Story (Who/What — user journey) → docs/stories/
        └── Card (How — technical spec)    → docs/cards/
              └── Code (@card reference)         → frontend/ or backend/
```

### Document Layer Decision

| Signal | Layer | Example |
|--------|-------|---------|
| New domain, no existing PRD | **PRD** | "Build a membership points system" |
| New user-facing capability | **Story** | "Users can view order history" |
| Technical task, parent exists | **Card** | "Add pagination to order list" |
| Bug fix, clear scope | **Code** | "Fix the pagination bug" |

### Card References in Code

```typescript
/**
 * @card CARD-PAY-011
 * @see docs/cards/CARD-PAY-011.md
 */
```

---

## Frontend Architecture (Next.js)

### Organization-Aware API Calls
```typescript
import { useOrgStore } from '@/stores/org-store'
const orqId = useOrgStore.getState().getSelectedOrq()
import { authenticatedFetch } from '@/lib/authenticated-fetch'
const response = await authenticatedFetch('/api/endpoint')
```

### Auth Modes (Three Mutually Exclusive)

| Mode | Env Flag | Login Endpoint |
|------|----------|----------------|
| **D11 Policy** (current) | `AUTH_POLICY=true` | `POST /login/email` |
| **D9 Centralized** (default) | Neither flag | `POST /shared/auth/email/login` |
| **D9 Direct** | `DIRECTUS_ONLY=true` | `POST /auth/login` |

### Two Directus Instances

| Instance | Env Var | Purpose |
|----------|---------|---------|
| **D9** | `NEXT_PUBLIC_API_ORQ` | Main SaaS |
| **D11** | `DIRECTUS_PRD_ENDPOINT` | Docs sync |

### Frontend Conventions
- **File naming:** kebab-case
- **State:** Zustand stores + React Context
- **i18n:** Main app: `useI18n()`. Landing pages: `useLanguage()` (isolated)
- **Homepage:** `/app` for all redirects, `/` for landing pages
- **API field expansion:** Match existing patterns — check before adding new ones

---

## Backend Architecture (Directus 11)

### Extension Types
| Type | Purpose | Location |
|------|---------|----------|
| `endpoints/` | Custom API endpoints | `backend/extensions/directus-extension-*/` |
| `hooks/` | Server-side event handlers | same |
| `interfaces/` | Custom input components | same |
| `modules/` | Full admin panel pages | same |
| `operations/` | Custom flow operations | same |

### Creating Extensions
```bash
cd backend/extensions
npx create-directus-extension@latest
```

### Extension Standards
- Use `defineEndpoint` from `@directus/extensions-sdk`
- Access services via `context.services` (ItemsService, UsersService, etc.)
- Use `req.accountability` for permission checks
- Use `context.logger` for logging
- Always `try/catch` with `next(error)` for async routes
- Never expose sensitive env vars in responses

### Building Extensions
```bash
cd backend/extensions/directus-extension-<name>
yarn install && yarn build    # Build once
yarn dev                      # Watch mode
```

### Directus API Quick Reference
```bash
# List with filter
GET /items/{collection}?filter[status][_eq]=published&limit=10

# Get with relations
GET /items/{collection}/{id}?fields=*,author.*,tags.*

# Create / Update
POST /items/{collection}    PATCH /items/{collection}/{id}

# Auth
POST /auth/login → Bearer <access_token>
```

### Common Filter Operators
`_eq` `_neq` `_contains` `_in` `_null` `_gte` `_lte` `_between`

### Environment Variables (Backend)
Key `.env` vars: `DB_CLIENT`, `DB_FILENAME`/`DB_HOST`, `SECRET`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `PUBLIC_URL`, `LOG_LEVEL`

---

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| "No data found" | Check field expansion pattern |
| Infinite re-renders | Don't use functions in useEffect deps |
| ORQ undefined | Use `useOrgStore.getState().getSelectedOrq()` |
| PRD not showing | Run lint-prd.sh; quote dates (`"2026-02-06"`) |
| D11 404 on collection | Singular names: `order` not `orders` |
| Wrong org ID in D11 | Use `Number(org.code)` not `org.id` |

---

## Three-Layer Consistency

When changing any pattern → update **Data** (DB/seed) + **Code** + **Docs**, or the fix is incomplete.

If a fix touches N>2 call sites, the fix is in the wrong place — push it down a layer.

---

## Skills Index

Skills are SOPs — execute step-by-step, don't improvise. Test before changing any skill (evidence-based only).

| Trigger Keywords | Skill | Purpose |
|------------------|-------|---------|
| Development tasks, PRD/Story/Card | `ai-workflow` | Step 0-4 workflow |
| "run migration", "create collection" | `migration` | Directus schema migrations |
| Schema questions, M2O/O2M/M2M | `directus-schema` | Schema references + seed data |
| "run e2e", "playwright test" | `e2e-test` | Full E2E pipeline |
| "run tests", "Newman" | `api-testing` | Newman/Postman tests |
| "synque", "sync card" | `pm-comments` | Card sync + PM comments |
| "/progress", "what's blocked" | `progress` | Query cards, detect blockers |
| "plan feature", business ideas | `business-prd-planner` | PRD planning |
| "business report" | `business-report` | Story-centric flow status |
| "RBAC", "policy", "permissions" | `rbac` | Directus access control |
| "backend extension", "OAuth" | `backend-extension` | Directus extensions |
| "d11 api", "d11 frontend" | `d11-frontend` | D11 page/API standard |
| "create landing page" | `landing-page` | Landing page creation |
| "review PR", "code review" | `code-review` | Systematic PR review |
| "use agent teams" | `agent-teams` | 7.5x parallel agents |
| "create skill" | `skill-creator` | Create new skills |
| "team health" | `team-health` | System coherence audit |
| "visualize" | `visualizer` | HTML visualizations |
| "browse", "QA", "点击测试", "ship", "production", "careful", "codex", "retro" | `gstack/*` | gstack 独有工具链 |

**Skill locations:** `.claude/skills/{name}/SKILL.md`

### Chains（工作流链路）

端到端链路，每个节点是一个 skill，顺序执行，不可跳过。gstack 节点（[gstack]）为必经步骤。

| ID | Chain | 节点序列 | 触发条件 |
|----|-------|---------|---------|
| C01 | `full-feature-lifecycle` | brainstorming → writing-plans → subagent-driven-development → **qa[gstack]** | "从零开始", "完整功能", "端到端实现" |
| C02 | `bug-fix-to-ship` | debugging → tdd → verification → **codex[gstack]** → requesting-code-review → finishing-branch | "修复bug", "线上故障", "hotfix" |
| C03 | `refactor-to-ship` | **codex[gstack]** → tdd → verification → requesting-code-review → finishing-branch | "重构", "技术债", "refactor" |
| C04 | `deploy-pipeline` | verification → requesting-code-review → **ship[gstack]** → **qa[gstack]** → finishing-branch | "部署", "上线", "发版" |
| C05 | `code-review-loop` | requesting-code-review → receiving-code-review → tdd → verification (循环 ≤3 轮) | "review loop", "审查循环" |

---

## Path-Scoped Rules (`.claude/rules/`)

| File | Loads when editing | Content |
|------|-------------------|---------|
| `core.md` | Always | Rules 0-9, enforcement hierarchy |
| `d11.md` | `backend/**`, D11 collections | D11 conventions, RBAC |
| `d9.md` | Legacy D9 extension files | D9 extension build/deploy |
| `auth.md` | `lib/auth-*.ts`, login pages | Three auth modes |
| `docs.md` | `docs/**`, `lib/prd-*.ts` | Card-first, doc hierarchy |
| `api-patterns.md` | `app/api/**`, `lib/d11/**` | Field expansion, two Directus instances |
| `commit.md` | `.git/**` | Atomic commits, @card in messages |

---

## Detailed References

| Topic | Reference |
|-------|-----------|
| Full dev workflow | `.claude/skills/ai-workflow/SKILL.md` |
| PRD template | `.claude/skills/ai-workflow/references/prd-template.md` |
| Card template | `.claude/skills/ai-workflow/references/card-template-v2.md` |
| Commit workflow | `.claude/skills/ai-workflow/references/commit-workflow.md` |
| Directus relations | `.claude/skills/directus-schema/references/directus-relations.md` |
| Directus SDK | `.claude/skills/directus-schema/references/directus-sdk-best-practices.md` |
| RBAC patterns | `.claude/skills/ai-workflow/references/directus-rbac-patterns.md` |

---

## gstack 工具链

gstack 补充了 .claude 体系中缺失的执行层工具。**始终使用 `gstack/browse` 替代任何 `mcp__claude-in-chrome__*` 工具进行 web 浏览。**

### 可用 Skills

| Skill | 触发关键词 | 用途 |
|-------|-----------|------|
| `gstack/browse` | "browse", "open url", "navigate" | headless 浏览器，~100ms/命令 |
| `gstack/qa` | "qa", "test the app", "click through" | 真实浏览器 QA 测试 |
| `gstack/qa-only` | "qa only", "just test" | 纯 QA，不含 review |
| `gstack/careful` | "production", "生产", "careful" | 生产操作安全模式 |
| `gstack/freeze` | "freeze", "lock scope" | 锁定编辑范围到指定目录 |
| `gstack/guard` | "guard", "maximum safety" | 最高安全模式 + 编辑警告 |
| `gstack/unfreeze` | "unfreeze", "unlock" | 解除 freeze/guard |
| `gstack/codex` | "adversarial review", "second opinion" | 对抗性代码审查 |
| `gstack/retro` | "retro", "stats", "周报" | 开发统计周报 |
| `gstack/ship` | "ship", "create pr", "deploy" | 一键 PR 创建 |
| `gstack/document-release` | "document release", "post-ship" | 发布后文档更新 |
| `gstack/office-hours` | "office hours", "YC 风格", "is this worth building" | YC 强迫性产品追问 |

### 重叠 Skill 路由规则

当意图模糊时，按以下规则路由：

| 意图 | 优先路由 | 理由 |
|------|---------|------|
| 需求探索 / brainstorm | `.claude/brainstorming` | 有 PRD/Story/Card 3 层文档输出 |
| YC 风格逼问 | `gstack/office-hours` | 专为 startup/product idea 设计 |
| code review | `.claude/code-review` | 已注入 SQL/LLM 检查清单 |
| 真实浏览器测试 | `gstack/qa` | 唯一具备浏览器能力的 skill |
| 生产系统操作 | `gstack/careful` | 安全锁定模式 |

### setup 故障排查

如果 gstack skills 无法运行：
```bash
cd .claude/skills/gstack && ./setup
```
