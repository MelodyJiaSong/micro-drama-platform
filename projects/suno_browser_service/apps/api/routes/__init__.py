from fastapi import APIRouter

from projects.suno_browser_service.apps.api.routes.job__route import router as jobs

router = APIRouter()
router.include_router(jobs)
