"""开始拼一份审片串联（follow-up 260）：输入没变就直接用上次的；否则放到后台线程逐条重编码再拼接，进度写进状态文件。"""
from __future__ import annotations

import os
import threading
import time
from collections.abc import Callable
from typing import Any

from libs.application.dtos.review_reel__dto import ReviewReelQdto
from libs.application.queries.review_reel__query import ReviewReelQuery
from libs.common.review_reel import FPS, HEIGHT, REEL_FORMAT, WIDTH
from libs.domain.value_objects.review_reel__valueobject import ReelClip, ReviewReelPlan
from libs.infrastructure.readers.review_reel__reader import ReviewReelReader
from libs.infrastructure.writers.review_reel__writer import ReviewReelWriter


def _background(job: Callable[[], None]) -> None:
    threading.Thread(target=job, name="review-reel", daemon=True).start()


def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


class ReviewReelCommand:
    def __init__(self, reader: ReviewReelReader, writer: ReviewReelWriter,
                 spawn: Callable[[Callable[[], None]], None] | None = None) -> None:
        self.reader = reader
        self.writer = writer
        self.query = ReviewReelQuery(reader)
        self.spawn = spawn or _background

    def start(self, episode_path: str, scene: str | None) -> ReviewReelQdto:
        current = self.query.read(episode_path, scene)
        if (current.state == "done" and not current.stale) or current.state == "running":
            return current
        path, _, chosen = self.query.episode(episode_path, scene)
        candidates = self.reader.candidates(path, chosen)
        plan = ReviewReelQuery.plan(current.name, scene, candidates)
        job = f"{path}/{current.name}"
        if not self.writer.claim(job):
            return self.query.read(episode_path, scene)
        folder = self.reader.folder(path)
        status = {"state": "running", "done": 0, "total": len(candidates), "pid": os.getpid(), "started_at": _now(), "error": ""}
        self.writer.save(folder / f"{current.name}.status.json", status)

        def run() -> None:
            try:
                self._build(path, folder, plan, candidates, status, job)
            except Exception as exc:   # noqa: BLE001 — 任何失败都要写进状态，后台线程不能吞掉
                self.writer.save(folder / f"{current.name}.status.json",
                                 {**status, "state": "failed", "error": str(exc)[:500], "finished_at": _now()})
            finally:
                self.writer.release(job)
        self.spawn(run)
        return self.query.read(episode_path, scene)

    def _build(self, path: str, folder, plan: ReviewReelPlan, candidates: list[tuple[str, str, list[dict[str, Any]]]],
               status: dict[str, Any], job: str) -> None:
        name = plan.name
        clips, durations, segments, skipped = [], [], [], []
        for index, (sid, key, takes) in enumerate(candidates):
            for order, take in enumerate(takes):
                made = self.writer.segment(folder, take)
                if made is None:
                    continue
                note = "" if order == 0 else f"最新一条（{takes[0]['id']}）读不出，可能还在写入；用了上一条（{take['id']}）"
                clips.append(ReelClip(sid, key, take["path"], take["video"], take["size"], take["mtime_ns"], take["review_status"], note))
                durations.append(made[1])
                segments.append(made[0])
                break
            else:
                skipped.append({"key": key, "scene": sid, "reason": "最新几条都读不出" if takes else "还没有生成"})
            self.writer.save(folder / f"{name}.status.json", {**status, "done": index + 1})
        if not segments:
            raise RuntimeError("这一范围里没有任何能读的生成条")
        used = ReviewReelPlan(name, plan.scene, clips, skipped)
        chapters = [{**c, "segment": seg.name} for c, seg in zip(used.chapters(durations), segments)]
        self.writer.concat(segments, folder / f"{name}.mp4")
        self.writer.save(folder / f"{name}.json", {
            "name": name, "episode_path": path, "scene": plan.scene, "fingerprint": plan.fingerprint, "created_at": _now(),
            "format": {"spec": REEL_FORMAT, "width": WIDTH, "height": HEIGHT, "fps": FPS},
            "duration": chapters[-1]["end"], "chapters": chapters, "skipped": skipped})
        keep = {c.get("segment") for m in folder.glob("*.json") if not m.name.endswith(".status.json")
                for c in (self.reader.load(path, m.stem, "manifest") or {}).get("chapters", [])}
        if self.writer.only(job):   # 另一份还在拼时它的中间件还没进清单，先不清
            self.writer.prune(folder, {k for k in keep if k})
        self.writer.save(folder / f"{name}.status.json", {**status, "state": "done", "done": len(candidates), "finished_at": _now()})
