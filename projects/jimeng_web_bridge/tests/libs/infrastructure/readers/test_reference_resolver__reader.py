from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.common.paths import RepoSandbox
from libs.infrastructure.readers.drama_tree__reader import DramaTreeReader
from tests.libs.infrastructure.support import require_junction, write_file

DEFAULT_EXCLUDE: list[str] = ["_deleted", "_candidates", "renders", "frames", "_blender"]
HY2 = "ai_videos/hs/hy2"
HY1 = "ai_videos/hs/hy1"
FLAT = "ai_videos/flat"
SHOTS = f"{FLAT}/5_6_分镜与prompt/shots"
EXCLUDED_LINK_TARGETS: dict[str, str] = {
    "p7_render": f"{HY1}/shots/shot01/renders/r.png",
    "p8_deleted": "ai_videos/_deleted/hs/hy1/d.png",
    "p9_candidate": f"{HY1}/props/p1_x/_candidates/p1-1/c.png",
    "p10_upper": f"{HY1}/shots/shot02/RENDERS/u.png",
}


@pytest.fixture
def tree(tmp_path: Path) -> DramaTreeReader:
    write_file(tmp_path, "ai_videos/hs/series.json", "{}")
    write_file(tmp_path, f"{HY1}/props/p2_随身装备/p2_随身装备.png", b"hy1-kit")
    write_file(tmp_path, f"{HY1}/characters/c1_造家的人/c1_造家的人.png", b"face")
    write_file(tmp_path, f"{HY1}/characters/c1_造家的人/c1_造家的人.mp4", b"turn")
    for ext in ("png", "mp4"):
        target = {"target": f"{HY1}/characters/c1_造家的人/c1_造家的人.{ext}"}
        write_file(tmp_path, f"{HY2}/characters/c1_造家的人/c1_造家的人.{ext}.link.json", json.dumps(target))
    write_file(tmp_path, f"{HY2}/props/p2_随身装备/p2_随身装备.png.link.json", json.dumps({"target": f"{HY1}/props/p2_随身装备/p2_随身装备.png"}))
    write_file(tmp_path, f"{HY2}/props/p3_树皮门与顶/p3-1_树皮门板锚点.png", b"door")
    write_file(tmp_path, f"{HY2}/props/p4_x/p4-1.png", b"exact")
    write_file(tmp_path, f"{HY2}/props/p4_x/p4-1_view.png", b"prefix")
    write_file(tmp_path, f"{HY2}/props/p5_bad/p5_bad.png.link.json", json.dumps({"target": "ai_videos/../projects/x.png"}))
    write_file(tmp_path, f"{HY1}/jimeng_config.toml", "[drama]\n")
    write_file(tmp_path, f"{HY2}/props/p6_cfg/p6_cfg.png.link.json", json.dumps({"target": f"{HY1}/jimeng_config.toml"}))
    for key, target in EXCLUDED_LINK_TARGETS.items():
        write_file(tmp_path, target, b"png")
        write_file(tmp_path, f"{HY2}/props/{key}/{key}.png.link.json", json.dumps({"target": target}))
    write_file(tmp_path, f"{FLAT}/scenes/x/bg3_a/bg3-1.png", b"a")
    write_file(tmp_path, f"{FLAT}/_candidates/bg3-1/bg3-1.png", b"c")
    write_file(tmp_path, f"{FLAT}/scenes/x/bg3_a/renders/bg3-1.png", b"r")
    write_file(tmp_path, f"{FLAT}/previz/frames/bg3-1.png", b"f")
    write_file(tmp_path, f"{FLAT}/scenes/x/bg3_a/_blender/bg3-1.png", b"b")
    write_file(tmp_path, f"{FLAT}/_deleted/bg3-1.png", b"d")
    write_file(tmp_path, f"{FLAT}/scenes/y/bg4_a/bg4-1.png", b"1")
    write_file(tmp_path, f"{FLAT}/props/p9_b/bg4-1.png", b"2")
    write_file(tmp_path, "ai_videos/_series/bg5-1.png", b"not-a-series-share")
    write_file(tmp_path, f"{HY2}/scenes/bg5_x/bg5-1.png", b"own")
    write_file(tmp_path, "ai_videos/hs/_series/bg5-1.png", b"shared")
    write_file(tmp_path, f"{SHOTS}/shot01/shot01_previz.mp4", b"v")
    write_file(tmp_path, f"{SHOTS}/shot02/previz/shot02_previz.mp4", b"v")
    write_file(tmp_path, f"{SHOTS}/shot02/renders/shot02_previz.mp4", b"r")
    write_file(tmp_path, f"{SHOTS}/shot02/shot02_lastframe.png", b"lf")
    (tmp_path / SHOTS / "shot03").mkdir(parents=True)
    (tmp_path / SHOTS / "shot05").mkdir(parents=True)
    return DramaTreeReader(RepoSandbox(tmp_path))


