"""换装 / 状态变体三面图的参考键（tools/gen_outfit_views.py）：view.refs 既收装备键 e…，也收道具键 p…
（shengji_zhilu follow-up 031：亚伦背着裹锤长包 p476 的状态变体要挂长包的正面图）。只读本地假剧目录，不调任何外部服务。"""
from pathlib import Path

import pytest
from PIL import Image

from tools import gen_outfit_views as gov

CARD = """# Hero · 阿明 · 主角

| # | 字段 | 值 |
|---|---|---|
| 8 | **角色识别标签**（≤30 字） | `瘦高青年，灰布衣布靴` |
"""
EQUIPMENT = """[meta]
key_digits = [1, 2]

[[slot]]
name = "头"
body = "头上"
empty = "头盔"
display = "单独摆放"

[[slot]]
name = "主手"
body = "手里"
empty = "兵器"
display = "斜放"
declare = false
"""
REGISTRY = """[[item]]
key = "e101"
name_zh = "旧锤"
slot = "主手"
tier = "白"
"""
ITEM = 'lock = "长柄旧锤"\n'


def _png(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (4, 4), "gray").save(path)
    return path


@pytest.fixture
def world(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    world = tmp_path / "ai_videos" / "demo" / "2_世界观人设"
    hero = world / "characters" / "c1_Hero"
    hero.mkdir(parents=True)
    (hero / "c1_Hero.md").write_text(CARD, encoding="utf-8")
    for role in ("front", "side", "back"):
        _png(hero / "views" / f"c1_Hero_{role}.png")
    equipment = world / "equipment"
    (equipment / "loadouts").mkdir(parents=True)
    (equipment / "equipment.toml").write_text(EQUIPMENT, encoding="utf-8")
    (equipment / "registry.toml").write_text(REGISTRY, encoding="utf-8")
    (equipment / "e101_白_旧锤").mkdir()
    (equipment / "e101_白_旧锤" / "item.toml").write_text(ITEM, encoding="utf-8")
    _png(equipment / "e101_白_旧锤" / "e101-1_正面.png")
    _png(world / "props" / "p9_旧布包" / "p9-1_正面.png")
    monkeypatch.setattr(gov, "REPO", tmp_path)
    return world


def _outfit(world: Path, stage: str) -> gov.Outfit:
    (world / "equipment" / "loadouts" / "c1_Hero.toml").write_text(
        'character = "c1_Hero"\nbase = []\n\n[[stage]]\n' + stage, encoding="utf-8")
    [outfit] = gov.outfits("demo", [])
    return outfit


VARIANT = 'id = "ep01_s2_背包"\nepisodes = []\nwear = []\nview = { key = "c1-2", name = "背包", refs = ["p9"], look = "背着长包" }\n'


def test_prop_key_in_refs_attaches_the_prop_front_image(world: Path) -> None:
    text, handles, refs = gov.prompts("demo", _outfit(world, VARIANT))["正面"]
    assert refs == [world / "characters" / "c1_Hero" / "views" / "c1_Hero_front.png",
                    world / "props" / "p9_旧布包" / "p9-1_正面.png"]
    assert handles[1] == "`p9-1_正面(道具·形制)=>@`"
    assert "其余参考图依次是旧布包，只锁这几件道具的形制、材质与配色，照搬道具外观" in text


def test_prop_anchor_image_wins_over_front_view(world: Path) -> None:
    anchor = _png(world / "props" / "p9_旧布包" / "p9_旧布包.png")
    _, handles, refs = gov.prompts("demo", _outfit(world, VARIANT))["正面"]
    assert refs[1] == anchor
    assert handles[1] == "`p9_旧布包(道具·形制)=>@`"


def test_equipment_and_prop_refs_mix_in_order(world: Path) -> None:
    stage = VARIANT.replace('refs = ["p9"]', 'refs = ["e101", "p9"]')
    text, handles, refs = gov.prompts("demo", _outfit(world, stage))["正面"]
    assert [p.name for p in refs[1:]] == ["e101-1_正面.png", "p9-1_正面.png"]
    assert handles[1:] == ["`e101-1_正面(装备·形制)=>@`", "`p9-1_正面(道具·形制)=>@`"]
    assert "其余参考图依次是旧锤、旧布包，只锁这几件装备与道具的形制" in text


def test_no_refs_front_names_only_the_anchor(world: Path) -> None:
    # 背上空着的状态变体（shengji_zhilu c1-11 / c1-12）不挂道具：不能留「其余参考图依次是，…照搬装备外观」
    text, handles, refs = gov.prompts("demo", _outfit(world, VARIANT.replace('refs = ["p9"]', "refs = []")))["正面"]
    assert refs == [world / "characters" / "c1_Hero" / "views" / "c1_Hero_front.png"]
    assert len(handles) == 1
    assert "其余参考图" not in text and "照搬装备外观" not in text
    assert "参考用法：只有参考图一，只锁这个人的长相、体型与便服，不照搬参考图的构图与背景。" in text


def test_unknown_prop_key_stops_with_its_name(world: Path) -> None:
    outfit = _outfit(world, VARIANT.replace('refs = ["p9"]', 'refs = ["p404"]'))
    with pytest.raises(SystemExit, match="p404"):
        gov.prompts("demo", outfit)


def test_nothing_worn_leaves_no_empty_gear_field_and_no_held_object(world: Path) -> None:
    ps = gov.prompts("demo", _outfit(world, VARIANT))
    for text, _, _ in ps.values():
        assert "本套装备：。" not in text
        assert "本套状态：背着长包。" in text
    assert "拿着的东西" not in ps["背面"][0]


def test_weapon_in_hand_keeps_gear_field_and_held_object(world: Path) -> None:
    stage = 'id = "ep01"\nepisodes = ["ep01"]\nwear = ["e101"]\nview = { key = "c1-1", name = "锤", refs = ["e101"] }\n'
    ps = gov.prompts("demo", _outfit(world, stage))
    assert "本套装备：主手——长柄旧锤。" in ps["正面"][0]
    assert "他右手一侧（连同右手拿着的东西）在画面右边" in ps["背面"][0]
    assert "整集" in gov.card("demo", _outfit(world, stage))


BACK_BY_STATE = "参考图一是正面、看不到后背，后背的样子（泥、破口、背着的东西）以「本套状态」为准"


def test_state_variant_back_view_takes_the_back_from_the_state_text(world: Path) -> None:
    # 正面图看不到后背：一身泥的状态变体只写「配色一律不变」，后背会照正面画成几块泥（shengji_zhilu c1-10）
    ps = gov.prompts("demo", _outfit(world, VARIANT))
    assert BACK_BY_STATE in ps["背面"][0]
    assert BACK_BY_STATE not in ps["侧面"][0] and BACK_BY_STATE not in ps["正面"][0]


def test_back_view_without_state_text_is_unchanged(world: Path) -> None:
    stage = 'id = "ep01"\nepisodes = ["ep01"]\nwear = ["e101"]\nview = { key = "c1-1", name = "锤", refs = ["e101"] }\n'
    assert BACK_BY_STATE not in gov.prompts("demo", _outfit(world, stage))["背面"][0]


def test_variant_card_says_it_is_not_picked_by_episode(world: Path) -> None:
    card = gov.card("demo", _outfit(world, VARIANT))
    assert "整集" not in card
    assert "状态变体" in card


MIRRORED = "左右翻转后的镜像"


def _back_view_call(world: Path, monkeypatch: pytest.MonkeyPatch, engine: str) -> tuple[str, list[Path]]:
    """只缺背面图时跑 images()：各家出图都换成本地假实现，记下背面那一次拿到的 (prompt, 参考图)。"""
    outfit = _outfit(world, VARIANT)
    gov.build("demo", [outfit])
    folder = world / "characters" / "c1_Hero" / outfit.folder
    front = _png(folder / "c1-2_front.png")
    _png(folder / "c1-2_side.png")
    calls: list[tuple[str, list[Path]]] = []

    def fake(text: str, refs: list[Path], out: Path, *_: object) -> str:
        calls.append((text, list(refs)))
        _png(out)
        return "fake"

    monkeypatch.setattr(gov.bgi, "_upload_copy", lambda p: p)
    monkeypatch.setattr(gov.ci, "render", fake)
    monkeypatch.setattr(gov, "_dreamina", lambda text, refs, out: fake(text, refs, out) and 0)
    monkeypatch.setattr(gov, "_eleven", fake)
    monkeypatch.setattr(gov, "_mirror", lambda p: p.with_name(p.stem + "_mirror.png"))
    assert gov.images("demo", [outfit], engine, force=False) == []
    [(text, refs)] = calls
    assert refs[1] == world / "characters" / "c1_Hero" / "views" / "c1_Hero_back.png"
    return text, [front, *refs]


@pytest.mark.parametrize("engine", ["codex", "elevenlabs"])
def test_gpt_image_engines_get_the_unmirrored_front_for_the_back_view(world: Path, monkeypatch: pytest.MonkeyPatch,
                                                                      engine: str) -> None:
    # GPT 图像自己会转身：喂正面的镜像它再转一次，背面左右就反了（状态变体 c1-9 / c1-10 首批 Codex 实测，出图时编号写作 c1-2 / c1-3）
    text, (front, sent, _) = _back_view_call(world, monkeypatch, engine)
    assert sent == front
    assert MIRRORED not in text


def test_dreamina_still_gets_the_mirrored_front_for_the_back_view(world: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # 即梦照搬参考图里东西在画面哪一边：背面仍喂正面的镜像（c2-1 首批即梦实测）
    text, (front, sent, _) = _back_view_call(world, monkeypatch, "dreamina")
    assert sent == front.with_name("c1-2_front_mirror.png")
    assert MIRRORED in text
