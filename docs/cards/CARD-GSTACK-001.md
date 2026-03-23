---
id: CARD-GSTACK-001
title: 将 gstack 目录复制到 .claude/skills/gstack/ 并构建二进制
description: 将 gstack/ 复制到正确的 skill 路径，运行 ./setup 构建 browse binary 和 gstack-config 等工具
parent_story: US-GSTACK-001
parent_prd: PRD-GSTACK
status: backlog
priority: high
estimate: 1h
implementation_checklist:
  - 将 gstack/ 复制到 .claude/skills/gstack/（不含 .git）
  - 检查 setup 脚本依赖（Bun v1.0+）
  - 运行 cd .claude/skills/gstack && ./setup
  - 验证 bin/gstack-config 和 bin/browse（或等效）可执行
  - 验证 ~/.gstack/ 目录已创建
files_to_modify:
  - .claude/skills/gstack/（新增目录）
---
