from collections.abc import Mapping
from datetime import datetime
from types import MappingProxyType

from libs.common.enums import OperationKind, OperationState
from libs.domain.errors.operation__error import IllegalOperationTransitionError, OperationInvariantError

O = OperationState


class OperationEntity:
    def __init__(
        self,
        operation_id: str,
        kind: OperationKind,
        created_at: datetime,
        subject_id: str | None = None,
        *,
        state: OperationState = O.PENDING,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        result: Mapping[str, object] | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> None:
        self._operation_id: str = operation_id
        self._kind: OperationKind = kind
        self._created_at: datetime = created_at
        self._subject_id: str | None = subject_id
        self._state: OperationState = state
        self._started_at: datetime | None = started_at
        self._finished_at: datetime | None = finished_at
        self._result: dict[str, object] | None = None if result is None else dict(result)
        self._error_code: str | None = error_code
        self._error_message: str | None = error_message
        if state is O.RUNNING and started_at is None:
            raise OperationInvariantError("running 的 operation 必须带 started_at")
        if state in (O.SUCCEEDED, O.FAILED) and finished_at is None:
            raise OperationInvariantError("已结束的 operation 必须带 finished_at")
        if (state is O.SUCCEEDED) != (result is not None) or (state is O.FAILED) != (error_code is not None):
            raise OperationInvariantError("result / error_code 与状态不一致")

    @property
    def operation_id(self) -> str:
        return self._operation_id

    @property
    def kind(self) -> OperationKind:
        return self._kind

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def subject_id(self) -> str | None:
        return self._subject_id

    @property
    def state(self) -> OperationState:
        return self._state

    @property
    def started_at(self) -> datetime | None:
        return self._started_at

    @property
    def finished_at(self) -> datetime | None:
        return self._finished_at

    @property
    def result(self) -> Mapping[str, object] | None:
        return None if self._result is None else MappingProxyType(self._result)

    @property
    def error_code(self) -> str | None:
        return self._error_code

    @property
    def error_message(self) -> str | None:
        return self._error_message

    @property
    def is_finished(self) -> bool:
        return self._state in (O.SUCCEEDED, O.FAILED)

    def start(self, at: datetime) -> None:
        if self._state is not O.PENDING:
            raise IllegalOperationTransitionError(self._state, "start")
        self._state = O.RUNNING
        self._started_at = at

    def succeed(self, result: Mapping[str, object], at: datetime) -> None:
        if self._state is not O.RUNNING:
            raise IllegalOperationTransitionError(self._state, "succeed")
        self._state = O.SUCCEEDED
        self._result = dict(result)
        self._finished_at = at

    def fail(self, error_code: str, message: str, at: datetime) -> None:
        if self.is_finished:
            raise IllegalOperationTransitionError(self._state, "fail")
        self._state = O.FAILED
        self._error_code = error_code
        self._error_message = message
        self._finished_at = at
