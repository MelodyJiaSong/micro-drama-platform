"""Routes package — per-aggregate route files combined into one APIRouter.

Per follow-up 062: the single 850-line `routes.py` was split into
`{aggregate}__route.py` files, one per aggregate. This `__init__.py`
exposes a combined `router` that `apps/api/app_factory.py` mounts on
the FastAPI app via `app.include_router(router)`. Each per-aggregate
file defines its own `APIRouter()`.

Follow-up 233 removed every route that only served the old 0–7 stage
pipeline (eval center, writers room, prompt editing, previz, frames/plates,
intro cards, production export, takes/concat/subtitles, seams, novels,
voices, actors/casting, performance library).
"""
from __future__ import annotations

from fastapi import APIRouter
from apps.api.routes.global_workflow__route import router as _global_workflow_router
from apps.api.routes.request_log__route import router as _request_log_router
from apps.api.routes.episode_workflow__route import router as _episode_workflow_router

from apps.api.routes.character__route import router as _character_router
from apps.api.routes.character_video__route import router as _character_video_router
from apps.api.routes.downloads__route import router as _downloads_router
from apps.api.routes.health__route import router as _health_router
from apps.api.routes.file__route import router as _file_router
from apps.api.routes.media__route import router as _media_router
from apps.api.routes.research__route import router as _research_router
from apps.api.routes.tree__route import router as _tree_router

router = APIRouter()
router.include_router(_global_workflow_router)
router.include_router(_episode_workflow_router)
router.include_router(_request_log_router)
router.include_router(_tree_router)
router.include_router(_file_router)
router.include_router(_media_router)
router.include_router(_downloads_router)
router.include_router(_health_router)
router.include_router(_character_router)
router.include_router(_character_video_router)
router.include_router(_research_router)
