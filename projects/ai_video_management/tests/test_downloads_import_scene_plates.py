"""Scene-plate routing for both plate-folder shapes.

Plate folders come in two shapes:

* legacy per-scene ``bg{N}_{方位}_{描述}`` (wushen_juexing), and
* numbered-scene ``s{N}_bg{M}_{方位}_{描述}`` (xianjian_yi_mv) — the ``s{N}_``
  prefix makes plate ids globally unique so two scenes can each own a ``bg1``.

Both must route on the 方位 segment that follows the ``bg{N}_`` part. The
numbered shape also has to survive the ``s1`` / ``s10`` prefix collision when a
drama has ten-plus scenes.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def test_orientation_token_legacy_shape() -> None:
    assert DownloadsImporter._plate_orientation_token("bg1_朝北_高座主位") == "朝北"


def test_orientation_token_numbered_scene_shape() -> None:
    assert DownloadsImporter._plate_orientation_token("s1_bg1_朝北_临街正门") == "朝北"
    assert DownloadsImporter._plate_orientation_token("s10_bg2_摊棚_侧街") == "摊棚"


def test_orientation_token_none_for_non_plate_folders() -> None:
    for name in ("renders", "archive", "frames", "characters", "s1_余杭客栈"):
        assert DownloadsImporter._plate_orientation_token(name) is None


def _scenes(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    scenes = root / "ai_videos" / "d" / "2_世界观人设" / "scenes"
    for scene, plates in {
        "s1_余杭客栈": ("s1_bg1_朝北_临街正门", "s1_bg3_内院_晾晒"),
        "s10_扬州街市": ("s10_bg1_街心_灯笼长廊",),
    }.items():
        for plate in plates:
            (scenes / scene / plate).mkdir(parents=True)
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, downloads


def test_numbered_plate_routes_by_orientation(tmp_path: Path) -> None:
    root, downloads = _scenes(tmp_path)
    drama = root / "ai_videos" / "d"
    dest = _importer(root, downloads)._match_plate_any_scene("s1_bg3_内院_晾晒.png", drama)
    assert dest is not None and dest.name == "s1_bg3_内院_晾晒"


def test_s1_prefix_does_not_swallow_s10_plate(tmp_path: Path) -> None:
    # "s1" is a substring of "s10"; routing must still land in the s10 scene.
    root, downloads = _scenes(tmp_path)
    drama = root / "ai_videos" / "d"
    dest = _importer(root, downloads)._match_plate_any_scene("s10_bg1_街心_灯笼长廊.png", drama)
    assert dest is not None and dest.parent.name == "s10_扬州街市"


def test_panorama_stays_at_scene_root(tmp_path: Path) -> None:
    # The step-1 panorama downloads as the bare scene token — it carries no 方位
    # segment, so it must NOT be pulled into any plate folder.
    root, downloads = _scenes(tmp_path)
    drama = root / "ai_videos" / "d"
    assert _importer(root, downloads)._match_plate_any_scene("s1_水乡客栈.png", drama) is None


def _scene_with(tmp_path: Path, *plates: str) -> tuple[Path, Path]:
    root = tmp_path / "repo"
    scene = root / "ai_videos" / "d" / "2_世界观人设" / "scenes" / "s2_仙灵岛"
    for p in plates:
        (scene / p).mkdir(parents=True)
    return root, scene


def test_longer_orientation_beats_shorter_one_it_contains(tmp_path: Path) -> None:
    root, scene = _scene_with(tmp_path, "s2_bg1_桃林_小径", "s2_bg2_桃林石案_月夜")
    dest = DownloadsImporter._match_scene_plate("s2_bg2_桃林石案_月夜.png", scene)
    assert dest is not None and dest.name == "s2_bg2_桃林石案_月夜"


def test_tied_orientation_refuses_to_guess(tmp_path: Path) -> None:
    # Two plates sharing the 方位 segment `桃林` is a naming defect; routing must
    # bail to the scene root instead of silently picking one.
    root, scene = _scene_with(tmp_path, "s2_bg2_桃林_石案月夜", "s2_bg3_桃林_小径纵深")
    assert DownloadsImporter._match_scene_plate("s2_bg2_桃林_石案月夜.png", scene) is None


def test_sibling_orientation_inside_description_refuses_to_guess(tmp_path: Path) -> None:
    # `s8_bg2_城墙_外水面` carries sibling `s8_bg4_水面_俯视`'s 方位 in its 描述.
    root, scene = _scene_with(tmp_path, "s8_bg2_城墙_外水面", "s8_bg4_水面_俯视")
    assert DownloadsImporter._match_scene_plate("s8_bg2_城墙_外水面.png", scene) is None
