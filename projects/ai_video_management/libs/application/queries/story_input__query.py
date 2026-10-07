from __future__ import annotations

from libs.application.dtos.story_input__dto import StoryInputQdto
from libs.common.episode_workflow import fingerprint
from libs.common.story_runs import StoryRunsError
from libs.domain.entities.story_run__entity import StoryRunEntity
from libs.infrastructure.readers.story_input__reader import StoryInputReader


class StoryInputQuery:
    def __init__(self, reader: StoryInputReader) -> None:
        self.reader = reader

    def read(self, episode_path: str, profile_id: str | None = None) -> StoryInputQdto:
        try:
            dao = self.reader.read(episode_path)
            selected = profile_id if profile_id is not None else dao.selected_profile
            if selected not in dao.inputs:
                raise FileNotFoundError("找不到输入profile")
            inputs = {key: StoryRunEntity.from_input(value).input for key, value in dao.inputs.items()}
            profiles = [{**profile, "input_hash": inputs[profile["id"]]["input_hash"],
                         "rules_hash": fingerprint(inputs[profile["id"]]["rules"])} for profile in dao.profiles]
            return StoryInputQdto(dao.episode_path, dao.selected_profile, selected, profiles, inputs[selected])
        except FileNotFoundError as exc:
            raise StoryRunsError("找不到共享输入或profile", 404) from exc
        except (ValueError, OSError) as exc:
            raise StoryRunsError("共享输入或规则格式无效，请检查索引和路径") from exc
