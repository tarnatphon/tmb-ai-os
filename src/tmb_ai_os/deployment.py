from dataclasses import dataclass

from .config import Settings
from .security_hardening import validate_security_config

SUPPORTED_AI_PROVIDERS = frozenset({"gemini"})
SUPPORTED_DATABASE_SCHEMES = (
    "sqlite:///",
    "postgresql://",
    "postgresql+psycopg://",
    "postgresql+psycopg2://",
)


@dataclass(frozen=True)
class DeploymentCheck:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class DeploymentReport:
    ready: bool
    checks: tuple[DeploymentCheck, ...]


def _validate_database_url(database_url: str) -> DeploymentCheck:
    normalized_url = database_url.strip().lower()

    if not normalized_url:
        return DeploymentCheck(
            name="database",
            passed=False,
            detail="Database URL is required",
        )

    if not normalized_url.startswith(SUPPORTED_DATABASE_SCHEMES):
        return DeploymentCheck(
            name="database",
            passed=False,
            detail="Unsupported database URL scheme",
        )

    if normalized_url == "sqlite:///:memory:":
        return DeploymentCheck(
            name="database",
            passed=False,
            detail="In-memory SQLite is not allowed in production",
        )

    return DeploymentCheck(
        name="database",
        passed=True,
        detail="Database configuration is supported",
    )


def _validate_provider(settings: Settings) -> DeploymentCheck:
    provider = settings.ai_provider.strip().lower()

    if provider not in SUPPORTED_AI_PROVIDERS:
        return DeploymentCheck(
            name="provider",
            passed=False,
            detail=f"Unsupported AI provider: {provider or '<empty>'}",
        )

    if provider == "gemini" and not settings.gemini_api_key.strip():
        return DeploymentCheck(
            name="provider",
            passed=False,
            detail="Gemini API key is required",
        )

    return DeploymentCheck(
        name="provider",
        passed=True,
        detail=f"AI provider is configured: {provider}",
    )


def validate_deployment(settings: Settings) -> DeploymentReport:
    security = validate_security_config(settings)

    checks = (
        DeploymentCheck(
            name="environment",
            passed=settings.env.strip().lower() == "production",
            detail=f"env={settings.env}",
        ),
        DeploymentCheck(
            name="security",
            passed=security.secure,
            detail=(
                "Security configuration is valid" if security.secure else "; ".join(security.issues)
            ),
        ),
        _validate_database_url(settings.database_url),
        _validate_provider(settings),
    )

    return DeploymentReport(
        ready=all(check.passed for check in checks),
        checks=checks,
    )
