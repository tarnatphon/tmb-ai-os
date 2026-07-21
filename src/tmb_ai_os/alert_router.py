"""Policy-driven alert routing."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from tmb_ai_os.alert_delivery import (
    AlertChannel,
    AlertDeliveryService,
    AlertMessage,
    DeliveryResult,
    DeliveryStatus,
)
from tmb_ai_os.alert_observability import AlertObservability
from tmb_ai_os.alert_policy import (
    AlertPolicy,
    DeploymentEnvironment,
)


@dataclass(frozen=True, slots=True)
class RoutingResult:
    alert_id: str
    channels: tuple[str, ...]
    deliveries: tuple[DeliveryResult, ...]
    routed_at: datetime

    @property
    def successful(self) -> bool:
        return any(result.status is DeliveryStatus.SUCCESS for result in self.deliveries)


class AlertRouter:
    """Route alerts through channels selected by an alert policy."""

    def __init__(
        self,
        *,
        policy: AlertPolicy,
        delivery_service: AlertDeliveryService,
        channels: Iterable[AlertChannel],
        environment: DeploymentEnvironment | str | None = None,
        observability: AlertObservability | None = None,
    ) -> None:
        channel_list = tuple(channels)

        self._policy = policy
        self._delivery_service = delivery_service
        self._environment = environment
        self._observability = observability
        self._channels = {channel.name: channel for channel in channel_list}
        self._history: list[RoutingResult] = []

        if len(self._channels) != len(channel_list):
            raise ValueError("channel names must be unique")

    @property
    def history(self) -> tuple[RoutingResult, ...]:
        return tuple(self._history)

    def route(self, alert: AlertMessage) -> RoutingResult:
        route = self._policy.resolve(
            alert,
            environment=self._environment,
        )
        deliveries: list[DeliveryResult] = []

        for channel_name in route.channel_names:
            channel = self._channels.get(channel_name)

            if channel is None:
                deliveries.append(
                    DeliveryResult(
                        status=DeliveryStatus.FAILED,
                        channel=channel_name,
                        attempted_at=datetime.now(UTC),
                        detail="Configured alert channel is unavailable.",
                        attempts=0,
                    )
                )
                continue

            result = self._delivery_service.deliver(alert, channel)
            deliveries.append(result)

            if result.status is DeliveryStatus.SUCCESS:
                break

        routing_result = RoutingResult(
            alert_id=alert.alert_id,
            channels=route.channel_names,
            deliveries=tuple(deliveries),
            routed_at=datetime.now(UTC),
        )
        self._history.append(routing_result)

        if self._observability is not None:
            self._observability.record(routing_result)

        return routing_result
