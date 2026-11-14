from dataclasses import dataclass
from datetime import datetime, timezone

from projects.suno_browser_service.libs.common.errors import ServiceError


@dataclass
class JobEntity:
    id: str
    key: str
    fingerprint: str
    status: str
    payload: dict
    version: int = 0

    def transition(self, status: str, **fields: object) -> None:
        allowed = {
            "queued": {"preparing", "downloading", "cancelled"},
            "preparing": {"submitting", "waiting", "needs_login", "needs_attention", "failed", "queued"},
            "submitting": {"waiting", "uncertain"},
            "waiting": {"downloading", "uncertain", "needs_attention", "needs_login", "queued"},
            "downloading": {"completed", "needs_attention", "needs_login", "queued"},
            "needs_login": {"queued", "cancelled"}, "needs_attention": {"queued", "cancelled"}, "uncertain": {"queued"},
        }
        if status not in allowed.get(self.status, set()):
            raise ServiceError("invalid_transition", f"不能从 {self.status} 转到 {status}")
        self.status = status
        self.payload.update(fields)
        self.payload["updated_at"] = datetime.now(timezone.utc).isoformat()

    def cancel(self) -> None:
        # Only work that never reached Create can be withdrawn; submitted jobs may already have cost credits.
        if self.payload.get("submitted") or self.status not in {"queued", "needs_login", "needs_attention"}:
            raise ServiceError("job_active", "只能取消尚未提交的排队或暂停任务")
        self.transition("cancelled")

    def resume(self, song_urls: list[str], recollect: bool = False) -> None:
        if self.status not in {"needs_login", "needs_attention", "uncertain"}:
            raise ServiceError("job_active", "仅可恢复暂停任务；排队、执行中或已完成任务不可恢复")
        if recollect:
            # Re-find the clips of a submitted job in the library; replaces any unconfirmed song_urls, never regenerates.
            if not self.payload.get("submitted") or song_urls or self.payload.get("files"):
                raise ServiceError("recollect_invalid", "重新认领只用于已提交、尚未下载文件的任务，且不能同时给 song_urls")
            self.payload.update(song_urls=[], recollect=True)
            self.transition("queued", error=None)
            return
        if self.payload.get("submitted") and not (song_urls or self.payload.get("song_urls")):
            raise ServiceError("song_urls_required", "提交结果未知；请在 Suno 确认歌曲后提供 song_urls，只恢复下载")
        if song_urls:
            self.payload["song_urls"] = song_urls
        self.transition("queued", error=None)
