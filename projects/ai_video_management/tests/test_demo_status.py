"""英雄 demo 定版标记（follow-up 315）：最高版本的「定版 / 锁片」cut 算定版，发布文案对上定版成片才算 ok。"""
from __future__ import annotations

import json
from pathlib import Path

from libs.infrastructure.readers.demo_status__reader import DemoStatusReader

CHARS = "ai_videos/dota/2_世界观人设/characters"


def hero(root: Path, rel: str, cuts: dict[int, str], publish: str | None = None, videos: tuple[int, ...] = ()) -> Path:
    folder = root / CHARS / rel
    final = folder / "demo" / "edit" / "final"
    final.mkdir(parents=True)
    (folder / f"{folder.name}.md").write_text("# x\n", encoding="utf-8")
    for version, status in cuts.items():
        data = {"version": version, "status": status, "output": {"file": f"ep01_final_v{version}.mp4"}}
        (final / f"cut_v{version}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    for version in videos:
        (final / f"ep01_final_v{version}.mp4").write_bytes(b"x")
    if publish is not None:
        (folder / "demo" / "publish.md").write_text(publish, encoding="utf-8")
    return folder


def test_finalized_heroes_and_publish_state(tmp_path: Path) -> None:
    (tmp_path / "ai_videos" / "dota" / "workflow.json").parent.mkdir(parents=True, exist_ok=True)
    hero(tmp_path, "天灾_scourge/c65_Axe", {8: "待用户看", 9: "定版"},
         "# 发布文案\n\n> 视频：`edit/final/ep01_final_v8.mp4`（53 s）\n", videos=(9,))
    hero(tmp_path, "近卫_sentinel/c2_Stone_Giant", {3: "锁片（用户定版）", 4: "定版（取代 v3）", 5: "待用户看"},
         "> 视频：`edit/final/ep01_final_v4.mp4`\n", videos=(4,))
    hero(tmp_path, "近卫_sentinel/c42_Slayer", {1: "待用户看"}, videos=(1,))
    hero(tmp_path, "天灾_scourge/c60_Chaos_Knight", {2: "被 v3 取代", 3: "定版"})

    got = {s.folder: s for s in DemoStatusReader(tmp_path).read()}
    assert set(got) == {"c65_Axe", "c2_Stone_Giant", "c60_Chaos_Knight"}

    axe = got["c65_Axe"]
    assert (axe.version, axe.publish_video, axe.publish_state) == (9, "ep01_final_v8.mp4", "stale")
    assert axe.video.endswith("c65_Axe/demo/edit/final/ep01_final_v9.mp4")

    tiny = got["c2_Stone_Giant"]
    assert (tiny.version, tiny.newer, tiny.publish_state) == (4, [5], "ok")

    ck = got["c60_Chaos_Knight"]
    assert (ck.version, ck.video, ck.publish, ck.publish_state) == (3, "", "", "missing")
