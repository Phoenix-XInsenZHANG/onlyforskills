# gstack Integration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 gstack 的 11 个独有 skills 结构性引入 `.claude/skills/gstack/`，并将 gstack 的三个最佳框架（Completeness Principle、SQL/LLM 检查清单、Completion Status Protocol）内容提炼进现有 .claude skills。

**Architecture:** 精选合并 + 内容提炼（方案 C）。阶段一完成结构引入和路由注册；阶段二修改 5 个现有 skill 文件注入框架内容。两阶段互不依赖，可并行执行。

**Tech Stack:** Bash（setup 构建）、Python3（register.md 生成）、Markdown（skill 文件编辑）

**Cards:** CARD-GSTACK-001 ~ CARD-GSTACK-005

---

## Chunk 1: 结构引入 (CARD-GSTACK-001 + CARD-GSTACK-002)

### Task 1: 复制 gstack 到 .claude/skills/gstack/ 并构建二进制

**@card CARD-GSTACK-001**

**Files:**
- Create: `.claude/skills/gstack/`（从 `gstack/` 复制，不含 `.git`）

- [ ] **Step 1: 确认 Bun 已安装**

```bash
bun --version
```

期望输出：`1.x.x` 或更高。如果未安装，访问 https://bun.sh 安装。

- [ ] **Step 2: 将 gstack 复制到正确路径**

```bash
cp -Rf /Users/Zhuanz/Desktop/onlyforskills/gstack /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/gstack
rm -rf /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/gstack/.git
```

验证：
```bash
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/gstack/
```
期望看到：`bin/  browse/  qa/  careful/  freeze/  guard/  review/  ship/  SKILL.md` 等目录。

- [ ] **Step 3: 运行 setup 构建二进制**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/gstack && ./setup
```

期望输出包含：构建成功信息，`bin/` 中生成 `gstack-config`、`browse` 等可执行文件。

- [ ] **Step 4: 验证二进制可用**

```bash
~/.claude/skills/gstack/bin/gstack-config get proactive 2>/dev/null || \
.claude/skills/gstack/bin/gstack-config get proactive 2>/dev/null || echo "binary path issue"
```

期望输出：`true` 或空字符串（不是 "binary path issue"）。

- [ ] **Step 5: 提交结构变更**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/gstack/
git commit -m "feat: add gstack skills namespace under .claude/skills/gstack/

@card CARD-GSTACK-001
- Copy gstack 21 skills to .claude/skills/gstack/
- Build binaries via ./setup (browse binary, gstack-config, etc.)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: 重新生成 register.md 并更新 CLAUDE.md

**@card CARD-GSTACK-002**

**Files:**
- Modify: `.claude/skills/general/references/register.md`（重新生成）
- Modify: `CLAUDE.md`（新增 gstack 节）

- [ ] **Step 1: 重新生成 register.md**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
python3 .claude/skills/general/scripts/generate-register.py
```

期望输出：提示扫描到的 skill 数量增加（应从 56/61 增加到包含 gstack skills）。

- [ ] **Step 2: 验证 register.md 包含 gstack skills**

```bash
grep -c "gstack/" /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/general/references/register.md
```

期望输出：>= 10（browse, qa, qa-only, careful, freeze, guard, unfreeze, codex, retro, ship, document-release 等）。

- [ ] **Step 3: 在 CLAUDE.md 中添加 gstack 节**

在 `CLAUDE.md` 的 `Skills Index` 表格中添加 gstack 行，并在文件末尾添加以下独立节：

