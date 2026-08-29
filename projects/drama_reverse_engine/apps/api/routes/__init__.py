from __future__ import annotations

from fastapi import APIRouter

from apps.api.routes import (
    artifact__route,
    drama__route,
    episode__route,
    export__route,
    health__route,
)

router = APIRouter()
router.include_router(health__route.router)
router.include_router(drama__route.router)
router.include_router(episode__route.router)
router.include_router(artifact__route.router)
router.include_router(export__route.router)

GUARDED_ROUTES: list[tuple[str, str]] = [
    ("POST", "/api/dramas"),
    ("POST", "/api/uploads"),
    ("POST", "/api/dramas/{drama_id}/upload"),
    ("POST", "/api/dramas/{drama_id}/export"),
    ("POST", "/api/episodes/step"),
    ("POST", "/api/episodes/run"),
    ("POST", "/api/episodes/rerun-stage"),
    ("POST", "/api/episodes/gate/release"),
    ("POST", "/api/episodes/edit-artifact"),
]
