#!/usr/bin/env bash
# .claude/hooks/force-general-gate.sh
#
# UserPromptSubmit hook — 在每次用户输入时注入 additionalContext，
# 强制 Claude 先执行 general skill 的两阶段确认流程。
#
# 工作原理：
#   UserPromptSubmit hook 的 stdout JSON 中的 additionalContext
#   会被注入到 Claude 可见的上下文中，作为强制指令。

set -euo pipefail

# 读取 stdin（hook 输入 JSON）
INPUT=$(cat)

# 提取用户的 prompt 内容
PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""')

# ── 白名单检测：这些情况跳过强制路由 ──
SKIP=false

# 用户明确说跳过
if echo "$PROMPT" | grep -qiE '跳过确认|不用问我|直接做|skip confirm'; then
  SKIP=true
fi

# 用户明确指定了 skill 名称（"用 xxx skill" 或 "/xxx"）
if echo "$PROMPT" | grep -qiE '用\s*\S+\s*skill|走\s*\S+\s*流程|/[a-z]'; then
  SKIP=true
fi

# ── 如果不在白名单中，注入强制路由指令 ──
if [ "$SKIP" = "false" ]; then
  cat <<'HOOK_JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "⛔ MANDATORY ROUTING GATE: 在执行用户的任何请求之前，你必须先执行 general skill 的两阶段确认流程。步骤：1) 读取 .claude/skills/general/references/register.md（如不存在则运行 python3 .claude/skills/general/scripts/generate-register.py 生成）；2) 使用 AskUserQuestion 询问用户选择执行模式（工具链/单独Skill/直接处理）；3) 等待用户回复后再继续。禁止跳过此流程直接执行任务。"
  }
}
HOOK_JSON
fi

exit 0