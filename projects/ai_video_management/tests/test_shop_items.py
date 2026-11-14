"""商店货单（follow-up 316）：读剧的 `2_世界观人设/props/shop_items.json`，路径换成仓库相对，物品反查出售方。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.shop_items__query import ShopItemsQuery
from libs.common.origin import BoundOrigin
from libs.domain.errors.drama__error import InvalidDramaPathError
from libs.infrastructure.readers.shop_items__reader import ShopItemsReader

DRAMA = "ai_videos/demo"
WORLD = f"{DRAMA}/2_世界观人设"
CLARITY = "props/中立_neutral/p157_Clarity_Potion"
URN = "props/中立_neutral/p187_Urn_of_Shadows"


def item(key: str, folder: str, **extra: str) -> dict[str, str]:
    name = folder.rsplit("/", 1)[-1]
    return {"prop_key": key, "name_zh": extra.get("zh", name), "name_en": extra.get("en", name), "category": extra.get("category", "消耗品"),
            "price": extra.get("price", "50"), "recipe": extra.get("recipe", ""), "card": f"{folder}/{name}.md", "image": f"{folder}/{name}.png"}


def write(root: Path, rel: str, data: bytes = b"x") -> None:
    path = root / WORLD / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    for rel in (f"{CLARITY}/p157_Clarity_Potion.md", f"{CLARITY}/p157_Clarity_Potion.png", f"{URN}/p187_Urn_of_Shadows.md",
                "background/近卫_sentinel/bg22_奇迹古树/bg22_奇迹古树.md", "background/近卫_sentinel/bg22_奇迹古树/bg22_奇迹古树.png",
                "characters/中立_neutral/m302_Supportive_Vestments/m302_Supportive_Vestments.md", "props/shop_items.md"):
        write(tmp_path, rel)
    clarity = item("p157", CLARITY, zh="净化药水", en="Clarity Potion")
    urn = item("p187", URN, zh="影之灵龛", en="Urn of Shadows", category="合成成品", price="250 / 875", recipe="艺人面罩 + 2 力量手套 + 卷轴")
    data = {
        "version": "6.83d", "note": "两边货单相同。",
        "sellers": [
            {"key": "bg22", "name_zh": "奇迹古树", "name_en": "Ancient of Wonders", "kind": "建筑（消耗品商店）", "where": "近卫泉水区 bg13",
             "card": "background/近卫_sentinel/bg22_奇迹古树", "count": 1, "items": [clarity]},
            {"key": "m302", "name_zh": "支援法衣", "name_en": "Supportive Vestments", "kind": "人形商人（合成）", "where": "近卫泉水区",
             "card": "characters/中立_neutral/m302_Supportive_Vestments", "count": 3,
             "items": [urn, clarity, {**clarity, "prop_key": ""}, {**item("p999", "props/x/p999_Evil"), "card": "../../../../etc/passwd",
                                                                    "image": "C:/Windows/win.ini"}]},
            {"name_zh": "没有键"},
        ],
        "items": [{**clarity, "sold_by": ["m302", "bg22"]}],
    }
    write(tmp_path, "props/shop_items.json", json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return tmp_path


def read(repo: Path, drama: str = DRAMA):
    return ShopItemsQuery(ShopItemsReader(repo)).read(drama)


def test_reads_sellers_and_resolves_paths(repo: Path) -> None:
    shop = read(repo)
    assert (shop.drama, shop.source, shop.doc, shop.version, shop.note, shop.error) == (
        DRAMA, f"{WORLD}/props/shop_items.json", f"{WORLD}/props/shop_items.md", "6.83d", "两边货单相同。", "")
    assert [s.key for s in shop.sellers] == ["bg22", "m302"]          # 没有键的出售方不列
    tree = shop.sellers[0]
    assert tree.folder == f"{WORLD}/background/近卫_sentinel/bg22_奇迹古树"
    assert tree.card == f"{tree.folder}/bg22_奇迹古树.md" and tree.image == f"{tree.folder}/bg22_奇迹古树.png"
    assert (tree.kind, tree.where, tree.count) == ("建筑（消耗品商店）", "近卫泉水区 bg13", 1)
    clarity = tree.items[0]
    assert (clarity.prop_key, clarity.name_zh, clarity.name_en, clarity.price) == ("p157", "净化药水", "Clarity Potion", "50")
    assert clarity.card == f"{WORLD}/{CLARITY}/p157_Clarity_Potion.md" and clarity.image == f"{WORLD}/{CLARITY}/p157_Clarity_Potion.png"


def test_missing_files_and_escaping_paths_are_blank(repo: Path) -> None:
    vest = read(repo).sellers[1]
    assert vest.image == ""                                            # 出售方目录里没有同名图
    assert [i.prop_key for i in vest.items] == ["p187", "p157", "p999"]   # 没有 prop_key 的物品不列
    urn, _, evil = vest.items
    assert urn.card.endswith("p187_Urn_of_Shadows.md") and urn.image == ""
    assert (urn.recipe, urn.price, urn.category) == ("艺人面罩 + 2 力量手套 + 卷轴", "250 / 875", "合成成品")
    assert (evil.card, evil.image) == ("", "")


def test_sold_by_is_computed_from_the_sellers(repo: Path) -> None:
    shop = read(repo)
    assert [(i.prop_key, i.sold_by) for i in shop.items] == [("p157", ["bg22", "m302"]), ("p187", ["m302"]), ("p999", ["m302"])]
    assert shop.sellers[0].items[0].sold_by == ["bg22", "m302"]


def test_drama_without_shop_items_is_empty(tmp_path: Path) -> None:
    (tmp_path / WORLD / "props").mkdir(parents=True)
    shop = read(tmp_path)
    assert (shop.source, shop.sellers, shop.items, shop.error) == ("", [], [], "")


def test_broken_json_reports_error(repo: Path) -> None:
    write(repo, "props/shop_items.json", b"{not json")
    shop = read(repo)
    assert shop.source.endswith("shop_items.json") and shop.sellers == [] and shop.error.startswith("读不了 shop_items.json")


@pytest.mark.parametrize("path", ["", "ai_videos", WORLD, "ai_videos/demo/../x", "other/demo"])
def test_rejects_non_drama_paths(repo: Path, path: str) -> None:
    with pytest.raises(InvalidDramaPathError):
        ShopItemsReader(repo).read(path)


def test_api_returns_the_shop_items(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container

    container = Container()
    container.repo_root_path.override(repo)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    body = client.get("/api/shop-items", params={"drama": DRAMA}).json()
    assert [s["key"] for s in body["sellers"]] == ["bg22", "m302"]
    assert body["items"][0]["sold_by"] == ["bg22", "m302"]
    assert body["sellers"][0]["items"][0]["image"].endswith("p157_Clarity_Potion.png")
    bad = client.get("/api/shop-items", params={"drama": WORLD})
    assert bad.status_code == 400 and bad.json()["detail"]["kind"] == "invalid_drama_path"
    assert client.get("/api/shop-items", params={"drama": "ai_videos/nope"}).status_code == 404
