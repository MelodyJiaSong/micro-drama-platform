"""UI ↔ HTTP JSON contract fixtures (validation strategy: shared JSON shapes vs UI field paths).

Every response DTO an HTTP route returns is rendered through the routes' own `to_json` into two
fixtures under `apps/ui/test/fixtures/contract/`: `full` (optionals filled, one element per list)
and `minimal` (optionals null, lists empty). The UI's `tsc -b` assigns each fixture to its wire
type, so a UI field the DTO lacks, or a non-null UI field the DTO may null, fails the UI build.

Regenerate after a DTO change: `python -m tests.contract.ui_contract` (or `make ui-contract`).
"""
from __future__ import annotations

import collections.abc
import dataclasses
import json
import sys
import types
import typing
from datetime import datetime
from pathlib import Path

from apps.api.routes._helpers import to_json
from libs.application.dtos.batch__dto import BatchConfirmationQdto, BatchConfirmCdto, BatchPrecheckCdto, BatchQdto
from libs.application.dtos.candidate__dto import PromoteCdto
from libs.application.dtos.drama_config__dto import DramaConfigQdto, DramaTreeQdto, ProposeCdto, SaveConfigCdto
from libs.application.dtos.entity__dto import ReconcileQdto
from libs.application.dtos.global_config__dto import GlobalConfigQdto, GlobalConfigSaveCdto
from libs.application.dtos.history__dto import DailyTotalsQdto, HistoryPageQdto
from libs.application.dtos.job__dto import JobDetailQdto, JobPageQdto, JobStateCdto, QueueStateCdto
from libs.application.dtos.operation__dto import OperationCdto, OperationQdto
from libs.application.dtos.session__dto import BrowserOpenCdto, HealthQdto, SessionStatusQdto
from libs.application.dtos.wait__dto import WaitQdto

FIXTURE_DIR: Path = Path(__file__).resolve().parents[2] / "apps" / "ui" / "test" / "fixtures" / "contract"
RESPONSE_DTOS: tuple[type, ...] = (
    HealthQdto,
    SessionStatusQdto,
    BrowserOpenCdto,
    OperationCdto,
    OperationQdto,
    BatchPrecheckCdto,
    BatchQdto,
    BatchConfirmationQdto,
    BatchConfirmCdto,
    JobPageQdto,
    JobDetailQdto,
    JobStateCdto,
    QueueStateCdto,
    WaitQdto,
    DramaTreeQdto,
    DramaConfigQdto,
    ProposeCdto,
    SaveConfigCdto,
    GlobalConfigQdto,
    GlobalConfigSaveCdto,
    ReconcileQdto,
    HistoryPageQdto,
    DailyTotalsQdto,
    PromoteCdto,
)
_SAMPLE_TIME: str = "2026-09-14T08:00:00+08:00"


def _sample(tp: object, name: str, full: bool, stack: tuple[type, ...]) -> object:
    origin = typing.get_origin(tp)
    if origin in (typing.Union, types.UnionType):
        options = [arg for arg in typing.get_args(tp) if arg is not type(None)]
        if len(options) < len(typing.get_args(tp)) and not full:
            return None
        return _sample(options[0], name, full, stack)
    if origin in (tuple, list, collections.abc.Sequence, set, frozenset):
        element = typing.get_args(tp)[0]
        if not full or (isinstance(element, type) and element in stack):
            return []
        return [_sample(element, name, full, stack)]
    if origin in (dict, collections.abc.Mapping):
        return {"key": "value"} if full else {}
    if dataclasses.is_dataclass(tp) and isinstance(tp, type):
        return _instance(tp, full, stack)
    if tp is str:
        return f"{name}_1"
    if tp is bool:
        return True
    if tp is int:
        return 1
    if tp is float:
        return 1.5
    if tp is datetime:
        return _SAMPLE_TIME
    return None


def _instance(cls: type, full: bool, stack: tuple[type, ...] = ()) -> dict[str, object]:
    hints = typing.get_type_hints(cls)
    return {
        field.name: _sample(hints[field.name], field.name, full, (*stack, cls)) for field in dataclasses.fields(cls)
    }


def render() -> dict[str, str]:
    files: dict[str, str] = {}
    for cls in RESPONSE_DTOS:
        for variant, full in (("full", True), ("minimal", False)):
            payload = to_json(_instance(cls, full))
            files[f"{cls.__name__}.{variant}.json"] = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    return files


def write() -> int:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    wanted = render()
    for stale in FIXTURE_DIR.glob("*.json"):
        if stale.name not in wanted:
            stale.unlink()
    for name, text in wanted.items():
        (FIXTURE_DIR / name).write_text(text, encoding="utf-8", newline="\n")
    return len(wanted)


if __name__ == "__main__":
    sys.stdout.write(f"wrote {write()} contract fixtures to {FIXTURE_DIR}\n")
