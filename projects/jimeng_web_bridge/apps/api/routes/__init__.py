from fastapi import APIRouter

from apps.api.routes.drama_config__route import router as drama_config_router
from apps.api.routes.entity__route import router as entity_router
from apps.api.routes.global_config__route import router as global_config_router
from apps.api.routes.media__route import router as media_router
from apps.api.routes.session__route import router as session_router

router = APIRouter()
for sub_router in (session_router, drama_config_router, global_config_router, entity_router, media_router):
    router.include_router(sub_router)
