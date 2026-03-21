#!/usr/bin/env python3
"""Scan all SKILL.md files and extract cross-references as a DOT directed graph."""

import os, re, sys

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")

# Collect all skill names from directory structure
skill_names = set()
for entry in os.listdir(SKILLS_DIR):
    skill_path = os.path.join(SKILLS_DIR, entry, "SKILL.md")
    if os.path.isfile(skill_path):
        skill_names.add(entry)

# superpowers: prefixed aliases
SUPERPOWERS = {
    "superpowers:brainstorming", "superpowers:dispatching-parallel-agents",
    "superpowers:executing-plans", "superpowers:finishing-a-development-branch",
    "superpowers:receiving-code-review", "superpowers:requesting-code-review",
    "superpowers:systematic-debugging", "superpowers:using-superpowers",
    "superpowers:subagent-driven-development", "superpowers:using-git-worktrees",
    "superpowers:test-driven-development", "superpowers:writing-plans",
    "superpowers:writing-skills", "superpowers:verification-before-completion",
    "superpowers:brainstorm", "superpowers:write-plan", "superpowers:execute-plan",
}

ALIAS_MAP = {
    "brainstorm": "brainstorming",
    "write-plan": "writing-plans",
    "execute-plan": "executing-plans",
    "systematic-debugging": "debugging",
    "finishing-a-development-branch": "finishing-branch",
    "using-git-worktrees": "git-worktrees",
    "test-driven-development": "tdd",
    "verification-before-completion": "verification",
    "using-superpowers": "using-superpowers",
}

def canonical(name):
    if name.startswith("superpowers:"):
        suffix = name.split(":", 1)[1]
        return ALIAS_MAP.get(suffix, suffix)
    return name

# Extract edges
edges = {}

for sname in sorted(skill_names):
    skill_path = os.path.join(SKILLS_DIR, sname, "SKILL.md")
    with open(skill_path, "r") as f:
        content = f.read()

    refs = set()

    # superpowers: prefixed references
    for sp in SUPERPOWERS:
        if sp in content:
            target = canonical(sp)
            if target != sname:
                refs.add(target)

    # Bare skill name references via common patterns
    for other in skill_names:
        if other == sname:
            continue
        patterns = [
            rf'(?:invoke|use|activate|call|load|trigger|run)\s+(?:the\s+)?{re.escape(other)}',
            rf'skill[:\s]+["\']?{re.escape(other)}["\']?',
            rf'Skill\(["\']?{re.escape(other)}["\']?\)',
            rf'`{re.escape(other)}`\s+skill',
            rf'{re.escape(other)}\s+skill',
            rf'→\s*{re.escape(other)}',
            rf'skills/{re.escape(other)}/',
        ]
        for pat in patterns:
            if re.search(pat, content, re.IGNORECASE):
                refs.add(other)
                break

    if refs:
        edges[sname] = refs

# Category colors
CATEGORIES = {
    "workflow": (["ai-workflow", "brainstorming", "writing-plans", "executing-plans",
                  "finishing-branch", "verification", "tdd", "debugging"], "#FFE0B2"),
    "review":  (["code-review", "requesting-code-review", "receiving-code-review"], "#C8E6C9"),
    "agents":  (["agent-teams", "dispatching-parallel-agents", "subagent-driven-development"], "#E1BEE7"),
    "docs":    (["business-prd-planner", "doc-coauthoring", "pdf", "docx", "pptx", "xlsx"], "#B3E5FC"),
    "testing": (["api-testing", "e2e-test", "web-testing"], "#FFCDD2"),
    "infra":   (["migration", "directus-schema", "rbac", "backend-extension", "d11-frontend"], "#D7CCC8"),
    "meta":    (["skill-creator", "writing-skills", "router", "onboard", "progress", "team-health"], "#F0F4C3"),
}

# Output
out = sys.stdout
out.write("digraph skill_dependencies {\n")
out.write('  rankdir=LR;\n')
out.write('  node [shape=box, style="rounded,filled", fillcolor="#E8F4FD", fontname="Helvetica"];\n')
out.write('  edge [color="#666666"];\n\n')

for cat, (members, color) in CATEGORIES.items():
    for m in members:
        if m in skill_names:
            out.write(f'  "{m}" [fillcolor="{color}"];\n')

out.write("\n")

for src, targets in sorted(edges.items()):
    for tgt in sorted(targets):
        out.write(f'  "{src}" -> "{tgt}";\n')

out.write("\n  // Legend\n")
out.write('  subgraph cluster_legend {\n')
out.write('    label="Categories"; style=dashed; fontname="Helvetica";\n')
for cat, (_, color) in CATEGORIES.items():
    out.write(f'    "legend_{cat}" [label="{cat}", fillcolor="{color}"];\n')
out.write("  }\n}\n")

# Summary to stderr
total = sum(len(t) for t in edges.values())
print(f"\n# {total} edges from {len(edges)} source skills (out of {len(skill_names)} total)", file=sys.stderr)
