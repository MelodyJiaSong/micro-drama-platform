"""The user's verdict on a take: a draft's 通过 lets `tools/shot_take.py submit --stage final` use it (follow-up 265);
a final's 通过 marks it usable for the cut, judged on the scene's 正片 tab (follow-up 273)."""
from __future__ import annotations

import time
from collections.abc import Callable

from libs.domain.errors.shot_take__error import ShotTakeError
from libs.infrastructure.writers.shot_take__writer import ShotTakeWriter

VERDICTS = {"draft": {"通过": "通过（用户 {now}，可出正式条）", "不通过": "不通过（用户 {now}）"},
            "final": {"通过": "通过（用户 {now}，正片可用）", "不通过": "不通过（用户 {now}）"}}


class ShotTakeCommand:
    def __init__(self, writer: ShotTakeWriter, clock: Callable[[], str] | None = None) -> None:
        self.writer = writer
        self.clock = clock or (lambda: time.strftime("%Y-%m-%d %H:%M"))

    def verdict(self, take_path: str, verdict: str) -> str:
        if verdict not in VERDICTS["draft"]:
            raise ShotTakeError("结论只能是：%s" % "、".join(VERDICTS["draft"]))
        folder = self.writer.folder(take_path)
        stage = self.writer.record(folder).get("stage") or ("draft" if folder.parent.name == "drafts" else "final")
        if stage not in VERDICTS:
            raise ShotTakeError("这一条既不是草稿也不是正式条：%s" % stage)
        status = VERDICTS[stage][verdict].format(now=self.clock())
        self.writer.set_status(folder, status)
        return status
