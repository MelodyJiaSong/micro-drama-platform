"""Writes ai_video_eval's editable surfaces (rubric / config) with backup +
validation. Rubric saves are validated by invoking the eval project's own CLI
(`rubric validate`) as a subprocess — no cross-project code import — and rolled
back if validation fails.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from libs.infrastructure.readers.eval_center__reader import EvalCenterError, EvalCenterReader


class EvalCenterWriter:
    def __init__(
        self, repo_root: Path, reader: EvalCenterReader, validate_after_write: bool = True
    ) -> None:
        self._repo_root = repo_root
        self._reader = reader
        self._validate = validate_after_write

    def save_rubric_file(self, name: str, content: str) -> dict[str, object]:
        path = self._reader.rubric_path(name)
        self._check_yaml(content)
        backup = path.read_text(encoding="utf-8")
        path.write_text(content, encoding="utf-8")
        if not self._validate:
            return {"validated": False, "output": "validation skipped"}
        code, output = self._run_validator()
        if code != 0:
            path.write_text(backup, encoding="utf-8")
            raise EvalCenterError(
                "rubric_invalid", f"rubric 校验失败，已回滚本次修改：\n{output[-1500:]}"
            )
        return {"validated": True, "output": output[-1500:]}

    def save_config(self, content: str) -> dict[str, object]:
        parsed = self._check_yaml(content)
        if not isinstance(parsed, dict) or "judge" not in parsed or "paths" not in parsed:
            raise EvalCenterError("config_invalid", "eval_config.yaml 须包含 paths 与 judge 两节")
        path = self._reader.eval_root / "config" / "eval_config.yaml"
        if not path.is_file():
            raise EvalCenterError("not_found", "eval_config.yaml 不存在")
        path.write_text(content, encoding="utf-8")
        return {"validated": True, "output": "yaml 解析通过"}

    @staticmethod
    def _check_yaml(content: str) -> object:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as exc:
            raise EvalCenterError("yaml_invalid", f"YAML 解析失败：{exc}") from exc

    def _run_validator(self) -> tuple[int, str]:
        python = self._repo_root / ".venv" / "Scripts" / "python.exe"
        executable = str(python) if python.is_file() else "python"
        try:
            completed = subprocess.run(
                [executable, "-m", "apps.cli.main", "rubric", "validate"],
                cwd=str(self._reader.eval_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return 1, f"validator 无法执行: {exc}"
        return completed.returncode, (completed.stdout or "") + (completed.stderr or "")
