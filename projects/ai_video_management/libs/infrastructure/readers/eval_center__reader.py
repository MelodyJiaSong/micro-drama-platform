"""Reads ai_video_eval's file surfaces (rubric / config / runs) for the portal.

The eval system stays runtime-independent: this reader only consumes its files
at projects/ai_video_eval/ — no code import crosses the project boundary.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

_RUN_ID = re.compile(r"^\d{8}-\d{6}-[A-Za-z0-9_\-]+$")
_UNIT_ID = re.compile(r"^[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+/[A-Za-z0-9_\-]+$")
_DIM_FILE = re.compile(r"^dimensions/[a-z0-9_]+\.yaml$")
_DIM_ID = re.compile(r"^[a-z0-9_]+$")
_JSON_FENCE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.DOTALL)


class EvalCenterError(Exception):
    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind


class EvalCenterReader:
    def __init__(self, repo_root: Path) -> None:
        self.eval_root = repo_root / "projects" / "ai_video_eval"

    # ---- rubric ----

    def rubric_file_names(self) -> list[str]:
        names = ["rubric.yaml"]
        dim_dir = self.eval_root / "rubric" / "dimensions"
        if dim_dir.is_dir():
            names.extend(f"dimensions/{p.name}" for p in sorted(dim_dir.glob("*.yaml")))
        return names

    def rubric_path(self, name: str) -> Path:
        if name != "rubric.yaml" and not _DIM_FILE.match(name):
            raise EvalCenterError("bad_name", f"不合法的 rubric 文件名: {name}")
        path = self.eval_root / "rubric" / Path(name)
        if not path.is_file():
            raise EvalCenterError("not_found", f"rubric 文件不存在: {name}")
        return path

    def rubric_file(self, name: str) -> dict[str, object]:
        path = self.rubric_path(name)
        return {"name": name, "content": path.read_text(encoding="utf-8")}

    def overview(self) -> dict[str, object]:
        top_path = self.eval_root / "rubric" / "rubric.yaml"
        if not top_path.is_file():
            raise EvalCenterError("not_found", "rubric.yaml 不存在（eval 项目未初始化？）")
        top = yaml.safe_load(top_path.read_text(encoding="utf-8"))
        weights = top.get("dimension_weights", {})
        dimensions = []
        for dim_id in top.get("dimensions", []):
            dim_path = self.eval_root / "rubric" / "dimensions" / f"{dim_id}.yaml"
            if not dim_path.is_file():
                continue
            data = yaml.safe_load(dim_path.read_text(encoding="utf-8"))
            data["weight"] = weights.get(dim_id, 1.0)
            data["file"] = f"dimensions/{dim_id}.yaml"
            dimensions.append(data)
        return {
            "version": top.get("version"),
            "verdict": top.get("verdict", {}),
            "dimension_weights": weights,
            "dimensions": dimensions,
            "files": self.rubric_file_names(),
        }

    # ---- config ----

    def config(self) -> dict[str, object]:
        path = self.eval_root / "config" / "eval_config.yaml"
        if not path.is_file():
            raise EvalCenterError("not_found", "eval_config.yaml 不存在")
        return {"content": path.read_text(encoding="utf-8")}

    # ---- runs ----

    def runs(self) -> dict[str, object]:
        runs_dir = self.eval_root / "runs"
        manifests: list[dict] = []
        if runs_dir.is_dir():
            for entry in sorted(runs_dir.iterdir(), reverse=True):
                manifest_path = entry / "manifest.json"
                if entry.name == "latest" or not manifest_path.is_file():
                    continue
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                verdicts_path = entry / "verdicts.json"
                if verdicts_path.is_file():
                    verdicts = json.loads(verdicts_path.read_text(encoding="utf-8"))
                    project_verdict = verdicts.get("project_verdict", {})
                    manifest["tier"] = project_verdict.get("tier")
                    manifest["composite"] = project_verdict.get("composite")
                findings_path = entry / "findings.json"
                if findings_path.is_file():
                    findings = json.loads(findings_path.read_text(encoding="utf-8"))
                    manifest["findings_total"] = len(findings)
                    manifest["findings_blocker"] = sum(
                        1 for f in findings if f.get("severity") == "blocker"
                    )
                manifests.append(manifest)
        latest: dict[str, str] = {}
        latest_dir = runs_dir / "latest"
        if latest_dir.is_dir():
            for pointer in latest_dir.glob("*.json"):
                data = json.loads(pointer.read_text(encoding="utf-8"))
                latest[pointer.stem] = data.get("run_id", "")
        return {"runs": manifests, "latest": latest}

    def _run_dir(self, run_id: str) -> Path:
        if not _RUN_ID.match(run_id):
            raise EvalCenterError("bad_name", f"不合法的 run_id: {run_id}")
        run_dir = self.eval_root / "runs" / run_id
        if not run_dir.is_dir():
            raise EvalCenterError("not_found", f"run 不存在: {run_id}")
        return run_dir

    def run_detail(self, run_id: str) -> dict[str, object]:
        run_dir = self._run_dir(run_id)
        detail: dict[str, object] = {
            "manifest": json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
        }
        for key, name in (("verdicts", "verdicts.json"), ("findings", "findings.json")):
            path = run_dir / name
            detail[key] = (
                json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
            )
        return detail

    def report(self, run_id: str) -> dict[str, object]:
        path = self._run_dir(run_id) / "report.md"
        if not path.is_file():
            raise EvalCenterError("not_found", f"report 不存在: {run_id}")
        return {"content": path.read_text(encoding="utf-8")}

    def unit_results(self, run_id: str, unit_id: str) -> dict[str, object]:
        if not _UNIT_ID.match(unit_id):
            raise EvalCenterError("bad_name", f"不合法的 unit_id: {unit_id}")
        path = self._run_dir(run_id) / "results" / f"{unit_id.replace('/', '__')}.json"
        if not path.is_file():
            raise EvalCenterError("not_found", f"unit 结果不存在: {unit_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def raw_judgments(self, run_id: str, unit_id: str, dim_id: str) -> dict[str, object]:
        if not _UNIT_ID.match(unit_id):
            raise EvalCenterError("bad_name", f"不合法的 unit_id: {unit_id}")
        if not _DIM_ID.match(dim_id):
            raise EvalCenterError("bad_name", f"不合法的 dim_id: {dim_id}")
        path = (
            self._run_dir(run_id) / "raw" / unit_id.replace("/", "__") / f"{dim_id}.json"
        )
        if not path.is_file():
            raise EvalCenterError("not_found", f"原始评审记录不存在: {unit_id}/{dim_id}")
        raw = json.loads(path.read_text(encoding="utf-8"))
        samples = []
        for record in raw.get("records", []):
            text = str(record.get("text", ""))
            judgments = self._parse_judgments(text)
            samples.append(
                {
                    "sample": record.get("sample"),
                    "error": record.get("error"),
                    "judgments": judgments,
                    "text_preview": None if judgments is not None else text[:1200],
                }
            )
        return {
            "unit_id": unit_id,
            "dim_id": dim_id,
            "model": raw.get("model"),
            "samples_requested": raw.get("samples"),
            "samples": samples,
        }

    @staticmethod
    def _parse_judgments(text: str) -> list[dict] | None:
        candidates = [text.strip()]
        fence = _JSON_FENCE.search(text)
        if fence:
            candidates.append(fence.group(1).strip())
        start, end = text.find("{"), text.rfind("}")
        if 0 <= start < end:
            candidates.append(text[start : end + 1])
        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict) and isinstance(parsed.get("judgments"), list):
                return parsed["judgments"]
        return None
