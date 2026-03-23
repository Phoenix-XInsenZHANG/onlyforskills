---
id: US-CHAINS-002
title: User can trigger bug-fix, refactor, or deploy workflows via dedicated chains
description: 用户说"修复bug"/"重构"/"部署"时，路由到对应 chain，gstack codex/ship/qa 节点均为必经步骤
parent_prd: PRD-CHAINS
cards:
  - CARD-CHAINS-002
  - CARD-CHAINS-003
  - CARD-CHAINS-004
status: backlog
acceptance_criteria:
  - bug-fix-to-ship 重写，包含 codex[gstack] 节点在 requesting-code-review 之前
  - refactor-to-ship 新建，从 codex[gstack] 开始
  - deploy-pipeline 新建，包含 ship[gstack] + qa[gstack] 节点
  - 三条 chain 均使用统一标准格式
---
