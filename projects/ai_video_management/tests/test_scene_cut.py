"""剪辑模块（follow-up 269）：各场 edit/{draft,final}/cut_v{N}.json 读成时间线；草稿剪辑与正片剪辑分开；导航列出有剪辑的场次。"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.queries.scene_cut__query import SceneCutQuery
from libs.common.episode_workflow import WORKFLOW_ID
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.domain.errors.scene_cut__error import SceneCutError
from libs.infrastructure.readers.scene_cut__reader import SceneCutReader
from libs.infrastructure.readers.tree__reader import TreeReader

EPISODE = "ai_videos/demo/episodes/ep01"


def shot(sid: str) -> dict:
    return {"id": sid, "duration": 1, "action": "a", "camera": "c", "dialogue": "", "cast": [], "blocking": "", "beats": "", "lighting": ""}


FILMING = {"scenes": [
    {"id": "s1", "background": "bg1", "location": "门前", "time": "白天", "purpose": "p", "shots": [shot("st1"), shot("st2")]},
    {"id": "s2", "background": "bg1", "location": "路上", "time": "清晨", "purpose": "p", "shots": [shot("st3")]},
]}


def cut(root: Path, scene: str, stage: str, version: int, rendered: bool = True, written_stage: str | None = None, **extra) -> Path:
    folder = root / EPISODE / "scenes" / scene / "edit" / stage
    folder.mkdir(parents=True, exist_ok=True)
    name = f"{scene}_{stage}_v{version}"
    data = {"scene": f"ep01/{scene}", "stage": written_stage or stage, "phase": "粗剪", "version": version, "base_version": version - 1,
            "status": "草稿", "approved_by": None, "made_by": "代理", "notes": ["临时响度"],
            "intentional_violations": [{"shot": "st1", "what": "米莉在门里", "why": "三轮上限"}],
            "events": [
                {"shot": "st1", "take": "20261016-230627_b1c10a24", "in": 1.0, "out": 4.0, "audio_in": 1.0, "audio_out": 4.5, "reason": "建立", "notes": ["L"]},
                {"shot": "st2", "placeholder": True, "duration": 6, "reason": "草稿未生成", "text": ["台词：Hi"]},
                {"shot": "st1", "take": "20261016-230627_b1c10a24", "in": 4.5, "out": 5.0, "reason": "拆出的反应"},
            ],
            "output": {"rendered_at": "2026-10-17T10:00:00", "files": {"clean": {"path": f"{name}.mp4", "duration_s": 9.5},
                                                                   "label": {"path": f"{name}_标注.mp4"}}}}
    data.update(extra)
    (folder / f"cut_v{version}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    if rendered:
        (folder / f"{name}.mp4").write_bytes(b"\x00" * 64)
    return folder


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    (tmp_path / EPISODE / "filming.json").write_text(json.dumps({"content": FILMING, "source_revision": None, "approved_revision": None},
                                                               ensure_ascii=False), encoding="utf-8")
    cut(tmp_path, "s1", "draft", 1)
    cut(tmp_path, "s1", "draft", 2, rendered=False)
    return tmp_path


def test_reads_versions_newest_first_with_timeline(repo: Path) -> None:
    result = SceneCutQuery(SceneCutReader(repo)).read(EPISODE)
    assert [s.scene for s in result.scenes] == ["s1", "s2"]
    s1, s2 = result.scenes
    assert s1.label == "门前 · 白天" and not s1.final and not s2.draft and not s2.final
    assert [v.version for v in s1.draft] == [2, 1]
    newest, older = s1.draft
    assert newest.video == "" and newest.path == f"{EPISODE}/scenes/s1/edit/draft/cut_v2.json"   # 没渲染：没有视频
    assert older.video == f"{EPISODE}/scenes/s1/edit/draft/s1_draft_v1.mp4" and older.labeled_video == ""   # 标注版文件不在
    assert older.duration == 9.5 and older.shots == 2 and older.placeholders == 1
    first, card, reaction = older.events
    assert (first.start, first.duration, first.cut_in, first.cut_out, first.audio_in, first.audio_out) == (0.0, 3.0, 1.0, 4.0, 1.0, 4.5)
    assert card.placeholder and card.start == 3.0 and card.duration == 6 and card.text == ["台词：Hi"]
    assert reaction.start == 9.0 and reaction.audio_in is None   # 声音跟画面一样：不报 J/L
    assert older.violations == [{"shot": "st1", "what": "米莉在门里", "why": "三轮上限"}]


def test_draft_and_final_stay_apart_and_mismatch_is_flagged(repo: Path) -> None:
    cut(repo, "s2", "final", 1, written_stage="draft")   # 放在 final/ 却写 stage=draft
    (repo / EPISODE / "scenes/s1/edit/final").mkdir()
    (repo / EPISODE / "scenes/s1/edit/final/cut_v3.json").write_text("{坏", encoding="utf-8")
    s1, s2 = SceneCutQuery(SceneCutReader(repo)).read(EPISODE).scenes
    assert [v.version for v in s1.final] == [3] and s1.final[0].error.startswith("读不出")
    assert [v.stage for v in s2.final] == ["final"] and "不一致" in s2.final[0].error and not s2.draft


def test_media_names_cannot_escape_the_cut_folder(repo: Path) -> None:
    cut(repo, "s2", "draft", 1, output={"files": {"clean": {"path": "../../../../workflow.json"}}})
    assert SceneCutQuery(SceneCutReader(repo)).read(EPISODE).scenes[1].draft[0].video == ""


def test_rejects_paths_outside_an_episode(repo: Path) -> None:
    with pytest.raises(SceneCutError) as err:
        SceneCutQuery(SceneCutReader(repo)).read("ai_videos/demo/episodes/../../x")
    assert err.value.status_code == 404


def test_api_lists_cuts(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container
    container = Container()
    container.repo_root_path.override(RepoRoot(path=repo).path)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    body = client.get("/api/scene-cuts", params={"episode_path": EPISODE}).json()
    assert [v["version"] for v in body["scenes"][0]["draft"]] == [2, 1]
    assert body["scenes"][0]["draft"][1]["events"][1]["placeholder"] is True
    assert client.get("/api/scene-cuts", params={"episode_path": "ai_videos/demo/episodes/ep09"}).status_code == 404


class _FakeExposed:
    def __init__(self, root: Path) -> None:
        self.root = root

    def excluded_dirs(self):
        return set()


def test_navigation_lists_scenes_with_cuts_under_edit(repo: Path) -> None:
    cut(repo, "s2", "final", 4)
    node = TreeReader(_FakeExposed(repo))._walk_project(repo / "ai_videos/demo")
    edit = next(child for child in node["children"] if child["name"] == "edit")
    episode = edit["children"][0]
    assert episode["type"] == "directory" and episode["navigation_href"].endswith("episode=ep01&module=edit")
    assert [(s["display_name"], [c["display_name"] for c in s["children"]]) for s in episode["children"]] == [
        ("s1 · 门前", ["草稿剪辑 · v2"]), ("s2 · 路上", ["正片剪辑 · v4"])]
    assert episode["children"][1]["children"][0]["navigation_href"].endswith("module=edit&scene=s2&cut=final")
    sound = next(child for child in node["children"] if child["name"] == "sound")
    assert sound["children"][0]["type"] == "workflow"   # 其他占位阶段不变


def joined(root: Path, version: int, **extra) -> Path:
    """集级剪辑决定（follow-up 278）：s1 v1（9.5 秒）叠化 1 秒接 s2 v4（9.5 秒）。"""
    folder = root / EPISODE / "edit" / "final"
    folder.mkdir(parents=True, exist_ok=True)
    data = {"stage": "final", "phase": "锁片", "version": version, "base_version": None, "status": "草稿",
            "head": {"type": "fade_black", "duration": 1}, "tail": {"type": "cut"},
            "scenes": [{"scene": "s1", "cut_version": 1}, {"scene": "s2", "cut_version": 4}],
            "transitions": [{"from": "s1", "to": "s2", "type": "dissolve", "duration": 1.0, "reason": "过了一夜"}],
            "output": {"path": f"ep01_final_v{version}.mp4", "sha256": "aa", "duration_s": 18.0, "rendered_at": "2026-10-18T09:00:00"},
            "independent_review": {"sha256": "aa", "verdict": "可锁片", "open_items": ["调色压黑位"]},
            "changes_from_base": ["s2 换条"]}
    data.update(extra)
    (folder / f"cut_v{version}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    (folder / f"ep01_final_v{version}.mp4").write_bytes(b"\x00" * 64)
    return folder


def test_episode_join_places_scenes_and_names_transitions(repo: Path) -> None:
    cut(repo, "s1", "final", 1)
    cut(repo, "s2", "final", 4)
    folder = joined(repo, 1)
    joined(repo, 2, output={"path": "ep01_final_v2.mp4", "sha256": "bb"})   # 改过之后没重审：审稿结论作废
    (folder / "转场样片_s1_s2.mp4").write_bytes(b"\x00" * 64)
    (folder / "转场样片_s1_s2.txt").write_text("  0.0s  切 cut\n  5.5s  叠化 dissolve 1.0s\n", encoding="utf-8")
    result = SceneCutQuery(SceneCutReader(repo)).read(EPISODE)
    assert not result.joined["draft"] and [v.version for v in result.joined["final"]] == [2, 1]
    stale, first = result.joined["final"]
    assert first.video == f"{EPISODE}/edit/final/ep01_final_v1.mp4" and first.duration == 18.0 and first.head == "淡入 / 淡出（黑）"
    assert [(s.scene, s.cut_version, s.start, s.duration) for s in first.segments] == [("s1", 1, 0.0, 9.5), ("s2", 4, 8.5, 9.5)]
    (tr,) = first.transitions
    assert (tr.name, tr.duration, tr.at, tr.reason) == ("叠化", 1.0, 8.5, "过了一夜")
    assert first.review_verdict == "可锁片" and first.review_items == ["调色压黑位"] and not first.review_stale
    assert stale.review_stale and stale.review_verdict == "" and stale.changes == ["s2 换条"]
    (gallery,) = result.galleries["final"]
    assert (gallery.from_scene, gallery.to_scene, gallery.video) == ("s1", "s2", f"{EPISODE}/edit/final/转场样片_s1_s2.mp4")
    assert [(e.start, e.label) for e in gallery.entries] == [(0.0, "切 cut"), (5.5, "叠化 dissolve 1.0s")]


def test_episode_join_flags_missing_scene_cut(repo: Path) -> None:
    joined(repo, 1)
    first = SceneCutQuery(SceneCutReader(repo)).read(EPISODE).joined["final"][0]
    assert "找不到场剪辑" in first.error and "s2 v4" in first.error


def test_navigation_puts_the_whole_episode_first(repo: Path) -> None:
    cut(repo, "s1", "final", 1)
    joined(repo, 3)
    node = TreeReader(_FakeExposed(repo))._walk_project(repo / "ai_videos/demo")
    episode = next(child for child in node["children"] if child["name"] == "edit")["children"][0]
    whole = episode["children"][0]
    assert whole["name"] == "episode" and [c["display_name"] for c in whole["children"]] == ["正片剪辑 · v3"]
    assert whole["children"][0]["navigation_href"].endswith("module=edit&scene=episode&cut=final")
