"""审片串联的状态（follow-up 260）：当前该用哪几条（算指纹判断过期）、后台进度、上次的结果。"""
from __future__ import annotations

import os
from typing import Any

from libs.application.dtos.review_reel__dto import ReviewReelQdto
from libs.domain.errors.review_reel__error import ReviewReelError
from libs.domain.value_objects.review_reel__valueobject import ReelClip, ReviewReelPlan
from libs.infrastructure.readers.review_reel__reader import ReviewReelReader


class ReviewReelQuery:
    def __init__(self, reader: ReviewReelReader) -> None:
        self.reader = reader

    def episode(self, episode_path: str, scene: str | None) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
        """(集目录, 全部场次, 本次要拼的场次)。"""
        try:
            path, scenes = self.reader.scenes(episode_path)
        except FileNotFoundError as exc:
            raise ReviewReelError(str(exc), 404) from exc
        except ValueError as exc:
            raise ReviewReelError("模块文件格式无效，请检查JSON内容") from exc
        chosen = [s for s in scenes if scene in (None, s["id"])]
        if scene is not None and not chosen:
            raise ReviewReelError(f"分镜里没有场次 {scene}", 404)
        return path, scenes, chosen

    @staticmethod
    def plan(name: str, scene: str | None, candidates: list[tuple[str, str, list[dict[str, Any]]]]) -> ReviewReelPlan:
        """每镜取最新一条；没有可用条的镜跳过。"""
        clips, skipped = [], []
        for sid, key, takes in candidates:
            if not takes:
                skipped.append({"key": key, "scene": sid, "reason": "还没有生成"})
                continue
            t = takes[0]
            clips.append(ReelClip(sid, key, t["path"], t["video"], t["size"], t["mtime_ns"], t["review_status"]))
        return ReviewReelPlan(name, scene, clips, skipped)

    def read(self, episode_path: str, scene: str | None) -> ReviewReelQdto:
        path, scenes, chosen = self.episode(episode_path, scene)
        name = f"{path.rsplit('/', 1)[-1]}_{scene or 'all'}"
        candidates = self.reader.candidates(path, chosen)
        current = self.plan(name, scene, candidates)
        options = [{"id": s["id"], "label": f"{s.get('location', '')} · {s.get('time', '')}", "shots": len(s["shots"])} for s in scenes]
        status = self.reader.load(path, name, "status") or {}
        manifest = self.reader.load(path, name, "manifest")
        video = f"{path}/{self.reader.folder(path).name}/{name}.mp4"
        has_video = manifest is not None and (self.reader.root / video).is_file()
        if has_video:   # 审核状态随时会改：按 take 目录换成现在的
            reviews = {t["path"]: t["review_status"] for _, _, takes in candidates for t in takes}
            manifest = {**manifest, "chapters": [{**c, "review_status": reviews.get(c["take"], c["review_status"])}
                                                  for c in manifest.get("chapters", [])]}
        state = status.get("state", "none")
        if state == "running" and status.get("pid") != os.getpid():
            state = "interrupted"     # 服务重启过，后台线程已不在
        if state in ("done", "none"):
            state = "done" if has_video else "none"
        return ReviewReelQdto(path, scene, name, state, int(status.get("done", 0)), int(status.get("total", len(candidates))),
                              str(status.get("error", "")), video if has_video else "",
                              bool(has_video and manifest.get("fingerprint") != current.fingerprint),
                              manifest if has_video else None, options)
