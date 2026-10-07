from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GlobalSourceDao:
    id: str
    path: str
    title: str
    group: str
    scope: str
    view: str
    status: str
    historical: bool = False
    number: str = ""
