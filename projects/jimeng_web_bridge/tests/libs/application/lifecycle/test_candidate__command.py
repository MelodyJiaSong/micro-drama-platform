from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.application.commands.candidate__command import CandidateCommand
from libs.common.clock import FrozenClock
from libs.common.paths import RepoSandbox
from libs.domain.value_objects.drama_config__valueobject import DramaConfig
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.errors.output__error import InvalidCandidateError, OutputPathRejectedError, PromoteTargetExistsError
from libs.infrastructure.writers.output__writer import OutputWriter
from tests.libs.application.lifecycle.fakes import CARD_REL, StubProber
from tests.libs.domain.builders import T0, global_data

CANDIDATE = f"{CARD_REL}/_candidates/c1-1/20260913-181500_2.png"


def setup(tmp_path: Path, on_existing: str = "archive") -> tuple[Path, CandidateCommand]:
    root = tmp_path / "repo"
    card = root / CARD_REL
    (card / "_candidates" / "c1-1").mkdir(parents=True)
    (card / "c1-1.png").write_bytes(b"old image")
    (card / "c1-1.png.jimeng.json").write_text('{"job_id": "job-old"}', encoding="utf-8")
    (root / CANDIDATE).write_bytes(b"new image")
    (root / (CANDIDATE + ".jimeng.json")).write_text(
        json.dumps({"job_id": "job-9", "cookie": "secret", "output": {"width": 1536, "height": 2048}}), encoding="utf-8"
    )
    cfg = GlobalConfig.from_dict(global_data())
    data = DramaConfig.defaults("hy3")
    outputs = data["outputs"]
    assert isinstance(outputs, dict)
    outputs["on_existing"] = on_existing
    drama = DramaConfig.from_dict(data, cfg.model_limits)
    writer = OutputWriter(RepoSandbox(root, (root / ".data",)), StubProber())  # type: ignore[arg-type]
    return root, CandidateCommand(writer, lambda rel: drama, lambda: cfg, FrozenClock(T0))


def test_promote_archives_the_old_file_and_sidecar_then_copies(tmp_path: Path) -> None:
    root, command = setup(tmp_path)
    result = command.promote(CANDIDATE)
    archive = "ai_videos/_deleted/huangye_shenghuo/hy3/2_世界观人设/characters/c1_砌炉的老人/c1-1.20260913-180000.png"
    assert result.target_rel == f"{CARD_REL}/c1-1.png"
    assert [(a.from_rel, a.to_rel) for a in result.archived] == [
        (f"{CARD_REL}/c1-1.png", archive), (f"{CARD_REL}/c1-1.png.jimeng.json", archive + ".jimeng.json"),
    ]
    assert (root / archive).read_bytes() == b"old image" and (root / result.target_rel).read_bytes() == b"new image"
    sidecar = json.loads((root / result.sidecar_rel).read_text(encoding="utf-8"))
    assert sidecar["promoted_from"] == CANDIDATE and "cookie" not in sidecar and sidecar["output"]["size"] == 9
    assert (root / CANDIDATE).is_file()


def test_on_existing_fail_moves_nothing(tmp_path: Path) -> None:
    root, command = setup(tmp_path, on_existing="fail")
    with pytest.raises(PromoteTargetExistsError) as caught:
        command.promote(CANDIDATE)
    assert caught.value.config_key == "outputs.on_existing"
    assert (root / CARD_REL / "c1-1.png").read_bytes() == b"old image" and not (root / "ai_videos" / "_deleted").exists()


@pytest.mark.parametrize(("rel", "error"), [
    (f"{CARD_REL}/c1-1.png", InvalidCandidateError),
    (CANDIDATE + ".jimeng.json", InvalidCandidateError),
    ("ai_videos/../outside.png", OutputPathRejectedError),
    ("C:/Windows/win.ini", OutputPathRejectedError),
])
def test_only_sandboxed_candidate_files_can_be_promoted(tmp_path: Path, rel: str, error: type[Exception]) -> None:
    _, command = setup(tmp_path)
    with pytest.raises(error):
        command.promote(rel)
