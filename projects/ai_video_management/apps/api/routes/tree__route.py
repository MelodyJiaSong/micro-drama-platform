"""Tree-aggregate routes: GET /api/tree, GET /api/tree/subtree, GET /api/events."""
from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from apps.api.container import Container
from libs.application.queries.tree__query import TreeQuery
from libs.infrastructure.watchers.file_change__watcher import FileChangeWatcher, Subscription

router = APIRouter()
HEARTBEAT_S = 15.0


@router.get("/api/tree")
@inject
def get_tree(lazy: bool = Query(False),
             query: TreeQuery = Depends(Provide[Container.tree_query])) -> dict[str, Any]:
    """`lazy=1` (follow-up 280): navigation skeleton plus the first folder levels;
    deeper folders come as `lazy` stubs, fetched with /api/tree/subtree."""
    return query.build(lazy=lazy).to_payload()


@router.get("/api/tree/subtree")
@inject
def get_subtree(path: str = Query(...), depth: int = Query(1, ge=0),
                query: TreeQuery = Depends(Provide[Container.tree_query])) -> dict[str, Any]:
    """One folder under ai_videos/; `depth=0` walks everything below it."""
    return query.subtree(path, depth or None).to_payload()


def sse_event(paths: list[str]) -> str:
    return f"event: change\ndata: {json.dumps({'paths': paths}, ensure_ascii=False)}\n\n"


async def event_stream(sub: Subscription, heartbeat_s: float = HEARTBEAT_S) -> AsyncIterator[str]:
    """Changed-path batches as server-sent events; a comment line every
    `heartbeat_s` keeps proxies from closing an idle stream and lets a vanished
    client surface as a failed write, which ends the generator."""
    try:
        yield "retry: 3000\n\n"
        while True:
            try:
                paths = await asyncio.wait_for(sub.queue.get(), timeout=heartbeat_s)
            except asyncio.TimeoutError:
                yield ": ping\n\n"
                continue
            yield sse_event(paths)
    finally:
        sub.close()


@router.get("/api/events")
@inject
async def get_events(watcher: FileChangeWatcher = Depends(Provide[Container.file_change_watcher])) -> StreamingResponse:
    """Live changes under ai_videos/ (follow-up 280): the page refetches what changed."""
    return StreamingResponse(event_stream(watcher.subscribe()), media_type="text/event-stream",
                             headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"})
