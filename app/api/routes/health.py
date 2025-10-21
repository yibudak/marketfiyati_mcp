from __future__ import annotations

from fastapi import APIRouter

from ...config import API_VERSION

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "marketfiyat-mcp", "version": API_VERSION}


@router.get("/version", tags=["health"])
async def get_version() -> dict:
    """Get API version"""
    return {"version": API_VERSION}
