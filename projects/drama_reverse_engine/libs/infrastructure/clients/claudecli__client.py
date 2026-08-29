from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from libs.infrastructure.errors.claudecli__error import ClaudeCliError


def extract_json_object(text: str) -> dict[str, Any]:
    """Pull the first {...last} JSON object out of a model reply that may wrap it in
    prose or a ```json fence."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise ClaudeCliError(f"claude reply contains no JSON object: {text[-300:]!r}")
    try:
        return json.loads(text[start : end + 1])
    except ValueError as exc:
        raise ClaudeCliError(f"claude reply JSON does not parse: {text[-300:]!r}") from exc


class ClaudeCliClient:
    """Zero-key LLM backend on the locally-authenticated Claude Code CLI: every call
    spawns a fresh headless session (`claude -p`, prompt over stdin, JSON envelope
    out). Follow-up 002 makes this the default engine; keyed HTTP backends stay as
    env-selected alternatives (NFR-O1)."""

    def __init__(self, binary: str = "claude", model: str = "", timeout_s: float = 1800.0) -> None:
        self._binary = binary or "claude"
        self._model = model
        self._timeout_s = timeout_s

    @property
    def available(self) -> bool:
        return shutil.which(self._binary) is not None

    def run_text(self, prompt: str, read_dirs: tuple[str, ...] = (), max_turns: int = 8) -> str:
        exe = shutil.which(self._binary)
        if exe is None:
            raise ClaudeCliError(f"claude CLI not found on PATH (binary={self._binary!r})")
        args = [exe, "-p", "--output-format", "json", "--max-turns", str(max_turns)]
        if self._model:
            args += ["--model", self._model]
        if read_dirs:
            args += ["--allowedTools", "Read"]
            for directory in read_dirs:
                args += ["--add-dir", directory]
        if exe.lower().endswith((".cmd", ".bat")):
            # CreateProcess cannot exec batch shims (npm installs) directly
            args = ["cmd", "/c", *args]
        try:
            proc = subprocess.run(
                args, input=prompt, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=self._timeout_s,
                cwd=_neutral_cwd(),
            )
        except subprocess.TimeoutExpired as exc:
            raise ClaudeCliError(f"claude -p timed out after {self._timeout_s:.0f}s") from exc
        if proc.returncode != 0:
            raise ClaudeCliError(f"claude -p exited {proc.returncode}: {(proc.stderr or proc.stdout)[-400:]}")
        try:
            envelope = json.loads(proc.stdout.strip())
        except ValueError as exc:
            raise ClaudeCliError(f"claude -p returned a non-JSON envelope: {proc.stdout[-400:]!r}") from exc
        if envelope.get("is_error"):
            raise ClaudeCliError(f"claude -p reported an error: {str(envelope.get('result'))[-400:]}")
        return str(envelope.get("result", ""))


def _neutral_cwd() -> str:
    # run outside any git repo so the session does not inherit an unrelated
    # project's CLAUDE.md (the workspace lives inside the spec_coding monorepo);
    # frame access is granted explicitly via --add-dir
    path = Path(tempfile.gettempdir()) / "dre_claude_cli"
    path.mkdir(parents=True, exist_ok=True)
    return str(path)
