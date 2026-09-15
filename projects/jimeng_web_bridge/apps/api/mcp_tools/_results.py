"""Shared MCP result shapes: structured content plus the same JSON as text; business errors as `is_error` text."""
import json
from collections.abc import Callable

from mcp.types import CallToolResult, TextContent

from apps.api.error_handlers import error_body
from apps.api.routes._helpers import to_json

TEXT_LIMIT_CHARS: int = 60000


def ok(value: object) -> CallToolResult:
    payload = to_json(value)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))[:TEXT_LIMIT_CHARS]
    structured = payload if isinstance(payload, dict) else {"result": payload}
    return CallToolResult(content=[TextContent(type="text", text=text)], structured_content=structured)


def failed(code: str, message: str) -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=f"{code}: {message}")], is_error=True)


def run(work: Callable[[], object]) -> CallToolResult:
    """Runs one Query/Command call; mapped business errors come back to the model as actionable text."""
    try:
        return ok(work())
    except Exception as error:  # every error is reported through the shared HTTP error table
        status, body = error_body(error)
        hint = f"（建议：{body['hint']}）" if body.get("hint") else ""
        return failed(str(body["error_code"]), f"{body['message']}{hint}（HTTP {status}）")
