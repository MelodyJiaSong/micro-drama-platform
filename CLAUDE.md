# CLAUDE.md — Claude Code 入口

@AGENTS.md

共用业务约定由 `AGENTS.md` 路由到 `CONVENTIONS.md`、skills 与 refs；不要在本文件维护第二份。
若当前客户端不展开 `@` 导入，开工先读取 `AGENTS.md`，再按其路由读取详细约定。

Claude 专用 hooks / env / permissions 在 `.claude/settings*.json`，MCP 声明在 `.mcp.json`。
它们不代表 Codex 已加载相同配置。工具名与权限以实际会话为准。
