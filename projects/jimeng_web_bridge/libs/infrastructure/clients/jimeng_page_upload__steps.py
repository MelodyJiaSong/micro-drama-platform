"""Reference uploads through the page's own upload tile (FR-30)."""
from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence

from libs.infrastructure.clients.jimeng_browser__client import BrowserSession
from libs.infrastructure.clients.jimeng_page__steps import detect_blocker, guard, locate, ms, named, require
from libs.infrastructure.daos.jimeng_page__dao import UploadItemDao
from libs.infrastructure.errors.jimeng_browser__error import PageStepError, StepFailureKind


async def upload_file(session: BrowserSession, item: UploadItemDao) -> None:
    """Uploads one file whose on-disk name is already `{name}{ext}`, and waits for the done signal."""
    await guard(session, "upload_input")
    trigger = await require(session, "upload_input")
    rejected = locate(session, "upload_rejected")
    real_face = locate(session, "real_face_notice")
    rejected_before, face_before = await rejected.count(), await real_face.count()
    async with session.page.expect_file_chooser(timeout=ms(session.timeouts.action_s)) as chooser_info:
        await trigger.click(timeout=ms(session.timeouts.action_s))
    chooser = await chooser_info.value
    await chooser.set_files(str(item.path))
    tile = named(session, "upload_tile", item.name)
    deadline = time.monotonic() + session.timeouts.upload_done_s
    while True:
        if await real_face.count() > face_before:
            raise PageStepError(StepFailureKind.REAL_FACE_REJECTED, "upload", await real_face.last.inner_text())
        if await rejected.count() > rejected_before:
            raise PageStepError(StepFailureKind.UPLOAD_REJECTED, "upload", await rejected.last.inner_text())
        if await tile.count() > 0 and await locate(session, "upload_done_signal", root=tile.first).count() == 0:
            return
        blocker = await detect_blocker(session)
        if blocker is not None:
            raise PageStepError(blocker, "upload", "blocking page UI is showing")
        if time.monotonic() > deadline:
            raise PageStepError(StepFailureKind.UPLOAD_TIMEOUT, "upload", f"{item.name} not done in time")
        await asyncio.sleep(0.1)


async def remove_upload(session: BrowserSession, name: str) -> None:
    tile = named(session, "upload_tile", name)
    if await tile.count() > 0:
        await locate(session, "upload_tile_remove", root=tile.first).first.click(timeout=ms(session.timeouts.action_s))


async def uploads_mismatch(session: BrowserSession, names: Sequence[str]) -> str | None:
    """None when the composer holds exactly `names`, each finished uploading."""
    total = await locate(session, "upload_tile").count()
    missing = []
    for name in names:
        tile = named(session, "upload_tile", name)
        if await tile.count() != 1 or await locate(session, "upload_done_signal", root=tile.first).count() > 0:
            missing.append(name)
    if missing or total != len(names):
        return f"参考素材不一致：期望 {list(names)}，页面共 {total} 个，缺少或未完成 {missing}"
    return None
