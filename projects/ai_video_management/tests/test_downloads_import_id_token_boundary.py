"""DownloadsImporter id-token boundary matching (xianjian_yi_mv, 2026-08-02).

An asset folder's id prefix (`c1`, `p3`, `p4`, `s10`) is a short ascii token,
and `_classify` used to substring-test it against the FULL filename including
the extension. Two consequences, both live:

* `p4` ⊂ "mp4" — every `.mp4` download scored a hit on `props/p4_…`; tying on
  token length with the character's own `c1` it then won on kind_priority
  (prop 3 > character 1), so all five character turntable videos landed in
  `props/p4_蝴蝶/`. `p3` ⊂ "mp3" is the same bug on the audio path.
* `s1` ⊂ "s10_…" — previously survived only because the longer `s10` token
  out-scored it; the boundary test makes it a non-match outright.
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
    return DownloadsImporter(exposed, resolver, MediaRenamer(exposed, resolver), downloads_dir=downloads)


def _touch(path: Path, payload: bytes = b"x") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _make_drama(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "repo"
    world = root / "ai_videos" / "td" / "2_世界观人设"
    char = world / "characters" / "c1_李逍遥"
    _touch(char / "c1_李逍遥.md")
    _touch(world / "characters" / "c9_姥姥" / "c9_姥姥.md")
    _touch(world / "props" / "p3_纸伞" / "p3_纸伞.md")
    _touch(world / "props" / "p4_蝴蝶" / "p4_蝴蝶.md")
    downloads = tmp_path / "Downloads"
    downloads.mkdir()
    return root, char, downloads


def test_mp4_extension_does_not_route_to_p4_prop(tmp_path: Path) -> None:
    root, char, downloads = _make_drama(tmp_path)
    _touch(downloads / "jimeng-2026-08-02-3616-c1_江湖游侠 · 男主角 · 游侠态 — 4s 单 take 角色 refer....mp4")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert [e["kind"] for e in result.moved] == ["character"], result.moved
    assert result.unmatched == []
    assert (root / "ai_videos" / "td" / "2_世界观人设" / "props" / "p4_蝴蝶").is_dir()
    assert list((root / "ai_videos" / "td" / "2_世界观人设" / "props" / "p4_蝴蝶").glob("*.mp4")) == []
    assert [p.name for p in char.glob("*.mp4")] == ["c1_李逍遥.mp4"]


def test_mp3_extension_does_not_route_to_p3_prop(tmp_path: Path) -> None:
    root, _char, downloads = _make_drama(tmp_path)
    _touch(downloads / "c9_白发老妇 · 段2 配角 声样.mp3")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert [e["kind"] for e in result.moved] == ["character"], result.moved
    assert list((root / "ai_videos" / "td" / "2_世界观人设" / "props" / "p3_纸伞").glob("*.mp3")) == []


def test_id_token_still_matches_on_underscore_boundary(tmp_path: Path) -> None:
    """The normal join key — download named from the prompt handle `c9_白发老妇`
    while the folder is `c9_姥姥` — must keep matching on the `c9` id."""
    root, _char, downloads = _make_drama(tmp_path)
    _touch(downloads / "jimeng-2026-08-02-3572-c9_白发老妇 · 段2 配角 · 山居守护老妪.png")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert [e["kind"] for e in result.moved] == ["character"], result.moved
    laolao = root / "ai_videos" / "td" / "2_世界观人设" / "characters" / "c9_姥姥"
    assert "c9_姥姥" in result.moved[0]["to"]
    assert [p.name for p in laolao.glob("*.png")] == ["c9_姥姥.png"]


def test_short_id_does_not_match_inside_longer_id(tmp_path: Path) -> None:
    root, _char, downloads = _make_drama(tmp_path)
    scenes = root / "ai_videos" / "td" / "2_世界观人设" / "scenes"
    _touch(scenes / "s1_余杭客栈" / "s1_余杭客栈.md")
    _touch(scenes / "s10_扬州街市" / "s10_扬州街市.md")
    _touch(downloads / "s10_扬州街市 全景底图.png")

    result = _make_importer(root, downloads).import_drama("ai_videos/td")

    assert len(result.moved) == 1, result.moved
    assert "s10_扬州街市" in result.moved[0]["to"]
    assert list((scenes / "s1_余杭客栈").glob("*.png")) == []
