"""审查单索引 /api/review-runs（follow-up 333）：左侧导航「审查单」一类的数据源。"""
from __future__ import annotations

import json

from fastapi.testclient import TestClient

from libs.common.exposed_tree import ExposedTree
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.infrastructure.readers.review_run__reader import ReviewRunReader
from tests.conftest import make_app


def write_run(tmp_path, drama, name, **extra):
    d = tmp_path / "ai_videos" / drama / "reviews" / name
    d.mkdir(parents=True)
    run = {"id": name, "title": name, "episode": "ep01", "loop": 1, "state": "已完成", "created_at": name.split("_")[1],
           "items": [{"status": "done", "findings": {"重出": 2, "记录": 1}}, {"status": "failed"}, {"status": "pending"}], **extra}
    (d / "checklist.json").write_text(json.dumps(run, ensure_ascii=False), encoding="utf-8")
    return d.relative_to(tmp_path).as_posix()


def test_lists_runs_of_flat_and_series_dramas_newest_first(tmp_path):
    old = write_run(tmp_path, "demo", "ep01_20261101-080000_pregen_r1")
    new = write_run(tmp_path, "series/demo2", "ep02_20261102-080000_pregen_r2", loop=2, chain="ep02_x_r1")
    (tmp_path / "ai_videos" / "demo" / "reviews" / "broken").mkdir()
    (tmp_path / "ai_videos" / "demo" / "reviews" / "broken" / "checklist.json").write_text("{", encoding="utf-8")
    runs = ReviewRunReader(ExposedTree(tmp_path)).list().runs
    assert [r["dir"] for r in runs] == [new, old]
    assert runs[0]["drama"] == "ai_videos/series/demo2" and runs[0]["loop"] == 2 and runs[0]["chain"] == "ep02_x_r1"
    assert runs[1]["totals"] == {"重出": 2, "可剪": 0, "记录": 1, "存疑": 0}
    assert (runs[1]["done"], runs[1]["failed"], runs[1]["total"]) == (1, 1, 3)
    assert (runs[1]["stage"], runs[1]["scenes"], runs[1]["max_loops"]) == ("", [], 3)


def test_summary_carries_stage_scenes_and_max_loops(tmp_path):
    """剧页故事板按场找最新一张出片前审查单（follow-up 336）。"""
    write_run(tmp_path, "demo", "ep01_20261101-080000_pregen_r1", stage="pregen", scenes=["s1", "s8"], max_loops=3)
    run = ReviewRunReader(ExposedTree(tmp_path)).list().runs[0]
    assert (run["stage"], run["scenes"], run["max_loops"]) == ("pregen", ["s1", "s8"], 3)


def test_summary_carries_what_the_nav_groups_by(tmp_path):
    """导航按「集 → 范围（集 + 阶段 + 场）」分组、每个范围标最新一张（用户 2026-11-08：看不出哪个是最新的）。"""
    write_run(tmp_path, "demo", "ep01_20261108-153208_pregen_r1", stage="pregen", scenes=["s1"], chain="ep01_20261108-153208_pregen_r1",
              title="ep01 · 场一 · 出片前（第 2 次） 第 1 轮 · 11-08 15:32", created_at="2026-11-08T15:32:08")
    run = ReviewRunReader(ExposedTree(tmp_path)).list().runs[0]
    assert {k: run[k] for k in ("title", "created_at", "episode", "stage", "scenes", "chain", "loop")} == {
        "title": "ep01 · 场一 · 出片前（第 2 次） 第 1 轮 · 11-08 15:32", "created_at": "2026-11-08T15:32:08", "episode": "ep01",
        "stage": "pregen", "scenes": ["s1"], "chain": "ep01_20261108-153208_pregen_r1", "loop": 1}


def test_api_returns_runs(tmp_path):
    write_run(tmp_path, "demo", "ep01_20261101-080000_pregen_r1")
    client = TestClient(make_app(RepoRoot(path=tmp_path), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    response = client.get("/api/review-runs")
    assert response.status_code == 200 and response.json()["runs"][0]["drama_name"] == "demo"


def test_checklist_endpoint_reads_runs_over_the_file_size_cap(tmp_path):
    """v5 审查单的 checklist.json 常超过 /api/file 的 1 MiB 上限（场二到场八第 2 轮 1.5 MB），审查页单独读。"""
    rel = write_run(tmp_path, "demo", "ep01_20261108-153205_pregen_r2", padding="字" * 600_000)
    assert (tmp_path / rel / "checklist.json").stat().st_size > 1_048_576
    client = TestClient(make_app(RepoRoot(path=tmp_path), BoundOrigin(host="127.0.0.1", port=8766)), base_url="http://127.0.0.1:8766")
    ok = client.get("/api/review-runs/checklist", params={"path": rel})
    assert ok.status_code == 200 and ok.json()["id"] == "ep01_20261108-153205_pregen_r2"
    for bad in ("ai_videos/demo", "ai_videos/demo/reviews/missing", "ai_videos/demo/reviews/../reviews/x", "../x/reviews/y"):
        assert client.get("/api/review-runs/checklist", params={"path": bad}).status_code == 404, bad


def test_lists_and_reads_edu_video_line_reviews(tmp_path):
    """教学视频台词审（tools/edu_review.py）的审查单在 edu_videos/<系列>/<知识点>/reviews/lines_rN/（用户 2026-11-08：审查结果记录在审查单下面）。"""
    d = tmp_path / "edu_videos" / "ai_terms" / "t01_overfitting" / "reviews" / "lines_r1"
    d.mkdir(parents=True)
    run = {"id": "lines_r1", "title": "t01 · 台词审 第 1 轮", "episode": "t01_overfitting", "loop": 1, "stage": "lines",
           "state": "已收轮", "created_at": "2026-11-08T22:28:00", "items": [{"status": "done"}]}
    (d / "checklist.json").write_text(json.dumps(run, ensure_ascii=False), encoding="utf-8")
    reader = ReviewRunReader(ExposedTree(tmp_path))
    runs = reader.list().runs
    assert [r["dir"] for r in runs] == ["edu_videos/ai_terms/t01_overfitting/reviews/lines_r1"]
    assert runs[0]["drama_name"] == "t01_overfitting" and runs[0]["stage"] == "lines"
    assert reader.checklist("edu_videos/ai_terms/t01_overfitting/reviews/lines_r1")["title"] == "t01 · 台词审 第 1 轮"
    assert reader.checklist("edu_videos/ai_terms/reviews/lines_r1") is None
