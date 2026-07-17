from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    healthy: bool
    detail: str


@dataclass(frozen=True)
class StartupDiagnostics:
    service: str
    version: str
    ready: bool
    checks: tuple[DiagnosticCheck, ...]


def check_directory(
    *,
    name: str,
    path: Path,
    create_if_missing: bool = False,
) -> DiagnosticCheck:
    """Check whether an application directory is usable."""
    try:
        if create_if_missing:
            path.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            return DiagnosticCheck(
                name=name,
                healthy=False,
                detail=f"Directory does not exist: {path}",
            )

        if not path.is_dir():
            return DiagnosticCheck(
                name=name,
                healthy=False,
                detail=f"Path is not a directory: {path}",
            )

        return DiagnosticCheck(
            name=name,
            healthy=True,
            detail=f"Directory is available: {path}",
        )
    except OSError as exc:
        return DiagnosticCheck(
            name=name,
            healthy=False,
            detail=f"Directory check failed: {exc}",
        )


def build_startup_diagnostics(
    *,
    service: str,
    version: str,
    content_directory: Path,
    output_directory: Path,
) -> StartupDiagnostics:
    """Build a non-sensitive startup diagnostic report."""
    checks = (
        check_directory(
            name="content_directory",
            path=content_directory,
        ),
        check_directory(
            name="output_directory",
            path=output_directory,
            create_if_missing=True,
        ),
    )

    return StartupDiagnostics(
        service=service,
        version=version,
        ready=all(check.healthy for check in checks),
        checks=checks,
    )


def log_startup_diagnostics(report: StartupDiagnostics) -> None:
    """Log startup diagnostics without exposing secrets."""
    logger.info(
        "Startup diagnostics: service=%s version=%s ready=%s",
        report.service,
        report.version,
        report.ready,
    )

    for check in report.checks:
        log_method = logger.info if check.healthy else logger.error
        log_method(
            "Startup check: name=%s healthy=%s detail=%s",
            check.name,
            check.healthy,
            check.detail,
        )


def startup_diagnostics_dict(
    report: StartupDiagnostics,
) -> dict[str, object]:
    """Convert startup diagnostics to a serializable dictionary."""
    return asdict(report)
