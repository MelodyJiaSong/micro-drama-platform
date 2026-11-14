import hashlib
import json
import re
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from pydantic import ValidationError

from projects.suno_browser_service.libs.application.dtos.job__dto import JobCdto, JobQdto
from projects.suno_browser_service.libs.application.mappers.job__mapper import JobMapper
from projects.suno_browser_service.libs.common.errors import ServiceError
from projects.suno_browser_service.libs.common.settings import REPO_ROOT, Settings
from projects.suno_browser_service.libs.common.generation import GenerationRequest
from projects.suno_browser_service.libs.infrastructure.clients.asset__client import AssetClient
from projects.suno_browser_service.libs.domain.entities.job__entity import JobEntity
from projects.suno_browser_service.libs.infrastructure.clients.database__client import DatabaseClient
from projects.suno_browser_service.libs.infrastructure.readers.job__reader import JobReader
from projects.suno_browser_service.libs.infrastructure.writers.job__writer import JobWriter


class JobCommand:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        db = DatabaseClient(settings.data_dir / "jobs.sqlite3")
        self.reader, self.writer = JobReader(db), JobWriter(db)

    def submit(self, key: str, request: JobCdto) -> JobQdto:
        if not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", key):
            raise ServiceError("invalid_key", "Idempotency-Key 须为 1–128 位 ASCII 字母、数字、_.:-", 422)
        if not request.prompt.strip() or len(request.prompt) > 2000 or request.format not in {"mp3", "wav"}:
            raise ServiceError("invalid_request", "prompt 需 1–2000 字符，format 为 mp3/wav", 422)
        if request.mode == "advanced" and not request.instrumental and not (request.lyrics and request.lyrics.strip()):
            raise ServiceError("lyrics_required", "人声模式须提供 lyrics；纯音乐使用 instrumental=true", 422)
        if request.lyrics and len(request.lyrics) > 5000:
            raise ServiceError("invalid_lyrics", "lyrics 最长 5000 字符", 422)
        target = self.settings.data_dir
        if request.target:
            target = (REPO_ROOT / request.target).resolve()
            # 归属根：短剧 ai_videos 与教学/热点视频 edu_videos（RequestLog 两者都支持；suno-music skill 约定 edu_videos/<系列>/<知识点>/）
            owner_roots = [(REPO_ROOT / name).resolve() for name in ("ai_videos", "edu_videos")]
            if not any(target.is_relative_to(r) and target != r for r in owner_roots) or not target.is_dir():
                raise ServiceError("invalid_target", "target 须为仓库 ai_videos 下已有的剧/集/资产目录，或 edu_videos 下已有的系列/知识点目录", 422)
        try:
            validated = GenerationRequest.model_validate(asdict(request))
        except ValidationError as exc:
            raise ServiceError("invalid_options", str(exc), 422) from None
        assets = AssetClient(self.settings)
        for ref in validated.references:
            if ref.asset_id:
                asset = assets.get(ref.asset_id)
                if validated.mode == "advanced" and asset["kind"] != "audio":
                    raise ServiceError("reference_mode", "图片/视频参考使用 simple 模式", 422)
        payload = {**validated.model_dump(exclude_none=True), "target": str(target)}
        # Preserve the original v1 identity when callers do not request new options.
        if validated.mode == "advanced" and not validated.title and not validated.references and not validated.options.model_dump(exclude_none=True):
            payload = {k: getattr(request, k) for k in ("prompt", "format", "instrumental", "target", "lyrics")}
            payload["target"] = str(target)
        fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        now = datetime.now(timezone.utc).isoformat()
        payload.update(created_at=now, updated_at=now, files=[], song_urls=[], submitted=False, error=None)
        job = JobEntity(uuid.uuid4().hex, key, fingerprint, "queued", payload)
        if not self.writer.insert(JobMapper.dao(job)):
            old = self.reader.by_key(key)
            if old is None or old.fingerprint != fingerprint:
                raise ServiceError("idempotency_conflict", "同一幂等键已用于不同请求")
            return JobMapper.dto(old)
        return JobMapper.dto(JobMapper.dao(job))

    def cancel(self, job_id: str) -> JobQdto:
        dao = self.reader.get(job_id)
        if dao is None:
            raise ServiceError("not_found", "任务不存在", 404)
        job = JobMapper.entity(dao)
        job.cancel()
        self.writer.save(JobMapper.dao(job))
        return JobMapper.dto(JobMapper.dao(job))

    def resume(self, job_id: str, song_urls: list[str], recollect: bool = False) -> JobQdto:
        dao = self.reader.get(job_id)
        if dao is None:
            raise ServiceError("not_found", "任务不存在", 404)
        if len(song_urls) > 2 or len(song_urls) != len(set(song_urls)):
            raise ServiceError("invalid_songs", "一次最多两首不同歌曲", 422)
        for url in song_urls:
            if not re.fullmatch(r"https://suno\.com/song/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", url):
                raise ServiceError("invalid_song_url", "只接受 https://suno.com/song/<UUID> 歌曲地址", 422)
        job = JobMapper.entity(dao)
        job.resume([url.lower() for url in song_urls], recollect)
        self.writer.save(JobMapper.dao(job))
        return JobMapper.dto(JobMapper.dao(job))
