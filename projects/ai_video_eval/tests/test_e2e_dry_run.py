import asyncio
import json
import os

import pytest

from apps.cli.container import PROJECT_ROOT
from libs.application.commands.eval_run__command import EvalRunCommand
from libs.application.dtos.eval__dto import SelectorCdto
from libs.application.mappers.grounding__mapper import GroundingMapper
from libs.application.mappers.judge__mapper import JudgeMapper
from libs.application.mappers.rubric__mapper import RubricMapper
from libs.application.mappers.shot__mapper import ShotMapper
from libs.application.mappers.verdict__mapper import VerdictMapper
from libs.infrastructure.daos.config__dao import (
    EvalConfigDao,
    GroundingConfigDao,
    JudgeModelConfigDao,
)
from libs.infrastructure.readers.canon__reader import CanonReader
from libs.infrastructure.readers.layout__reader import LayoutReader
from libs.infrastructure.readers.rubric__reader import RubricReader
from libs.infrastructure.readers.run__reader import RunReader
from libs.infrastructure.readers.script__reader import ScriptReader
from libs.infrastructure.readers.shot__reader import ShotReader
from libs.infrastructure.writers.report__writer import ReportWriter
from libs.infrastructure.writers.run__writer import RunWriter

from tests.conftest import FIXTURES


@pytest.fixture()
def command(tmp_path):
    judge = JudgeModelConfigDao(model="claude-opus-5", effort="high", samples=3, max_tokens=16000)
    grounding_config = GroundingConfigDao(6000, 4000, 20000, 20000, 5000, 3000)
    config = EvalConfigDao(
        project_root=str(tmp_path),
        videos_root=FIXTURES,
        runs_dir=str(tmp_path / "runs"),
        disputes_dir=str(tmp_path / "disputes"),
        golden_dir=str(tmp_path / "golden"),
        api_key_envs=("NOPE_KEY",),
        judge_engine="api",
        judge_default=judge,
        judge_per_dimension={},
        grounding=grounding_config,
    )
    top, dims, content_hash = RubricReader(os.path.join(PROJECT_ROOT, "rubric")).read()
    rubric = RubricMapper().map(top, dims, content_hash)
    return EvalRunCommand(
        config=config,
        rubric=rubric,
        layout_reader=LayoutReader(FIXTURES),
        shot_reader=ShotReader(),
        canon_reader=CanonReader(),
        script_reader=ScriptReader(),
        run_reader=RunReader(config.runs_dir),
        run_writer=RunWriter(config.runs_dir),
        report_writer=ReportWriter(),
        client=None,
        shot_mapper=ShotMapper(),
        grounding_mapper=GroundingMapper(grounding_config),
        judge_mapper=JudgeMapper(),
        verdict_mapper=VerdictMapper(),
    )


def test_dry_run_end_to_end(command):
    selector = SelectorCdto(project="mini_drama", dry_run=True)
    estimate = command.estimate(selector)
    assert estimate.unit_count == 2
    assert estimate.llm_call_count > 0

    result = asyncio.run(command.run(selector))
    assert result.unit_count == 2
    assert os.path.isfile(result.report_path)

    with open(os.path.join(result.run_dir, "verdicts.json"), encoding="utf-8") as fh:
        verdicts = json.load(fh)
    units = {u["unit_id"]: u for u in verdicts["units"]}
    assert set(units) == {"mini_drama/ep01/shot01", "mini_drama/ep01/shot02"}

    with open(os.path.join(result.run_dir, "findings.json"), encoding="utf-8") as fh:
        findings = json.load(fh)
    by_unit_field = {(f["unit_id"], f["field_id"]) for f in findings}
    assert ("mini_drama/ep01/shot02", "locked_descriptor_byte_identical") in by_unit_field
    assert ("mini_drama/ep01/shot01", "locked_descriptor_byte_identical") not in by_unit_field
    assert ("mini_drama/ep01/shot02", "cps_hard_cap") in by_unit_field
    assert ("mini_drama/ep01/shot01", "cps_hard_cap") not in by_unit_field

    manifest_path = os.path.join(result.run_dir, "manifest.json")
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    assert manifest["status"] == "completed"
    assert manifest["rubric_version"]
    assert len(manifest["unit_hashes"]) == 2