在 Skills Index 表格新增行：
```
| "browse", "QA", "点击测试", "ship", "production" | `gstack/*` | gstack 独有工具链 |
```

在文件末尾新增：
```markdown
## gstack 工具链

gstack 补充了 .claude 体系中缺失的执行层工具。**始终使用 `/browse` 替代任何 `mcp__claude-in-chrome__*` 工具进行 web 浏览。**

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
```
```

- [ ] **Step 4: 验证 CLAUDE.md 已正确更新**

```bash
grep -c "gstack" /Users/Zhuanz/Desktop/onlyforskills/CLAUDE.md
```

期望输出：>= 15（多处提及 gstack）。

- [ ] **Step 5: 提交**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/general/references/register.md CLAUDE.md
git commit -m "feat: register gstack skills in router and add CLAUDE.md gstack section

@card CARD-GSTACK-002
- Regenerate register.md to include gstack's 11+ unique skills
- Add gstack section to CLAUDE.md with routing rules and skill index
- Declare browse as replacement for mcp__claude-in-chrome__* tools

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Chunk 2: 内容提炼 (CARD-GSTACK-003 + CARD-GSTACK-004 + CARD-GSTACK-005)

> 此 chunk 修改 5 个现有 .claude skill 文件，注入 gstack 的三个框架。
> 建议先读完目标文件再编辑，避免破坏现有结构。

### Task 3: 注入 Completeness Principle 到 brainstorming 和 tdd

**@card CARD-GSTACK-003**

**Files:**
- Modify: `.claude/skills/brainstorming/SKILL.md`（在 Key Principles 章节前，约第 245 行）
- Modify: `.claude/skills/tdd/SKILL.md`（在文件末尾 "Remember" 或 "Key Principles" 后）

**要注入的内容（从 gstack/review/SKILL.md 提炼）：**

```markdown
## Completeness Principle — Boil the Lake

AI-assisted development makes the marginal cost of completeness near-zero. When evaluating options:

- **Always recommend the complete implementation** over shortcuts when the delta is small. 80 lines vs 150 lines is meaningless with AI assistance.
- **Lake vs. ocean:** A "lake" is boilable — full feature implementation, 100% coverage for a module, all edge cases handled. An "ocean" is not — full system rewrites, multi-quarter migrations. Recommend boiling lakes; flag oceans as out of scope.
- **Show both effort scales** when estimating work:

| Task type | Human team | With AI | Compression |
|-----------|-----------|---------|-------------|
| Boilerplate / scaffolding | 2 days | 15 min | ~100x |
| Test writing | 1 day | 15 min | ~50x |
| Feature implementation | 1 week | 30 min | ~30x |
| Bug fix + regression test | 4 hours | 15 min | ~20x |
| Architecture / design | 2 days | 4 hours | ~5x |
| Research / exploration | 1 day | 3 hours | ~3x |

**Anti-patterns:**
- BAD: "Choose B — it covers 90% of the value." (If A costs 70 more lines, choose A.)
- BAD: "Defer test coverage to a follow-up PR." (Tests are the cheapest lake to boil.)
- BAD: Quoting only human effort: "This takes 2 weeks." (Say: "2 weeks human / ~1 hour with AI.")
```

- [ ] **Step 1: 读取 brainstorming/SKILL.md 确认注入位置**

```bash
grep -n "Key Principles\|Exploring approaches\|After the Design" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/brainstorming/SKILL.md
```

期望看到 "Key Principles" 在约 245 行、"Exploring approaches" 在约 100 行。

- [ ] **Step 2: 在 brainstorming/SKILL.md 的 "Key Principles" 前注入 Completeness Principle**

使用 Edit 工具，在 `## Key Principles` 前插入上述 Completeness Principle 内容块。

验证：
```bash
grep -c "Boil the Lake\|Completeness Principle" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/brainstorming/SKILL.md
```
期望输出：>= 2

- [ ] **Step 3: 读取 tdd/SKILL.md 确认注入位置**

```bash
grep -n "coverage\|Remember\|Key Principle\|complete\|DONE" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tdd/SKILL.md | tail -15
```

- [ ] **Step 4: 在 tdd/SKILL.md 末尾追加 Completeness Principle（测试覆盖率版本）**

在文件末尾追加：

```markdown
## Completeness Principle for Tests

AI makes test writing near-zero marginal cost. Apply these rules:

- **Never defer test coverage** — adding missing tests costs ~15 min with AI vs 1 day human time
- **100% coverage for the module you're touching is a lake, not an ocean** — always boil it
- If writing 3 happy-path tests, write the 2 negative-path tests too. The delta is minutes.
- **Anti-pattern:** "I'll add edge case tests in a follow-up" — this never happens. Do it now.

Show both effort estimates when suggesting test scope:
- "Adding these 5 edge-case tests: ~2 days human / ~10 min with AI"
```

验证：
```bash
grep -c "Completeness Principle\|lake" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tdd/SKILL.md
```
期望输出：>= 2

- [ ] **Step 5: 提交**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/brainstorming/SKILL.md .claude/skills/tdd/SKILL.md
git commit -m "feat: inject Completeness Principle (Boil the Lake) into brainstorming and tdd

@card CARD-GSTACK-003
- brainstorming: add Completeness Principle + AI vs human time compression table before Key Principles
- tdd: add Completeness Principle for test coverage decisions at end of skill

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: 注入 SQL 安全 + LLM 信任边界检查清单到 code-review

**@card CARD-GSTACK-004**

**Files:**
- Modify: `.claude/skills/code-review/SKILL.md`（在 CRITICAL ISSUES 章节前）

**要注入的内容：**

```markdown
## Security & Trust Boundary Checklist

Run this checklist during every code review. These are **CRITICAL** — flag any violation.

### SQL & Data Safety
- [ ] No string interpolation in SQL queries (use parameterized queries: `sanitize_sql_array`, prepared statements, `?` placeholders)
- [ ] No TOCTOU races: check-then-set patterns should use atomic `WHERE` + `UPDATE` instead
- [ ] No bypassing model validations for direct DB writes (`update_column`, `QuerySet.update()`, raw queries)
- [ ] No N+1 queries: associations used in loops should be eager-loaded (`.includes()`, `joinedload()`, `include:`)

### LLM Output Trust Boundary
- [ ] LLM-generated values (emails, URLs, names) validated before DB writes or external calls — add lightweight guards (`EMAIL_REGEXP`, `URI.parse`, `.strip`)
- [ ] Structured tool output (arrays, hashes) type/shape-checked before database writes
- [ ] User-controlled data NOT passed to unsafe HTML rendering (`html_safe`, `dangerouslySetInnerHTML`, `v-html`, `|safe`)
- [ ] LLM prompt text does not list tools/capabilities that aren't actually wired up

### Race Conditions
- [ ] find-or-create has unique DB index to prevent concurrent duplicate creation
- [ ] Status transitions use atomic `WHERE old_status = ? UPDATE SET new_status` pattern
- [ ] Read-check-write patterns protected by uniqueness constraint or duplicate-key retry

### Enum & Value Completeness
When a new enum value, status, or type constant appears in the diff:
- [ ] Traced through all consumers (switch/case, if-elsif, filter arrays) — READ the files, don't just grep
- [ ] All `%w[]` allowlists and `case` branches updated to handle the new value
- [ ] Frontend and backend both handle the new value consistently
```

- [ ] **Step 1: 读取 code-review/SKILL.md 找到注入位置**

```bash
grep -n "CRITICAL ISSUES\|## Phase\|## Step\|checklist" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/code-review/SKILL.md | head -20
```

找到 `### ❌ CRITICAL ISSUES` 附近的行号作为注入锚点（约第 387 行）。

- [ ] **Step 2: 检查现有 code-review 是否已有 SQL/LLM 检查**

```bash
grep -c "SQL\|LLM\|parameterized\|trust boundary" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/code-review/SKILL.md
```

如果输出 > 0，说明已有部分覆盖，注入时避免重复。

- [ ] **Step 3: 在 `### ❌ CRITICAL ISSUES` 前注入 Security & Trust Boundary Checklist**

使用 Edit 工具，在该章节前插入上述检查清单内容。

验证：
```bash
grep -c "SQL & Data Safety\|LLM Output Trust Boundary\|parameterized" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/code-review/SKILL.md
```
期望输出：>= 3

- [ ] **Step 4: 暂存（与 Task 5 一起提交）**

```bash
git add /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/code-review/SKILL.md
```

---

### Task 5: 注入 Completion Status Protocol 到 debugging、code-review、verification

**@card CARD-GSTACK-005**

**Files:**
- Modify: `.claude/skills/debugging/SKILL.md`（末尾追加）
- Modify: `.claude/skills/code-review/SKILL.md`（末尾追加，与 Task 4 同文件）
- Modify: `.claude/skills/verification/SKILL.md`（末尾追加）

**要注入的内容（三个文件相同）：**

```markdown
## Completion Status Protocol

When finishing this skill's workflow, always report using one of these statuses:

- **DONE** — All steps completed. Evidence provided for each claim. No unverified assertions.
- **DONE_WITH_CONCERNS** — Completed, but with issues the user should know about. List each concern explicitly.
- **BLOCKED** — Cannot proceed. State what is blocking and what was tried.
- **NEEDS_CONTEXT** — Missing information required to continue. State exactly what you need.

### Escalation Rules

Bad work is worse than no work. Escalate when:
- Attempted the same task 3 times without success → STOP
- Uncertain about a security-sensitive change → STOP
- Scope of work exceeds what you can verify → STOP

Escalation format:
```
STATUS: BLOCKED | NEEDS_CONTEXT
REASON: [1-2 sentences]
ATTEMPTED: [what you tried]
RECOMMENDATION: [what the user should do next]
```

**Verification rule:** Before claiming something is "handled" or "tested" — cite the specific file and line. Never say "likely handled" or "probably tested."
```

- [ ] **Step 1: 追加 Status Protocol 到 debugging/SKILL.md**

使用 Edit 工具，在文件末尾（"Real-World Impact" 章节之后）追加 Completion Status Protocol 内容。

验证：
```bash
grep -c "DONE_WITH_CONCERNS\|Completion Status Protocol\|BLOCKED" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/debugging/SKILL.md
```
期望输出：>= 3

- [ ] **Step 2: 追加 Status Protocol 到 code-review/SKILL.md**

使用 Edit 工具，在文件最末尾追加 Completion Status Protocol 内容。

验证：
```bash
grep -c "DONE_WITH_CONCERNS\|Completion Status Protocol" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/code-review/SKILL.md
```
期望输出：>= 2

- [ ] **Step 3: 追加 Status Protocol 到 verification/SKILL.md**

使用 Edit 工具，在 "This is non-negotiable." 末尾追加 Completion Status Protocol 内容。

验证：
```bash
grep -c "DONE_WITH_CONCERNS\|Completion Status Protocol" \
  /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/verification/SKILL.md
```
期望输出：>= 2

- [ ] **Step 4: 验证三个文件格式一致**

```bash
for f in debugging code-review verification; do
  echo "=== $f ==="
  grep "Completion Status Protocol" \
    /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/$f/SKILL.md
done
```

期望三个文件都有匹配行。

- [ ] **Step 5: 提交 Task 4 + Task 5 的所有修改**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/code-review/SKILL.md \
        .claude/skills/debugging/SKILL.md \
        .claude/skills/verification/SKILL.md
git commit -m "feat: inject SQL/LLM checklist and Status Protocol from gstack into .claude skills

@card CARD-GSTACK-004 @card CARD-GSTACK-005
- code-review: add Security & Trust Boundary checklist (SQL safety, LLM trust boundary, race conditions, enum completeness)
- debugging: add Completion Status Protocol (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT)
- code-review: add Completion Status Protocol
- verification: add Completion Status Protocol

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 验收检查（全部完成后运行）

```bash
# 1. gstack binaries 可用
.claude/skills/gstack/bin/gstack-config get proactive && echo "✅ gstack binary OK"

# 2. register.md 包含 gstack skills
python3 .claude/skills/general/scripts/generate-register.py
grep "gstack/browse\|gstack/qa\|gstack/careful" \
  .claude/skills/general/references/register.md && echo "✅ register.md OK"

# 3. CLAUDE.md 有 gstack 节
grep "gstack 工具链\|gstack/browse" CLAUDE.md && echo "✅ CLAUDE.md OK"

# 4. brainstorming 注入成功
grep "Boil the Lake" .claude/skills/brainstorming/SKILL.md && echo "✅ brainstorming OK"

# 5. code-review 注入成功
grep "SQL & Data Safety\|LLM Output Trust Boundary" .claude/skills/code-review/SKILL.md && echo "✅ code-review OK"

# 6. Status Protocol 三处注入
for f in debugging code-review verification; do
  grep -q "DONE_WITH_CONCERNS" .claude/skills/$f/SKILL.md && echo "✅ $f Status Protocol OK"
done
```

全部输出 ✅ 代表实施完成。
