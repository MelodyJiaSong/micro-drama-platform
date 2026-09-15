"""MCP tools — transport-edge wrappers, one tool per Query/Command method (spec v2 §8 divergence 1)."""
from mcp.server.mcpserver import MCPServer

from apps.api.container import Container
from apps.api.mcp_tools import entity__tool, session__tool

SERVER_NAME: str = "jimeng_bridge"
_INSTRUCTIONS: str = (
    "即梦桥接服务。你可以预检批次、查询与等待作业、取消与恢复、分步调试到预演、同步与对账主体。"
    "你不能确认批次或提交生成：确认只在本地管理网页由人完成，工具会返回确认页链接。"
)


def build_mcp_server(container: Container) -> MCPServer:
    server = MCPServer(SERVER_NAME, title="即梦桥接", instructions=_INSTRUCTIONS)
    for module in (session__tool, entity__tool):
        module.register(server, container)
    return server
