"""One folder per subject, several named views inside it.

A scene subject (`bg1_广场`) holds every angle of that place — `广场正向.png`,
`广场反向.png`, `广场材质.png` — plus one .md carrying all their prompts. The
download is named after the prompt's first line (the view key), so the importer
must keep that key as the filename and overwrite only that view; and the
folder-name rename pass must leave those names alone, because collapsing them
to `bg1_广场{N}.png` both loses the view identity and reshuffles it on every
import.
"""
from __future__ import annotations

from pathlib import Path

from libs.common.exposed_tree import ExposedTree
from libs.common.safe_resolve import SafeResolver
from libs.infrastructure.writers.downloads__writer import DownloadsImporter, _view_key
from libs.infrastructure.writers.media__writer import MediaRenamer


def _importer(root: Path, downloads: Path) -> DownloadsImporter:
    exposed = ExposedTree(root)
    resolver = SafeResolver(root)
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    scenes = root / "ai_videos" / "d" / "2_世界观人设" / "scenes"
    plaza = scenes / "bg1_广场"
    plaza.mkdir(parents=True)
    _touch(plaza / "bg1_广场.md", b"# prompts")
    (scenes / "bg2_主街").mkdir(parents=True)
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, plaza, downloads


def test_view_key_extraction() -> None:
    assert _view_key("广场正向 电影级实拍", "bg1_广场") == "广场正向"
    assert _view_key("广场反向 (1)", "bg1_广场") == "广场反向"
    assert _view_key("广场", "bg1_广场") == "广场"
    # a name that does not start with a folder token must not claim the namespace
    assert _view_key("随便什么图", "bg1_广场") is None


def test_several_views_coexist_in_one_folder(tmp_path: Path) -> None:
    root, plaza, downloads = _drama(tmp_path)
    for view in ("广场正向", "广场反向", "广场材质"):
        _touch(downloads / f"{view} 电影级实拍.png")

    result = _importer(root, downloads).import_drama("ai_videos/d")

    assert result.unmatched == [] and result.errors == []
    got = sorted(p.name for p in plaza.iterdir() if p.suffix == ".png")
    assert got == ["广场primary.png".replace("primary", "反向"),
                   "广场材质.png", "广场正向.png"]


def test_reroll_overwrites_only_that_view(tmp_path: Path) -> None:
    root, plaza, downloads = _drama(tmp_path)
    _touch(plaza / "广场正向.png", b"old-anchor")
    _touch(plaza / "广场反向.png", b"reverse")
    _touch(downloads / "广场正向 (1).png", b"new-anchor")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (plaza / "广场正向.png").read_bytes() == b"new-anchor"
    assert (plaza / "广场反向.png").read_bytes() == b"reverse"


def test_rename_pass_leaves_view_names_alone(tmp_path: Path) -> None:
    root, plaza, downloads = _drama(tmp_path)
    for view in ("广场正向", "广场反向", "广场斜瞰"):
        _touch(plaza / f"{view}.png")
    _touch(downloads / "广场材质.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    got = sorted(p.name for p in plaza.iterdir() if p.suffix == ".png")
    assert got == ["广场反向.png", "广场斜瞰.png", "广场材质.png", "广场正向.png"]
    assert not (plaza / "bg1_广场1.png").exists()


def test_longer_subject_token_wins_over_shorter(tmp_path: Path) -> None:
    """`广场复原` is its own subject; its views must not fall into `广场`."""
    root, plaza, downloads = _drama(tmp_path)
    restored = plaza.parent / "bg6_广场复原"
    restored.mkdir()
    _touch(downloads / "广场复原正向.png")
    _touch(downloads / "广场正向.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (restored / "广场复原正向.png").is_file()
    assert (plaza / "广场正向.png").is_file()
    assert not (plaza / "广场复原正向.png").exists()


def test_md_beside_the_views_is_untouched(tmp_path: Path) -> None:
    root, plaza, downloads = _drama(tmp_path)
    _touch(downloads / "广场正向.png")

    _importer(root, downloads).import_drama("ai_videos/d")

    assert (plaza / "bg1_广场.md").read_bytes() == b"# prompts"
