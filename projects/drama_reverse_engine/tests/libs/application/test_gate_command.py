from __future__ import annotations

from pathlib import Path

import pytest

from libs.application.commands.gate__command import GateCommand
from libs.domain.errors.episode__error import InvalidStageTransitionError
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter


def _gate(tmp_path: Path) -> tuple[GateCommand, ArtifactWriter, Path]:
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    PipelineStateWriter(ws).init_state("d1/ep01")
    cmd = GateCommand(reader=PipelineStateReader(ws), states=PipelineStateWriter(ws),
                      writer=writer, artifacts=ArtifactReader(ws), workspace=ws)
    return cmd, writer, tmp_path


def test_edit_within_episode_versions_previous(tmp_path: Path) -> None:
    cmd, writer, root = _gate(tmp_path)
    writer.write_text("d1/ep01/script.md", "old")
    result = cmd.edit_artifact("d1/ep01", "d1/ep01/script.md", "new")
    assert (root / "d1/ep01/script.md").read_text(encoding="utf-8") == "new"
    assert result["needs_recompose"] is True  # script.md is a recompose trigger
    versions = list((root / "d1/ep01/.versions").glob("*-script.md"))
    assert len(versions) == 1 and versions[0].read_text(encoding="utf-8") == "old"


def test_traversal_out_of_episode_rejected(tmp_path: Path) -> None:
    cmd, writer, root = _gate(tmp_path)
    writer.write_json("d2/authorization_stub.json", {"sha256": "legit"})
    with pytest.raises(InvalidStageTransitionError):
        cmd.edit_artifact("d1/ep01", "d1/ep01/../../d2/authorization_stub.json", "TAMPERED")
    assert "TAMPERED" not in (root / "d2/authorization_stub.json").read_text(encoding="utf-8")


def test_editing_the_episode_dir_itself_rejected(tmp_path: Path) -> None:
    cmd, _, _ = _gate(tmp_path)
    with pytest.raises(InvalidStageTransitionError):
        cmd.edit_artifact("d1/ep01", "d1/ep01", "x")


def test_non_trigger_edit_does_not_mark_recompose(tmp_path: Path) -> None:
    cmd, writer, _ = _gate(tmp_path)
    writer.write_text("d1/ep01/qc_report.md", "old")
    result = cmd.edit_artifact("d1/ep01", "d1/ep01/qc_report.md", "annotated")
    assert result["needs_recompose"] is False
