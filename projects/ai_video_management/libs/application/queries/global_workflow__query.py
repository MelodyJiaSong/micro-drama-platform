from __future__ import annotations

from dataclasses import asdict
from typing import Any

from libs.application.dtos.global_workflow__dto import GlobalWorkflowQdto
from libs.common.global_workflow import GlobalWorkflowError, global_source_id
from libs.infrastructure.readers.global_workflow__reader import GlobalWorkflowReader
from libs.infrastructure.readers.story_runs__reader import StoryRunsReader


class GlobalWorkflowQuery:
    def __init__(self, reader: GlobalWorkflowReader, runs: StoryRunsReader) -> None:
        self.reader = reader
        self.runs = runs

    def read(self) -> GlobalWorkflowQdto:
        try:
            groups, sources = self.reader.catalog()
            return GlobalWorkflowQdto(groups, [asdict(source) for source in sources], self.reader.categories())
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
        catalog = self.read()
        registered = {source["id"]: source for source in catalog.sources}
        links: list[dict[str, Any]] = []
        gaps: list[dict[str, str]] = []
        for episode in self.reader.episodes():
            try:
                runs = self.runs.read(episode).runs
                for run in runs:
                    for group in ("sources", "rules"):
                        for index, source in enumerate(run["input"][group]):
                            path = source.get("path") if isinstance(source, dict) else None
                            identity = global_source_id(path, episode=episode) if isinstance(path, str) else None
                            if identity:
                                current = registered.get(identity)
                                links.append({"episode_path": episode, "run_id": run["run_id"], "item_id": f"{group}-{index}",
                                              "source_id": identity, "source_path": path, "source_hash": source.get("sha256"),
                                              "source_number": current["number"] if current else "", "source_title": current["title"] if current else path,
                                              "status": current["status"] if current else "unregistered"})
            except (OSError, ValueError, KeyError) as exc:
                gaps.append({"episode_path": episode, "status": "unavailable", "note": type(exc).__name__})
        return {"links": links, "gaps": gaps, "inventory": self.reader.inventory(), "note": "按已保存的 run 输入核对全局来源。历史未留存的系统指令、父代理上下文与完整代理配置不能补证；当前配置不等于当次实际输入。"}
