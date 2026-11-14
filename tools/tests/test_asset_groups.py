"""卡目录可直接在 characters/ / props/ 下，也可在一层分组目录下（dota_yingxiong follow-up 025，
ai_video_management follow-up 284）。平铺与分组两种都测；只读本地假剧目录，不调任何外部服务。"""
from pathlib import Path

import pytest

from tools import char_assets, episode_shots, gen_outfit_views, gen_turntable_videos, props_lib, skill_pack, gen_char_images

LAYOUTS = {"flat": "", "grouped": "近卫_sentinel"}


def _card(root: Path, group: str, name: str, body: str = "") -> Path:
    d = root / group / name if group else root / name
    d.mkdir(parents=True)
    (d / f"{name}.md").write_text(f"# {name}\n{body}", encoding="utf-8")
    return d


@pytest.fixture(params=sorted(LAYOUTS))
def world(request: pytest.FixtureRequest, tmp_path: Path) -> tuple[Path, str]:
    drama = tmp_path / "ai_videos" / "demo"
    (drama / "2_世界观人设").mkdir(parents=True)
    (drama / "workflow.json").write_text("{}", encoding="utf-8")
    return drama / "2_世界观人设", LAYOUTS[request.param]


def test_card_lookup_finds_cards_in_either_layout(world: tuple[Path, str]) -> None:
    settings, group = world
    axe = _card(settings / "characters", group, "c65_Axe")
    _card(settings / "characters", "天灾_scourge" if group else "", "c8_Lich")
    assert episode_shots.card_dir(settings.parent, "c65") == axe
    assert gen_turntable_videos.chars_root(axe) == settings / "characters"
    rows = char_assets.rows(settings / "characters", [])
    assert [r.dir.name for r in rows] == ["c8_Lich", "c65_Axe"]


def test_outfit_card_dir_follows_the_group(world: tuple[Path, str], monkeypatch: pytest.MonkeyPatch) -> None:
    settings, group = world
    axe = _card(settings / "characters", group, "c65_Axe")
    monkeypatch.setattr(gen_outfit_views, "REPO", settings.parents[2])
    assert gen_outfit_views.card_dir("demo", "c65_Axe") == axe
    with pytest.raises(SystemExit, match="c9_Nobody"):
        gen_outfit_views.card_dir("demo", "c9_Nobody")


def test_turntable_todo_lists_grouped_cards(world: tuple[Path, str]) -> None:
    settings, group = world
    _card(settings / "characters", group, "c65_Axe", "```text\nc65_Axe_turntable\n比例：画幅 9:16，时长 4 秒\n```\n")
    assert [d.name for d in gen_turntable_videos.todo(settings / "characters", ["c65"])] == ["c65_Axe"]


def test_props_find_and_scene_objects_in_either_layout(world: tuple[Path, str]) -> None:
    settings, group = world
    group = group and "中立_neutral"
    rune = _card(settings / "props", group, "p1_极速神符")
    (rune / "asset.toml").write_text('key = "p1"\n', encoding="utf-8")
    legacy = _card(settings / "props", "", "玉佩")
    assert props_lib.find(settings, "p1") == rune
    assert props_lib.scene_objects(settings) == [rune]
    assert props_lib.in_props(rune)
    assert set(props_lib.prop_dirs(settings / "props")) == {rune, legacy}


def test_skill_cards_and_their_refs_resolve_under_a_group(world: tuple[Path, str], monkeypatch: pytest.MonkeyPatch) -> None:
    settings, group = world
    axe = _card(settings / "characters", group, "c65_Axe")
    portrait = axe / "c65_Axe.png"
    portrait.write_bytes(b"png")
    rel = portrait.relative_to(settings).as_posix()
    skill = axe / "skills" / "k651_Call"
    skill.mkdir(parents=True)
    (skill / "k651_Call.md").write_text(
        f"# k651\n## 技能视频 prompt\n视频参考: axe={rel}\n```text\nk651_Call_clip\n时长：10秒\n```\n", encoding="utf-8")
    monkeypatch.setattr(skill_pack, "REPO", settings.parents[2])
    assert skill_pack.skill_dirs("demo", []) == [skill]
    shot = skill_pack.shot(skill)
    assert shot is not None and shot["refs"][0]["path"] == portrait.relative_to(settings.parents[2]).as_posix()


