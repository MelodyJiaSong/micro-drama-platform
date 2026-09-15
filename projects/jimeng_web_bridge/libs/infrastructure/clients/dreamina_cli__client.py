from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

from libs.infrastructure.daos.dreamina_result__dao import (
    DreaminaCreditDao,
    DreaminaResultDao,
    DreaminaSubmitDao,
    DreaminaTaskDao,
    DreaminaVersionDao,
)
from libs.infrastructure.errors.dreamina_cli__error import DreaminaCliError, DreaminaFailureKind

_SECRET_ENV_PREFIX: str = "JIMENG_BRIDGE_"
_TAIL_CHARS: int = 800
_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_LOGIN_MARKERS: tuple[str, ...] = ("not logged in", "login required", "please login", "dreamina login", "未登录", "请先登录")


class DreaminaCliClient:
    """Thin, blocking wrapper over the official `dreamina` executable (spec v2 FR-38..FR-41).

    Blocking on purpose: callers run it in a worker thread so the event loop never waits on
    a subprocess. Arguments always travel as an argv list in `--flag=value` form, so no shell
    ever parses a prompt.
    """

    def __init__(
        self,
        executable: Path,
        timeout_s: float,
        launcher_prefix: Sequence[str] = (),
        base_env: Mapping[str, str] | None = None,
    ) -> None:
        if not launcher_prefix and executable.suffix.lower() != ".exe":
            raise DreaminaCliError(
                DreaminaFailureKind.EXECUTABLE_REJECTED, f"cli path must be an .exe: {executable.name}", None, ""
            )
        self._argv0: list[str] = [*launcher_prefix, str(executable)]
        self._timeout_s = timeout_s
        source_env = os.environ if base_env is None else base_env
        self._env: dict[str, str] = {k: v for k, v in source_env.items() if not k.startswith(_SECRET_ENV_PREFIX)}

    def version(self) -> DreaminaVersionDao:
        data = _as_dict(self._run_json(["version"]))
        return DreaminaVersionDao(
            version=str(data.get("version", "")), commit=_opt_str(data.get("commit")), build_time=_opt_str(data.get("build_time"))
        )

    def user_credit(self) -> DreaminaCreditDao:
        data = _as_dict(self._run_json(["user_credit"]))
        return DreaminaCreditDao(total_credit=int(data.get("total_credit", 0)), vip_level=_opt_str(data.get("vip_level")))

    def text2image(self, prompt: str, model_version: str, ratio: str, resolution_type: str) -> DreaminaSubmitDao:
        args = ["text2image", f"--prompt={prompt}", f"--model_version={model_version}", f"--ratio={ratio}", f"--resolution_type={resolution_type}"]
        return _submit(_as_dict(self._run_json(args)))

    def image2image(
        self, images: Sequence[Path], prompt: str, model_version: str, ratio: str, resolution_type: str
    ) -> DreaminaSubmitDao:
        args = [
            "image2image",
            f"--images={','.join(str(path) for path in images)}",
            f"--prompt={prompt}",
            f"--model_version={model_version}",
            f"--ratio={ratio}",
            f"--resolution_type={resolution_type}",
        ]
        return _submit(_as_dict(self._run_json(args)))

    def query_result(self, submit_id: str, download_dir: Path) -> DreaminaResultDao:
        download_dir.mkdir(parents=True, exist_ok=True)
        before = {path.name for path in download_dir.iterdir()}
        data = _as_dict(self._run_json(["query_result", f"--submit_id={submit_id}", f"--download_dir={download_dir}"]))
        new_files = tuple(sorted(path for path in download_dir.iterdir() if path.is_file() and path.name not in before))
        return DreaminaResultDao(
            submit_id=str(data.get("submit_id", submit_id)),
            gen_status=_opt_str(data.get("gen_status")),
            fail_reason=_opt_str(data.get("fail_reason")) or None,
            downloaded_files=new_files,
            raw=data,
        )

    def list_task(self, limit: int, submit_id: str | None = None) -> list[DreaminaTaskDao]:
        args = ["list_task", f"--limit={limit}"] + ([f"--submit_id={submit_id}"] if submit_id else [])
        payload = self._run_json(args)
        rows = payload if isinstance(payload, list) else _as_dict(payload).get("tasks", [])
        return [_task(row) for row in rows if isinstance(row, dict)]

    def _run_json(self, args: list[str]) -> object:
        output = self._run(args)
        return _extract_json(output)

    def _run(self, args: list[str]) -> str:
        try:
            completed = subprocess.run(
                [*self._argv0, *args],
                capture_output=True,
                timeout=self._timeout_s,
                env=self._env,
                shell=False,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            tail = _tail((error.stdout or b"") + (error.stderr or b""))
            raise DreaminaCliError(DreaminaFailureKind.TIMEOUT, f"{args[0]} timed out", None, tail) from error
        output = _decode(completed.stdout) + _decode(completed.stderr)
        if completed.returncode != 0:
            raise DreaminaCliError(_classify(output), f"{args[0]} exited {completed.returncode}", completed.returncode, _tail_text(output))
        return _decode(completed.stdout)


def _classify(output: str) -> DreaminaFailureKind:
    lowered = output.lower()
    if "aigccomplianceconfirmationrequired" in lowered:
        return DreaminaFailureKind.COMPLIANCE_CONFIRMATION_REQUIRED
    if any(marker in lowered for marker in _LOGIN_MARKERS):
        return DreaminaFailureKind.NOT_LOGGED_IN
    if "record not found" in lowered:
        return DreaminaFailureKind.NOT_FOUND
    return DreaminaFailureKind.UNKNOWN


def _extract_json(output: str) -> object:
    starts = [index for index in (output.find("{"), output.find("[")) if index >= 0]
    if not starts:
        raise DreaminaCliError(DreaminaFailureKind.UNPARSEABLE_OUTPUT, "no JSON in output", 0, _tail_text(output))
    try:
        payload, _ = json.JSONDecoder().raw_decode(output[min(starts):])
    except json.JSONDecodeError as error:
        raise DreaminaCliError(DreaminaFailureKind.UNPARSEABLE_OUTPUT, str(error), 0, _tail_text(output)) from error
    return payload


def _submit(data: dict[str, object]) -> DreaminaSubmitDao:
    submit_id = data.get("submit_id")
    if not isinstance(submit_id, str) or not submit_id:
        raise DreaminaCliError(DreaminaFailureKind.UNPARSEABLE_OUTPUT, "submit output has no submit_id", 0, json.dumps(data)[:_TAIL_CHARS])
    return DreaminaSubmitDao(submit_id=submit_id, gen_status=_opt_str(data.get("gen_status")), raw=data)


def _task(row: dict[str, object]) -> DreaminaTaskDao:
    result = _as_dict(row.get("result_json"))
    commerce = _as_dict(row.get("commerce_info"))
    credit = commerce.get("credit_count")
    return DreaminaTaskDao(
        submit_id=str(row.get("submit_id", "")),
        gen_task_type=_opt_str(row.get("gen_task_type")),
        gen_status=_opt_str(row.get("gen_status")),
        fail_reason=_opt_str(row.get("fail_reason")) or None,
        credit_count=credit if isinstance(credit, int) else None,
        image_count=len(result.get("images") or []) if isinstance(result.get("images"), list) else 0,
        video_count=len(result.get("videos") or []) if isinstance(result.get("videos"), list) else 0,
    )


def _as_dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}


def _opt_str(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _decode(raw: bytes) -> str:
    return _ANSI.sub("", raw.decode("utf-8", errors="replace"))


def _tail(raw: bytes) -> str:
    return _tail_text(_decode(raw))


def _tail_text(text: str) -> str:
    return text[-_TAIL_CHARS:]
