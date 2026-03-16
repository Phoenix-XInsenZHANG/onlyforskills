# Claude Code Skills

This directory contains specialized skills that Claude Code automatically invokes based on task descriptions.

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

This directory contains specialized skills that Claude Code automatically invokes based on task descriptions.

## Skill Architecture

Skills follow a **modular, domain-specific pattern** where complex workflows are separated into focused, auto-invocable skills.

## Available Skills

### Core Workflow

**[ai-workflow](ai-workflow/SKILL.md)** - Main development workflow
- **Lines**: 664 (reduced from 829 after skill extraction)
- **Purpose**: Core Step 0-4 development process
- **Auto-invokes**: Always loaded for development tasks
- **Handles**: Intent analysis, document layer decisions, proposal generation, code implementation

### Specialized Skills

**[migration](migration/SKILL.md)** - Schema migration workflow
- **Lines**: ~150
- **Purpose**: Run/create migrations with mandatory snapshot workflow
- **Triggers**: "run migration", "migration latest", "create migration", "take snapshot", "create collection", "add field", "add relation"
- **Handles**: Before/after snapshots, migration scripts, registry updates, collection creation

**[directus-schema](directus-schema/SKILL.md)** - Schema references & seed data
- **Lines**: 400+
- **Purpose**: Seed data, fresh database setup, schema reference docs
- **Triggers**: "seed data", "setup database", "M2O/O2M/M2M" (reference)
- **Handles**: Seed scripts, fresh DB setup, relation patterns (reference only)

**[e2e-test](e2e-test/SKILL.md)** - E2E & integration test workflow
- **Lines**: ~500
- **Purpose**: Full pipeline: clean test data → run Playwright → generate report → view at /test-report
- **Triggers**: "run e2e", "e2e test", "playwright test", "clean and test", "full pipeline test", "run integration test"
- **Handles**: Data cleanup, Playwright execution, multi-project report generation, dynamic report viewer (Frontend/Backend/Pipeline tabs)

**[api-testing](api-testing/SKILL.md)** - API testing & validation
- **Lines**: 257
- **Purpose**: Newman/Postman tests, PRD test coverage
- **Triggers**: "Run tests", "Test API", "Newman test", "Phase 4"
- **Handles**: Test execution, statistics extraction, PRD frontmatter updates

**[visualizer](visualizer/SKILL.md)** - Data visualizations
- **Lines**: ~150
- **Purpose**: Generate HTML visualizations from YAML data
- **Triggers**: "Visualize", "Show progress", "Card progress"
- **Handles**: Card progress heatmap (zero hardcoding)

**[landing-page](landing-page/SKILL.md)** - Landing page management
- **Lines**: ~180
- **Purpose**: Create landing pages with domain routing and CSS isolation
- **Triggers**: "Create landing page", "Add domain routing", "Map domain", "Brand page"
- **Handles**: Domain-to-page routing, CSS scoping, navigation control, showcase integration
- **Domain Mappings**: synque.hk, homemiles.com, aticonsultant.com

**[pm-comments](pm-comments/SKILL.md)** - PM Comments & Sync workflow
- **Lines**: ~300
- **Purpose**: Sync cards to Directus + process PM comments
- **Triggers**: "synque", "sync card", "pm comments", "pull comments"
- **Handles**: Card sync, format validation, comment parsing, interactive resolution

**[skill-creator](skill-creator/SKILL.md)** - Skill creation automation
- **Lines**: ~150
- **Purpose**: Create new skills with proper structure and registration
- **Triggers**: "create skill", "new skill", "add skill"
- **Handles**: Directory setup, SKILL.md template, README registration, checklist

**[rbac](rbac/SKILL.md)** - RBAC policy management
- **Lines**: ~280
- **Purpose**: Directus 11 role/policy/permission management for multi-tenant access
- **Triggers**: "rbac", "create policy", "assign role", "permissions", "multi-tenant access"
- **Handles**: Role creation, policy CRUD, permission configuration with `validation` field, directus_access linking

**[backend-extension](backend-extension/SKILL.md)** - Backend extension development
- **Lines**: ~200
- **Purpose**: Directus 11 custom API endpoints, OAuth providers, business logic modules
- **Triggers**: "backend extension", "directus extension", "custom endpoint", "create extension", "oauth extension"
- **Handles**: Extension structure, modular architecture, endpoint patterns, Newman testing

**[business-prd-planner](business-prd-planner/SKILL.md)** - Business idea to PRD planning
- **Lines**: ~200
- **Purpose**: Turn business ideas into PRDs, Stories, and Cards
- **Triggers**: "plan feature", "create prd", "business idea", "product planning", "feature planning"
- **Handles**: Capture business context, identify PRD candidates, create documentation structure

**[code-review](code-review/SKILL.md)** - Systematic code review workflow
- **Lines**: ~500
- **Purpose**: Comprehensive PR review for documentation and code changes
- **Triggers**: "code review", "review PR", "review this branch", "review PR #XXX"
- **Handles**: Context gathering, doc quality checks, claim verification, build testing, scorecard generation
- **Key Feature**: Numerical claim verification (e.g., relationship counts, collection counts)

**[d11-frontend](d11-frontend/SKILL.md)** - D11 frontend integration standard
- **Lines**: ~250
- **Purpose**: How to write Next.js pages and API modules that talk to Directus 11
- **Triggers**: "d11 api", "d11 frontend", "new d11 module", "authenticatedFetch pattern", "migrate to d11"
- **Handles**: API module template (`lib/d11/*.ts`), page pattern (PRDAuthGate wrapper), D9→D11 migration tracker
- **Reference impl**: `lib/d11/orders.ts`, `app/order/my-orders/page.tsx`

