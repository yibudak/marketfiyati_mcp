from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from ...models import SearchRequest, SearchResponse
from ...services import MarketfiyatService, MarketfiyatServiceError
from ..dependencies import get_marketfiyat_service

router = APIRouter()


@router.post(
    "/search_by_categories",
    response_model=SearchResponse,
    tags=["search"],
)
async def search_by_categories(
    request: SearchRequest,
    service: MarketfiyatService = Depends(get_marketfiyat_service),
) -> SearchResponse:
    """
    Search for products by categories and keywords.

    This endpoint allows you to search for products available in Turkish markets
    based on categories, keywords, location, and other filters.
    """
    try:
        return await service.search_by_categories(request)
    except MarketfiyatServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.get(
    "/search_by_categories",
    response_model=SearchResponse,
    tags=["search"],
)
async def search_by_categories_get(
    keywords: Annotated[str, Query(description="Search keywords or category name")],
    latitude: Annotated[float, Query(description="User latitude coordinate")],
    longitude: Annotated[float, Query(description="User longitude coordinate")],
    pages: Annotated[int, Query(ge=0, description="Page number for pagination")] = 0,
    size: Annotated[
        int, Query(ge=1, le=100, description="Number of results per page")
    ] = 24,
    menuCategory: Annotated[
        bool, Query(description="Search in menu categories")
    ] = True,
    distance: Annotated[
        int | None, Query(description="Search radius in kilometers")
    ] = 5,
    depots: Annotated[
        list[str] | None, Query(description="List of depot IDs to search in")
    ] = None,
    service: MarketfiyatService = Depends(get_marketfiyat_service),
) -> SearchResponse:
    """
    Search for products by categories and keywords (GET method).

    This endpoint requires location coordinates to search for products
    in nearby markets.
    """
    request = SearchRequest(
        keywords=keywords,
        pages=pages,
        size=size,
        menuCategory=menuCategory,
        latitude=latitude,
        longitude=longitude,
        distance=distance,
        depots=depots,
    )

    try:
        return await service.search_by_categories(request)
    except MarketfiyatServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
