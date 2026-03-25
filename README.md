# Claude Code Skills Collection

A curated collection of **156 skills** and **11 chains** for Claude Code CLI — covering the full product lifecycle from discovery to release.

## Quick Start

| I want to... | Use |
|--------------|-----|
| Run the full product lifecycle | Chains: `product-discovery` → `strategic-alignment` → `feature-spec-design` → `engineering-review` → `dev-execution` → `release-retro` |
| Build a feature end-to-end | Chain: `full-feature-lifecycle` |
| Fix a bug and ship it | Chain: `bug-fix-to-ship` |
| Refactor and ship safely | Chain: `refactor-to-ship` |
| Deploy to production | Chain: `deploy-pipeline` |
| Handle review feedback loop | Chain: `code-review-loop` |
| Explore a product idea | Chain: `product-discovery` |
| Prioritize features & analyze competitors | Chain: `strategic-alignment` |
| Write PRD + design system | Chain: `feature-spec-design` |
| Run tests | `web-testing` or `api-testing` |
| Design a page | `frontend-design` |
| Create documents | `pdf` / `pptx` / `docx` |
| Analyze market / users | `competitor-analysis` / `user-personas` / `market-sizing` |
| Understand the project | `onboard` |
| Find the right skill | `router` |

## Chains

End-to-end workflows — each node is a skill, executed in sequence. **gstack nodes** and **ai-workflow nodes** are mandatory.

### Engineering Chains (C01-C05)

| ID | Chain | Node Sequence | Trigger |
|----|-------|---------------|---------|
| C01 | `full-feature-lifecycle` | brainstorming → writing-plans → subagent-driven-development → **qa[gstack]** | "complete feature", "end-to-end" |
| C02 | `bug-fix-to-ship` | debugging → tdd → verification → **codex[gstack]** → requesting-code-review → finishing-branch | "fix bug", "hotfix" |
| C03 | `refactor-to-ship` | **codex[gstack]** → tdd → verification → requesting-code-review → finishing-branch | "refactor", "tech debt" |
| C04 | `deploy-pipeline` | verification → requesting-code-review → **ship[gstack]** → **qa[gstack]** → finishing-branch | "deploy", "release" |
| C05 | `code-review-loop` | requesting-code-review → receiving-code-review → tdd → verification (loop ≤3) | "review loop" |

### Product Lifecycle Chains (C06-C11)

6-phase closed loop — retro data flows back to discovery.

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
  ^                                                    |
  └──────────────── retro data flows back ─────────────┘
```

| ID | Chain | Node Sequence | Trigger |
|----|-------|---------------|---------|
| C06 | `product-discovery` | office-hours → brainstorming → **ai-workflow** → brainstorm-ideas → identify-assumptions → brainstorm-experiments | "discovery", "new idea" |
| C07 | `strategic-alignment` | value-proposition → prioritize-features → competitor-analysis → **ai-workflow** | "prioritize", "competitive analysis" |
| C08 | `feature-spec-design` | plan-ceo-review → plan-design-review → design-consultation → writing-plans → create-prd → **ai-workflow** → metrics-dashboard | "feature spec", "write PRD" |
| C09 | `engineering-review` | plan-eng-review → writing-plans → user-stories → **ai-workflow** | "eng review", "architecture review" |
| C10 | `dev-execution` | **ai-workflow** → executing-plans → review → **qa[gstack]** | "start coding", "execute plan" |
| C11 | `release-retro` | **ship[gstack]** → **ai-workflow** → gtm-strategy → north-star-metric → retro | "release", "ship and retro" |

> **ai-workflow** validates PRD/Story/Card 3-layer doc standard at every phase transition.

## Skills Categories (156 total)

### Core (4)
`router` · `onboard` · `progress` · `general`

### Workflow (7)
`brainstorming` · `writing-plans` · `executing-plans` · `subagent-driven-development` · `tdd` · `debugging` · `verification`

### Code Review (4)
`code-review` · `requesting-code-review` · `receiving-code-review` · `codex`

### Testing & QA (5)
`web-testing` · `api-testing` · `e2e-test` · `qa` · `qa-only`

### Browser & Deployment (4)
`browse` · `ship` · `deploy-pipeline` · `gstack-upgrade`

### Safety & Guards (5)
`careful` · `guard` · `freeze` · `unfreeze` · `review`

### Design (5)
`frontend-design` · `ui-ux-system` · `canvas-design` · `design-consultation` · `design-review`

### Documents (6)
`pdf` · `pptx` · `docx` · `xlsx` · `theme-factory` · `document-release`

### Tools (8)
`mcp-builder` · `skill-creator` · `claude-api` · `planning` · `office-hours` · `retro` · `algorithmic-art` · `web-artifacts-builder`

### PM — Product Strategy (12)
`product-strategy` · `product-vision` · `value-proposition` · `business-model` · `lean-canvas` · `startup-canvas` · `swot-analysis` · `pestle-analysis` · `porters-five-forces` · `ansoff-matrix` · `pricing-strategy` · `monetization-strategy`

### PM — Product Discovery (13)
`brainstorm-ideas-existing` · `brainstorm-ideas-new` · `brainstorm-experiments-existing` · `brainstorm-experiments-new` · `identify-assumptions-existing` · `identify-assumptions-new` · `prioritize-assumptions` · `prioritize-features` · `analyze-feature-requests` · `opportunity-solution-tree` · `interview-script` · `summarize-interview` · `metrics-dashboard`

### PM — Market Research (7)
`competitor-analysis` · `user-personas` · `user-segmentation` · `sentiment-analysis` · `market-sizing` · `market-segments` · `customer-journey-map`

### PM — Data Analytics (3)
`ab-test-analysis` · `cohort-analysis` · `sql-queries`

### PM — Marketing & Growth (5)
`north-star-metric` · `marketing-ideas` · `positioning-ideas` · `value-prop-statements` · `product-name`

### PM — Go-to-Market (6)
`gtm-strategy` · `gtm-motions` · `beachhead-segment` · `ideal-customer-profile` · `competitive-battlecard` · `growth-loops`

### PM — Execution (15)
`create-prd` · `user-stories` · `job-stories` · `wwas` · `brainstorm-okrs` · `sprint-plan` · `stakeholder-map` · `prioritization-frameworks` · `outcome-roadmap` · `test-scenarios` · `pre-mortem` · `release-notes` · `summarize-meeting` · `dummy-dataset` · `retro`

### PM — Toolkit (4)
`grammar-check` · `review-resume` · `privacy-policy` · `draft-nda`

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
