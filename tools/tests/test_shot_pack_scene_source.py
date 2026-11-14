"""A scene compiled on its own (follow-up 259) carries `source`; shot_pack judges that scene by it, so a fresh scene's
packs stay valid while another scene's filming changed, and a legacy scene without `source` still follows the episode."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from tools import shot_pack


def scene(sid: str, action: str) -> dict:
    return {"id": sid, "background": "bg1", "location": "门前", "time": "白天", "purpose": "p",
            "shots": [{"id": "st1", "duration": 5, "action": action}]}


def write(ep: Path, filming_scenes: list[dict], prompt_scenes: list[dict], doc_source: str | None) -> None:
    ep.mkdir(parents=True, exist_ok=True)
    (ep / "filming.json").write_text(json.dumps({"content": {"scenes": filming_scenes}, "source_revision": "story-1",
                                                 "approved_revision": None}), encoding="utf-8")
    (ep / "prompts.json").write_text(json.dumps({"content": {"compiler_version": shot_pack.COMPILER_VERSION,
                                                             "scenes": prompt_scenes},
                                                 "source_revision": doc_source, "approved_revision": None}), encoding="utf-8")


def compiled(sid: str, source: str | None) -> dict:
    out = {"id": sid, "shots": [{"id": f"ep1_{sid}_st1", "text": f"ep1_{sid}_st1", "refs": []}]}
    return out if source is None else {**out, "source": source}


def stale(shots: list[dict]) -> dict[str, bool]:
    return {s["id"]: bool(s.get("stale")) for s in shots}


def test_scene_source_decides_staleness_per_scene(tmp_path: Path) -> None:
    ep = tmp_path / "ep01"
    s1, s2 = scene("s1", "旧动作"), scene("s2", "新动作")
    old_s1 = copy.deepcopy(s1)
    s1["shots"][0]["action"] = "分镜改过"
    write(ep, [s1, s2], [compiled("s1", shot_pack.scene_revision(old_s1, "story-1")),
                         compiled("s2", shot_pack.scene_revision(s2, "story-1"))], doc_source="old")
    shots, reason = shot_pack.episode_problems(ep)
    assert reason == ""
    assert stale(shots) == {"ep1_s1_st1": True, "ep1_s2_st1": False}


def test_scene_without_source_follows_the_episode_revision(tmp_path: Path) -> None:
    ep = tmp_path / "ep01"
    write(ep, [scene("s1", "a")], [compiled("s1", None)], doc_source="old")
    shots, _ = shot_pack.episode_problems(ep)
    assert stale(shots) == {"ep1_s1_st1": True}


def test_scene_dropped_from_filming_is_stale(tmp_path: Path) -> None:
    ep = tmp_path / "ep01"
    gone = scene("s9", "a")
    write(ep, [scene("s1", "a")], [compiled("s9", shot_pack.scene_revision(gone, "story-1"))], doc_source="old")
    shots, _ = shot_pack.episode_problems(ep)
    assert stale(shots) == {"ep1_s9_st1": True}


def test_a_shot_group_is_packed_in_its_own_folder_and_follows_its_scene(tmp_path: Path) -> None:
    """镜组 (follow-up 331): `ep1_s1_g2` lives in scenes/s1/groups/g2 and goes stale with its scene."""
    ep = tmp_path / "ep01"
    s1 = scene("s1", "a")
    entry = {**compiled("s1", shot_pack.scene_revision(s1, "story-1")),
             "groups": [{"id": "ep1_s1_g2", "shots": ["ep1_s1_st1"], "text": "ep1_s1_g2", "refs": []}]}
    write(ep, [s1], [entry], doc_source="old")
    shots, _ = shot_pack.episode_problems(ep)
    assert stale(shots) == {"ep1_s1_st1": False, "ep1_s1_g2": False}
    assert shot_pack.shot_dir(ep, "s1", "ep1_s1_g2") == ep / "scenes" / "s1" / "groups" / "g2"
    assert shot_pack.shot_dir(ep, "s1", "ep1_s1_st1") == ep / "scenes" / "s1" / "shots" / "st1"
    s1["shots"][0]["action"] = "分镜改过"
    write(ep, [s1], [entry], doc_source="old")
    assert stale(shot_pack.episode_problems(ep)[0]) == {"ep1_s1_st1": True, "ep1_s1_g2": True}


def test_an_older_compile_invalidates_every_pack(tmp_path: Path) -> None:
    """shot_pack reads COMPILER_VERSION from the app (no second copy); prompts from the previous version (e.g. v12,
    before v13 limited voices to speakers and dropped the 「本场」 line) must be recompiled before any pack is valid."""
    current = shot_pack.COMPILER_VERSION
    assert current >= 13
    ep = tmp_path / "ep01"
    s1 = scene("s1", "a")
    write(ep, [s1], [compiled("s1", shot_pack.scene_revision(s1, "story-1"))], doc_source="old")
    doc = json.loads((ep / "prompts.json").read_text(encoding="utf-8"))
    doc["content"]["compiler_version"] = current - 1
    (ep / "prompts.json").write_text(json.dumps(doc), encoding="utf-8")
    shots, reason = shot_pack.episode_problems(ep)
    assert [s["id"] for s in shots] == ["ep1_s1_st1"]
    assert reason == "prompts.json 是编译器 v%d 的结果，当前是 v%d：重新编译" % (current - 1, current)
