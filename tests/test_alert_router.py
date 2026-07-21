from datetime import UTC, datetime

import pytest

from tmb_ai_os.alert_delivery import (
    AlertDeliveryService,
    AlertMessage,
    DeliveryResult,
    DeliveryStatus,
)
from tmb_ai_os.alert_policy import AlertPolicy, AlertRoute, AlertSeverity
from tmb_ai_os.alert_router import AlertRouter


class ConfigurableChannel:
    def __init__(
        self,
        name: str,
        status: DeliveryStatus,
    ) -> None:
        self._name = name
        self._status = status
        self.calls = 0

    @property
    def name(self) -> str:
        return self._name

    def deliver(self, alert: AlertMessage) -> DeliveryResult:
        self.calls += 1
        return DeliveryResult(
            status=self._status,
            channel=self.name,
            attempted_at=datetime.now(UTC),
        )


def make_alert(severity: str = "critical") -> AlertMessage:
    return AlertMessage(
        alert_id="database-unavailable",
        title="Database unavailable",
        message="Database health check failed.",
        severity=severity,
        created_at=datetime.now(UTC),
    )


def make_policy(*channels: str) -> AlertPolicy:
    return AlertPolicy({AlertSeverity.CRITICAL: AlertRoute(channel_names=tuple(channels))})


def test_router_delivers_to_selected_channel() -> None:
    primary = ConfigurableChannel(
        "primary",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(primary,),
    )

    result = router.route(make_alert())

    assert result.successful is True
    assert primary.calls == 1
    assert result.deliveries[0].status is DeliveryStatus.SUCCESS


def test_router_uses_fallback_after_failure() -> None:
    primary = ConfigurableChannel(
        "primary",
        DeliveryStatus.FAILED,
    )
    fallback = ConfigurableChannel(
        "fallback",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary", "fallback"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(primary, fallback),
    )

    result = router.route(make_alert())

    assert result.successful is True
    assert primary.calls == 1
    assert fallback.calls == 1
    assert len(result.deliveries) == 2


def test_router_stops_after_first_success() -> None:
    primary = ConfigurableChannel(
        "primary",
        DeliveryStatus.SUCCESS,
    )
    fallback = ConfigurableChannel(
        "fallback",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary", "fallback"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(primary, fallback),
    )

    router.route(make_alert())

    assert primary.calls == 1
    assert fallback.calls == 0


def test_missing_channel_records_failed_delivery() -> None:
    router = AlertRouter(
        policy=make_policy("missing"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(),
    )

    result = router.route(make_alert())

    assert result.successful is False
    assert result.deliveries[0].status is DeliveryStatus.FAILED
    assert result.deliveries[0].attempts == 0


def test_route_with_no_channels_records_empty_result() -> None:
    router = AlertRouter(
        policy=AlertPolicy({}),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(),
    )

    result = router.route(make_alert("warning"))

    assert result.successful is False
    assert result.channels == ()
    assert result.deliveries == ()


def test_router_rejects_duplicate_channel_names() -> None:
    first = ConfigurableChannel("duplicate", DeliveryStatus.SUCCESS)
    second = ConfigurableChannel("duplicate", DeliveryStatus.SUCCESS)

    with pytest.raises(ValueError, match="unique"):
        AlertRouter(
            policy=make_policy("duplicate"),
            delivery_service=AlertDeliveryService(),
            channels=(first, second),
        )


def test_router_records_history() -> None:
    channel = ConfigurableChannel(
        "primary",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(channel,),
    )

    router.route(make_alert())

    assert len(router.history) == 1


def test_router_uses_environment_specific_route() -> None:
    from tmb_ai_os.alert_policy import DeploymentEnvironment

    general = ConfigurableChannel(
        "general",
        DeliveryStatus.SUCCESS,
    )
    production = ConfigurableChannel(
        "production",
        DeliveryStatus.SUCCESS,
    )
    policy = AlertPolicy(
        {AlertSeverity.CRITICAL: AlertRoute(channel_names=("general",))},
        environment_routes={
            DeploymentEnvironment.PRODUCTION: {
                AlertSeverity.CRITICAL: AlertRoute(channel_names=("production",))
            }
        },
    )
    router = AlertRouter(
        policy=policy,
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(general, production),
        environment=DeploymentEnvironment.PRODUCTION,
    )

    result = router.route(make_alert())

    assert result.successful is True
    assert result.channels == ("production",)
    assert production.calls == 1
    assert general.calls == 0


def test_router_records_observability_metrics() -> None:
    from tmb_ai_os.alert_observability import AlertObservability

    observability = AlertObservability()
    channel = ConfigurableChannel(
        "primary",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(channel,),
        observability=observability,
    )

    router.route(make_alert())

    snapshot = observability.snapshot()

    assert snapshot.routed_total == 1
    assert snapshot.delivery_success_total == 1
    assert snapshot.delivery_failed_total == 0


def test_router_records_fallback_metrics() -> None:
    from tmb_ai_os.alert_observability import AlertObservability

    observability = AlertObservability()
    primary = ConfigurableChannel(
        "primary",
        DeliveryStatus.FAILED,
    )
    fallback = ConfigurableChannel(
        "fallback",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary", "fallback"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(primary, fallback),
        observability=observability,
    )

    router.route(make_alert())

    snapshot = observability.snapshot()

    assert snapshot.routed_total == 1
    assert snapshot.delivery_failed_total == 1
    assert snapshot.delivery_success_total == 1
    assert snapshot.fallback_total == 1


def test_router_works_without_observability() -> None:
    channel = ConfigurableChannel(
        "primary",
        DeliveryStatus.SUCCESS,
    )
    router = AlertRouter(
        policy=make_policy("primary"),
        delivery_service=AlertDeliveryService(cooldown_seconds=0),
        channels=(channel,),
    )

    result = router.route(make_alert())

    assert result.successful is True
