from __future__ import annotations

import json
import time
from pathlib import Path

from libs.application.dtos.probe__dto import ProbeResultCdto
from libs.domain.value_objects.safeworkspace__valueobject import SafeWorkspace
from libs.infrastructure.clients.gemini__client import GeminiClient
from libs.infrastructure.clients.qwen__client import QwenClient


class ProbeCommand:
    """FR-13.3/13.4 PoC probes for the video-understanding layer. Each probe is skipped
    (not failed) when its API key is absent. (The Seedance/Seedream probes were removed
    with the regeneration side, follow-up 001.)"""

    def __init__(self, gemini: GeminiClient, qwen: QwenClient, workspace: SafeWorkspace) -> None:
        self._gemini = gemini
        self._qwen = qwen
        self._workspace = workspace

    def run(self, names: list[str]) -> list[ProbeResultCdto]:
        dispatch = {"understand-connectivity": self.understand_connectivity}
        selected = list(dispatch) if names == ["all"] else names
        results = [dispatch[n]() for n in selected]
        self._write_report(results)
        return results

    def understand_connectivity(self) -> ProbeResultCdto:
        """FR-13.3/13.4: Gemini reachability from this deployment + Qwen fallback."""
        data: dict[str, str] = {}
        for name, client in (("gemini", self._gemini), ("qwen", self._qwen)):
            if not client.configured:
                data[name] = "skipped: missing key"
                continue
            try:
                data[name] = json.dumps(client.ping())
            except Exception as exc:  # network failure IS the probe result here
                data[name] = f"unreachable: {type(exc).__name__}"
        status = "skipped" if all(v.startswith("skipped") for v in data.values()) else "ok"
        return ProbeResultCdto("understand-connectivity", status, "reachability recorded", data)

    def _write_report(self, results: list[ProbeResultCdto]) -> None:
        rel = f"probes/report-{time.strftime('%Y%m%d-%H%M%S')}.json"
        path = Path(self._workspace.resolve(rel))
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [{"name": r.name, "status": r.status, "detail": r.detail, "data": r.data} for r in results]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
