"""Concat output canvas is derived from the SOURCE clips, never hardcoded.

Regression for 荒野造家 (2026-09-06): both concat paths carried their own
`_CONCAT_TARGET_W = 720 / _CONCAT_TARGET_H = 1280`, so a 16:9 drama's 1280x720
clips were letterboxed into a vertical 720x1280 frame with thick black bars —
both for the stitched 成片 and for the character-views reel.
"""
from __future__ import annotations

from pathlib import Path

from libs.common import video_canvas as vc


def test_fit_canvas_keeps_landscape_landscape() -> None:
    assert vc.fit_canvas(1280, 720) == (1280, 720)
    assert vc.fit_canvas(1920, 1080) == (1280, 720)


def test_fit_canvas_keeps_portrait_portrait() -> None:
    """The historical 9:16 reel is unchanged — existing dramas must not move."""
    assert vc.fit_canvas(720, 1280) == (720, 1280)
    assert vc.fit_canvas(1080, 1920) == (720, 1280)


def test_fit_canvas_preserves_odd_aspects() -> None:
    assert vc.fit_canvas(1440, 1080) == (1280, 960)
    assert vc.fit_canvas(640, 480) == (640, 480)


def test_fit_canvas_forces_even_dimensions() -> None:
    """h.264 + yuv420p rejects odd dimensions."""
    w, h = vc.fit_canvas(1001, 563)
    assert w % 2 == 0 and h % 2 == 0


def test_target_canvas_falls_back_when_nothing_probes(tmp_path: Path) -> None:
    clip = tmp_path / "not_a_video.mp4"
    clip.write_bytes(b"nope")
    assert vc.target_canvas("definitely-not-ffmpeg", [clip]) == vc.FALLBACK_CANVAS


def test_target_canvas_takes_the_modal_size(monkeypatch) -> None:
    """One stray off-size clip is padded into the majority shape, not the other
    way round."""
    sizes = {"a": (1280, 720), "b": (1280, 720), "c": (720, 1280)}
    monkeypatch.setattr(vc, "probe_dims", lambda _ff, src: sizes[src.name])

    got = vc.target_canvas("ffmpeg", [Path("a"), Path("b"), Path("c")])

    assert got == (1280, 720)


def test_target_canvas_tie_breaks_toward_the_larger_frame(monkeypatch) -> None:
    sizes = {"a": (640, 360), "b": (1280, 720)}
    monkeypatch.setattr(vc, "probe_dims", lambda _ff, src: sizes[src.name])

    assert vc.target_canvas("ffmpeg", [Path("a"), Path("b")]) == (1280, 720)


def test_target_canvas_skips_unprobeable_clips(monkeypatch) -> None:
    sizes: dict[str, tuple[int, int] | None] = {"a": None, "b": (1280, 720)}
    monkeypatch.setattr(vc, "probe_dims", lambda _ff, src: sizes[src.name])

    assert vc.target_canvas("ffmpeg", [Path("a"), Path("b")]) == (1280, 720)


def test_dims_regex_ignores_sar_and_dar() -> None:
    """`[SAR 1:1 DAR 16:9]` sits on the same stderr line as the real WxH."""
    line = (
        "  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), "
        "yuv420p(tv, bt709), 1280x720 [SAR 1:1 DAR 16:9], 2314 kb/s, 24 fps"
    )
    match = vc._DIMS_RE.search(line)
    assert match is not None and match.groups() == ("1280", "720")
