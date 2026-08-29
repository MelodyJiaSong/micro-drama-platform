"""DownloadsImporter multi-form prop routing (follow-up wushen_juexing/105).

One prop folder may hold SEVERAL named ref images (e.g. the 玉佩 ships 完整 /
主角半 / 师兄半 forms from one 组图 generation): a download whose stem starts
with `{prop}_` must keep its underscore variant as `{prop}_{variant}.ext`
instead of collapsing onto the canonical `{prop}.ext` — the old behaviour made
the three forms overwrite each other on import.
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


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _make_prop(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    prop = root / "ai_videos" / "td" / "props" / "玉佩"
    prop.mkdir(parents=True)
    _touch(prop / "玉佩.md")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, prop, downloads


def test_three_prop_forms_coexist_without_overwrite(tmp_path: Path) -> None:
    root, prop, downloads = _make_prop(tmp_path)
    _touch(downloads / "玉佩_完整.png")
    _touch(downloads / "玉佩_师兄半枚.png")
    _touch(downloads / "玉佩 道具参考图 武神令玄玉.png")  # bare handle + prompt text

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert {e["kind"] for e in result.moved} == {"prop"}, result.moved
    assert result.unmatched == []
    assert result.errors == []
    pngs = sorted(p.name for p in prop.iterdir() if p.suffix == ".png")
    assert pngs == ["玉佩.png", "玉佩_完整.png", "玉佩_师兄半枚.png"]


def test_variant_reroll_overwrites_only_its_own_form(tmp_path: Path) -> None:
    root, prop, downloads = _make_prop(tmp_path)
    _touch(prop / "玉佩.png", b"canonical")
    _touch(prop / "玉佩_完整.png", b"old-full")
    # Browser duplicate marker on a re-downloaded form.
    _touch(downloads / "玉佩_完整 (1).png", b"new-full")

    _make_importer(root, downloads).import_drama("ai_videos/td")

    assert (prop / "玉佩_完整.png").read_bytes() == b"new-full"
    assert (prop / "玉佩.png").read_bytes() == b"canonical"  # untouched


def test_variant_with_trailing_prompt_text_routes_to_variant(tmp_path: Path) -> None:
    root, prop, downloads = _make_prop(tmp_path)
    _touch(downloads / "玉佩_师兄半枚 道具参考图 右半镇印之手.png")

    _make_importer(root, downloads).import_drama("ai_videos/td")

    assert (prop / "玉佩_师兄半枚.png").is_file()
    assert not (prop / "玉佩.png").exists()
