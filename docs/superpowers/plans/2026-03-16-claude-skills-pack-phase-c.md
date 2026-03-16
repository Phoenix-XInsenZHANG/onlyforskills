# Claude Skills Pack - Phase C: Skills 整合实现计划

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从已安装的插件复制 33 个 skills 到项目的 `.claude/skills/` 目录，实现完全自包含。

**Architecture:** 按层级组织：workflow/（14个）、design/（2个）、docs/（7个）、tools/（6个）、保留现有 domain/（18个）。

**Tech Stack:** 文件复制，目录结构重组

**Spec:** `docs/superpowers/specs/2026-03-16-claude-skills-pack-design.md`

---

## 源目录映射

| 来源 | 源路径 |
|------|--------|
| Superpowers | `/Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/` |
| Example-skills | `/Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/` |
| UI-UX-Pro-Max | `/Users/Zhuanz/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.0.1/` |
| Planning-with-files | `/Users/Zhuanz/.claude/plugins/cache/planning-with-files/planning-with-files/2.23.0/skills/` |

---

## Chunk 1: Workflow 层 - Superpowers Skills

### Task 1: 复制 Superpowers Skills（14 个）

**Files:**
- Copy: 14 个 skill 目录到 `.claude/skills/workflow/`

- [ ] **Step 1: 复制 brainstorming**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/brainstorming \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 2: 复制 test-driven-development**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/test-driven-development \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/tdd
```

注意：重命名为 `tdd`

- [ ] **Step 3: 复制 systematic-debugging**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/systematic-debugging \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/debugging
```

注意：重命名为 `debugging`

- [ ] **Step 4: 复制 writing-plans**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/writing-plans \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 5: 复制 executing-plans**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/executing-plans \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 6: 复制 subagent-driven-development**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/subagent-driven-development \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 7: 复制 dispatching-parallel-agents**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/dispatching-parallel-agents \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 8: 复制 using-git-worktrees**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/using-git-worktrees \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/git-worktrees
```

注意：重命名为 `git-worktrees`

- [ ] **Step 9: 复制 finishing-a-development-branch**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/finishing-a-development-branch \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/finishing-branch
```

注意：重命名为 `finishing-branch`

- [ ] **Step 10: 复制 requesting-code-review**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/requesting-code-review \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 11: 复制 receiving-code-review**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/receiving-code-review \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 12: 复制 verification-before-completion**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/verification-before-completion \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/verification
```

注意：重命名为 `verification`

- [ ] **Step 13: 复制 writing-skills**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/superpowers-marketplace/superpowers/5.0.2/skills/writing-skills \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

- [ ] **Step 14: 验证 workflow 层**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/
```

Expected: 13 个目录

---

## Chunk 2: Design 层

### Task 2: 复制设计相关 Skills

**Files:**
- Copy: `frontend-design` 到 `.claude/skills/design/`
- Copy: UI-UX 系统到 `.claude/skills/design/`

- [ ] **Step 1: 复制 frontend-design**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/frontend-design \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/
```

- [ ] **Step 2: 复制 UI-UX 系统文件**

UI-UX-Pro-Max 结构不同，需要手动整合：

```bash
mkdir -p /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/ui-ux-system/references

# 复制 CLAUDE.md 作为主要参考
cp /Users/Zhuanz/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.0.1/CLAUDE.md \
   /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/ui-ux-system/SKILL.md
```

- [ ] **Step 3: 验证 design 层**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/
```

Expected: 2 个目录

---

## Chunk 3: Docs 层

### Task 3: 复制文档处理 Skills

**Files:**
- Copy: 7 个文档 skills 到 `.claude/skills/docs/`

- [ ] **Step 1: 批量复制文档 skills**

```bash
cd /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/

for skill in pdf pptx docx xlsx canvas-design doc-coauthoring theme-factory; do
  cp -r "$skill" /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/docs/
done
```

- [ ] **Step 2: 验证 docs 层**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/docs/
```

Expected: 7 个目录

---

## Chunk 4: Tools 层

### Task 4: 复制工具 Skills

**Files:**
- Copy: 6 个工具 skills 到 `.claude/skills/tools/`

- [ ] **Step 1: 复制 mcp-builder**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/mcp-builder \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

- [ ] **Step 2: 复制 skill-creator**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/skill-creator \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

- [ ] **Step 3: 复制 claude-api**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/claude-api \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

- [ ] **Step 4: 复制 algorithmic-art**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/algorithmic-art \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

- [ ] **Step 5: 复制 web-artifacts-builder**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/anthropic-agent-skills/example-skills/b0cbd3df1533/skills/web-artifacts-builder \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

- [ ] **Step 6: 复制 planning-with-files**

```bash
cp -r /Users/Zhuanz/.claude/plugins/cache/planning-with-files/planning-with-files/2.23.0/skills/planning-with-files \
      /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/planning
