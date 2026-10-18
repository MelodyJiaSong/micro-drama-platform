"""整集审片串联（follow-up 260）：每镜最新一条按分镜顺序拼成一条，带章节；输入不变就复用，最新一条读不出就退用上一条。"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
import pytest
from fastapi.testclient import TestClient

from libs.application.commands.review_reel__command import ReviewReelCommand
from libs.application.queries.review_reel__query import ReviewReelQuery
from libs.common.episode_workflow import WORKFLOW_ID
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.domain.errors.review_reel__error import ReviewReelError
from libs.domain.value_objects.review_reel__valueobject import ReelClip, ReviewReelPlan
from libs.infrastructure.readers.review_reel__reader import ReviewReelReader
from libs.infrastructure.writers.review_reel__writer import ReviewReelWriter

EPISODE = "ai_videos/demo/episodes/ep01"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def shot(sid: str) -> dict:
    return {"id": sid, "duration": 1, "action": "a", "camera": "c", "dialogue": "", "cast": [], "blocking": "", "beats": "", "lighting": ""}


FILMING = {"scenes": [
    {"id": "s1", "background": "bg1", "location": "门前", "time": "白天", "purpose": "p", "shots": [shot("st1"), shot("st2")]},
    {"id": "s2", "background": "bg1", "location": "路上", "time": "清晨", "purpose": "p", "shots": [shot("st3")]},
]}


def video(path: Path, seconds: float, size: str, rate: int, audio: bool, audio_seconds: float | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    args = [FFMPEG, "-y", "-v", "error", "-f", "lavfi", "-i", f"testsrc=size={size}:rate={rate}:duration={seconds}"]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=frequency=440:sample_rate=44100:duration={audio_seconds or seconds}", "-c:a", "aac", "-ac", "1"]
    args += ["-c:v", "libx264", "-pix_fmt", "yuv420p", *([] if audio_seconds else ["-shortest"]), str(path)]
    subprocess.run(args, check=True, capture_output=True)
    return path


def take(root: Path, scene: str, st: str, stamp: str, seconds: float = 1.0, size: str = "640x360", rate: int = 25,
         audio: bool = True, status: str | None = None, broken: bool = False, mtime: float | None = None,
         audio_seconds: float | None = None) -> Path:
    folder = root / EPISODE / "scenes" / scene / "shots" / st / "renders" / stamp
    mp4 = folder / f"{stamp}.mp4"
    if broken:
        folder.mkdir(parents=True, exist_ok=True)
        mp4.write_bytes(b"\x00\x00\x00\x18ftypmp42 half written")
    else:
        video(mp4, seconds, size, rate, audio, audio_seconds)
    if status:
        (folder / "review.md").write_text(f"# 审核\n\n状态：{status}\n", encoding="utf-8")
    if mtime is not None:
        os.utime(mp4, (mtime, mtime))
    return folder


def probe(path: Path) -> str:
    return subprocess.run([FFMPEG, "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / EPISODE).mkdir(parents=True)
    (tmp_path / "ai_videos/demo/workflow.json").write_text(json.dumps({"workflow": WORKFLOW_ID}), encoding="utf-8")
    (tmp_path / EPISODE / "filming.json").write_text(json.dumps({"content": FILMING, "source_revision": None, "approved_revision": None},
                                                               ensure_ascii=False), encoding="utf-8")
    take(tmp_path, "s1", "st1", "20261015-100000_old", seconds=2.0, mtime=1_700_000_000)
    take(tmp_path, "s1", "st1", "20261015-120000_new", seconds=1.0, status="候选", mtime=1_700_000_100)
    take(tmp_path, "s2", "st3", "20261015-130000_only", seconds=1.0, size="320x240", rate=24, audio=False, status="建议重出")
    return tmp_path


def build(root: Path, scene: str | None = None):
    reader, writer = ReviewReelReader(root), ReviewReelWriter(root)
    command = ReviewReelCommand(reader, writer, spawn=lambda job: job())   # run inline
    query = ReviewReelQuery(reader)
    return command, query


def test_plan_chapters_follow_clip_order_and_durations() -> None:
    clips = [ReelClip("s1", "ep1_s1_st1", "a/t1", "a/t1/v.mp4", 10, 1, "候选", ""),
             ReelClip("s2", "ep1_s2_st3", "a/t3", "a/t3/v.mp4", 20, 2, "", "")]
    plan = ReviewReelPlan("ep01_all", None, clips, [{"key": "ep1_s1_st2", "scene": "s1", "reason": "还没有生成"}])
    chapters = plan.chapters([2.0, 1.5])
    assert [(c["key"], c["start"], c["end"]) for c in chapters] == [("ep1_s1_st1", 0.0, 2.0), ("ep1_s2_st3", 2.0, 3.5)]
    assert plan.fingerprint == ReviewReelPlan("ep01_all", None, list(clips), []).fingerprint
    moved = [ReelClip("s1", "ep1_s1_st1", "a/t1", "a/t1/v.mp4", 11, 1, "候选", ""), clips[1]]
    assert plan.fingerprint != ReviewReelPlan("ep01_all", None, moved, []).fingerprint


def test_builds_reel_from_latest_take_in_filming_order(repo: Path) -> None:
    command, query = build(repo)
    assert query.read(EPISODE, None).state == "none"
    result = command.start(EPISODE, None)
    assert result.state == "done", result.error
    manifest = result.manifest
    assert [c["key"] for c in manifest["chapters"]] == ["ep1_s1_st1", "ep1_s2_st3"]
    first, second = manifest["chapters"]
    assert first["take"].endswith("20261015-120000_new") and first["review_status"] == "候选"
    assert second["review_status"] == "建议重出"
    assert first["start"] == 0 and abs(first["end"] - 1.0) < 0.1 and abs(second["start"] - first["end"]) < 1e-6
    assert manifest["skipped"] == [{"key": "ep1_s1_st2", "scene": "s1", "reason": "还没有生成"}]
    out = repo / result.video_path
    assert result.video_path == f"{EPISODE}/review_reel/ep01_all.mp4" and out.is_file()
    info = probe(out)
    assert "1280x720" in info and "Audio: aac" in info
    total = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    assert total and abs(float(total[3]) - manifest["duration"]) < 0.2


def test_unchanged_inputs_reuse_and_new_take_marks_stale(repo: Path) -> None:
    command, query = build(repo)
    first = command.start(EPISODE, None)
    out = repo / first.video_path
    stamp = out.stat().st_mtime_ns
    again = command.start(EPISODE, None)
    assert again.state == "done" and out.stat().st_mtime_ns == stamp
    assert query.read(EPISODE, None).stale is False
    take(repo, "s1", "st2", "20261015-140000_fresh", status="候选")
    assert query.read(EPISODE, None).stale is True
    rebuilt = command.start(EPISODE, None)
    assert [c["key"] for c in rebuilt.manifest["chapters"]] == ["ep1_s1_st1", "ep1_s1_st2", "ep1_s2_st3"]
    assert rebuilt.manifest["skipped"] == [] and query.read(EPISODE, None).stale is False


def test_scene_filter_and_half_written_latest_falls_back(repo: Path) -> None:
    take(repo, "s1", "st1", "20261015-150000_writing", broken=True, mtime=1_700_000_200)
    command, query = build(repo)
    one = command.start(EPISODE, "s1")
    assert one.state == "done" and one.video_path.endswith("review_reel/ep01_s1.mp4")
    chapter = one.manifest["chapters"][0]
    assert chapter["take"].endswith("20261015-120000_new") and "上一条" in chapter["note"]
    assert [c["key"] for c in one.manifest["chapters"]] == ["ep1_s1_st1"]
    assert query.read(EPISODE, None).state == "none"   # 整集的串联是另一份


def test_rejects_unknown_scene_and_paths_outside_episodes(repo: Path) -> None:
    command, query = build(repo)
    with pytest.raises(ReviewReelError):
        command.start(EPISODE, "s9")
    with pytest.raises(ReviewReelError):
        query.read("ai_videos/demo/episodes/../../x", None)


def test_api_starts_reel_and_media_serves_ranges(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container
    container = Container()
    container.repo_root_path.override(RepoRoot(path=repo).path)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.review_reel_command.override(ReviewReelCommand(ReviewReelReader(repo), ReviewReelWriter(repo), spawn=lambda job: job()))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    assert client.get("/api/review-reel", params={"episode_path": EPISODE}).json()["state"] == "none"
    started = client.post("/api/review-reel", json={"episode_path": EPISODE, "scene": None}, headers={"Origin": "http://127.0.0.1:8765"})
    assert started.status_code == 200, started.text
    body = client.get("/api/review-reel", params={"episode_path": EPISODE}).json()
    assert body["state"] == "done" and [s["id"] for s in body["scenes"]] == ["s1", "s2"]
    ranged = client.get("/api/media", params={"path": body["video_path"]}, headers={"Range": "bytes=0-99"})
    assert ranged.status_code == 206 and len(ranged.content) == 100
    bad = client.get("/api/review-reel", params={"episode_path": EPISODE, "scene": "s9"})
    assert bad.status_code == 404


def test_audio_longer_than_picture_is_cut_to_the_picture(repo: Path) -> None:
    """真实素材里有音轨比画面长的条（s2 有 7 秒画面配 16–22 秒音轨）：每段必须按画面长度截断，串联总长才等于章节总长。"""
    take(repo, "s1", "st2", "20261015-160000_long_audio", seconds=1.0, audio_seconds=4.0)
    command, _ = build(repo)
    reel = command.start(EPISODE, None)
    assert reel.state == "done", reel.error
    info = probe(repo / reel.video_path)
    total = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    assert total and abs(float(total[3]) - reel.manifest["duration"]) < 0.2
    assert abs(reel.manifest["duration"] - 3.0) < 0.2
