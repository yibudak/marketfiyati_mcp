from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

LifespanContext = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def merge_lifespans(
    existing: LifespanContext | None,
    extra: LifespanContext,
) -> LifespanContext:
    @asynccontextmanager
    async def _lifespan(application: FastAPI):
        if existing is not None:
            async with existing(application):
                async with extra(application):
                    yield
        else:
            async with extra(application):
                yield

    return _lifespan
