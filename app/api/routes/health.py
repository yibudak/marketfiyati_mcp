from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "service": "marketfiyat-mcp"}
