from __future__ import annotations

import json
from pathlib import Path

from libs.application.commands.probe__command import ProbeCommand
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace


class _UnconfiguredClient:
    configured = False


class _ReachableClient:
    configured = True

    def ping(self) -> dict[str, str]:
        return {"status_code": "200", "ok": "True"}


def _command(tmp_path: Path, gemini: object, qwen: object) -> ProbeCommand:
    return ProbeCommand(gemini=gemini, qwen=qwen, workspace=SafeWorkspace(root=str(tmp_path)))  # type: ignore[arg-type]


def test_probe_skips_cleanly_without_keys(tmp_path: Path) -> None:
    results = _command(tmp_path, _UnconfiguredClient(), _UnconfiguredClient()).run(["all"])
    assert results[0].status == "skipped"
    reports = list((tmp_path / "probes").glob("report-*.json"))
    assert len(reports) == 1
    assert json.loads(reports[0].read_text(encoding="utf-8"))[0]["name"] == "understand-connectivity"


def test_probe_reports_reachability_when_configured(tmp_path: Path) -> None:
    result = _command(tmp_path, _ReachableClient(), _UnconfiguredClient()).understand_connectivity()
    assert result.status == "ok"
    assert '"ok": "True"' in result.data["gemini"]
    assert result.data["qwen"].startswith("skipped")
