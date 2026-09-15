from __future__ import annotations

import re

from libs.common.drama_ref import ASSET_KIND_DIR_NAMES
from libs.common.paths import RepoSandbox
from libs.infrastructure.daos.asset_card__dao import AssetBlockDao, AssetCardDao
from libs.infrastructure.daos.markdown__dao import MarkdownDocumentDao, MarkdownFenceDao
from libs.infrastructure.readers.markdown__reader import TEXT_FENCE_INFO, MarkdownReader
from libs.infrastructure.readers.prompt_field__reader import PromptFieldReader
from libs.infrastructure.readers.reference_line__reader import ReferenceLineReader

_ROUTING_KEY_RE = re.compile(r"^((?:bg|c|p)\d+-\d+)(?!\d)")
_FOLDER_KEY_RE = re.compile(r"^((?:bg|[cp])\d+)(?:_|$)", re.IGNORECASE)


class AssetCardReader:
    """Only ```text blocks whose first line starts with a routing key are requests (spec v2 FR-9)."""

    def __init__(self, sandbox: RepoSandbox) -> None:
        self._sandbox: RepoSandbox = sandbox
        self._markdown: MarkdownReader = MarkdownReader()
        self._fields: PromptFieldReader = PromptFieldReader()
        self._references: ReferenceLineReader = ReferenceLineReader()

    def read(self, rel: str) -> AssetCardDao:
        source_rel, data = self._markdown.load(self._sandbox, rel)
        return self.parse_bytes(data, source_rel)

    def parse_bytes(self, data: bytes, source_rel: str) -> AssetCardDao:
        document = self._markdown.parse(self._markdown.decode(data, source_rel))
        parts = source_rel.split("/")
        card_dir_name = parts[-2] if len(parts) >= 2 else ""
        blocks = tuple(
            self._block(document, fence)
            for fence in document.fences
            if fence.info == TEXT_FENCE_INFO and _ROUTING_KEY_RE.match(_first_line(fence))
        )
        return AssetCardDao(
            source_rel=source_rel,
            card_dir_name=card_dir_name,
            subject_kind=next((part for part in reversed(parts[:-1]) if part in ASSET_KIND_DIR_NAMES), None),
            folder_key=_folder_key(card_dir_name),
            blocks=blocks,
        )

    def _block(self, document: MarkdownDocumentDao, fence: MarkdownFenceDao) -> AssetBlockDao:
        first_line = _first_line(fence)
        fields = self._fields.fields(fence.content)
        ratio, _ = self._fields.ratio(fields)
        duration_s, _ = self._fields.duration(fields)
        key_match = _ROUTING_KEY_RE.match(first_line)
        return AssetBlockDao(
            key=key_match.group(1) if key_match else first_line,
            first_line=first_line,
            body=fence.content,
            heading=next((h.text for h in reversed(document.headings) if h.line < fence.open_line), None),
            fields=self._fields.names(fields),
            ratio=ratio,
            duration_s=duration_s,
            references=self._references.parse(fence.content),
        )


def _first_line(fence: MarkdownFenceDao) -> str:
    return fence.content.split("\n", 1)[0].strip()


def _folder_key(folder_name: str) -> str | None:
    match = _FOLDER_KEY_RE.match(folder_name.strip())
    if match is None:
        return None
    # Scene plates (`bg1_朝北_城门`) are single-image folders keyed by their own name.
    if folder_name.lower().startswith("bg") and folder_name.count("_") >= 2:
        return None
    return match.group(1)
