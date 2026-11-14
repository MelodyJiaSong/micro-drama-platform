from projects.suno_browser_service.libs.application.dtos.job__dto import JobQdto
from projects.suno_browser_service.libs.domain.entities.job__entity import JobEntity
from projects.suno_browser_service.libs.infrastructure.daos.job__dao import JobDao


class JobMapper:
    @staticmethod
    def entity(dao: JobDao) -> JobEntity:
        return JobEntity(dao.id, dao.key, dao.fingerprint, dao.status, dao.payload, dao.version)

    @staticmethod
    def dao(entity: JobEntity) -> JobDao:
        return JobDao(entity.id, entity.key, entity.fingerprint, entity.status, entity.payload, entity.version)

    @staticmethod
    def dto(dao: JobDao) -> JobQdto:
        p = dao.payload
        return JobQdto(dao.id, dao.status, p["prompt"], p["format"], p["instrumental"],
                       p.get("song_urls", []), p.get("files", []), p.get("error"), p["created_at"], p["updated_at"],
                       {k: p[k] for k in ("prompt", "format", "instrumental", "lyrics", "mode", "title", "options", "references") if k in p},
                       {"completed": "download_files", "cancelled": "none_cancelled_before_submit", "uncertain": "verify_in_suno_then_resume_with_song_urls",
                        "needs_login": "manual_login_then_resume", "needs_attention": "read_error_before_resume"}.get(dao.status, p.get("human_action") or "poll_same_job_do_not_resubmit"),
                       p.get("applied_options", {}))
