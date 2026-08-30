"""Object-prop view routing (ai_video.md rule 4d, follow-up duikang_shangzeng/006).

An OBJECT prop — one whose identity needs several camera angles rather than a
single image — keeps each angle in its own `v{N}_{视角}` sub-folder under the
prop folder, mirroring a scene's `bg{N}_{方位}_{描述}` plates.

The routing key is the 视角 token itself, NOT the prop handle: an out-of-image
tool truncates the download filename to the prompt's first ~9 chars, so a
pinyin-led key (`f80_ferrari_全景` → `f80_ferra`) loses the angle and every view
collides on one file. A leading Chinese view token survives any truncation.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter
from libs.infrastructure.writers.media__writer import MediaRenamer

VIEWS = ("v1_车外全景", "v2_车外正面", "v3_车外侧面", "v4_车外背面")


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    prop = root / "ai_videos" / "d" / "2_世界观人设" / "props" / "f80_ferrari"
    for view in VIEWS:
        (prop / view).mkdir(parents=True)
    _touch(prop / "f80_ferrari.md")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, prop, downloads


def test_view_token_parsing() -> None:
    assert DownloadsImporter._prop_view_token("v1_车外全景") == "车外全景"
    assert DownloadsImporter._prop_view_token("v10_车内正面") == "车内正面"
    for name in ("whitemodel", "renders", "ref_images", "bg1_朝北_临街"):
        assert DownloadsImporter._prop_view_token(name) is None


def test_four_views_route_to_their_own_folders(tmp_path: Path) -> None:
    root, prop, downloads = _drama(tmp_path)
    for view in ("车外全景", "车外正面", "车外侧面", "车外背面"):
        _touch(downloads / f"{view}.png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert {e["kind"] for e in result.moved} == {"prop_view"}, result.moved
    assert result.unmatched == []
    assert result.errors == []
    for folder in VIEWS:
        # renamed to the view-folder name by the rename pass
        assert (prop / folder / f"{folder}.png").is_file(), folder


def test_truncated_filename_still_routes(tmp_path: Path) -> None:
    """The out-of-image tool truncates to the prompt's first line + noise."""
    root, prop, downloads = _drama(tmp_path)
    _touch(downloads / "车外侧面 产品级汽车摄影.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (prop / "v3_车外侧面" / "v3_车外侧面.png").is_file()


def test_reroll_overwrites_only_its_own_view(tmp_path: Path) -> None:
    root, prop, downloads = _drama(tmp_path)
    _touch(prop / "v1_车外全景" / "v1_车外全景.png", b"old-anchor")
    _touch(prop / "v2_车外正面" / "v2_车外正面.png", b"front")
    _touch(downloads / "车外全景 (1).png", b"new-anchor")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (prop / "v1_车外全景" / "v1_车外全景.png").read_bytes() == b"new-anchor"
    assert (prop / "v2_车外正面" / "v2_车外正面.png").read_bytes() == b"front"


def test_prop_root_asset_without_view_token_stays_at_root(tmp_path: Path) -> None:
    root, prop, downloads = _drama(tmp_path)
    _touch(downloads / "f80_ferrari 道具参考图.png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert [e["kind"] for e in result.moved] == ["prop"], result.moved
    assert (prop / "f80_ferrari.png").is_file()


def test_same_view_token_on_two_props_is_not_misrouted(tmp_path: Path) -> None:
    """`车外全景` on one prop and `车内全景` on another are distinct, but an
    ambiguous token shared by two props must go unmatched, never guessed."""
    root, prop, downloads = _drama(tmp_path)
    other = prop.parent / "f80_cockpit"
    (other / "v1_车外全景").mkdir(parents=True)  # deliberately duplicated token
    _touch(downloads / "车外全景.png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert result.moved == []
    assert [e["kind"] for e in result.unmatched] == ["unmatched"]
    assert (downloads / "车外全景.png").is_file()  # left untouched in Downloads


def test_second_object_views_coexist(tmp_path: Path) -> None:
    root, prop, downloads = _drama(tmp_path)
    cockpit = prop.parent / "f80_cockpit"
    (cockpit / "v1_车内全景").mkdir(parents=True)
    _touch(downloads / "车内全景.png")
    _touch(downloads / "车外全景.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (cockpit / "v1_车内全景" / "v1_车内全景.png").is_file()
    assert (prop / "v1_车外全景" / "v1_车外全景.png").is_file()


def test_generated_folders_keep_contract_filenames(tmp_path: Path) -> None:
    """`whitemodel/` holds render-tool output whose `{name}_{tag}.png` naming is
    a downstream contract; the folder-name rename pass must not collapse it."""
    root, prop, downloads = _drama(tmp_path)
    angles = prop / "whitemodel" / "angles"
    for tag in ("front", "side", "rear"):
        _touch(angles / f"f80_ferrari_{tag}.png")
    _touch(downloads / "车外全景.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    for tag in ("front", "side", "rear"):
        assert (angles / f"f80_ferrari_{tag}.png").is_file(), tag
    assert not (angles / "angles1.png").exists()
