from __future__ import annotations

import threading
import time
from collections.abc import Iterator

import pytest

from libs.application.errors.lifecycle__error import ExecutorKeyInUseError
from libs.application.executors.backend__executor import BackendExecutor, ExecutorResult
from libs.common.enums import BackendKind

W, C = BackendKind.WEB, BackendKind.CLI


@pytest.fixture
def executor() -> Iterator[BackendExecutor]:
    pool = BackendExecutor(cli_workers=2)
    yield pool
    pool.shutdown()


def _collect(executor: BackendExecutor, count: int, timeout_s: float = 5.0) -> list[ExecutorResult]:
    deadline = time.monotonic() + timeout_s
    results: list[ExecutorResult] = []
    while len(results) < count and time.monotonic() < deadline:
        results.extend(executor.poll_done())
        time.sleep(0.01)
    return results


def test_web_lane_runs_one_item_at_a_time(executor: BackendExecutor) -> None:
    lock = threading.Lock()
    active = [0, 0]

    def work(value: int) -> int:
        with lock:
            active[0] += 1
            active[1] = max(active[1], active[0])
        time.sleep(0.03)
        with lock:
            active[0] -= 1
        return value

    for index in range(3):
        executor.submit(W, f"k{index}", lambda index=index: work(index))
    assert executor.busy(W)
    results = _collect(executor, 3)
    assert sorted(r.value for r in results) == [0, 1, 2] and active[1] == 1  # type: ignore[type-var]
    assert not executor.busy(W)


def test_cli_lane_runs_two_items_concurrently(executor: BackendExecutor) -> None:
    barrier = threading.Barrier(2, timeout=2)
    executor.submit(C, "a", lambda: barrier.wait())
    assert not executor.busy(C)
    executor.submit(C, "b", lambda: barrier.wait())
    results = _collect(executor, 2)
    assert len(results) == 2 and all(result.ok for result in results)


def test_errors_are_returned_not_raised(executor: BackendExecutor) -> None:
    def boom() -> None:
        raise RuntimeError("backend exploded")

    executor.submit(W, "boom", boom)
    (result,) = _collect(executor, 1)
    assert not result.ok and isinstance(result.error, RuntimeError) and result.value is None and result.key == "boom"


def test_duplicate_key_is_refused_until_collected(executor: BackendExecutor) -> None:
    release = threading.Event()
    executor.submit(W, "same", lambda: release.wait(2))
    with pytest.raises(ExecutorKeyInUseError):
        executor.submit(W, "same", lambda: None)
    assert executor.in_flight(W, "same")
    release.set()
    _collect(executor, 1)
    executor.submit(W, "same", lambda: None)
