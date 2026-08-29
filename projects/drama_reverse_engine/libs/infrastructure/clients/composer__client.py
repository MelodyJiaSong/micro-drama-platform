from __future__ import annotations

from typing import Protocol


class LlmComposer(Protocol):
    """NFR-O1 seam for literary composition (novel + descriptor authoring)."""

    @property
    def available(self) -> bool: ...

    def compose_novel(self, script_markdown: str, narrative: str) -> str: ...

    def author_descriptor(self, character_name: str, ref_notes: str) -> str: ...


class NullLlmComposer:
    available = False

    def compose_novel(self, script_markdown: str, narrative: str) -> str:
        raise NotImplementedError("no LLM composer backend configured")

    def author_descriptor(self, character_name: str, ref_notes: str) -> str:
        raise NotImplementedError("no LLM composer backend configured")
