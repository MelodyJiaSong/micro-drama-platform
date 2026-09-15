from __future__ import annotations

import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Protocol

from libs.application.dtos.job__dto import QueueStateCdto
from libs.application.dtos.session__dto import (
    CanaryCheckQdto,
    CliSessionQdto,
    HealthQdto,
    SessionStatusQdto,
    WebSessionQdto,
)
from libs.common.clock import Clock, iso
from libs.common.enums import BackendKind, OperationKind, OperationState, PauseReason, QueueState
from libs.domain.value_objects.global_config__valueobject import GlobalConfig
from libs.infrastructure.daos.operation__dao import OperationDao
from libs.infrastructure.readers.batch__reader import BatchReader
from libs.infrastructure.readers.operation__reader import OperationReader
from libs.infrastructure.readers.store_record__reader import QueueStateReader
from libs.infrastructure.writers.output__writer import zone_for

_LOGIN_REASONS: frozenset[str] = frozenset({PauseReason.LOGIN_EXPIRED.value, PauseReason.CLI_LOGIN_REQUIRED.value})


class BrowserState(Protocol):
    @property
    def is_started(self) -> bool: ...

    @property
    def is_lost(self) -> bool: ...

    @property
    def web_version(self) -> str | None: ...


class SessionQuery:
    """Session page and `session_status`: the last stored canary snapshots plus flags that cost nothing to read.

    Never launches the browser, runs a canary or calls the CLI inside a request (spec v2 §5.10 `/api/session`).
    """

    def __init__(
        self,
        operations: OperationReader,
        queue_states: QueueStateReader,
        batches: BatchReader,
        global_config_provider: Callable[[], GlobalConfig],
        browser_provider: Callable[[], BrowserState],
        clock: Clock,
        test_mode: bool,
    ) -> None:
        self._operations = operations
        self._queue_states = queue_states
        self._batches = batches
        self._global_config = global_config_provider
        self._browser = browser_provider
        self._clock = clock
        self._test_mode = test_mode

    def health(self) -> HealthQdto:
        return HealthQdto(ok=True)

    def status(self) -> SessionStatusQdto:
        config = self._global_config()
        now = self._clock.now()
        day_start = now.astimezone(zone_for(config.time.timezone)).replace(hour=0, minute=0, second=0, microsecond=0)
        today = self._batches.confirmed_credits_between(iso(day_start), iso(day_start + timedelta(days=1)))
        return SessionStatusQdto(self._web(), self._cli(config), self._queues(now), today, self._test_mode)

    def _web(self) -> WebSessionQdto:
        operation = self._operations.latest(OperationKind.CANARY.value, BackendKind.WEB.value)
        result = _object(None if operation is None else operation.result_json)
        failed = tuple(str(name) for name in _list(result.get("failed_checks")))
        canary_ok = _canary_ok(operation, result)
        browser = self._browser()
        if operation is not None and operation.state == OperationState.FAILED.value:
            checks: tuple[CanaryCheckQdto, ...] = (CanaryCheckQdto("canary", False, _error_message(operation)),)
        elif failed:
            checks = tuple(CanaryCheckQdto(name, False, None) for name in failed)
        else:
            checks = (CanaryCheckQdto("canary", True, None),) if canary_ok else ()
        if result.get("pause_reason") in _LOGIN_REASONS:
            login_state = "logged_out"
        elif canary_ok:
            login_state = "logged_in"
        else:
            login_state = "unknown"
        return WebSessionQdto(
            login_state=login_state,
            browser_open=browser.is_started and not browser.is_lost,
            web_version=browser.web_version or _str(result.get("version")),
            checked_at=_finished_at(operation),
            canary_operation_id=None if operation is None else operation.operation_id,
            canary_state=None if operation is None else operation.state,
            canary_ok=canary_ok,
            canary_checks=checks,
        )

    def _cli(self, config: GlobalConfig) -> CliSessionQdto:
        operation = self._operations.latest(OperationKind.CANARY.value, BackendKind.CLI.value)
        result = _object(None if operation is None else operation.result_json)
        version = _str(result.get("version"))
        logged_in = result.get("logged_in")
        balance = result.get("balance")
        if operation is not None and operation.state == OperationState.FAILED.value:
            error = _error_message(operation)
        else:
            error = None if _canary_ok(operation, result) is not False else _str(result.get("pause_reason"))
        return CliSessionQdto(
            configured=bool(config.cli.path) and Path(os.path.expanduser(config.cli.path)).is_file(),
            logged_in=logged_in if isinstance(logged_in, bool) else None,
            version=version,
            min_version=config.cli.min_version,
            version_ok=None if version is None else not bool(result.get("version_warning")),
            credit_balance=balance if isinstance(balance, int) and not isinstance(balance, bool) else None,
            checked_at=_finished_at(operation),
            error=error,
        )

    def _queues(self, now: datetime) -> tuple[QueueStateCdto, ...]:
        stored = {row.backend: row for row in self._queue_states.all()}
        return tuple(
            QueueStateCdto(row.backend, row.state, row.reason, row.updated_at)
            if (row := stored.get(kind.value)) is not None
            else QueueStateCdto(kind.value, QueueState.RUNNING.value, None, iso(now))
            for kind in BackendKind
        )


def _canary_ok(operation: OperationDao | None, result: dict[str, object]) -> bool | None:
    if operation is None or operation.state in (OperationState.PENDING.value, OperationState.RUNNING.value):
        return None
    return operation.state == OperationState.SUCCEEDED.value and result.get("ok") is True


def _finished_at(operation: OperationDao | None) -> str | None:
    if operation is None:
        return None
    return _str(_object(operation.payload_json).get("finished_at")) or operation.updated_at


def _error_message(operation: OperationDao) -> str | None:
    error = _object(operation.error_json)
    return _str(error.get("message")) or _str(error.get("error_code"))


def _object(text: str | None) -> dict[str, object]:
    if not text:
        return {}
    try:
        value = json.loads(text)
    except ValueError:
        return {}
    return value if isinstance(value, dict) else {}


def _list(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def _str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
