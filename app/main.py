from __future__ import annotations

from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from .api import build_api_router
from .config import (
    ALLOWED_ORIGINS,
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    DEFAULT_CACHE_SECONDS,
)
from .mcp import configure_mcp
from .services import MarketfiyatService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await app.state.marketfiyat_service.initialize()
    yield
    # Shutdown
    await app.state.marketfiyat_service.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.marketfiyat_service = MarketfiyatService(DEFAULT_CACHE_SECONDS)

    app.include_router(build_api_router())

    configure_mcp(app)

    return app


app = create_app()
mcp = cast(FastMCP, app.state.mcp)


__all__ = ["app", "create_app", "mcp"]
