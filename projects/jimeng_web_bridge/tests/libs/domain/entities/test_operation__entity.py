import pytest

from libs.common.enums import OperationKind, OperationState
from libs.domain.entities.operation__entity import OperationEntity
from libs.domain.errors.operation__error import IllegalOperationTransitionError, OperationInvariantError
from tests.libs.domain.builders import T0


def op() -> OperationEntity:
    return OperationEntity("op-1", OperationKind.CANARY, T0, "web")


def test_success_path() -> None:
    o = op()
    o.start(T0)
    o.succeed({"checks": ["login_marker"]}, T0)
    assert o.state is OperationState.SUCCEEDED and o.result == {"checks": ["login_marker"]} and o.is_finished
    with pytest.raises(TypeError):
        o.result["x"] = 1  # type: ignore[index]


def test_fail_from_pending_or_running() -> None:
    pending = op()
    pending.fail("browser_missing", "找不到浏览器", T0)
    assert pending.state is OperationState.FAILED and pending.error_code == "browser_missing"
    running = op()
    running.start(T0)
    running.fail("page_contract_broken", "生成按钮缺失", T0)
    assert running.is_finished


def test_illegal_transitions() -> None:
    o = op()
    with pytest.raises(IllegalOperationTransitionError):
        o.succeed({}, T0)
    o.start(T0)
    with pytest.raises(IllegalOperationTransitionError):
        o.start(T0)
    o.succeed({}, T0)
    with pytest.raises(IllegalOperationTransitionError):
        o.fail("x", "y", T0)


def test_state_is_read_only() -> None:
    with pytest.raises(AttributeError):
        op().state = OperationState.SUCCEEDED  # type: ignore[misc]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"state": OperationState.RUNNING},
        {"state": OperationState.SUCCEEDED, "started_at": T0},
        {"state": OperationState.FAILED, "finished_at": T0},
        {"result": {"x": 1}},
    ],
)
def test_rehydrate_invariants(kwargs: dict[str, object]) -> None:
    with pytest.raises(OperationInvariantError):
        OperationEntity("op-1", OperationKind.CANARY, T0, **kwargs)  # type: ignore[arg-type]
