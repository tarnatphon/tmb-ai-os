from dataclasses import asdict

from fastapi import APIRouter

from .config import get_settings
from .deployment import validate_deployment

router = APIRouter(prefix="/v12", tags=["Milestone 5.3"])


@router.get("/deployment/status")
def deployment_status() -> dict[str, object]:
    settings = get_settings()
    report = validate_deployment(settings)

    return {
        "ready": report.ready,
        "checks": [asdict(check) for check in report.checks],
    }


@router.get("/deployment/config")
def deployment_config() -> dict[str, object]:
    settings = get_settings()

    return {
        "env": settings.env,
        "database_url_configured": bool(settings.database_url),
        "provider": settings.ai_provider,
        "scheduler_enabled": settings.scheduler_enabled,
        "secure_api_key_required": settings.require_secure_api_key,
        "rate_limit_requests": settings.rate_limit_requests,
        "rate_limit_window_seconds": settings.rate_limit_window_seconds,
    }
