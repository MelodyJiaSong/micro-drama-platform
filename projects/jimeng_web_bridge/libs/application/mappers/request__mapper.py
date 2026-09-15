from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from libs.application.dtos.batch__dto import (
    AssetItemInput,
    BatchItemInput,
    EntityCreateItemInput,
    RawItemInput,
    ShotItemInput,
)
from libs.application.errors.batch__error import BatchItemRejectedError
from libs.application.mappers.request_asset__mapper import AssetRequestMapper
from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache, DramaSettingsMapper
from libs.application.mappers.request_entity__mapper import EntityCreateRequestMapper
from libs.application.mappers.request_input__mapper import RequestInputMapper
from libs.application.mappers.request_raw__mapper import RawRequestMapper
from libs.application.mappers.request_reference__mapper import MappedRequest, ResolvedReferences
from libs.application.mappers.request_shot__mapper import ShotRequestMapper
from libs.common import drama_ref
from libs.common.canonical_json import canonical_sha256
from libs.common.enums import BackendKind
from libs.common.paths import RepoSandbox, segment_violation
from libs.domain.errors.precheck__error import InvalidRequestError
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import MarkdownParseError


@dataclass(frozen=True)
class MappedItem:
    input: Mapping[str, object]
    reroll: bool
    request: GenerationRequest
    backend: BackendKind
    settings: DramaSettings
    output_dir: str | None
    references: ResolvedReferences
    config_digest: str

    @property
    def drama_rel(self) -> str | None:
        return self.settings.drama_rel


class RequestMapper:
    """Batch item inputs → GenerationRequests. Client paths must already be canonical `ai_videos/…` with `/` only."""

    def __init__(
        self,
        sandbox: RepoSandbox,
        inputs: RequestInputMapper,
        dramas: DramaSettingsMapper,
        shots: ShotRequestMapper,
        assets: AssetRequestMapper,
        raws: RawRequestMapper,
        entities: EntityCreateRequestMapper,
    ) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._inputs: RequestInputMapper = inputs
        self._dramas: DramaSettingsMapper = dramas
        self._shots: ShotRequestMapper = shots
        self._assets: AssetRequestMapper = assets
        self._raws: RawRequestMapper = raws
        self._entities: EntityCreateRequestMapper = entities

    def map_all(
        self, items: Sequence[BatchItemInput], global_config: GlobalConfig, global_sha256: str | None
    ) -> list[MappedItem]:
        cache = DramaSettingsCache(self._dramas, global_config.model_limits)
        return [self._map_one(index, item, cache, global_config, global_sha256) for index, item in enumerate(items)]

    def _map_one(
        self,
        index: int,
        item: BatchItemInput,
        cache: DramaSettingsCache,
        global_config: GlobalConfig,
        global_sha256: str | None,
    ) -> MappedItem:
        prefix: str = f"第 {index + 1} 条："
        try:
            self._guard_paths(item)
            mapped: MappedRequest = self._dispatch(item, cache, global_config)
        except BatchItemRejectedError as error:
            raise BatchItemRejectedError(error.reason, prefix + error.message, index, error.config_key) from error
        except SandboxError as error:
            raise BatchItemRejectedError("path_rejected", f"{prefix}{error}", index) from error
        except MarkdownParseError as error:
            raise BatchItemRejectedError(error.code, f"{prefix}{error.source_rel} 解析失败（{error.code}）", index) from error
        except InvalidRequestError as error:
            raise BatchItemRejectedError(error.error_code, prefix + error.message, index) from error
        reroll: bool = False if isinstance(item, EntityCreateItemInput) else item.reroll
        digest: str = canonical_sha256({"global": global_sha256, "drama": mapped.settings.file_sha256})
        return MappedItem(
            input=self._inputs.to_dict(item),
            reroll=reroll,
            request=mapped.request,
            backend=mapped.backend,
            settings=mapped.settings,
            output_dir=mapped.output_dir,
            references=mapped.references,
            config_digest=digest,
        )

    def _dispatch(self, item: BatchItemInput, cache: DramaSettingsCache, global_config: GlobalConfig) -> MappedRequest:
        routing = global_config.routing
        if isinstance(item, ShotItemInput):
            return self._shots.map(item.shot_path, cache, routing)
        if isinstance(item, AssetItemInput):
            return self._assets.map(item.card_path, item.key, cache, routing)
        if isinstance(item, RawItemInput):
            return self._raws.map(item, cache, routing)
        return self._entities.map(item.drama_rel, item.character_dir, item.description, cache)

    def _guard_paths(self, item: BatchItemInput) -> None:
        if isinstance(item, EntityCreateItemInput) and "/" not in item.character_dir:
            if "\\" in item.character_dir or segment_violation(item.character_dir) is not None:
                raise BatchItemRejectedError("path_rejected", f"character_dir {item.character_dir!r} 不是合法的目录名")
        for raw in _client_paths(item):
            violation: str | None = drama_ref.canonical_rel_violation(raw)
            if violation is None:
                verdict = self._sandbox.check_read(raw)
                violation = verdict.violation or (None if verdict.rel == raw else "non_canonical")
            if violation is not None:
                raise BatchItemRejectedError(
                    "path_rejected", f"路径 {raw!r} 必须是 ai_videos/ 下以 / 分隔的规范相对路径（{violation}）"
                )


def _client_paths(item: BatchItemInput) -> tuple[str, ...]:
    if isinstance(item, ShotItemInput):
        return (item.shot_path,)
    if isinstance(item, AssetItemInput):
        return (item.card_path,)
    if isinstance(item, RawItemInput):
        return (item.output_dir, *item.reference_paths)
    return (item.drama_rel, *((item.character_dir,) if "/" in item.character_dir else ()))