def test_class_skill_cards_are_found_next_to_hero_skills(world: tuple[Path, str], monkeypatch: pytest.MonkeyPatch) -> None:
    settings, group = world
    hero = _card(settings / "characters", group, "c65_Axe") / "skills" / "k651_Call"
    hero.mkdir(parents=True)
    (hero / "k651_Call.md").write_text("# k651\n", encoding="utf-8")
    holy = settings / "classes" / "cl2_圣骑士" / "skills" / "k201_圣光术"
    holy.mkdir(parents=True)
    (holy / "k201_圣光术.md").write_text("# k201\n", encoding="utf-8")
    (holy / "notes.md").write_text("不是卡\n", encoding="utf-8")
    monkeypatch.setattr(skill_pack, "REPO", settings.parents[2])
    assert set(skill_pack.skill_dirs("demo", [])) == {hero, holy}
    assert skill_pack.skill_dirs("demo", ["k201"]) == [holy]


def test_turntable_job_uploads_prop_anchor_after_portrait(world: tuple[Path, str]) -> None:
    """dota_yingxiong follow-up 071：参考行立绘之后的 `p{N}_…` 项上传道具锚点图，填 @图片2。"""
    settings, group = world
    axe = _card(settings / "characters", group, "c65_Axe",
                "```text\nc65_Axe_turntable\n参考: `c65_Axe(立绘)=>@`、`p30_Axe_Great_Axe(斧头)=>@`\n"
                "比例：画幅 16:9，时长 10 秒\n```\n")
    (axe / "c65_Axe.png").write_bytes(b"png")
    prop = _card(settings / "props", group and "天灾_scourge", "p30_Axe_Great_Axe")
    (prop / "p30_Axe_Great_Axe.png").write_bytes(b"png")
    stem, imgs, audio, body, ratio, dur = gen_turntable_videos.job(axe)
    assert (stem, imgs, audio, ratio, dur) == ("c65_Axe_turntable", [axe / "c65_Axe.png", prop / "p30_Axe_Great_Axe.png"], [], "16:9", 10)
    assert "`c65_Axe(立绘)=>@图片1`、`p30_Axe_Great_Axe(斧头)=>@图片2`" in body
    (prop / "p30_Axe_Great_Axe.png").unlink()
    with pytest.raises(SystemExit, match="p30_Axe_Great_Axe"):
        gen_turntable_videos.job(axe)


def test_declared_weapon_is_required_and_uploaded_for_portrait_and_video(world, monkeypatch):
    settings, group = world
    hero = _card(settings / "characters", group, "c1_Hero",
                 "武器参考: p1\n# Seedream 立绘 prompt\n```text\nc1_Hero\n一名西欧白人战士。\n比例: 9:16\n```\n"
                 "```text\nc1_Hero_turntable\n参考: `c1_Hero=>@`\n比例：画幅 16:9，时长 10 秒\n```\n")
    (hero / "c1_Hero.png").write_bytes(b"portrait")
    with pytest.raises(FileNotFoundError, match="固定武器 p1"):
        gen_char_images.Job(hero, gen_char_images.KINDS["characters"][0], "9:16")
    prop = _card(settings / "props", group, "p1_Sword")
    image = prop / "p1_Sword.png"
    image.write_bytes(b"sword")
    job = gen_char_images.Job(hero, gen_char_images.KINDS["characters"][0], "9:16")
    assert job.refs == [image]
    sent = []
    monkeypatch.setattr(gen_char_images.ci, "render", lambda text, refs, out, aspect: sent.extend(refs) or "ok")
    gen_char_images.run_one(job, "codex", None)
    assert sent == [image]
    stem, images, audio, body, _, _ = gen_turntable_videos.job(hero)
    assert images == [hero / "c1_Hero.png", image]
    assert "`p1_Sword=>@图片2`" in body


def test_skill_automatically_adds_declared_weapon_once(world, monkeypatch):
    settings, group = world
    hero = _card(settings / "characters", group, "c1_Hero", "武器参考: p1\n")
    portrait = hero / "c1_Hero.png"
    portrait.write_bytes(b"portrait")
    prop = _card(settings / "props", group, "p1_Sword")
    (prop / "p1_Sword.png").write_bytes(b"sword")
    skill = hero / "skills/k11_Call"
    skill.mkdir(parents=True)
    (skill / "k11_Call.md").write_text(
        f"## 技能视频 prompt\n视频参考: hero={portrait.relative_to(settings).as_posix()}\n"
        "```text\nk11_Call_clip\n时长：10秒\n参考：`hero=>@`\n```\n",encoding="utf-8")
    monkeypatch.setattr(skill_pack, "REPO", settings.parents[2])
    shot = skill_pack.shot(skill)
    assert [r["key"] for r in shot["refs"]] == ["hero", "p1_Sword"]
    assert "`p1_Sword=>@`" in shot["text"]
    (prop / "p1_Sword.png").unlink()
    with pytest.raises(FileNotFoundError, match="先生成并验收"):
        skill_pack.shot(skill)
