# Claude Code Skills Collection

A curated collection of specialized skills for Claude Code CLI.

## Quick Start

| I want to... | Use Skill |
|--------------|-----------|
| Create a new feature | `brainstorming` → `writing-plans` → `tdd` |
| Fix a bug | `debugging` |
| Run tests | `web-testing` or `api-testing` |
| Design a page | `frontend-design` |
| Create documents | `pdf` / `pptx` / `docx` |
| Review code | `code-review` |
| Understand the project | `onboard` |
| Find the right skill | `router` |

## Skills Categories

### Core
`router` · `onboard` · `progress`

### Workflow
`brainstorming` · `writing-plans` · `executing-plans` · `tdd` · `debugging` · `verification`

### Testing
`web-testing` · `api-testing` · `e2e-test`

### Design
`frontend-design` · `ui-ux-system` · `canvas-design`

### Documents
`pdf` · `pptx` · `docx` · `xlsx` · `theme-factory`

### Tools
`mcp-builder` · `skill-creator` · `claude-api` · `planning`

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
