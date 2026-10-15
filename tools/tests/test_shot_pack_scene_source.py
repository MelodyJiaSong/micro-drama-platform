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
