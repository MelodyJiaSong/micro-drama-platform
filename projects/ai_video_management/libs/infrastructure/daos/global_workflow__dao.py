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
    parent: str = ""
    # Formats this source applies to; empty = shared by every format (follow-up 211).
    formats: tuple[str, ...] = ()
    # Shared sources this format page adapts: {"source_id", "section"}.
    adapts: tuple[dict[str, str], ...] = ()
