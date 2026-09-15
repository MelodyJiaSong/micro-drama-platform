from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult

from apps.api.container import Container
from apps.api.mcp_tools._results import failed, run


def register(server: MCPServer, container: Container) -> None:
    def entities(action: str = "reconcile", drama: str | None = None) -> CallToolResult:
        """即梦人物主体：action=reconcile 对账各剧期望主体名与最近一次同步的主体快照（只读）。

        drama：可选，`ai_videos/…` 形式的剧根，只看这部剧的映射。
        """
        if action != "reconcile":
            return failed("invalid_action", f"不支持的 action：{action}（当前可用：reconcile）")
        return run(lambda: container.entity_query().reconcile(drama))

    server.add_tool(entities, name="entities", description=entities.__doc__)
