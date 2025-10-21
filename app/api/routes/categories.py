from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ...models import CategoriesResponse
from ...services import MarketfiyatService, MarketfiyatServiceError
from ..dependencies import get_marketfiyat_service

router = APIRouter()


@router.get(
    "/categories",
    response_model=CategoriesResponse,
    tags=["categories"],
)
async def get_categories(
    service: MarketfiyatService = Depends(get_marketfiyat_service),
) -> CategoriesResponse:
    """
    Get available product categories.

    This endpoint returns all available product categories and their subcategories
    from the Marketfiyati API.
    """
    try:
        return await service.get_categories()
    except MarketfiyatServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
