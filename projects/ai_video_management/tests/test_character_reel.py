"""人物卡「样片与正片」（follow-up 286）：人物视频＋各技能最新正式条、各技能全部草稿、接进这个人物素材的剪辑成片。"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.character_reel__query import CharacterReelQuery
from libs.common.origin import BoundOrigin
from libs.domain.errors.character_video__error import NotCharacterCardDirError
from libs.infrastructure.readers.character_reel__reader import CharacterReelReader

DRAMA = "ai_videos/demo"
AXE = f"{DRAMA}/2_世界观人设/characters/天灾_scourge/c65_Axe"
TREANT = f"{DRAMA}/2_世界观人设/characters/近卫_sentinel/m1_Treant"


def take(skill: Path, kind: str, name: str, stamp: int, **record) -> str:
    folder = skill / kind / name
    folder.mkdir(parents=True)
    video = folder / f"{skill.name}_clip.mp4"
    video.write_bytes(b"\x00" * 16)
    os.utime(video, (stamp, stamp))
    if record:
        (folder / "generation.json").write_text(json.dumps(record), encoding="utf-8")
    return video.as_posix()


def skill(root: Path, folder: str, title: str, icon: bool = True) -> Path:
    path = root / AXE / "skills" / folder
    path.mkdir(parents=True)
    (path / f"{folder}.md").write_text(f"> 键：`{folder[:4]}`\n\n# {title}\n\n## 画面\n", encoding="utf-8")
    if icon:
        (path / "icon").mkdir()
        (path / "icon" / f"{folder.split('_')[0]}_icon_dota1.png").write_bytes(b"png")
    return path


def cut(root: Path, stage: str, version: int, clips: list[str], rendered: bool = True, under: str = f"{DRAMA}/episodes/ep01") -> None:
    folder = root / under / "edit" / stage
    folder.mkdir(parents=True, exist_ok=True)
    name = f"ep01_{stage}_v{version}.mp4"
    data = {"stage": stage, "version": version, "status": "待用户看", "note": f"第 {version} 版",
            "events": [{"clip": c, "in": 0, "out": 5} for c in clips], "output": {"file": name, "duration": 12.5}}
    (folder / f"cut_v{version}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    if rendered:
        (folder / name).write_bytes(b"\x00")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    axe = tmp_path / AXE
    axe.mkdir(parents=True)
    (axe / "c65_Axe.md").write_text("# 斧王\n", encoding="utf-8")
    (axe / "c65_Axe_turntable.mp4").write_bytes(b"\x00")
    (tmp_path / TREANT).mkdir(parents=True)
    q = skill(tmp_path, "k651_Berserkers_Call", "狂战士的怒吼 · Berserker's Call")
    for n in (1, 3, 2):
        (q / f"k651_Berserkers_Call_peak_v{n}.png").write_bytes(b"png")
    take(q, "drafts", "20261018-160642_2008d025", 100, submit_id="2008d025-e0be", credits=120, downloaded_at="2026-10-18T16:06:42")
    take(q, "drafts", "20261018-172230_a7d756bd", 200, submit_id="a7d756bd-439c", credits=120)
    (q / "drafts" / ".pending").mkdir()
    take(q, "renders", "20261018-190000_00000001", 300, submit_id="00000001-x", credits=286)
    take(q, "renders", "20261018-202244_656a8814", 400, submit_id="656a8814-400b", credits=286, downloaded_at="2026-10-18T20:22:44")
    r = skill(tmp_path, "k654_Culling_Blade", "淘汰之刃 · Culling Blade", icon=False)
    (r / "k654_Culling_Blade_peak.png").write_bytes(b"png")
    (r / "k654_Culling_Blade_peak_v9.png").write_bytes(b"png")
    skill(tmp_path, "k652_Battle_Hunger", "战斗饥渴 · Battle Hunger")
    draft = f"{AXE}/skills/k651_Berserkers_Call/drafts/20261018-172230_a7d756bd/k651_Berserkers_Call_clip.mp4"
    cut(tmp_path, "draft", 1, [draft])
    cut(tmp_path, "draft", 2, [f"{AXE}/c65_Axe_turntable.mp4", draft], rendered=False)
    cut(tmp_path, "final", 1, [f"{AXE}/skills/k651_Berserkers_Call/renders/20261018-202244_656a8814/k651_Berserkers_Call_clip.mp4"])
    cut(tmp_path, "draft", 3, [f"{TREANT}/m1_Treant_turntable.mp4"])
    return tmp_path


def test_finals_are_the_turntable_plus_each_skills_newest_render_in_key_order(repo: Path) -> None:
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(AXE)
    assert reel.turntable is not None and reel.turntable.video == f"{AXE}/c65_Axe_turntable.mp4"
    assert [s.key for s in reel.skills] == ["k651", "k652", "k654"]
    q = reel.skills[0]
    assert q.title == "狂战士的怒吼 · Berserker's Call"
    assert q.icon.endswith("icon/k651_icon_dota1.png")
    assert q.final is not None and q.final.id == "20261018-202244_656a8814"
    assert (q.final.submit_id, q.final.credits, q.final.generated_at) == ("656a8814", 286, "2026-10-18T20:22:44")
    assert len(q.finals) == 2
    assert reel.skills[1].final is None and reel.skills[1].drafts == []
    assert reel.skills[2].icon == ""


def test_drafts_newest_first_with_peak_and_stamp_fallback(repo: Path) -> None:
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(AXE)
    q, r = reel.skills[0], reel.skills[2]
    assert [d.submit_id for d in q.drafts] == ["a7d756bd", "2008d025"]
    assert q.drafts[0].generated_at == "2026-10-18T17:22:30"
    assert q.peak.endswith("k651_Berserkers_Call_peak_v3.png")
    assert r.peak.endswith("k654_Culling_Blade_peak.png")


def test_cuts_that_use_this_characters_clips_by_stage_newest_version_first(repo: Path) -> None:
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(AXE)
    assert [c.version for c in reel.cuts["draft"]] == [2, 1]
    assert [c.version for c in reel.cuts["final"]] == [1]
    v2, v1 = reel.cuts["draft"]
    assert v2.video == "" and v1.video == f"{DRAMA}/episodes/ep01/edit/draft/ep01_draft_v1.mp4"
    assert (v1.note, v1.duration, v1.episode) == ("第 1 版", 12.5, "ep01")
    assert reel.watch == [AXE, f"{DRAMA}/episodes"]


def test_card_without_skills_has_nothing_to_review(repo: Path) -> None:
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(TREANT)
    assert reel.skills == [] and reel.turntable is None
    assert [c.version for c in reel.cuts["draft"]] == [3]


@pytest.mark.parametrize("path", [f"{AXE}/skills", f"{DRAMA}/2_世界观人设/characters/天灾_scourge", "ai_videos/demo/../x", f"{AXE}/../c99_None"])
def test_rejects_paths_that_are_not_a_card_folder(repo: Path, path: str) -> None:
    with pytest.raises(NotCharacterCardDirError):
        CharacterReelReader(repo).read(path)


def test_api_returns_the_reel(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container

    container = Container()
    container.repo_root_path.override(repo)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    body = client.get("/api/character-reel", params={"path": AXE}).json()
    assert [s["key"] for s in body["skills"]] == ["k651", "k652", "k654"]
    assert body["skills"][0]["final"]["credits"] == 286
    assert len(body["cuts"]["draft"]) == 2
    bad = client.get("/api/character-reel", params={"path": f"{AXE}/skills"})
    assert bad.status_code == 400 and bad.json()["detail"]["kind"] == "not_a_character_dir"


def test_demo_cuts_in_the_character_folder_come_first(repo: Path) -> None:
    """follow-up 288：没有分集的剧把英雄 demo 放人物目录 demo/edit/{draft,final}/，全算这个人物的，排在各集剪辑前。"""
    demo = f"{AXE}/demo"
    cut(repo, "draft", 1, [f"{AXE}/c65_Axe_turntable.mp4"], under=demo)
    cut(repo, "draft", 2, [], rendered=False, under=demo)
    cut(repo, "final", 6, [], under=demo)
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(AXE)
    assert [(c.episode, c.version) for c in reel.cuts["draft"]] == [("demo", 2), ("demo", 1), ("ep01", 2), ("ep01", 1)]
    assert [(c.episode, c.version, c.own) for c in reel.cuts["final"]] == [("demo", 6, True), ("ep01", 1, False)]
    mine = reel.cuts["draft"][1]
    assert mine.path == f"{demo}/edit/draft/cut_v1.json" and mine.video == f"{demo}/edit/draft/ep01_draft_v1.mp4"
    assert reel.cuts["draft"][0].video == ""
    other = CharacterReelQuery(CharacterReelReader(repo)).read(TREANT)
    assert [c.episode for c in other.cuts["draft"]] == ["ep01"]


def test_drama_without_episodes_reads_only_the_demo_folder(repo: Path) -> None:
    import shutil

    shutil.rmtree(repo / DRAMA / "episodes")
    cut(repo, "final", 1, [], under=f"{AXE}/demo")
    reel = CharacterReelQuery(CharacterReelReader(repo)).read(AXE)
    assert reel.cuts["draft"] == []
    assert [(c.episode, c.version) for c in reel.cuts["final"]] == [("demo", 1)]
