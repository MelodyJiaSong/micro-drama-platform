from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libs.application.dtos.global_workflow__dto import GlobalWorkflowQdto
from libs.common.global_workflow import GlobalWorkflowError
from libs.infrastructure.readers.global_workflow__reader import GlobalWorkflowReader


class GlobalWorkflowQuery:
    def __init__(self, reader: GlobalWorkflowReader) -> None:
        self.reader = reader

    def read(self) -> GlobalWorkflowQdto:
        try:
            groups, sources = self.reader.catalog()
            return GlobalWorkflowQdto(groups, [asdict(source) for source in sources], self.reader.categories(), self.reader.formats())
        except (OSError, ValueError, KeyError) as exc:
            raise GlobalWorkflowError("全局目录不可读取", 503) from exc

    def source(self, source_id: str) -> dict[str, Any]:
        try:
            return self.reader.source(source_id)
        except FileNotFoundError as exc:
            raise GlobalWorkflowError("未登记的全局源") from exc
        except (OSError, ValueError, KeyError) as exc:
            raise GlobalWorkflowError("全局目录不可读取", 503) from exc

    def coverage(self) -> dict[str, Any]:
        return {"inventory": self.reader.inventory()}
