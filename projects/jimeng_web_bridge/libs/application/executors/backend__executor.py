from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import TypeVar

from libs.application.errors.lifecycle__error import ExecutorKeyInUseError
from libs.common.enums import BackendKind

T = TypeVar("T")

# Serialises every load → mutate → save of a job aggregate across the scheduler loop, executor workers and API
# threads, so a cancel arriving mid-tick can never be overwritten by a stale entity.
JOB_MUTATION_LOCK: threading.RLock = threading.RLock()


@dataclass(frozen=True)
class ExecutorResult:
    backend: BackendKind
    key: str
    value: object | None
    error: BaseException | None

    @property
    def ok(self) -> bool:
        return self.error is None


class BackendExecutor:
    """One lane per backend: the web lane is a single thread (one UI actor), the cli lane a small pool.

    Work is never interrupted once it starts; cancellation is decided by whoever applies the result.
    """

    def __init__(self, cli_workers: int = 2) -> None:
        self._capacity: dict[BackendKind, int] = {BackendKind.WEB: 1, BackendKind.CLI: cli_workers}
        self._pools: dict[BackendKind, ThreadPoolExecutor] = {
            BackendKind.WEB: ThreadPoolExecutor(max_workers=1, thread_name_prefix="jwb-web"),
            BackendKind.CLI: ThreadPoolExecutor(max_workers=cli_workers, thread_name_prefix="jwb-cli"),
        }
        self._lock = threading.Lock()
        self._futures: list[tuple[BackendKind, str, Future[object]]] = []

    def submit(self, backend: BackendKind, key: str, fn: Callable[[], T]) -> None:
        with self._lock:
            if any(b is backend and k == key for b, k, _ in self._futures):
                raise ExecutorKeyInUseError(f"{backend}:{key} 仍在执行或未被取走")
            self._futures.append((backend, key, self._pools[backend].submit(fn)))

    def busy(self, backend: BackendKind) -> bool:
        with self._lock:
            running = sum(1 for b, _, future in self._futures if b is backend and not future.done())
        return running >= self._capacity[backend]

    def in_flight(self, backend: BackendKind, key: str) -> bool:
        with self._lock:
            return any(b is backend and k == key for b, k, _ in self._futures)

    def poll_done(self) -> list[ExecutorResult]:
        with self._lock:
            done = [entry for entry in self._futures if entry[2].done()]
            self._futures = [entry for entry in self._futures if not entry[2].done()]
        results: list[ExecutorResult] = []
        for backend, key, future in done:
            error = future.exception()
            results.append(ExecutorResult(backend, key, None if error is not None else future.result(), error))
        return results

    def shutdown(self, wait: bool = True) -> None:
        for pool in self._pools.values():
            pool.shutdown(wait=wait, cancel_futures=True)
