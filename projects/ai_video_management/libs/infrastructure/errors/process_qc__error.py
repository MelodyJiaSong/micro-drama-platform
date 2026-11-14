"""流程与自检读取失败（剧不存在、登记表不可解析等）。"""
from __future__ import annotations


class ProcessQcError(Exception):
    def __init__(self, message: str, status_code: int = 404) -> None:
        super().__init__(message)
        self.status_code = status_code
