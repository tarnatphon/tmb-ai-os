from dataclasses import dataclass

from .config import Settings
from .security_hardening import validate_security_config


@dataclass(frozen=True)
class DeploymentCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class DeploymentReport:
    ready: bool
    checks: tuple[DeploymentCheck, ...]


def validate_deployment(
    settings: Settings,
) -> DeploymentReport:
    security = validate_security_config(settings)

    checks = [
        DeploymentCheck(
            name="environment",
            passed=settings.env == "production",
            detail=f"env={settings.env}",
        ),
        DeploymentCheck(
            name="security",
            passed=security.secure,
            detail=(
                "Security configuration is valid" if security.secure else "; ".join(security.issues)
            ),
        ),
        DeploymentCheck(
            name="database",
            passed=bool(settings.database_url.strip()),
            detail=settings.database_url,
        ),
        DeploymentCheck(
            name="provider",
            passed=bool(settings.ai_provider.strip()),
            detail=settings.ai_provider,
        ),
    ]

    return DeploymentReport(
        ready=all(check.passed for check in checks),
        checks=tuple(checks),
    )
