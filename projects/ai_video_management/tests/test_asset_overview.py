"""资产总览（follow-up 293）：人物、背景、道具各一节，按分组、键号排，每个资产一格。"""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.asset_overview__query import AssetOverviewQuery
from libs.common.origin import BoundOrigin
from libs.domain.errors.drama__error import InvalidDramaPathError
from libs.infrastructure.readers.asset_overview__reader import AssetOverviewReader

DRAMA = "ai_videos/demo"
WORLD = f"{DRAMA}/2_世界观人设"


def card(root: Path, rel: str, head: str = "", files: tuple[str, ...] = ()) -> Path:
    folder = root / WORLD / rel
    folder.mkdir(parents=True)
    name = folder.name
    if head is not None:
        (folder / f"{name}.md").write_text(head, encoding="utf-8")
    for f in files:
        (folder / f).write_bytes(b"x")
    return folder


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    card(tmp_path, "characters/近卫_sentinel/c24_Anti_Mage",
         "> 键：`c24`　｜　近卫 / 敏捷\n> 状态：立绘用 v3。\n\n# 敌法师 · Anti-Mage · Magina\n\n> 不是开头的引用\n",
         ("c24_Anti_Mage_v10.png", "c24_Anti_Mage.png", "c24_Anti_Mage_v2.png"))
    axe = card(tmp_path, "characters/天灾_scourge/c65_Axe", "# 斧王 · Axe\n", ("c65_Axe.png", "old.mp4", "c65_Axe_turntable.mp4"))
    os.utime(axe / "old.mp4", (100, 100))
    os.utime(axe / "c65_Axe_turntable.mp4", (200, 200))
    (axe / "skills" / "k651_x").mkdir(parents=True)
    card(tmp_path, "characters/近卫_sentinel/m100_Treant", "# 树人\n")
    card(tmp_path, "characters/近卫_sentinel/c3_Omniknight", "# 全能骑士 · Omniknight\n", ("ref_v1.png",))
    card(tmp_path, "characters/中立_neutral/m7_Roshan", "# 肉山 · Roshan\n", ("m7_Roshan.png",))
    card(tmp_path, "background/近卫_sentinel/bg4_近卫中路一塔", "# 近卫中路一塔\n", ("bg4_近卫中路一塔.png",))
    card(tmp_path, "background/中立_neutral/bg1_中路河道交叉口", "# 中路河道交叉口\n", ("bg1_中路河道交叉口.png",))
    (tmp_path / WORLD / "background/中立_neutral/bg1_中路河道交叉口/planning").mkdir()
    card(tmp_path, "props/中立_neutral/p10_Divine_Rapier", "# 圣剑 · Divine Rapier\n", ("p10_Divine_Rapier.png",))
    card(tmp_path, "props/近卫_sentinel/p29_月刃", None, ("p29_月刃.png",))
    return tmp_path


def overview(repo: Path):
    return AssetOverviewQuery(AssetOverviewReader(repo)).read(DRAMA)


def test_sections_groups_and_key_order(repo: Path) -> None:
    o = overview(repo)
    assert [(s.kind, s.label, s.count) for s in o.sections] == [("characters", "人物", 5), ("background", "背景", 2), ("props", "道具", 2)]
    chars = o.sections[0]
    # 分组按组里最小的键：近卫 c3 → 天灾 c65 → 中立 m7；组内英雄 c 在召唤物 m 前
    assert [g.name for g in chars.groups] == ["近卫_sentinel", "天灾_scourge", "中立_neutral"]
    assert [t.key for t in chars.groups[0].tiles] == ["c3", "c24", "m100"]
    assert [g.name for g in o.sections[1].groups] == ["中立_neutral", "近卫_sentinel"]
    assert o.watch == [f"{WORLD}/background", f"{WORLD}/characters", f"{WORLD}/props"]


def test_tile_reads_title_meta_portrait_images_and_videos(repo: Path) -> None:
    am = overview(repo).sections[0].groups[0].tiles[1]
    assert (am.key, am.name, am.title) == ("c24", "敌法师", "敌法师 · Anti-Mage · Magina")
    assert am.meta == ["键：`c24`　｜　近卫 / 敏捷", "状态：立绘用 v3。"]
    assert am.card == f"{WORLD}/characters/近卫_sentinel/c24_Anti_Mage/c24_Anti_Mage.md"
    assert [p.rsplit("/", 1)[-1] for p in am.images] == ["c24_Anti_Mage.png", "c24_Anti_Mage_v2.png", "c24_Anti_Mage_v10.png"]
    axe = overview(repo).sections[0].groups[1].tiles[0]
    assert [p.rsplit("/", 1)[-1] for p in axe.videos] == ["c65_Axe_turntable.mp4", "old.mp4"]


def test_portrait_fallbacks(repo: Path) -> None:
    chars = overview(repo).sections[0].groups[0].tiles
    assert chars[0].portrait.endswith("ref_v1.png")       # 没有同名图，取第一张
    assert chars[2].portrait == "" and chars[2].images == []
    rapier, moon = (g.tiles[0] for g in overview(repo).sections[2].groups)
    assert moon.card == "" and moon.name == "p29_月刃" and moon.portrait.endswith("p29_月刃.png")


@pytest.mark.parametrize("path", ["", "ai_videos", f"{WORLD}", "ai_videos/_series", "ai_videos/demo/../x", "other/demo"])
def test_rejects_non_drama_paths(repo: Path, path: str) -> None:
    with pytest.raises(InvalidDramaPathError):
        AssetOverviewReader(repo).read(path)


def test_api_returns_the_overview(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container

    container = Container()
    container.repo_root_path.override(repo)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    body = client.get("/api/asset-overview", params={"drama": DRAMA}).json()
    assert [s["count"] for s in body["sections"]] == [5, 2, 2]
    assert body["sections"][0]["groups"][0]["tiles"][1]["portrait"].endswith("c24_Anti_Mage.png")
    bad = client.get("/api/asset-overview", params={"drama": WORLD})
    assert bad.status_code == 400 and bad.json()["detail"]["kind"] == "invalid_drama_path"
    missing = client.get("/api/asset-overview", params={"drama": "ai_videos/nope"})
    assert missing.status_code == 404
