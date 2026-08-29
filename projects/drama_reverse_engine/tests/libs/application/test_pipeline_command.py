from __future__ import annotations

from pathlib import Path

from libs.application.commands.pipeline__command import PipelineCommand
from libs.application.dtos.assets__dto import ReferenceLibraryCdto
from libs.application.dtos.compose__dto import ComposeResultCdto
from libs.application.dtos.extract__dto import ExtractResultCdto
from libs.application.dtos.understand__dto import UnderstandResultCdto
from libs.common.enums import PipelineStage
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.readers.artifact__reader import ArtifactReader
from libs.infrastructure.readers.pipelinestate__reader import PipelineStateReader
from libs.infrastructure.writers.artifact__writer import ArtifactWriter
from libs.infrastructure.writers.pipelinestate__writer import PipelineStateWriter

_EP = "d1/ep01"


def _stub_commands(calls: list[str]):
    class Extract:
        def run(self, ep, force=False):
            calls.append(f"extract:{force}")
            return ExtractResultCdto(ep, 3, 2, 0, [])

    class Assets:
        def build_reference_library(self, d, eps, force=False):
            calls.append("assets")
            return ReferenceLibraryCdto(1, 9, [])

    class Understand:
        def run(self, d, ep, force=False):
            calls.append("understand")
            return UnderstandResultCdto(ep, 3, 0, 0)

    class Compose:
        def run(self, d, ep, force=False):
            calls.append(f"compose:{force}")
            return ComposeResultCdto(ep, ["s1"], f"{ep}/script.md", f"{ep}/novel.md", [])

    return Extract(), Assets(), Understand(), Compose()


def _setup(tmp_path: Path, gate_a: bool = False):
    ws = SafeWorkspace(root=str(tmp_path))
    writer = ArtifactWriter(ws)
    writer.write_json("d1/drama.json", {"drama_id": "d1", "title": "t",
                                        "gate_a_enabled": gate_a, "gate_b_enabled": False})
    states = PipelineStateWriter(ws)
    states.init_state(_EP)
    calls: list[str] = []
    ex, as_, un, co = _stub_commands(calls)
    cmd = PipelineCommand(extract=ex, assets=as_, understand=un, compose=co,  # type: ignore[arg-type]
                          reader=ArtifactReader(ws), writer=writer,
                          state_reader=PipelineStateReader(ws), state_writer=states)
    return cmd, calls, tmp_path


def test_full_walk_reaches_done_with_gates_disabled(tmp_path: Path) -> None:
    cmd, calls, root = _setup(tmp_path)
    state = cmd.run_to_completion("d1", _EP)
    assert state["stage"] == PipelineStage.DONE.value
    assert calls == ["extract:False", "assets", "understand", "compose:False"]
    events = (root / "d1/job_events.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(events) >= 7  # one per stage step through DONE (FR-10.3)


def test_gate_a_holds_until_release(tmp_path: Path) -> None:
    cmd, _, root = _setup(tmp_path, gate_a=True)
    state = cmd.run_to_completion("d1", _EP)
    assert state["stage"] == PipelineStage.GATE_A.value and state["gate_hold"] is True
    from libs.application.commands.gate__command import GateCommand

    ws = SafeWorkspace(root=str(root))
    gate = GateCommand(reader=PipelineStateReader(ws), states=PipelineStateWriter(ws),
                       writer=ArtifactWriter(ws), artifacts=ArtifactReader(ws), workspace=ws)
    released = gate.release(_EP)
    assert released["stage"] == PipelineStage.GATE_B.value and not released["gate_hold"]
    final = cmd.run_to_completion("d1", _EP)
    assert final["stage"] == PipelineStage.DONE.value


def test_rerun_stage_forces_recompute(tmp_path: Path) -> None:
    cmd, calls, _ = _setup(tmp_path)
    cmd.run_to_completion("d1", _EP)
    calls.clear()
    state = cmd.rerun_stage("d1", _EP, "compose")
    assert "compose:True" in calls
    assert state["stage"] == PipelineStage.GATE_A.value


def test_stage_failure_marks_failed_and_stops(tmp_path: Path) -> None:
    cmd, _, _ = _setup(tmp_path)

    def boom(d, ep, force=False):
        raise RuntimeError("understand backend down")

    cmd._understand.run = boom  # type: ignore[attr-defined]
    state = cmd.run_to_completion("d1", _EP)
    assert state["stage"] == PipelineStage.UNDERSTAND.value
    assert "understand backend down" in (state["failed_reason"] or "")
