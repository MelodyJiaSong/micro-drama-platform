from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from tools.service_request import RequestLog

T = TypeVar("T")


class AuditClient:
    def __init__(self, target: Path) -> None:
        self.log = RequestLog(target)

    def call(self, operation: str, request: dict, action: Callable[[], T]) -> T:
        return self.log.invoke("suno-browser", operation, request, action)
