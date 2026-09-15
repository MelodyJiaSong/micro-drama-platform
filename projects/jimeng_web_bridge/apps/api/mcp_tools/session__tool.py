from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult

from apps.api.container import Container
from apps.api.mcp_tools._results import run


def register(server: MCPServer, container: Container) -> None:
    def session_status() -> CallToolResult:
        """即梦桥接服务的会话快照（只读）：网页登录与最近一次 canary、CLI 登录/版本/余额、各队列是否暂停、今日已确认积分。

        不会在调用里启动浏览器、跑 canary 或调用 CLI；需要刷新时请人在管理网页的「会话」页点「运行 canary」。
        """
        return run(lambda: container.session_query().status())

    server.add_tool(session_status, name="session_status", description=session_status.__doc__)
