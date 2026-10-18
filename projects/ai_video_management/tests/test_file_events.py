"""Live file changes for the browser (follow-up 280): one watcher on
`ai_videos/`, batches of repo-relative paths fanned out to `/api/events`."""
from __future__ import annotations

import asyncio
import time
from pathlib import Path

from apps.api.routes.tree__route import event_stream, sse_event
from libs.common.exposed_tree import ExposedTree
from libs.infrastructure.watchers.file_change__watcher import QUEUE_LIMIT, RESET, FileChangeWatcher


def _watcher(tmp_path: Path) -> FileChangeWatcher:
    (tmp_path / "ai_videos").mkdir(exist_ok=True)
    return FileChangeWatcher(ExposedTree(tmp_path), debounce_ms=100)


def test_batch_is_repo_relative_sorted_and_drops_noise(tmp_path: Path) -> None:
    w = _watcher(tmp_path)
    root = tmp_path / "ai_videos"
    changes = {(1, str(root / "d/ep01/story.json")), (2, str(root / "d/a.png")),
               (1, str(root / "d/.git/index")), (1, str(root / "d/x.mp4.part")), (3, str(tmp_path.parent / "elsewhere"))}
    assert w.batch(changes) == ["ai_videos/d/a.png", "ai_videos/d/ep01/story.json"]


def test_sse_event_format() -> None:
    assert sse_event(["ai_videos/甲.md"]) == 'event: change\ndata: {"paths": ["ai_videos/甲.md"]}\n\n'


def test_publish_reaches_every_subscriber_and_overflow_resets(tmp_path: Path) -> None:
    w = _watcher(tmp_path)
    w._ensure_started = lambda: None   # unit test: no real watching thread

    async def run() -> None:
        a, b = w.subscribe(), w.subscribe()
        w.publish(["ai_videos/x.md"])
        await asyncio.sleep(0)
        assert a.queue.get_nowait() == ["ai_videos/x.md"] and b.queue.get_nowait() == ["ai_videos/x.md"]
        b.close()
        for i in range(QUEUE_LIMIT + 3):
            w.publish([f"ai_videos/{i}.md"])
        await asyncio.sleep(0)
        assert b.queue.empty()
        drained = [a.queue.get_nowait() for _ in range(a.queue.qsize())]
        assert [RESET] in drained and len(drained) <= QUEUE_LIMIT
        a.close()

    asyncio.run(run())


def test_event_stream_sends_retry_heartbeat_and_changes(tmp_path: Path) -> None:
    w = _watcher(tmp_path)
    w._ensure_started = lambda: None

    async def run() -> list[str]:
        sub = w.subscribe()
        stream = event_stream(sub, heartbeat_s=0.05)
        out = [await stream.__anext__(), await stream.__anext__()]
        w.publish(["ai_videos/d/st1.mp4"])
        out.append(await stream.__anext__())
        await stream.aclose()
        assert sub not in w._subs   # closing the stream unsubscribes
        return out

    assert asyncio.run(run()) == ["retry: 3000\n\n", ": ping\n\n", sse_event(["ai_videos/d/st1.mp4"])]


def test_real_watcher_reports_a_new_file(tmp_path: Path) -> None:
    w = _watcher(tmp_path)

    async def run() -> list[str]:
        sub = w.subscribe()
        await asyncio.sleep(0.5)   # let the watcher thread start watching
        target = tmp_path / "ai_videos/d/ep01/new.md"
        target.parent.mkdir(parents=True)
        target.write_text("x", encoding="utf-8")
        deadline = time.monotonic() + 10
        seen: list[str] = []
        while time.monotonic() < deadline and "ai_videos/d/ep01/new.md" not in seen:
            try:
                seen += await asyncio.wait_for(sub.queue.get(), timeout=1)
            except asyncio.TimeoutError:
                pass
        sub.close()
        return seen

    try:
        assert "ai_videos/d/ep01/new.md" in asyncio.run(run())
    finally:
        w.close()
