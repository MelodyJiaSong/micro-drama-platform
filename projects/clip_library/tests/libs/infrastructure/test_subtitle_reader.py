from pathlib import Path

from libs.infrastructure.readers.subtitle__reader import SubtitleReader
from libs.infrastructure.readers.youtube__reader import search_filter

ROLLING_AUTO_SUBS = """WEBVTT
Kind: captions

00:00:01.000 --> 00:00:03.000 align:start position:0%
how<00:00:01.500><c> hard</c><00:00:02.000><c> could</c>

00:00:03.000 --> 00:00:03.010 align:start position:0%
how hard could

00:00:03.010 --> 00:00:05.000 align:start position:0%
how hard could
it be &amp; why
"""


def test_rolling_auto_captions_are_deduplicated(tmp_path: Path) -> None:
    path = tmp_path / "video.en.vtt"
    path.write_text(ROLLING_AUTO_SUBS, encoding="utf-8")
    reader = SubtitleReader()
    cues = reader.read(path)
    assert [(cue.start, cue.end, cue.text) for cue in cues] == [(1.0, 3.0, "how hard could"), (3.01, 5.0, "it be & why")]
    assert reader.language(path) == "en"


def test_search_filter_matches_youtube_encoding() -> None:
    assert search_filter(0, 0, True) == "EgIwAQ=="
    assert search_filter(2, 3, True) == "CAMSBBgCMAE="
    assert search_filter(0, 0, False) == ""
