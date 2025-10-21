from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta

import httpx

from ..config import DEFAULT_CACHE_SECONDS, MARKETFIYAT_BASE_URL
from ..models import SearchRequest, SearchResponse

CacheKey = tuple[str, int, int, float | None, float | None]


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
        """Initialize the HTTP client"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=MARKETFIYAT_BASE_URL,
                timeout=30.0,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )

    async def close(self) -> None:
        """Close the HTTP client"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def search_by_categories(self, request: SearchRequest) -> SearchResponse:
        """Search products by categories"""
        if self._client is None:
            await self.initialize()

        cache_key = self._build_cache_key(request)
        cached = await self._read_cache(cache_key)
        if cached is not None:
            return cached

        try:
            response = await self._client.post(
                "/api/v2/searchByCategories",
                json=request.model_dump(exclude_none=False),
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

    # Internal helpers -------------------------------------------------

    @staticmethod
    def _build_cache_key(request: SearchRequest) -> CacheKey:
        return (
            request.keywords.lower(),
            request.pages,
            request.size,
            request.latitude,
            request.longitude,
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
