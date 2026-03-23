---
id: CARD-GSTACK-002
title: 重新生成 register.md 并更新 CLAUDE.md gstack 节
description: 将 gstack 的独有 skills 加入 general 路由体系；在 CLAUDE.md 声明 gstack 触发关键词和 skill 映射表
parent_story: US-GSTACK-001
parent_prd: PRD-GSTACK
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 运行 python3 .claude/skills/general/scripts/generate-register.py 重新生成 register.md
  - 确认 register.md 中包含 browse、qa、qa-only、careful、freeze、guard、unfreeze、codex、retro、ship、document-release、setup-browser-cookies、gstack-upgrade
  - 在 CLAUDE.md 的 Skills Index 表格中新增 gstack 行，列出触发关键词
  - 在 CLAUDE.md 增加 gstack 独立节，说明：路由规则（browse/qa/careful/codex 等关键词）+ 声明 browse 替代 mcp_chrome 工具
files_to_modify:
  - .claude/skills/general/references/register.md（重新生成）
  - CLAUDE.md（新增 gstack 节）
---
