"""智能补帧升级 (follow-up 155) contracts.

- `_plan_for_used` maps the new UI methods (blend / retime / external / rife
  with direct-timestep frames + model) onto tool-level plan entries, and an
  external seam whose bridge clip is missing fails LOUD (never a silent
  butt-join of a seam the user explicitly routed to a generated bridge).
- `tools/seam_concat._resolve_rife_model` prefers the newest v4 model dir next
  to the exe and honors explicit names — the old code passed no `-m` at all,
  silently running the binary-default rife-v2.3.
- `tools/seam_concat._rife_direct` guards the known silent-`-s` bug class:
  byte-identical samples mean the timestep flag was ignored → fall back.
- `tools/seam_retime._atempo_chain` stays within atempo's quality band.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.domain.errors.episode__error import EpisodeConcatFailedError
from libs.infrastructure.writers.episode__writer import (
    EpisodeConcatBuilder,
    ShotClip,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _load_tool(name: str) -> ModuleType:
    path = _REPO_ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{name}_tool", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _builder(root: Path) -> EpisodeConcatBuilder:
    return EpisodeConcatBuilder(ExposedTree(root), SafeResolver(root))


def _used() -> list[ShotClip]:
    return [ShotClip("shot01", "a.mp4"), ShotClip("shot02", "b.mp4")]


def _entry(method: str, **kw) -> list[dict]:
    return [{"from": "shot01", "to": "shot02", "method": method, **kw}]


def test_plan_maps_blend_to_blend_bridge(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    [e] = b._plan_for_used(_entry("blend", trim=0.12, blend=6), _used(), tmp_path)
    assert e == {"bridge": True, "rife": False, "trim": 0.12, "depth": None,
                 "blend": 6}


def test_plan_maps_retime_window(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    [e] = b._plan_for_used(_entry("retime", window=0.35), _used(), tmp_path)
    assert e["bridge"] is True and e["rife"] is False
    assert e["retime_window"] == 0.35


def test_plan_maps_rife_frames_and_model(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    [e] = b._plan_for_used(
        _entry("rife", trim=0.1, frames=5, model="rife-v4.25"), _used(), tmp_path)
    assert e["rife"] is True and e["frames"] == 5 and e["model"] == "rife-v4.25"
    assert e["depth"] is None  # frames wins over legacy depth


def test_plan_rife_legacy_depth_still_lands(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    [e] = b._plan_for_used(_entry("rife", trim=0.1, depth=3), _used(), tmp_path)
    assert e["rife"] is True and e["depth"] == 3 and "frames" not in e


def test_plan_external_missing_clip_raises(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    with pytest.raises(EpisodeConcatFailedError):
        b._plan_for_used(_entry("external"), _used(), tmp_path)


def test_plan_external_present_carries_clip_path(tmp_path: Path) -> None:
    clip = tmp_path / "bridges" / "bridge_shot01_shot02.mp4"
    clip.parent.mkdir(parents=True)
    clip.write_bytes(b"x")
    b = _builder(tmp_path)
    [e] = b._plan_for_used(_entry("external"), _used(), tmp_path)
    assert e["bridge"] is True and e["clip"] == str(clip)


def test_resolve_rife_model_prefers_newest_v4(tmp_path: Path) -> None:
    sc = _load_tool("seam_concat")
    exe = tmp_path / "rife-ncnn-vulkan.exe"
    exe.write_bytes(b"x")
    (tmp_path / "rife-v4.18").mkdir()
    (tmp_path / "rife-v4.25").mkdir()
    assert sc._resolve_rife_model(str(exe)) == str(tmp_path / "rife-v4.25")
    # explicit bare name resolves next to the exe; unknown name → None
    assert sc._resolve_rife_model(str(exe), "rife-v4.18") == str(tmp_path / "rife-v4.18")
    assert sc._resolve_rife_model(str(exe), "rife-v9.99") is None


def test_rife_direct_rejects_byte_identical_samples(tmp_path: Path) -> None:
    sc = _load_tool("seam_concat")
    a, b = tmp_path / "a.png", tmp_path / "b.png"
    a.write_bytes(b"a"); b.write_bytes(b"b")

    def fake_pair(rife, model, a_, b_, dst, t=None):
        dst.write_bytes(b"IDENTICAL")  # the silent--s bug: every t → same frame
        return True

    sc._rife_pair = fake_pair
    assert sc._rife_direct("rife.exe", None, a, b, 3, tmp_path) == []

    def good_pair(rife, model, a_, b_, dst, t=None):
        dst.write_bytes(f"frame@{t}".encode())
        return True

    sc._rife_pair = good_pair
    outs = sc._rife_direct("rife.exe", None, a, b, 3, tmp_path)
    assert len(outs) == 3


def test_atempo_chain_stays_in_quality_band() -> None:
    sr = _load_tool("seam_retime")
    assert sr._atempo_chain(1.5) == "atempo=1.5000"
    assert sr._atempo_chain(5.0) == "atempo=2.0,atempo=2.0,atempo=1.2500"
    # ratios are clamped into [0.5, 8.0] = 2.0 × 2.0 × 2.0
    assert sr._atempo_chain(100.0) == "atempo=2.0,atempo=2.0,atempo=2.0000"


def test_color_transfer_identity_and_full_strength() -> None:
    """seam_color._transfer: s=0 leaves the frame untouched; s=1 moves its LAB
    mean onto the reference (follow-up 156 色彩对齐)."""
    import numpy as np

    scol = _load_tool("seam_color")
    import cv2

    img = np.full((32, 32, 3), (60, 120, 180), dtype=np.uint8)  # BGR
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float64)
    mu_b = lab.reshape(-1, 3).mean(axis=0)
    sd_b = np.maximum(lab.reshape(-1, 3).std(axis=0), 1e-3)
    mu_a = mu_b + np.array([20.0, -5.0, 8.0])
    sd_a = sd_b
    out0 = scol._transfer(img, mu_b, sd_b, mu_a, sd_a, 0.0)
    assert np.array_equal(out0, img)
    out1 = scol._transfer(img, mu_b, sd_b, mu_a, sd_a, 1.0)
    lab1 = cv2.cvtColor(out1, cv2.COLOR_BGR2LAB).astype(np.float64)
    got = lab1.reshape(-1, 3).mean(axis=0)
    assert np.all(np.abs(got - mu_a) < 3.0)  # uint8 round-trip tolerance


def _scored(m1: float, m2: float, m3: float, m4: float, method: str = "rife",
            trim: float = 0.1) -> dict:
    """A minimal candidate result dict shaped like _build_and_measure's output,
    for exercising rank_key. floor_pass = every metric ≥ 80 (the scorer's rule)."""
    lo = min(m1, m2, m3, m4)
    return {
        "score": (m1 * 40 + m2 * 15 + m3 * 25 + m4 * 20) / 100,
        "floor_pass": lo >= 80.0, "min_metric": lo,
        "M1_velocity": {"score": m1}, "M2_no_freeze": {"score": m2},
        "M3_no_jump": {"score": m3}, "M4_junction_ssim": {"score": m4},
        "method": method, "trim": trim,
    }


def test_rank_prefers_even_over_peak_with_a_dip() -> None:
    """No weak board: a uniform 91/91/91/91 beats a peak-heavy 100/100/100/90 even
    though the latter's weighted average (98) is far higher (2026-07-07 directive)."""
    mx = _load_tool("seam_metrics")
    even = _scored(91, 91, 91, 91)
    peak = _scored(100, 100, 100, 90)
    assert peak["score"] > even["score"]           # weighted avg would pick the peak…
    assert max((even, peak), key=mx.rank_key) is even  # …but leximin picks the even one


def test_rank_floor_pass_beats_sub_floor_defect() -> None:
    mx = _load_tool("seam_metrics")
    clean = _scored(80, 80, 80, 80)      # min 80 → floor_pass
    defect = _scored(100, 100, 100, 79)  # one board below 80
    assert max((clean, defect), key=mx.rank_key) is clean


def test_rank_leximin_falls_through_on_hopeless_board() -> None:
    """Below the floor, when the weakest board is capped low for every candidate
    (~level within the dead-band), prefer the one better on the OTHER boards rather
    than chase sub-point noise on the hopeless board."""
    mx = _load_tool("seam_metrics")
    hopeless_but_good = _scored(13.2, 100, 100, 100)  # weakest 13.2
    hopeless_and_bad = _scored(13.7, 20, 30, 40)      # weakest 13.7 (barely higher)
    assert max((hopeless_but_good, hopeless_and_bad), key=mx.rank_key) is hopeless_but_good


def test_plan_color_flag_lands_for_smoothing_methods_only(tmp_path: Path) -> None:
    b = _builder(tmp_path)
    [e] = b._plan_for_used(_entry("trim", trim=0.1, color=True), _used(), tmp_path)
    assert e["color"] is True
    [e] = b._plan_for_used(_entry("rife", trim=0.1, frames=3, color=True), _used(), tmp_path)
    assert e["color"] is True
    [e] = b._plan_for_used(_entry("retime", window=0.5, color=True), _used(), tmp_path)
    assert "color" not in e  # retime manages the junction itself
    [e] = b._plan_for_used(_entry("butt", color=True), _used(), tmp_path)
    assert "color" not in e  # 硬切 is never corrected
