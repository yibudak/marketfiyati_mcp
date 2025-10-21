from __future__ import annotations

from fastapi import Request

from ..services import MarketfiyatService


def get_marketfiyat_service(request: Request) -> MarketfiyatService:
    """Dependency to get the MarketfiyatService from app state"""
    return request.app.state.marketfiyat_service
