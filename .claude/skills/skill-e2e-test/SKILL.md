---
name: skill-e2e-test
description: E2E test suite for the skills framework. Use when asked to test skills, run skill evals, check skill health, validate the skill framework, measure trigger rate or chain completion rate, or run the P1/P2/P3/P4 test suite. Invoke before any skill quality assessment.
---

# Skill E2E Test Suite

Runs a four-tier quantitative test suite against `.claude/skills/` and outputs a scored report.

## Announce at start

Say: "Running skill-e2e-test. This will take several minutes and make multiple `claude -p` calls."

## Prerequisites check

```bash
# Confirm we're in the repo root
ls .claude/skills/ | head -5
# Confirm claude CLI available
claude --version
```

If `.claude/skills/` doesn't exist, stop and tell the user.

## Test execution order

Run all four phases in sequence. Each phase writes its result to `.skill-test-results/`.

```bash
mkdir -p .skill-test-results
```

---

## Phase P0 — Structure validation (zero cost)

Run `scripts/p0_validate.py`. This checks every SKILL.md for:
- Required frontmatter fields (`name`, `description`)
- `name` is kebab-case, ≤ 64 chars
- `description` has no `<>`, ≤ 1024 chars
- No unexpected frontmatter keys

```bash
python3 .claude/skills/skill-e2e-test/scripts/p0_validate.py \
  --skills-dir .claude/skills \
  --output .skill-test-results/p0.json
```

**Pass threshold:** 100% (structure errors are blocking)

---

## Phase P3 — Leaf node trigger rate (CI gate)

Run `scripts/p3_trigger.py` against every skill that has no outbound references in the graph (independent skills: pdf, xlsx, docx, frontend-design, web-testing, api-testing, etc.).

```bash
python3 .claude/skills/skill-e2e-test/scripts/p3_trigger.py \
  --skills-dir .claude/skills \
  --output .skill-test-results/p3.json \
  --max-turns 3 \
  --repeats 3 \
  --threshold 0.75
```

This script:
1. Reads `evals/trigger_evals.json` for should-trigger / should-not-trigger queries per skill
2. Calls `claude -p` 3 times per query (majority vote)
3. Parses `stream-json` output for `{"type":"tool_use","name":"Skill","input":{"skill":"<name>"}}`
4. Outputs per-skill trigger rate and overall pass/fail

**Pass threshold:** ≥ 75% per skill, ≥ 80% overall

---

## Phase P1 — Hub node chain propagation

Run `scripts/p1_chain.py` against the four long chains. Uses prompts designed to force auto-proceed through all skills without interactive approval. No turn limit — chains must complete regardless of how many turns it takes.

```bash
python3 .claude/skills/skill-e2e-test/scripts/p1_chain.py \
  --skills-dir .claude/skills \
  --output .skill-test-results/p1.json \
  --max-turns 0 \
  --repeats 2
```

`--max-turns 0` means unlimited turns. The script should let the session run until it either completes the chain or the LLM stops naturally.

Chain definitions (from `evals/chains.json`):
- `full-feature-lifecycle` (6 steps): brainstorming → ai-workflow → writing-plans → tdd → subagent-driven-development → executing-plans
- `bug-fix-to-ship` (5 steps): debugging → tdd → verification → requesting-code-review → finishing-branch
- `product-idea-to-code` (6 steps): business-prd-planner → ai-workflow → writing-plans → subagent-driven-development → executing-plans → verification
- `backend-feature-full-stack` (7 steps): brainstorming → ai-workflow → backend-extension → migration → directus-schema → api-testing → verification

**Pass threshold:** ≥ 60% chain completion rate (LLM behavior is probabilistic)

---

## Phase P4 — Loop / deadlock detection

Run `scripts/p4_loop.py`. Uses a tight turn budget and checks for repeated skill invocations.

```bash
python3 .claude/skills/skill-e2e-test/scripts/p4_loop.py \
  --skills-dir .claude/skills \
  --output .skill-test-results/p4.json \
  --max-turns 20
```

Checks:
- No skill appears twice in one session's sequence
- Session terminates with `stop=success`, not `error_max_turns`

**Pass threshold:** 0 loops detected

---

## Phase P2 — Business chain integrity (nightly only)

Only run P2 if the user explicitly says "full" or "nightly". It's expensive (~$2-5 per run).

```bash
python3 .claude/skills/skill-e2e-test/scripts/p2_business.py \
  --skills-dir .claude/skills \
  --output .skill-test-results/p2.json \
  --max-turns 20 \
  --repeats 2
```

Chain definitions:
- `ai-workflow → api-testing, directus-schema, pm-comments`
- `backend-extension → api-testing, directus-schema, migration`

---

## Report generation

After all phases complete:

```bash
python3 .claude/skills/skill-e2e-test/scripts/report.py \
  --results-dir .skill-test-results \
  --output .skill-test-results/report.json
```

Then print a summary table in this exact format:

```
╔══════════════════════════════════════════════════════╗
║           Skill E2E Test Report                      ║
╠══════════╦═══════════╦══════════╦════════╦══════════╣
║ Phase    ║ Score     ║ Threshold║ Status ║ Cost     ║
╠══════════╬═══════════╬══════════╬════════╬══════════╣
║ P0 Valid ║ 52/52     ║ 100%     ║ ✅ PASS ║ $0.00   ║
║ P3 Trig  ║ 78%       ║ 75%      ║ ✅ PASS ║ $1.20   ║
║ P1 Chain ║ 2/3 steps ║ 60%      ║ ✅ PASS ║ $0.80   ║
║ P4 Loop  ║ 0 loops   ║ 0        ║ ✅ PASS ║ $0.40   ║
╠══════════╬═══════════╬══════════╬════════╬══════════╣
║ OVERALL  ║           ║          ║ ✅ PASS ║ $2.40   ║
╚══════════╩═══════════╩══════════╩════════╩══════════╝
```

## CI gate rule

Overall PASS requires P0 + P3 both passing. P1 and P4 failures are warnings, not blockers (LLM behavior is probabilistic). P2 is never a CI gate.

## Key insight: P3 prompt design

For trigger tests, prompts must be **natural and ambiguous enough** that Claude must rely on skill descriptions to decide. Bad: "use the pdf skill to...". Good: "把这份报告保存成文件". See `evals/trigger_evals.json` for examples.

## Key insight: P1 chain prompts

Chain prompts must include "no approval needed, auto-proceed through all steps" to bypass the interactive confirmation gates that brainstorming and writing-plans build in. Without this, the chain stalls after the first skill.
