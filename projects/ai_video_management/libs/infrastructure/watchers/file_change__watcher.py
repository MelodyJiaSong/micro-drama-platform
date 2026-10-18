"""Live file changes under `ai_videos/` for the browser (follow-up 280).

The UI used to show new takes, prompts and cuts only after a manual reload, and
every reload re-walked the whole tree. One background thread now watches
`ai_videos/` (watchfiles: ReadDirectoryChangesW / inotify, not polling) and fans
each debounced batch of changed paths out to the open `/api/events` streams;
the page refetches only what a batch touches.

The thread starts with the first subscriber and keeps running (daemon) — one
watcher per server process no matter how many tabs are open.
"""
from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass, field
from pathlib import Path

from libs.common.exposed_tree import ExposedTree

log = logging.getLogger(__name__)

# Path segments whose churn never matters to the UI.
IGNORED_SEGMENTS: frozenset[str] = frozenset({".git", "__pycache__", "node_modules", ".pytest_cache"})
# Partial downloads and editor swap files: the finished file arrives as its own change.
IGNORED_SUFFIXES: tuple[str, ...] = (".part", ".tmp", ".swp", "~")
DEBOUNCE_MS = 700
QUEUE_LIMIT = 64
# A subscriber that falls this far behind gets one `reset` instead of the backlog.
RESET = "*"


@dataclass(eq=False)   # identity-hashed: kept in a set of open streams
class Subscription:
    queue: asyncio.Queue[list[str]]
    loop: asyncio.AbstractEventLoop
    _owner: FileChangeWatcher | None = field(default=None, repr=False)

    def close(self) -> None:
        if self._owner is not None:
            self._owner._unsubscribe(self)
            self._owner = None


class FileChangeWatcher:
    def __init__(self, exposed: ExposedTree, debounce_ms: int = DEBOUNCE_MS) -> None:
        self._root = exposed.root
        self._watched = self._root / "ai_videos"
        # The tree never shows these folders, so their churn is never news to the page.
        self._ignored = IGNORED_SEGMENTS | frozenset(exposed.excluded_dirs())
        self._debounce_ms = debounce_ms
        self._subs: set[Subscription] = set()
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    # --- subscribers ---------------------------------------------------------
    def subscribe(self) -> Subscription:
        """Must be called from inside the event loop that will read the queue."""
        sub = Subscription(queue=asyncio.Queue(maxsize=QUEUE_LIMIT), loop=asyncio.get_running_loop(), _owner=self)
        with self._lock:
            self._subs.add(sub)
            self._ensure_started()
        return sub

    def _unsubscribe(self, sub: Subscription) -> None:
        with self._lock:
            self._subs.discard(sub)

    def publish(self, rel_paths: list[str]) -> None:
        """Hand one batch to every subscriber (safe from any thread)."""
        if not rel_paths:
            return
        with self._lock:
            subs = list(self._subs)
        for sub in subs:
            try:
                sub.loop.call_soon_threadsafe(self._deliver, sub, rel_paths)
            except RuntimeError:   # loop already closed: the stream is gone
                self._unsubscribe(sub)

    @staticmethod
    def _deliver(sub: Subscription, rel_paths: list[str]) -> None:
        try:
            sub.queue.put_nowait(rel_paths)
        except asyncio.QueueFull:
            while not sub.queue.empty():
                sub.queue.get_nowait()
            sub.queue.put_nowait([RESET])

    # --- watching --------------------------------------------------------------
    def relevant(self, rel_path: str) -> bool:
        parts = rel_path.split("/")
        return not any(part in self._ignored for part in parts) and not rel_path.endswith(IGNORED_SUFFIXES)

    def to_rel(self, path: str | Path) -> str | None:
        try:
            return Path(path).relative_to(self._root).as_posix()
        except ValueError:
            return None

    def batch(self, changes: set[tuple[object, str]]) -> list[str]:
        """Changed paths of one watchfiles batch, repo-relative, noise dropped."""
        out = {rel for _, raw in changes if (rel := self.to_rel(raw)) is not None and self.relevant(rel)}
        return sorted(out)

    def _ensure_started(self) -> None:
        if self._thread is not None or not self._watched.is_dir():
            return
        self._thread = threading.Thread(target=self._run, name="ai-videos-watcher", daemon=True)
        self._thread.start()

    def _run(self) -> None:
        try:
            from watchfiles import watch
            for changes in watch(self._watched, stop_event=self._stop, debounce=self._debounce_ms,
                                 raise_interrupt=False, ignore_permission_denied=True):
                self.publish(self.batch(changes))
        except Exception:   # never take the server down with the watcher
            log.exception("ai_videos watcher stopped")
        finally:
            with self._lock:
                self._thread = None

    def close(self) -> None:
        self._stop.set()
