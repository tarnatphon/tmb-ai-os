from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


@dataclass(frozen=True)
class Alert:
    code: str
    title: str
    detail: str
    severity: AlertSeverity
    occurred_at: datetime


def make_alert(
    *,
    code: str,
    title: str,
    detail: str,
    severity: AlertSeverity,
) -> Alert:
    return Alert(
        code=code,
        title=title,
        detail=detail,
        severity=severity,
        occurred_at=datetime.now(UTC),
    )
