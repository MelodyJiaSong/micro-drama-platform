from __future__ import annotations

from libs.infrastructure.clients.understanding__client import (
    FallbackVideoUnderstanding,
    NullVideoUnderstanding,
)
from libs.infrastructure.daos.shotanalysis__dao import EpisodeUnderstandingDao


def _episode(tag: str) -> EpisodeUnderstandingDao:
    return EpisodeUnderstandingDao(tag, (), "", {}, ())


class _Primary:
    def __init__(self, fail_times: int = 0) -> None:
        self.available = True
        self._fail_times = fail_times
        self.calls = 0

    def episode_pass(self, video_abs_path, dialogue_lines):
        self.calls += 1
        if self.calls <= self._fail_times:
            raise RuntimeError("gemini down")
        return _episode("primary")

    def shot_pass(self, *a):
        raise NotImplementedError


class _Fallback:
    available = True

    def episode_pass(self, video_abs_path, dialogue_lines):
        return _episode("fallback")

    def shot_pass(self, *a):
        raise NotImplementedError


def test_primary_used_when_healthy() -> None:
    fb = FallbackVideoUnderstanding(_Primary(), _Fallback())
    assert fb.episode_pass("v", []).narrative == "primary"
    assert fb.last_backend == "primary"


def test_falls_back_after_primary_retries_exhausted() -> None:
    fb = FallbackVideoUnderstanding(_Primary(fail_times=99), _Fallback(), retries=2)
    assert fb.episode_pass("v", []).narrative == "fallback"
    assert fb.last_backend == "fallback"


def test_unavailable_both_reports_unavailable() -> None:
    fb = FallbackVideoUnderstanding(NullVideoUnderstanding(), NullVideoUnderstanding())
    assert fb.available is False
