"""流程与自检（dota_yingxiong follow-up 257）：仓库级与剧级分开返回、不混；只读。"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from fastapi.testclient import TestClient

from libs.common.origin import BoundOrigin
from libs.common.process_qc import REPO_REGISTRY
from libs.common.repo_root import RepoRoot
from tests.conftest import make_app

REPO_REG = '[[check]]\nid = "video.no_text"\nstage = "video"\nkind = "machine"\ngate = true\nauto = false\nbasis = "共用规则：不烧字幕"\n'
DRAMA_REG = ('[[check]]\nid = "video.scale"\nstage = "video"\nkind = "review"\ngate = true\nauto = false\n'
             'sources = ["demo#245"]\n')


def build(root: Path) -> None:
    (root / REPO_REGISTRY).parent.mkdir(parents=True)
    (root / REPO_REGISTRY).write_text(REPO_REG, encoding="utf-8")
    demo = root / "ai_videos" / "demo"
    (demo / "renders" / "20261026-130000_aa").mkdir(parents=True)
    (demo / "workflow.json").write_text("{}", encoding="utf-8")
    (demo / "qc_checks.toml").write_text(DRAMA_REG, encoding="utf-8")
    (demo / "renders" / "20261026-130000_aa" / "qc.json").write_text(json.dumps(
        {"artifact": "a.mp4", "checks": {"video.scale": {"verdict": "pass"}, "video.no_text": {"verdict": "未审"}}}), encoding="utf-8")
    (root / "ai_videos" / "other").mkdir()
    (root / "ai_videos" / "other" / "workflow.json").write_text("{}", encoding="utf-8")
    spec = root / "specs" / "ai_video" / "demo"
    (spec / "user_input" / "follow_ups").mkdir(parents=True)
    today = dt.date.today().isoformat()
    (spec / "user_input" / "follow_ups" / "202610.md").write_text(
        f"## 001 — {today} 10:00:00 — a\n\nx\n\n## 002 — {today} 11:00:00 — b\n\ny\n\n## 002 — {today} 12:00:00 — c\n", encoding="utf-8")
    (spec / "changelog.md").write_text(f"## Follow-up 001 — {today} 10:00:00\nAuto-updated:\n- （待补）\n", encoding="utf-8")
    art = "ai_videos/demo/renders/20261026-130000_aa/a.mp4"
    (spec / "defects.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in [
        {"category": "video.scale", "caught_by": "user", "artifact": art, "followup": "245"},
        {"category": "new:wings", "caught_by": "user", "followup": "196"},
        {"category": "video.scale", "caught_by": "review"},
    ]) + "\n", encoding="utf-8")


def client(root: Path) -> TestClient:
    return TestClient(make_app(RepoRoot(root), BoundOrigin("127.0.0.1", 8766)))


def test_repo_view_lists_only_repo_checks_and_per_drama_health(tmp_path: Path) -> None:
    build(tmp_path)
    body = client(tmp_path).get("/api/process-qc").json()
    assert [c["id"] for c in body["checks"]] == ["video.no_text"] and body["checks"][0]["level"] == "仓库级"
    rows = {d["drama"]: d for d in body["dramas"]}
    assert rows["ai_videos/demo"]["enabled"] and rows["ai_videos/demo"]["drama_checks"] == 1
    assert not rows["ai_videos/other"]["enabled"] and rows["ai_videos/other"]["renders_total"] == 0
    assert rows["ai_videos/demo"]["escape_rate"] == 2 / 3
    fu = rows["ai_videos/demo"]["followup"]
    assert (fu["followups"], fu["logged"], fu["duplicates"], fu["pending"]) == (3, 1, [2], 1)


def test_drama_view_keeps_levels_apart_and_explains_escapes(tmp_path: Path) -> None:
    build(tmp_path)
    body = client(tmp_path).get("/api/process-qc/drama", params={"drama": "ai_videos/demo"}).json()
    assert [c["id"] for c in body["drama_checks"]] == ["video.scale"] and body["drama_checks"][0]["level"] == "剧级"
    assert [c["id"] for c in body["repo_checks"]] == ["video.no_text"]
    reasons = {e["followup"]: e["reason"] for e in body["escapes"]}
    assert reasons == {"245": "检查放过了", "196": "没有这条检查"}
    assert body["renders"][0]["verdicts"] == {"video.scale": "pass", "video.no_text": "未审"}


def test_non_drama_paths_and_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    build(tmp_path)
    c = client(tmp_path)
    assert c.get("/api/process-qc/drama", params={"drama": "ai_videos/demo/renders"}).status_code == 404
    assert c.get("/api/process-qc/drama", params={"drama": "../etc"}).status_code == 404
    (tmp_path / "ai_videos" / "demo" / "qc_checks.toml").write_text(REPO_REG, encoding="utf-8")
    assert c.get("/api/process-qc/drama", params={"drama": "ai_videos/demo"}).status_code == 409


def test_overrides_are_false_positives_not_defects(tmp_path: Path) -> None:
    build(tmp_path)
    with (tmp_path / "specs" / "ai_video" / "demo" / "defects.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"category": "video.scale", "caught_by": "override", "kind": "false_positive"}) + "\n")
    row = next(d for d in client(tmp_path).get("/api/process-qc").json()["dramas"] if d["drama"] == "ai_videos/demo")
    assert (row["defects"], row["false_positives"], row["escape_rate"]) == (3, 1, 2 / 3)
