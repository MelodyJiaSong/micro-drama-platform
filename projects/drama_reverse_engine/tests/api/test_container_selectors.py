from __future__ import annotations

import pytest

from apps.api.container import Container
from libs.infrastructure.clients.claude_composer__client import ClaudeLlmComposer
from libs.infrastructure.clients.claude_subtitle__client import ClaudeSubtitleExtractor
from libs.infrastructure.clients.claude_understanding__client import ClaudeVideoUnderstanding
from libs.infrastructure.clients.doubao_composer__client import DoubaoLlmComposer
from libs.infrastructure.clients.subtitle__client import NullSubtitleExtractor
from libs.infrastructure.clients.understanding__client import FallbackVideoUnderstanding


def test_default_engine_is_claude_cli_zero_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DRE_UNDERSTANDING", raising=False)
    monkeypatch.delenv("DRE_COMPOSER", raising=False)
    monkeypatch.delenv("DRE_SUBTITLES", raising=False)
    container = Container()
    assert isinstance(container.vlm(), ClaudeVideoUnderstanding)
    assert isinstance(container.composer(), ClaudeLlmComposer)
    assert isinstance(container.subtitles(), ClaudeSubtitleExtractor)


def test_env_switches_back_to_keyed_backends(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DRE_UNDERSTANDING", "gemini_qwen")
    monkeypatch.setenv("DRE_COMPOSER", "doubao")
    monkeypatch.setenv("DRE_SUBTITLES", "null")
    container = Container()
    assert isinstance(container.vlm(), FallbackVideoUnderstanding)
    assert isinstance(container.composer(), DoubaoLlmComposer)
    assert isinstance(container.subtitles(), NullSubtitleExtractor)
