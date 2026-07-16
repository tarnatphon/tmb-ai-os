from fastapi import APIRouter

from .config import get_settings
from .security_hardening import validate_security_config

router = APIRouter(prefix="/v11", tags=["Milestone 5.2"])


@router.get("/security/config")
def security_config() -> dict[str, object]:
    settings = get_settings()
    report = validate_security_config(settings)

    return {
        "secure": report.secure,
        "issues": list(report.issues),
        "rate_limit_requests": settings.rate_limit_requests,
        "rate_limit_window_seconds": (settings.rate_limit_window_seconds),
        "require_secure_api_key": (settings.require_secure_api_key),
    }


@router.get("/security/rate-limit")
def rate_limit_config() -> dict[str, int]:
    settings = get_settings()
    return {
        "requests": settings.rate_limit_requests,
        "window_seconds": settings.rate_limit_window_seconds,
    }
