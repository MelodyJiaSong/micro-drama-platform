from __future__ import annotations

from pathlib import PurePosixPath

from libs.application.errors.batch__error import BatchItemRejectedError
from libs.application.mappers.request_drama__mapper import DramaSettings, DramaSettingsCache
from libs.application.mappers.request_reference__mapper import (
    MappedRequest,
    ReferenceRequestMapper,
    ResolvedReferences,
)
from libs.common.enums import BackendKind, GenerationKind, RefKind, SourceType
from libs.common.paths import RepoSandbox
from libs.domain.errors.config__error import MissingAbbrevError
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.generation_request__valueobject import GenerationRequest, RequestSource
from libs.domain.value_objects.precheck_context__valueobject import ReferenceIssue
from libs.domain.value_objects.reference_item__valueobject import ReferenceItem
from libs.infrastructure.daos.drama_tree__dao import CharacterCardDao
from libs.infrastructure.errors.sandbox__error import SandboxError
from libs.infrastructure.errors.shot_parse__error import MarkdownParseError
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from libs.infrastructure.readers.markdown__reader import MarkdownReader

LOCKED_DESCRIPTOR_MARK: str = "锁定描述符"
SOURCE_IMAGE_LABEL: str = "主体参考图"


class EntityCreateRequestMapper:
    """A character card → an `entity_create` request (FR-49): name via naming rules, image via `entities.source_images`."""

    def __init__(
        self, sandbox: RepoSandbox, tree: DramaTreeReader, markdown: MarkdownReader, references: ReferenceRequestMapper
    ) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._tree: DramaTreeReader = tree
        self._markdown: MarkdownReader = markdown
        self._references: ReferenceRequestMapper = references

    def map(self, drama_rel: str, character_dir: str, description: str | None, dramas: DramaSettingsCache) -> MappedRequest:
        if self._tree.drama_root_of(drama_rel) != drama_rel:
            raise BatchItemRejectedError("not_a_drama_root", f"{drama_rel} 不是剧根目录")
        cards: list[CharacterCardDao] = [
            card for card in self._tree.character_cards(drama_rel) if character_dir in (card.dir_name, card.dir_rel)
        ]
        if len(cards) != 1:
            reason = "character_card_not_found" if not cards else "character_card_ambiguous"
            raise BatchItemRejectedError(reason, f"{drama_rel} 下名为 {character_dir} 的角色卡有 {len(cards)} 个，必须恰好 1 个")
        card: CharacterCardDao = cards[0]
        settings: DramaSettings = dramas.get(drama_rel)
        config: DramaConfig = settings.config
        issues: list[ReferenceIssue] = []
        try:
            entity_name: str = self._references.naming_for(card, config, dramas).entity_name(card.dir_name)
        except MissingAbbrevError as error:
            entity_name = card.character_name
            issues.append(ReferenceIssue(error.error_code, error.message, None, error.field_path))
        references: tuple[ReferenceItem, ...] = self._source_image(card, config)
        prompt: str = description if description is not None else (self._locked_descriptor(card) or "")
        request = GenerationRequest(
            kind=GenerationKind.ENTITY,
            prompt=prompt,
            negative_prompt=None,
            references=references,
            params=None,
            output_slot=card.dir_rel,
            source=RequestSource(SourceType.ENTITY_CREATE, card.dir_rel),
            entity_name=entity_name,
        )
        resolved = ResolvedReferences(references, tuple(issues), (), {entity_name: card.dir_name})
        return MappedRequest(request, BackendKind.WEB, settings, None, resolved)

    def _source_image(self, card: CharacterCardDao, config: DramaConfig) -> tuple[ReferenceItem, ...]:
        for pattern in config.entities.source_images:
            hits = self._references.card_images(pattern.format(card_dir=card.dir_rel, card_dir_name=card.dir_name))
            if hits:
                target: str = hits[0]
                return (self._references.file_reference(PurePosixPath(target).stem, SOURCE_IMAGE_LABEL, RefKind.IMAGE, target),)
        return ()

    def _locked_descriptor(self, card: CharacterCardDao) -> str | None:
        try:
            source_rel, data = self._markdown.load(self._sandbox, f"{card.dir_rel}/{card.dir_name}.md")
            document = self._markdown.parse(self._markdown.decode(data, source_rel))
        except (SandboxError, MarkdownParseError):
            return None
        heading = next((h for h in document.headings if LOCKED_DESCRIPTOR_MARK in h.text), None)
        if heading is None:
            return None
        end: int = next(
            (h.line for h in document.headings if h.line > heading.line and h.level <= heading.level), len(document.lines)
        )
        fence = next((f for f in document.fences if heading.line < f.open_line < end), None)
        text: str = "" if fence is None else fence.content.strip()
        return text or None
