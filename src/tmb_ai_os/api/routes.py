from __future__ import annotations

from fastapi import APIRouter, Request

from tmb_ai_os import __version__
from tmb_ai_os.api.schemas import HealthResponse, PluginResponse
from tmb_ai_os.core.config import get_settings
from tmb_ai_os.core.runtime import Runtime

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.environment,
        version=__version__,
    )


@router.get("/plugins", response_model=list[PluginResponse], tags=["plugins"])
def plugins(request: Request) -> list[PluginResponse]:
    runtime: Runtime = request.app.state.runtime
    return [
        PluginResponse(
            name=item.name,
            version=item.version,
            enabled=item.enabled,
            capabilities=list(item.capabilities),
        )
        for item in runtime.plugins.list_plugins()
    ]
