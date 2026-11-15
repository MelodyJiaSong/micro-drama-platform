from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


REMINDER_TEMPLATE = (
    "This prompt references a spec-driven project (matched: {matched}). "
    "Per CONVENTIONS.md -> 'Follow-up prompt handling', BEFORE editing any code: "
    "(1) triage which project is impacted; "
    "(2) persist abstracted intent with 'python tools/followup.py new'; "
    "(3) walk downstream artifacts and surgically patch conflicts or gaps; "
    "(4) finish with 'python tools/followup.py done'. "
    "The code change and follow-up persistence MUST happen in the same turn."
)


def find_repo_root(start: Path) -> Path | None:
    for candidate in (start.resolve(), *start.resolve().parents):
        if all((candidate / path).exists() for path in ("AGENTS.md", "CONVENTIONS.md", "specs", "tools")):
            return candidate
    return None


def project_names(repo: Path) -> list[str]:
    return [path.name for path in (repo / "specs").glob("*/*") if path.is_dir()]


def detect_match(prompt: str, names: list[str]) -> str | None:
    lowered = prompt.lower()
    if re.search(r"spec[-_ ]driven", lowered):
        return "the literal phrase 'spec-driven'"
    for name in names:
        pattern = r"(?:^|[^a-z0-9_])" + re.escape(name.lower()) + r"(?:[^a-z0-9_]|$)"
        if re.search(pattern, lowered):
            return f"the project name '{name}'"
    return None


def triage(payload: dict, repo: Path) -> int:
    prompt = payload.get("prompt") or ""
    if not isinstance(prompt, str) or not prompt.strip():
        return 0
    matched = detect_match(prompt, project_names(repo))
    if matched is None:
        return 0
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": REMINDER_TEMPLATE.format(matched=matched),
        }
    }
    sys.stdout.write(json.dumps(output))
    return 0


def stop_check(mode: str, payload: dict, repo: Path) -> int:
    commands = {
        "shot-pack": (["tools/shot_pack.py", "sync", "--all", "--quiet"], False),
        "workflow-catalog": (["tools/workflow_catalog.py", "--check", "--quiet"], False),
        "followup": (["tools/followup.py", "check", "--all", "--hook"], True),
    }
    argv, pass_payload = commands[mode]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    if payload.get("session_id"):
        env["FOLLOWUP_OWNER"] = str(payload["session_id"])
    result = subprocess.run(
        [sys.executable, str(repo / argv[0]), *argv[1:]],
        cwd=repo,
        input=json.dumps(payload) if pass_payload else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return result.returncode


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0
    repo = find_repo_root(Path(payload.get("cwd") or os.getcwd()))
    if repo is None:
        return 0
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "triage":
        return triage(payload, repo)
    if mode in {"shot-pack", "workflow-catalog", "followup"}:
        return stop_check(mode, payload, repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
