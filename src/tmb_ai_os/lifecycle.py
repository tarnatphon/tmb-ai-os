import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from .database import initialize_database
from .scheduler import start_scheduler, stop_scheduler
from .startup_diagnostics import (
    build_startup_diagnostics,
    log_startup_diagnostics,
)


@asynccontextmanager
async def application_lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    initialize_database()
    start_scheduler()
    content_directory = Path(os.getenv("TMB_CONTENT_DIR", "content"))
    output_directory = Path(os.getenv("TMB_OUTPUT_DIR", "output"))

    startup_report = build_startup_diagnostics(
        service="tmb-ai-os",
        version=app.version,
        content_directory=content_directory,
        output_directory=output_directory,
    )
    app.state.startup_diagnostics = startup_report
    log_startup_diagnostics(startup_report)

    yield
    stop_scheduler(wait=False)
