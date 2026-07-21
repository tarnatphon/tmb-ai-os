"""Alert routing policy definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from tmb_ai_os.alert_delivery import AlertMessage


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class AlertRoute:
    channel_names: tuple[str, ...]
    enabled: bool = True


class AlertPolicy:
    """Resolve delivery routes from alert severity."""

    def __init__(
        self,
        routes: dict[AlertSeverity, AlertRoute],
        *,
        default_route: AlertRoute | None = None,
    ) -> None:
        self._routes = dict(routes)
        self._default_route = default_route or AlertRoute(channel_names=())

    def resolve(self, alert: AlertMessage) -> AlertRoute:
        try:
            severity = AlertSeverity(alert.severity.lower())
        except ValueError:
            return self._default_route

        route = self._routes.get(severity, self._default_route)

        if not route.enabled:
            return AlertRoute(channel_names=(), enabled=False)

        return route
