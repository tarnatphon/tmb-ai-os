from __future__ import annotations

import platform
import sys
import time
from datetime import UTC, datetime
from typing import Final

from typing_extensions import TypedDict

_PROCESS_STARTED_AT: Final[float] = time.monotonic()


class ProcessHealth(TypedDict):
    uptime_seconds: float
    python_version: str
    platform: str


class ApiHealth(TypedDict):
    readiness: bool


class ServiceHealth(TypedDict):
    application: str
    alert_metrics: str


class SystemHealth(TypedDict):
    status: str
    generated_at: str
    process: ProcessHealth
    api: ApiHealth
    services: ServiceHealth


def get_system_health() -> SystemHealth:
    """Return a dependency-free snapshot of application health."""
    uptime_seconds = max(0.0, time.monotonic() - _PROCESS_STARTED_AT)

    return {
        "status": "healthy",
        "generated_at": datetime.now(UTC).isoformat(),
        "process": {
            "uptime_seconds": round(uptime_seconds, 3),
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "api": {
            "readiness": True,
        },
        "services": {
            "application": "healthy",
            "alert_metrics": "healthy",
        },
    }