def test_exact_stem_found(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(FLAT, "bg3-1", DEFAULT_EXCLUDE)
    assert (result.status, result.path, result.step) == ("found", f"{FLAT}/scenes/x/bg3_a/bg3-1.png", "exact_stem")


def test_hard_excludes_survive_empty_config(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(FLAT, "bg3-1", [])
    assert result.status == "ambiguous"
    assert set(result.candidates) == {
        f"{FLAT}/previz/frames/bg3-1.png",
        f"{FLAT}/scenes/x/bg3_a/_blender/bg3-1.png",
        f"{FLAT}/scenes/x/bg3_a/bg3-1.png",
    }


def test_multi_segment_exclude(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(FLAT, "bg3-1", ["previz/frames", "_blender"])
    assert result.status == "found"


def test_ambiguous_within_one_step_lists_candidates(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(FLAT, "bg4-1", DEFAULT_EXCLUDE)
    assert result.status == "ambiguous"
    assert result.candidates == (f"{FLAT}/props/p9_b/bg4-1.png", f"{FLAT}/scenes/y/bg4_a/bg4-1.png")


def test_series_shared_dir_is_in_scope(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "bg5-1", DEFAULT_EXCLUDE)
    assert result.status == "ambiguous"
    assert result.candidates == (f"{HY2}/scenes/bg5_x/bg5-1.png", "ai_videos/hs/_series/bg5-1.png")
    assert tree.resolve_asset_file(FLAT, "bg5-1", DEFAULT_EXCLUDE).status == "not_found"


def test_routing_key_prefix_step(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "p3-1", DEFAULT_EXCLUDE)
    assert (result.status, result.step) == ("found", "routing_key_prefix")
    assert result.path == f"{HY2}/props/p3_树皮门与顶/p3-1_树皮门板锚点.png"
    assert tree.resolve_asset_file(HY2, "p3", DEFAULT_EXCLUDE).status == "not_found"


def test_first_step_with_results_wins(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "p4-1", DEFAULT_EXCLUDE)
    assert (result.status, result.path, result.step) == ("found", f"{HY2}/props/p4_x/p4-1.png", "exact_stem")


def test_link_resolves_to_target(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "p2_随身装备", DEFAULT_EXCLUDE)
    assert result.status == "found"
    assert result.path == f"{HY1}/props/p2_随身装备/p2_随身装备.png"
    assert result.link_path == f"{HY2}/props/p2_随身装备/p2_随身装备.png.link.json"


def test_image_resolver_ignores_video_link_with_same_stem(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "c1_造家的人", DEFAULT_EXCLUDE)
    assert (result.status, result.path) == ("found", f"{HY1}/characters/c1_造家的人/c1_造家的人.png")


def test_escaping_link_is_link_invalid(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "p5_bad", DEFAULT_EXCLUDE)
    assert (result.status, result.reason, result.path) == ("link_invalid", "traversal", None)


def test_image_link_to_non_media_file_is_link_invalid(tree: DramaTreeReader) -> None:
    result = tree.resolve_asset_file(HY2, "p6_cfg", DEFAULT_EXCLUDE)
    assert (result.status, result.reason, result.path) == ("link_invalid", "target_type_mismatch", None)


@pytest.mark.parametrize("key", sorted(EXCLUDED_LINK_TARGETS))
def test_link_into_excluded_folder_never_resolves(tree: DramaTreeReader, key: str) -> None:
    result = tree.resolve_asset_file(HY2, key, DEFAULT_EXCLUDE)
    assert (result.status, result.reason, result.path) == ("link_invalid", "target_excluded", None)


def test_not_a_drama(tree: DramaTreeReader) -> None:
    assert tree.resolve_asset_file("ai_videos/hs", "bg5-1", DEFAULT_EXCLUDE).reason == "not_a_drama"
    assert tree.resolve_asset_file("ai_videos/../x", "bg5-1", DEFAULT_EXCLUDE).reason == "not_a_drama"


def test_shot_video_exact_in_previz_subdir_and_renders_excluded(tree: DramaTreeReader) -> None:
    result = tree.resolve_shot_video(f"{SHOTS}/shot02", "shot02_previz", DEFAULT_EXCLUDE)
    assert (result.status, result.path) == ("found", f"{SHOTS}/shot02/previz/shot02_previz.mp4")


def test_shot_video_swapped_alias(tree: DramaTreeReader) -> None:
    result = tree.resolve_shot_video(f"{SHOTS}/shot01", "previz_shot01", DEFAULT_EXCLUDE)
    assert (result.status, result.step, result.path) == ("found", "swapped_alias", f"{SHOTS}/shot01/shot01_previz.mp4")
    assert tree.resolve_shot_video(f"{SHOTS}/shot01", "previz_shot09", DEFAULT_EXCLUDE).status == "not_found"


def test_prev_shot_lastframe(tree: DramaTreeReader) -> None:
    found = tree.resolve_prev_shot_lastframe(f"{SHOTS}/shot03", "本镜首帧")
    assert (found.status, found.path, found.name) == ("found", f"{SHOTS}/shot02/shot02_lastframe.png", "本镜首帧")
    missing = tree.resolve_prev_shot_lastframe(f"{SHOTS}/shot05", "本镜首帧")
    assert (missing.status, missing.reason, missing.looked_for) == (
        "not_found",
        "missing",
        f"{SHOTS}/shot04/shot04_lastframe.png",
    )
    first = tree.resolve_prev_shot_lastframe(f"{SHOTS}/shot01", "本镜首帧")
    assert (first.status, first.reason, first.looked_for) == ("not_found", "first_shot", None)


def test_junction_inside_drama_is_not_indexed(tree: DramaTreeReader, tmp_path: Path) -> None:
    write_file(tmp_path, "outside/bg9-1.png", b"x")
    require_junction(tmp_path / FLAT / "linked", tmp_path / "outside")
    assert tree.resolve_asset_file(FLAT, "bg9-1", DEFAULT_EXCLUDE).status == "not_found"
