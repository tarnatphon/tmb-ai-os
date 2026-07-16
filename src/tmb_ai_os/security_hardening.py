from dataclasses import dataclass

from .config import Settings


@dataclass(frozen=True)
class SecurityConfigReport:
    secure: bool
    issues: tuple[str, ...]


def validate_security_config(
    settings: Settings,
) -> SecurityConfigReport:
    issues: list[str] = []

    if settings.require_secure_api_key:
        if settings.api_key == "change-me":
            issues.append("TMB_API_KEY must not use the default value")
        if len(settings.api_key) < 32:
            issues.append("TMB_API_KEY must be at least 32 characters")

    if settings.rate_limit_requests < 1:
        issues.append("TMB_RATE_LIMIT_REQUESTS must be at least 1")

    if settings.rate_limit_window_seconds < 1:
        issues.append("TMB_RATE_LIMIT_WINDOW_SECONDS must be at least 1")

    return SecurityConfigReport(
        secure=not issues,
        issues=tuple(issues),
    )
