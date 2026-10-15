"""DownloadsImporter routes a shot render by its full `ep{N}_s{N}_st{N}` key into
`episodes/epNN/scenes/sN/shots/stN/renders/<take>/`, one folder per generation
(follow-up 230), keeping the ORIGINAL filename; an incomplete, unknown or
ambiguous key is reported and the file stays in Downloads. The trailing rename
pass never touches `episodes/`.

The old shot routes (`episodes/epNN/shots|prompts/shotNN/`, the `{NN}集{NN}镜`
tag, single-piece `shots/`), intro-card nameplates and `bg{N}_{方位}` scene
plates were removed with the old pipeline (follow-up 233).
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer


def _make_importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    renamer = MediaRenamer(exposed, resolver)
    return DownloadsImporter(exposed, resolver, renamer, downloads_dir=downloads)


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"x")


def test_scene_scoped_keys_route_exactly_and_preserve_unknown_downloads(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    drama = root / "ai_videos/td"
    folders = {}
    for ep, scene, shot in ((1, 1, 1), (1, 10, 1), (1, 1, 10), (2, 1, 1)):
        folder = drama / f"episodes/ep{ep:02d}/scenes/s{scene}/shots/st{shot}"
        folder.mkdir(parents=True)
        folders[f"ep{ep}_s{scene}_st{shot}"] = folder
    background = drama / "2_世界观人设/background/bg2_修道院"
    _touch(background / "bg2_修道院.md")
    downloads = tmp_path / "Downloads"
    names = [f"generator_{key}_参考_bg2_修道院.mp4" for key in folders]
    for name in names:
        _touch(downloads / name)
    unknown = ["ep1_s1_st_参考_bg2_修道院.mp4", "ep1_s1_st99_bg2_修道院.mp4",
               "ep1_s1_st1x_bg2_修道院.mp4", "ep1_s1_st_参考_ep2_s1_st1.mp4"]
    for name in unknown:
        _touch(downloads / name)
    result = _make_importer(root, downloads).import_drama("ai_videos/td")
    assert len(result.moved) == 4
    assert {item["kind"] for item in result.moved} == {"shot"}
    assert len(result.unmatched) == len(unknown)
    assert not result.errors
    for key, folder in folders.items():
        assert (folder / "renders" / f"generator_{key}_参考_bg2_修道院" / f"generator_{key}_参考_bg2_修道院.mp4").is_file()   # one folder per take (follow-up 230)
    assert all((downloads / name).is_file() for name in unknown)
    assert not list(background.glob("*.mp4"))


def test_duplicate_episode_keys_are_reported_without_moving(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    for ep in ("ep01", "ep1"):
        (root / f"ai_videos/td/episodes/{ep}/scenes/s1/shots/st1").mkdir(parents=True)
    downloads = tmp_path / "Downloads"
    _touch(downloads / "ep1_s1_st1.mp4")
    result = _make_importer(root, downloads).import_drama("ai_videos/td")
    assert not result.moved
    assert result.unmatched[0]["reason"] == "ambiguous_shot_key"
    assert (downloads / "ep1_s1_st1.mp4").is_file()


def test_prop_download_routes_to_prop_folder(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    prop = root / "ai_videos" / "td" / "props" / "玉佩"
    prop.mkdir(parents=True)
    _touch(prop / "玉佩.md")  # prop spec already present
    downloads = tmp_path / "Downloads"
    _touch(downloads / "玉佩 道具参考图 半枚螭龙云纹古玉.png")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert {e["kind"] for e in result.moved} == {"prop"}, result.moved
    assert (prop / "玉佩.png").is_file()


def test_rename_pass_preserves_episode_final_cuts(tmp_path: Path) -> None:
    """Regression (follow-up 128): the trailing rename pass must NOT touch
    anything under `episodes/`. Older dramas keep language-tagged final cuts
    `ep{NN}_{lang}.mp4` in `episodes/ep{NN}/`; the folder-name rename would
    collapse two such files (folder `ep01`) to `ep011.mp4` / `ep012.mp4`.
    Importing must leave them intact."""
    root = tmp_path / "repo"
    ep_dir = root / "ai_videos" / "td" / "episodes" / "ep01"
    _touch(ep_dir / "ep01_zh.mp4")
    _touch(ep_dir / "ep01_en.mp4")
    _touch(ep_dir / "script.md")
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert result.errors == []
    # Final cuts keep their deliberate names — NOT renamed to ep01{1,2}.mp4.
    assert (ep_dir / "ep01_zh.mp4").is_file()
    assert (ep_dir / "ep01_en.mp4").is_file()
    assert not (ep_dir / "ep011.mp4").exists()
    assert not (ep_dir / "ep012.mp4").exists()
    renamed_to = {r["to"] for r in result.rename["renamed"]}
    assert not any("episodes/" in t for t in renamed_to), renamed_to


def test_unrelated_file_is_not_imported(tmp_path: Path) -> None:
    """Unmatched downloads are reported but NOT imported: the file stays in
    Downloads untouched and no `not_matched/` folder is created."""
    root = tmp_path / "repo"
    (root / "ai_videos" / "td" / "episodes" / "ep01" / "scenes" / "s1" / "shots" / "st1").mkdir(parents=True)
    downloads = tmp_path / "Downloads"
    _touch(downloads / "totally_unrelated.png")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert result.moved == []
    assert [e["kind"] for e in result.unmatched] == ["unmatched"]
    # File left in place; never moved into the drama tree.
    assert (downloads / "totally_unrelated.png").is_file()
    assert not (root / "ai_videos" / "td" / "not_matched").exists()


def test_old_shot_folders_and_tags_are_no_longer_routes(tmp_path: Path) -> None:
    """`shots/shotNN` folders and the `{NN}集{NN}镜` / `epNN_shotNN` tags are not
    routes any more: such downloads are reported unmatched and stay put."""
    root = tmp_path / "repo"
    old_shot = root / "ai_videos" / "td" / "episodes" / "ep01" / "shots" / "shot01"
    _touch(old_shot / "shot01.md")
    downloads = tmp_path / "Downloads"
    names = ["01集01镜视 远景.mp4", "ep01_shot01.mp4", "shot01_start.png"]
    for name in names:
        _touch(downloads / name)

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert result.moved == []
    assert len(result.unmatched) == len(names)
    assert all((downloads / name).is_file() for name in names)
    assert not (old_shot / "renders").exists()