```

注意：重命名为 `planning`

- [ ] **Step 7: 验证 tools 层**

```bash
ls -la /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/
```

Expected: 6 个目录

---

## Chunk 5: 迁移现有 Domain Skills

### Task 5: 迁移现有 skills 到 domain 层

**Files:**
- Move: 现有 skills 到 `.claude/skills/domain/`

- [ ] **Step 1: 创建 domain 目录**

```bash
mkdir -p /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/domain
```

- [ ] **Step 2: 迁移 Directus 相关 skills**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills/.claude/skills

# 迁移 Directus 相关
mv directus-schema domain/
mv d11-frontend domain/
mv rbac domain/
mv backend-extension domain/
mv migration domain/
```

- [ ] **Step 3: 迁移项目管理 skills**

```bash
mv ai-workflow domain/
mv pm-comments domain/
mv progress domain/
mv visualizer domain/
```

- [ ] **Step 4: 迁移其他 skills**

```bash
mv landing-page domain/
mv landing-audit domain/
mv agent-teams domain/
mv team-health domain/
mv meta-evaluation domain/
mv context-review domain/
mv business-prd-planner domain/
mv business-report domain/
mv user-journey-mapper domain/
```

- [ ] **Step 5: 保留 api-testing 在 testing 层**

```bash
# api-testing 保留在 testing 层，不迁移
mv api-testing ../testing/
```

- [ ] **Step 6: 验证迁移结果**

```bash
ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/domain/
```

Expected: 18 个目录（现有 skills 数量）

---

## Chunk 6: 更新 SKILL-CATALOG.md

### Task 6: 更新完整技能索引

**Files:**
- Modify: `.claude/skills/SKILL-CATALOG.md`

- [ ] **Step 1: 更新 workflow 层详情**

在 SKILL-CATALOG.md 的 workflow 部分添加每个 skill 的详细触发词。

- [ ] **Step 2: 更新 design 层详情**

- [ ] **Step 3: 更新 docs 层详情**

- [ ] **Step 4: 更新 tools 层详情**

- [ ] **Step 5: 更新 domain 层详情**

---

## Chunk 7: 验证与提交

### Task 7: 验证完整性

- [ ] **Step 1: 统计各层 skills 数量**

```bash
echo "=== Workflow ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/workflow/ | wc -l
echo "=== Testing ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/testing/ | wc -l
echo "=== Design ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/design/ | wc -l
echo "=== Docs ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/docs/ | wc -l
echo "=== Tools ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/tools/ | wc -l
echo "=== Domain ===" && ls /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/domain/ | wc -l
```

Expected:
- Workflow: 13
- Testing: 2
- Design: 2
- Docs: 7
- Tools: 6
- Domain: 18
- **Total: 48 skills**

- [ ] **Step 2: 验证目录结构**

```bash
tree -L 2 /Users/Zhuanz/Desktop/onlyforskills/.claude/skills/
```

- [ ] **Step 3: 提交 Phase C 完成**

```bash
cd /Users/Zhuanz/Desktop/onlyforskills
git add .claude/skills/
git commit -m "feat(skills): integrate all skills from plugins

- Add 13 workflow skills from Superpowers
- Add 2 design skills (frontend-design, ui-ux-system)
- Add 7 docs skills (pdf, pptx, docx, etc.)
- Add 6 tools skills (mcp-builder, skill-creator, etc.)
- Migrate 18 existing skills to domain layer
- Update SKILL-CATALOG.md with all skills

Phase C of Claude Skills Pack implementation."
```

---

## 完成检查

- [ ] Workflow 层包含 13 个 skills
- [ ] Testing 层包含 2 个 skills（web-testing + api-testing）
- [ ] Design 层包含 2 个 skills
- [ ] Docs 层包含 7 个 skills
- [ ] Tools 层包含 6 个 skills
- [ ] Domain 层包含 18 个 skills
- [ ] SKILL-CATALOG.md 已更新
- [ ] Git 提交完成

---

## 下一步

Phase C 完成后，继续执行：
- **Phase D**: 分发包（README + 清理）
