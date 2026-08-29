"""Eval-center module: reader/writer over a fake ai_video_eval tree."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from libs.infrastructure.readers.eval_center__reader import EvalCenterError, EvalCenterReader
from libs.infrastructure.writers.eval_center__writer import EvalCenterWriter

RUN_ID = "20260728-210000-demo"


@pytest.fixture()
def repo_root(tmp_path: Path) -> Path:
    eval_root = tmp_path / "projects" / "ai_video_eval"
    (eval_root / "rubric" / "dimensions").mkdir(parents=True)
    (eval_root / "config").mkdir()
    (eval_root / "rubric" / "rubric.yaml").write_text(
        "version: 1.0.0\ndimensions: [demo]\ndimension_weights: {demo: 1.0}\n"
        "verdict: {pass_min: 75}\n",
        encoding="utf-8",
    )
    (eval_root / "rubric" / "dimensions" / "demo.yaml").write_text(
        "dimension_id: demo\nname_cn: 演示\ndescription_cn: d\n"
        "subcategories:\n- id: s1\n  name_cn: 子\n  weight: 1.0\n  fields:\n"
        "  - id: f1\n    name_cn: 字段\n    evaluator: llm\n    weight: 3\n"
        "    anchors: {g1: a, g3: b, g5: c}\n",
        encoding="utf-8",
    )
    (eval_root / "config" / "eval_config.yaml").write_text(
        "paths: {videos_root: ../../ai_videos}\njudge: {engine: api}\n", encoding="utf-8"
    )
    run_dir = eval_root / "runs" / RUN_ID
    (run_dir / "results").mkdir(parents=True)
    (eval_root / "runs" / "latest").mkdir()
    (run_dir / "manifest.json").write_text(
        json.dumps({"run_id": RUN_ID, "project": "demo_drama", "status": "completed", "ts": "t"}),
        encoding="utf-8",
    )
    (run_dir / "verdicts.json").write_text(
        json.dumps(
            {
                "project_verdict": {"tier": "pass", "composite": 90.0},
                "episode_verdicts": {},
                "units": [],
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "findings.json").write_text(
        json.dumps([{"severity": "blocker", "finding_id": "x"}]), encoding="utf-8"
    )
    (run_dir / "results" / "demo_drama__ep01__shot01.json").write_text(
        json.dumps({"unit_id": "demo_drama/ep01/shot01", "fields": []}), encoding="utf-8"
    )
    raw_dir = run_dir / "raw" / "demo_drama__ep01__shot01"
    raw_dir.mkdir(parents=True)
    fenced = '前言\n```json\n{"judgments": [{"field_id": "f1", "grade": 4, "confidence": 0.9, "justification": "j", "evidence": [], "revision_hint": ""}]}\n```'
    (raw_dir / "demo.json").write_text(
        json.dumps(
            {
                "model": "claude-opus-5",
                "samples": 2,
                "records": [
                    {"sample": 0, "text": fenced},
                    {"sample": 1, "text": "totally not json", "error": "boom"},
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (run_dir / "report.md").write_text("# 报告", encoding="utf-8")
    (eval_root / "runs" / "latest" / "demo_drama.json").write_text(
        json.dumps({"run_id": RUN_ID}), encoding="utf-8"
    )
    return tmp_path


def test_reader_overview_and_files(repo_root: Path) -> None:
    reader = EvalCenterReader(repo_root)
    overview = reader.overview()
    assert overview["version"] == "1.0.0"
    dims = overview["dimensions"]
    assert len(dims) == 1 and dims[0]["weight"] == 1.0
    assert reader.rubric_file_names() == ["rubric.yaml", "dimensions/demo.yaml"]
    assert "dimension_id" in reader.rubric_file("dimensions/demo.yaml")["content"]


def test_reader_runs_and_detail(repo_root: Path) -> None:
    reader = EvalCenterReader(repo_root)
    runs = reader.runs()
    assert runs["latest"] == {"demo_drama": RUN_ID}
    entry = runs["runs"][0]
    assert entry["tier"] == "pass"
    assert entry["findings_blocker"] == 1
    detail = reader.run_detail(RUN_ID)
    assert detail["verdicts"]["project_verdict"]["composite"] == 90.0
    assert reader.report(RUN_ID)["content"].startswith("# 报告")
    unit = reader.unit_results(RUN_ID, "demo_drama/ep01/shot01")
    assert unit["unit_id"] == "demo_drama/ep01/shot01"


def test_reader_raw_judgments(repo_root: Path) -> None:
    reader = EvalCenterReader(repo_root)
    raw = reader.raw_judgments(RUN_ID, "demo_drama/ep01/shot01", "demo")
    assert raw["model"] == "claude-opus-5"
    samples = raw["samples"]
    assert samples[0]["judgments"][0]["field_id"] == "f1"
    assert samples[0]["text_preview"] is None
    assert samples[1]["judgments"] is None
    assert samples[1]["text_preview"] == "totally not json"
    with pytest.raises(EvalCenterError):
        reader.raw_judgments(RUN_ID, "demo_drama/ep01/shot01", "../evil")
    with pytest.raises(EvalCenterError):
        reader.raw_judgments(RUN_ID, "demo_drama/ep01/shot01", "nope")


def test_reader_rejects_traversal(repo_root: Path) -> None:
    reader = EvalCenterReader(repo_root)
    with pytest.raises(EvalCenterError):
        reader.rubric_path("../config/eval_config.yaml")
    with pytest.raises(EvalCenterError):
        reader.run_detail("../../secrets")
    with pytest.raises(EvalCenterError):
        reader.unit_results(RUN_ID, "../etc/passwd")


def test_writer_config_and_rubric(repo_root: Path) -> None:
    reader = EvalCenterReader(repo_root)
    writer = EvalCenterWriter(repo_root, reader, validate_after_write=False)

    result = writer.save_config("paths: {a: 1}\njudge: {engine: api}\n")
    assert result["validated"] is True
    with pytest.raises(EvalCenterError):
        writer.save_config("not: [valid")
    with pytest.raises(EvalCenterError):
        writer.save_config("only_paths: 1\n")

    saved = writer.save_rubric_file("dimensions/demo.yaml", "dimension_id: demo\n")
    assert saved["validated"] is False
    assert "dimension_id" in reader.rubric_file("dimensions/demo.yaml")["content"]
    with pytest.raises(EvalCenterError):
        writer.save_rubric_file("dimensions/demo.yaml", "bad: [yaml")
    with pytest.raises(EvalCenterError):
        writer.save_rubric_file("../pyproject.toml", "x: 1")
