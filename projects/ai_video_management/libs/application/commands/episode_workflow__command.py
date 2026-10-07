from __future__ import annotations

from typing import Any

from libs.application.dtos.episode_workflow__dto import EpisodeWorkflowCdto
from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.writers.episode_workflow__writer import EpisodeWorkflowWriter


class EpisodeWorkflowCommand:
    def __init__(self, reader: EpisodeWorkflowReader, writer: EpisodeWorkflowWriter) -> None:
        self.reader = reader
        self.writer = writer

    def change(self, episode_path: str, module: str, operation: str, expected: str,
               source: str | None, content: dict[str, Any] | None = None) -> EpisodeWorkflowCdto:
        with self.writer.lock:
            try:
                dao = self.reader.read(episode_path)
                entity = EpisodeWorkflowEntity(dao.documents, dao.episode_path.rsplit("/", 1)[-1])
            except FileNotFoundError as exc:
                raise EpisodeWorkflowError(str(exc), 404) from exc
            except ValueError as exc:
                raise EpisodeWorkflowError("模块文件格式无效，请检查JSON内容") from exc
            entity.check_edit(module, expected, source)
            if operation == "save" and content is not None:
                entity.save(module, content)
            elif operation == "approve":
                entity.approve(module)
            elif operation == "compile" and module == "prompts":
                entity.compile()
            else:
                raise EpisodeWorkflowError("无效操作")
            self.writer.write(episode_path, module, entity.documents[module])
        return EpisodeWorkflowCdto(module)
