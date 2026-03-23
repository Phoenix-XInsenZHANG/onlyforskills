# Claude Code Skills Collection

A curated collection of specialized skills for Claude Code CLI.

## Quick Start

| I want to... | Use |
|--------------|-----|
| Build a feature end-to-end | Chain: `full-feature-lifecycle` |
| Fix a bug and ship it | Chain: `bug-fix-to-ship` |
| Refactor and ship safely | Chain: `refactor-to-ship` |
| Deploy to production | Chain: `deploy-pipeline` |
| Handle review feedback loop | Chain: `code-review-loop` |
| Run tests | `web-testing` or `api-testing` |
| Design a page | `frontend-design` |
| Create documents | `pdf` / `pptx` / `docx` |
| Understand the project | `onboard` |
| Find the right skill | `router` |

## Chains（工作流链路）

End-to-end workflows — each node is a skill, executed in sequence. **gstack nodes are mandatory** and cannot be skipped.

| ID | Chain | Node Sequence | Trigger Keywords |
|----|-------|---------------|-----------------|
| C01 | `full-feature-lifecycle` | brainstorming → writing-plans → subagent-driven-development → **qa[gstack]** | "从零开始", "完整功能", "端到端实现" |
| C02 | `bug-fix-to-ship` | debugging → tdd → verification → **codex[gstack]** → requesting-code-review → finishing-branch | "修复bug", "线上故障", "hotfix" |
| C03 | `refactor-to-ship` | **codex[gstack]** → tdd → verification → requesting-code-review → finishing-branch | "重构", "技术债", "refactor" |
| C04 | `deploy-pipeline` | verification → requesting-code-review → **ship[gstack]** → **qa[gstack]** → finishing-branch | "部署", "上线", "发版" |
| C05 | `code-review-loop` | requesting-code-review → receiving-code-review → tdd → verification (loop ≤3 rounds) | "review loop", "审查循环" |

## Skills Categories

### Core
`router` · `onboard` · `progress` · `general`

### Workflow
`brainstorming` · `writing-plans` · `executing-plans` · `subagent-driven-development` · `tdd` · `debugging` · `verification`

### Code Review
`code-review` · `requesting-code-review` · `receiving-code-review` · `codex`

### Testing & QA
`web-testing` · `api-testing` · `e2e-test` · `qa` · `qa-only`

### Browser & Deployment
`browse` · `ship` · `deploy-pipeline` · `gstack-upgrade`

### Safety & Guards
`careful` · `guard` · `freeze` · `unfreeze` · `review`

### Design
`frontend-design` · `ui-ux-system` · `canvas-design` · `design-consultation` · `design-review`

### Documents
`pdf` · `pptx` · `docx` · `xlsx` · `theme-factory` · `document-release`

### Tools
`mcp-builder` · `skill-creator` · `claude-api` · `planning` · `office-hours` · `retro`

## Structure

```
.claude/skills/
├── [skill-name]/        # Each skill at depth 1
│   ├── SKILL.md         # Skill manifest
│   ├── references/      # Reference files (optional)
│   └── templates/       # Template files (optional)
├── SKILL-CATALOG.md     # Full index
├── README.md            # English docs
└── README-CN.md         # Chinese docs (中文文档)
```

## Usage

Skills auto-activate based on task description:

```
User: "Run the migration"
→ Invokes `migration` skill

User: "Review PR #106"
→ Invokes `code-review` skill
```

Or invoke manually: `/brainstorming`, `/tdd`, `/web-testing`

## Key Discovery

**Skills must be at directory depth 1** to be discovered. Nested directories won't work:

```
✅ skills/my-skill/SKILL.md      # Works
❌ skills/category/my-skill/SKILL.md  # Won't work
```

## License

MIT