## Skill Invocation

### Automatic Invocation

Claude Code automatically invokes skills when their description matches user intent:

```
User: "Run the migration latest"
→ Claude Code invokes `migration` skill

User: "Create a new collection for users_multi"
→ Claude Code invokes `migration` skill

User: "Run Newman tests for OAuth API"
→ Claude Code invokes `api-testing` skill

User: "Show Card progress"
→ Claude Code invokes `visualizer` skill

User: "Create landing page for newbrand.com"
→ Claude Code invokes `landing-page` skill

User: "synque"
→ Claude Code invokes `pm-comments` skill (sync + comments)

User: "Review PR #106"
→ Claude Code invokes `code-review` skill
```

### Manual Invocation

Users can explicitly invoke skills:

```bash
/migration         # or "run migration", "migration latest"
/directus-schema   # or "seed data", "setup database"
/api-testing
/visualizer
/landing-page
/pm-comments       # or just "synque"
/skill-creator     # or "create skill", "new skill"
/rbac              # or "create policy", "assign role"
/backend-extension # or "create extension", "oauth extension"
/business-prd-planner # or "plan feature", "business idea"
/code-review       # or "review PR", "review this branch"
/d11-frontend      # or "d11 api", "new d11 module", "migrate to d11"
```

## Context Loading Hierarchy

Claude Code loads context in this order:

1. **CLAUDE.md** (always loaded first) - Project overview
2. **Skills** (auto-invoked by description) - Domain-specific workflows
3. **References** (on-demand) - Detailed templates and patterns
4. **User messages & IDE context** - Current task details
5. **Tool results** (dynamic) - Runtime information

## Skill Structure

Each skill follows this pattern:

```
.claude/skills/[skill-name]/
├── SKILL.md                 ← Skill manifest with description
├── README.md                ← Developer documentation (optional)
└── references/              ← On-demand reference files
    ├── reference-1.md
    └── reference-2.md
```

## Migration from Monolithic ai-workflow

**Before** (829 lines):
- Single large ai-workflow/SKILL.md
- All Directus, API testing, visualization in one file
- Loaded entire context for every task

**After** (664 + 218 + 257 = 1139 lines, but modular):
- Core ai-workflow (664 lines) - always loaded
- Specialized skills - loaded only when needed
- Better focus, faster invocation, clearer ownership

## Benefits of Skill Separation

1. **Focused Context** - Only load relevant information
2. **Faster Invocation** - Smaller description matching
3. **Independent Evolution** - Skills evolve separately
4. **Clear Ownership** - Each domain has dedicated documentation
5. **Reduced Complexity** - Core workflow is cleaner

## When to Create a New Skill

Create a new skill when:
- ✅ Self-contained domain (database, testing, visualization)
- ✅ Specific workflow that doesn't need full Step 0-4
- ✅ Large enough to warrant separate documentation (>100 lines)
- ✅ Clear trigger patterns for auto-invocation
- ✅ Domain-specific tools and patterns

Do NOT create a skill when:
- ❌ Part of core development flow
- ❌ Too small (<50 lines)
- ❌ No clear trigger patterns
- ❌ Frequently combined with other tasks

## Skill Development Guide

### 1. Create Skill Structure

```bash
mkdir -p .claude/skills/[skill-name]/references
```

### 2. Write SKILL.md Manifest

```yaml
---
name: skill-name
description: What this skill does. Triggers when user says X, Y, Z.
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash(*), Read, Write
---

# Skill Name

When to use, triggers, workflow...
```

### 3. Move Reference Files

```bash
cp .claude/skills/ai-workflow/references/related.md \
   .claude/skills/[skill-name]/references/
```

### 4. Update ai-workflow/SKILL.md

Remove extracted section, add delegation note:

```markdown
## Specialized Skills (Delegated)

### Your New Skill
**→ Use `skill-name` skill** for...
```

### 5. Update References Table

```markdown
| ~~`references/old-file.md`~~ | **→ Moved to `skill-name` skill** |
```

## Future Skill Candidates

Potential skills to extract (not yet implemented):

- **prd-parser** - PRD YAML parsing and validation

## See Also

- [CLAUDE.md](../../CLAUDE.md) - Project overview and architecture
- [ai-workflow/SKILL.md](ai-workflow/SKILL.md) - Core development workflow
- [migration/SKILL.md](migration/SKILL.md) - Schema migration workflow
- [directus-schema/SKILL.md](directus-schema/SKILL.md) - Schema references & seed data
- [api-testing/SKILL.md](api-testing/SKILL.md) - API testing and validation
- [landing-page/SKILL.md](landing-page/SKILL.md) - Landing page management
- [pm-comments/SKILL.md](pm-comments/SKILL.md) - PM Comments & Sync workflow
- [skill-creator/SKILL.md](skill-creator/SKILL.md) - Skill creation automation
- [rbac/SKILL.md](rbac/SKILL.md) - RBAC policy management
- [backend-extension/SKILL.md](backend-extension/SKILL.md) - Backend extension development
- [visualizer/SKILL.md](visualizer/SKILL.md) - Data visualizations
- [business-prd-planner/SKILL.md](business-prd-planner/SKILL.md) - Business idea to PRD planning
- [code-review/SKILL.md](code-review/SKILL.md) - Systematic code review workflow
- [d11-frontend/SKILL.md](d11-frontend/SKILL.md) - D11 frontend integration standard
