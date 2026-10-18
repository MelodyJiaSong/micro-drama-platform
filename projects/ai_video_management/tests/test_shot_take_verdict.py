"""The user's verdict on a draft take (follow-up 265): 通过 lets `tools/shot_take.py --stage final` use it for the 720p take."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from libs.application.commands.shot_take__command import ShotTakeCommand
from libs.common.origin import BoundOrigin
from libs.common.repo_root import RepoRoot
from libs.domain.errors.shot_take__error import ShotTakeError
from libs.infrastructure.readers.shot_renders__reader import ShotRendersReader
from libs.infrastructure.writers.shot_take__writer import ShotTakeWriter

SHOT = "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1"
REVIEW = "# 审核：ep1_s1_st1 · {take}\n\n状态：待审核\n\nVision：\n\n## 对的\n\n- 走位对\n"


def take(repo: Path, name: str, stage: str | None = "draft", review: bool = True) -> str:
    folder = repo / SHOT / ("drafts" if stage == "draft" else "renders") / name
    folder.mkdir(parents=True)
    record = {"key": "ep1_s1_st1", "take": name, "resolution": "480p" if stage == "draft" else "720p"}
    if stage:
        record["stage"] = stage
    (folder / "generation.json").write_text(json.dumps(record), encoding="utf-8")
    (folder / f"ep1_s1_st1_{name}.mp4").write_bytes(b"v")
    if review:
        (folder / "review.md").write_text(REVIEW.format(take=name), encoding="utf-8")
    return f"{SHOT}/{'drafts' if stage == 'draft' else 'renders'}/{name}"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "ai_videos").mkdir()
    return tmp_path


def command(repo: Path) -> ShotTakeCommand:
    return ShotTakeCommand(ShotTakeWriter(repo), clock=lambda: "2026-10-16 21:00")


def test_passing_a_draft_rewrites_only_the_status_line(repo: Path) -> None:
    path = take(repo, "20261016-200000_aaaa1111")
    status = command(repo).verdict(path, "通过")
    review = (repo / path / "review.md").read_text(encoding="utf-8")
    assert status == "通过（用户 2026-10-16 21:00，可出正式条）"
    assert review == REVIEW.format(take="20261016-200000_aaaa1111").replace("状态：待审核", "状态：" + status)
    assert command(repo).verdict(path, "不通过") == "不通过（用户 2026-10-16 21:00）"


def test_a_draft_without_a_review_gets_one(repo: Path) -> None:
    path = take(repo, "20261016-200000_bbbb2222", review=False)
    command(repo).verdict(path, "通过")
    review = (repo / path / "review.md").read_text(encoding="utf-8")
    assert "状态：通过（用户 2026-10-16 21:00，可出正式条）" in review and "Vision：" in review


@pytest.mark.parametrize("bad", [
    "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/renders/../../st1",
    "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1",
    "ai_videos/demo/episodes/ep01/scenes/s1/shots/st1/renders/missing",
    "projects/x/renders/20261016-200000_aaaa1111",
])
def test_only_an_existing_take_folder_can_be_judged(repo: Path, bad: str) -> None:
    take(repo, "20261016-200000_aaaa1111")
    with pytest.raises(ShotTakeError):
        command(repo).verdict(bad, "通过")


def test_a_final_is_judged_for_the_cut(repo: Path) -> None:
    final = take(repo, "20261016-210000_cccc3333", stage="final")
    assert command(repo).verdict(final, "通过") == "通过（用户 2026-10-16 21:00，正片可用）"
    assert command(repo).verdict(final, "不通过") == "不通过（用户 2026-10-16 21:00）"


def test_unknown_verdicts_are_refused(repo: Path) -> None:
    draft = take(repo, "20261016-200000_aaaa1111")
    with pytest.raises(ShotTakeError):
        command(repo).verdict(draft, "随便")


def test_the_ui_sees_stage_and_where_a_final_came_from(repo: Path) -> None:
    take(repo, "20261016-200000_aaaa1111")
    folder = repo / SHOT / "renders" / "20261016-210000_cccc3333"
    folder.mkdir(parents=True)
    (folder / "generation.json").write_text(json.dumps({"stage": "final", "resolution": "720p",
                                                        "from_take": "20261016-200000_aaaa1111"}), encoding="utf-8")
    prompts = {"scenes": [{"id": "s1", "shots": [{"id": "ep1_s1_st1"}]}]}
    takes = ShotRendersReader(repo).read("ai_videos/demo/episodes/ep01", prompts)["ep1_s1_st1"]
    assert [t["path"].split("/")[-2] for t in takes] == ["renders", "drafts"]   # 草稿与正式条合在一起，新的在前
    by_id = {t["id"]: t for t in takes}
    assert by_id["20261016-200000_aaaa1111"]["generation"]["stage"] == "draft"
    assert by_id["20261016-210000_cccc3333"]["generation"]["from_take"] == "20261016-200000_aaaa1111"


def test_api_records_the_verdict(repo: Path) -> None:
    from apps.api.app_factory import create_app
    from apps.api.container import Container
    path = take(repo, "20261016-200000_aaaa1111")
    container = Container()
    container.repo_root_path.override(RepoRoot(path=repo).path)
    container.bound_origin.override(BoundOrigin(host="127.0.0.1", port=8765))
    container.wire(packages=["apps.api.routes"])
    client = TestClient(create_app(container, serve_static=False), base_url="http://127.0.0.1:8765")
    origin = {"Origin": "http://127.0.0.1:8765"}
    done = client.post("/api/shot-take/verdict", json={"take_path": path, "verdict": "通过"}, headers=origin)
    assert done.status_code == 200, done.text
    assert done.json()["review_status"].startswith("通过（用户 ")
    bad = client.post("/api/shot-take/verdict", json={"take_path": SHOT, "verdict": "通过"}, headers=origin)
    assert bad.status_code == 400
