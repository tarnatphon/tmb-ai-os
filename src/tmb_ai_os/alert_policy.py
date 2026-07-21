"""Alert routing policy definitions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

from tmb_ai_os.alert_delivery import AlertMessage


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DeploymentEnvironment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class AlertRoute:
    channel_names: tuple[str, ...]
    enabled: bool = True

    def __post_init__(self) -> None:
        normalized_names = tuple(
            channel_name.strip() for channel_name in self.channel_names if channel_name.strip()
        )

        if len(normalized_names) != len(set(normalized_names)):
            raise ValueError("channel_names must be unique")

        object.__setattr__(self, "channel_names", normalized_names)


class AlertPolicy:
    """Resolve delivery routes by severity and deployment environment."""

    def __init__(
        self,
        routes: Mapping[AlertSeverity, AlertRoute],
        *,
        environment_routes: Mapping[
            DeploymentEnvironment,
            Mapping[AlertSeverity, AlertRoute],
        ]
        | None = None,
        default_route: AlertRoute | None = None,
    ) -> None:
        self._routes = MappingProxyType(dict(routes))
        self._environment_routes = MappingProxyType(
            {
                environment: MappingProxyType(dict(severity_routes))
                for environment, severity_routes in (environment_routes or {}).items()
            }
        )
        self._default_route = default_route or AlertRoute(channel_names=())

    def resolve(
        self,
        alert: AlertMessage,
        *,
        environment: DeploymentEnvironment | str | None = None,
    ) -> AlertRoute:
        severity = self._parse_severity(alert.severity)

        if severity is None:
            return self._default_route

        parsed_environment = self._parse_environment(environment)

        if parsed_environment is not None:
            severity_routes = self._environment_routes.get(parsed_environment)

            if severity_routes is not None:
                environment_route = severity_routes.get(severity)

                if environment_route is not None:
                    return self._normalize_route(environment_route)

        route = self._routes.get(severity, self._default_route)
        return self._normalize_route(route)

    @staticmethod
    def _parse_severity(value: str) -> AlertSeverity | None:
        try:
            return AlertSeverity(value.strip().lower())
        except ValueError:
            return None

    @staticmethod
    def _parse_environment(
        value: DeploymentEnvironment | str | None,
    ) -> DeploymentEnvironment | None:
        if value is None:
            return None

        if isinstance(value, DeploymentEnvironment):
            return value

        try:
            return DeploymentEnvironment(value.strip().lower())
        except ValueError as exc:
            raise ValueError(f"Unsupported deployment environment: {value}") from exc

    @staticmethod
    def _normalize_route(route: AlertRoute) -> AlertRoute:
        if route.enabled:
            return route

        return AlertRoute(channel_names=(), enabled=False)
