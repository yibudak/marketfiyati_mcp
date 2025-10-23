from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta

import httpx
from httpx_socks import AsyncProxyTransport

from ..config import DEFAULT_CACHE_SECONDS, MARKETFIYAT_BASE_URL, SOCKS_PROXY
from ..models import (
    CategoriesResponse,
    NearestDepot,
    NearestDepotRequest,
    SearchByCategoryRequest,
    SearchRequest,
    SearchResponse,
)

CacheKey = tuple[str, int, int, float, float, int]


@dataclass
class CacheEntry:
    response: SearchResponse
    expires_at: datetime


class MarketfiyatServiceError(Exception):
    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


class MarketfiyatService:
    def __init__(self, cache_seconds: int = DEFAULT_CACHE_SECONDS) -> None:
        self._cache_seconds = max(cache_seconds, 0)
        self._cache: dict[CacheKey, CacheEntry] = {}
        self._cache_lock = asyncio.Lock()
        self._client: httpx.AsyncClient | None = None

    async def initialize(self) -> None:
        """Initialize the HTTP client with optional SOCKS proxy support"""
        if self._client is None:
            client_kwargs = {
                "base_url": MARKETFIYAT_BASE_URL,
                "timeout": 30.0,
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            }

            # Configure SOCKS proxy if SOCKS_PROXY environment variable is set
            if SOCKS_PROXY:
                transport = AsyncProxyTransport.from_url(SOCKS_PROXY)
                client_kwargs["transport"] = transport

            self._client = httpx.AsyncClient(**client_kwargs)

    async def close(self) -> None:
        """Close the HTTP client"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get_nearest_depots(
        self, latitude: float, longitude: float, distance: int = 1
    ) -> list[NearestDepot]:
        """Get nearest depots within the specified distance"""
        if self._client is None:
            await self.initialize()

        try:
            nearest_request = NearestDepotRequest(
                latitude=latitude, longitude=longitude, distance=distance
            )
            response = await self._client.post(
                "/api/v2/nearest",
                json=nearest_request.model_dump(),
            )
            response.raise_for_status()
            data = response.json()
            return [NearestDepot(**depot) for depot in data]

        except httpx.HTTPStatusError as exc:
            raise MarketfiyatServiceError(
                "Nearest depots API request failed "
                f"with status {exc.response.status_code}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise MarketfiyatServiceError(
                f"Failed to connect to Marketfiyat API: {str(exc)}"
            ) from exc
        except Exception as exc:
            raise MarketfiyatServiceError(f"Unexpected error: {str(exc)}") from exc

    async def search(self, request: SearchRequest) -> SearchResponse:
        """
        Search products using a two-step process (without menuCategory):
        1. Get nearest depots based on location and distance
        2. Search products in those depots
        """
        if self._client is None:
            await self.initialize()

        cache_key = self._build_cache_key(request)
        cached = await self._read_cache(cache_key)
        if cached is not None:
            return cached

        try:
            # Step 1: Get nearest depots based on location and distance
            nearest_depots = await self.get_nearest_depots(
                latitude=request.latitude,
                longitude=request.longitude,
                distance=request.distance,
            )
            # Extract depot IDs from nearest depots
            depot_ids = [depot.id for depot in nearest_depots]

            # Step 2: Search products using the depot IDs
            search_payload = {
                "keywords": request.keywords,
                "pages": request.pages,
                "size": request.size,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "distance": request.distance,
                "depots": depot_ids,
            }

            response = await self._client.post(
                "/api/v2/search",
                json=search_payload,
            )
            response.raise_for_status()
            data = response.json()
            search_response = SearchResponse(**data)

            await self._write_cache(cache_key, search_response)
            return search_response

        except httpx.HTTPStatusError as exc:
            raise MarketfiyatServiceError(
                f"API request failed with status {exc.response.status_code}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise MarketfiyatServiceError(
                f"Failed to connect to Marketfiyat API: {str(exc)}"
            ) from exc
        except Exception as exc:
            raise MarketfiyatServiceError(f"Unexpected error: {str(exc)}") from exc

    async def search_by_categories(
        self, request: SearchByCategoryRequest
    ) -> SearchResponse:
        """
        Search products by categories using a two-step process (with menuCategory):
        1. Get nearest depots based on location and distance
        2. Search products in those depots
        """
        if self._client is None:
            await self.initialize()

        cache_key = self._build_cache_key_with_menu(request)
        cached = await self._read_cache(cache_key)
        if cached is not None:
            return cached

        try:
            # Step 1: Get nearest depots based on location and distance
            nearest_depots = await self.get_nearest_depots(
                latitude=request.latitude,
                longitude=request.longitude,
                distance=request.distance,
            )
            # Extract depot IDs from nearest depots
            depot_ids = [depot.id for depot in nearest_depots]

            # Step 2: Search products using the depot IDs
            search_payload = {
                "keywords": request.keywords,
                "pages": request.pages,
                "size": request.size,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "distance": request.distance,
                "depots": depot_ids,
                "menuCategory": request.menuCategory,
            }

            response = await self._client.post(
                "/api/v2/search",
                json=search_payload,
            )
            response.raise_for_status()
            data = response.json()
            search_response = SearchResponse(**data)

            await self._write_cache(cache_key, search_response)
            return search_response

        except httpx.HTTPStatusError as exc:
            raise MarketfiyatServiceError(
                f"API request failed with status {exc.response.status_code}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise MarketfiyatServiceError(
                f"Failed to connect to Marketfiyat API: {str(exc)}"
            ) from exc
        except Exception as exc:
            raise MarketfiyatServiceError(f"Unexpected error: {str(exc)}") from exc

    async def get_categories(self) -> CategoriesResponse:
        """Get available product categories"""
        if self._client is None:
            await self.initialize()

        try:
            response = await self._client.get("/api/v1/info/categories")
            response.raise_for_status()
            data = response.json()
            return CategoriesResponse(**data)

        except httpx.HTTPStatusError as exc:
            raise MarketfiyatServiceError(
                f"Categories API request failed with status {exc.response.status_code}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.RequestError as exc:
            raise MarketfiyatServiceError(
                f"Failed to connect to Marketfiyat API: {str(exc)}"
            ) from exc
        except Exception as exc:
            raise MarketfiyatServiceError(f"Unexpected error: {str(exc)}") from exc

    # Internal helpers -------------------------------------------------

    @staticmethod
    def _build_cache_key(request: SearchRequest) -> CacheKey:
        return (
            request.keywords.lower(),
            request.pages,
            request.size,
            request.latitude,
            request.longitude,
            request.distance,
        )

    @staticmethod
    def _build_cache_key_with_menu(request: SearchByCategoryRequest) -> CacheKey:
        # For category search, we append menuCategory as part of the cache key
        # We convert bool to int (0 or 1) to fit the tuple structure
        return (
            f"{request.keywords.lower()}_{int(request.menuCategory)}",
            request.pages,
            request.size,
            request.latitude,
            request.longitude,
            request.distance,
        )

    async def _read_cache(self, cache_key: CacheKey) -> SearchResponse | None:
        if self._cache_seconds <= 0:
            return None

        async with self._cache_lock:
            entry = self._cache.get(cache_key)
            if entry and entry.expires_at > datetime.utcnow():
                return entry.response
        return None

    async def _write_cache(self, cache_key: CacheKey, response: SearchResponse) -> None:
        if self._cache_seconds <= 0:
            return

        async with self._cache_lock:
            self._cache[cache_key] = CacheEntry(
                response=response,
                expires_at=datetime.utcnow() + timedelta(seconds=self._cache_seconds),
            )
