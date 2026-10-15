from __future__ import annotations

from libs.application.dtos.episode_workflow__dto import EpisodeWorkflowQdto
from libs.common.episode_workflow import MODULE_LABELS, MODULES, fingerprint
from libs.common.production_key import shot_key
from libs.domain.entities.episode_workflow__entity import EpisodeWorkflowEntity
from libs.domain.errors.episode_workflow__error import EpisodeWorkflowError
from libs.infrastructure.readers.episode_workflow__reader import EpisodeWorkflowReader
from libs.infrastructure.readers.shot_pack__reader import ShotPackReader
from libs.infrastructure.readers.shot_renders__reader import ShotRendersReader


class EpisodeWorkflowQuery:
    def __init__(self, reader: EpisodeWorkflowReader, packs: ShotPackReader | None = None,
                 renders: ShotRendersReader | None = None) -> None:
        self.reader = reader
        self.packs = packs or ShotPackReader(reader.root)
        self.renders = renders or ShotRendersReader(reader.root)

    def read(self, episode_path: str) -> EpisodeWorkflowQdto:
        try:
            dao = self.reader.read(episode_path)
        except FileNotFoundError as exc:
            raise EpisodeWorkflowError(str(exc), 404) from exc
        except ValueError as exc:
            raise EpisodeWorkflowError("模块文件格式无效，请检查JSON内容") from exc
        entity = EpisodeWorkflowEntity(dao.documents, dao.episode_path.rsplit("/", 1)[-1])
        modules = []
        for module in MODULES:
            upstream = entity.upstream(module)
            modules.append({"id": module, "label": MODULE_LABELS[module], "status": entity.status(module),
                            "revision": entity.revision(module), "etag": fingerprint(dao.documents[module]),
                            "input_revision": entity.revision(upstream) if upstream else None,
                            "can_edit": upstream is None or entity.status(upstream) == "approved",
                            **dao.documents[module]})
        keys = {scene["id"]: {shot["id"]: shot_key(entity.episode_id, scene["id"], shot["id"]).value
                              for shot in scene["shots"]}
                for scene in dao.documents["filming"]["content"]["scenes"]}
        packs = self.packs.read(dao.episode_path, dao.documents["prompts"]["content"])
        renders = self.renders.read(dao.episode_path, dao.documents["prompts"]["content"])
        return EpisodeWorkflowQdto(dao.episode_path, modules, keys, packs, renders)
