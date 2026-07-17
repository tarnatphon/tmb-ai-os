from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from .scheduler import get_scheduler_state


@dataclass(frozen=True)
class HealthCheck:
    name: str
    healthy: bool
    detail: str


@dataclass(frozen=True)
class ReadinessReport:
    ready: bool
    checks: tuple[HealthCheck, ...]


def check_database(session: Session) -> HealthCheck:
    try:
        session.execute(text("select 1"))
    except Exception as exc:
        return HealthCheck(
            name="database",
            healthy=False,
            detail=str(exc),
        )

    return HealthCheck(
        name="database",
        healthy=True,
        detail="Database connection is available",
    )


def check_scheduler() -> HealthCheck:
    state = get_scheduler_state()

    if not state.enabled:
        return HealthCheck(
            name="scheduler",
            healthy=True,
            detail="Scheduler is disabled by configuration",
        )

    return HealthCheck(
        name="scheduler",
        healthy=state.running,
        detail=(
            "Scheduler is running" if state.running else "Scheduler is enabled but not running"
        ),
    )


def build_readiness_report(
    session: Session,
) -> ReadinessReport:
    checks = (
        check_database(session),
        check_scheduler(),
    )
    return ReadinessReport(
        ready=all(check.healthy for check in checks),
        checks=checks,
    )


def public_health_report(
    *,
    service: str,
    version: str,
) -> dict[str, str]:
    """Return public, non-sensitive application health metadata."""
    return {
        "status": "ok",
        "service": service,
        "version": version,
    }
