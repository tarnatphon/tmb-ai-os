from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import initialize_database
from .scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def application_lifespan(
    _: FastAPI,
) -> AsyncIterator[None]:
    initialize_database()
    start_scheduler()
    yield
    stop_scheduler(wait=False)
