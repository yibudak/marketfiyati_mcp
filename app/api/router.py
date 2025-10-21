from __future__ import annotations

from fastapi import APIRouter

from .routes import categories_router, health_router, search_router


def build_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health_router)
    router.include_router(search_router)
    router.include_router(categories_router)
    return router
