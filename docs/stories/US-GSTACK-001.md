---
id: US-GSTACK-001
title: 用户可以使用 gstack 的独有工具（browse/qa/careful/freeze/codex/retro/ship）
description: gstack 的 11 个独有 skills 被注册进 .claude 体系，用户通过 general 路由可以发现并调用它们
parent_prd: PRD-GSTACK
cards:
  - CARD-GSTACK-001
  - CARD-GSTACK-002
status: backlog
acceptance_criteria:
  - gstack 目录已复制到 .claude/skills/gstack/
  - ./setup 构建成功，bin/ 中有可执行的 gstack-config 和 browse binary
  - register.md 重新生成后包含 gstack 的独有 skills（browse, qa, careful, freeze, guard, unfreeze, codex, retro, ship, document-release, setup-browser-cookies, gstack-upgrade）
  - CLAUDE.md 有 gstack 节，列出触发关键词和 skill 映射
  - general skill 路由时能正确区分 gstack 独有 skill 和 .claude 已有 skill 的意图
---
