from datetime import UTC, datetime

from tmb_ai_os.alert_delivery import DeliveryResult, DeliveryStatus
from tmb_ai_os.alert_observability import AlertObservability
from tmb_ai_os.alert_router import RoutingResult


def make_delivery(
    status: DeliveryStatus,
    channel: str = "webhook",
) -> DeliveryResult:
    return DeliveryResult(
        status=status,
        channel=channel,
        attempted_at=datetime.now(UTC),
    )


def make_routing_result(
    *,
    channels: tuple[str, ...] = ("webhook",),
    deliveries: tuple[DeliveryResult, ...] = (),
) -> RoutingResult:
    return RoutingResult(
        alert_id="system-alert",
        channels=channels,
        deliveries=deliveries,
        routed_at=datetime.now(UTC),
    )


def test_records_successful_delivery() -> None:
    observability = AlertObservability()

    observability.record(make_routing_result(deliveries=(make_delivery(DeliveryStatus.SUCCESS),)))

    snapshot = observability.snapshot()

    assert snapshot.routed_total == 1
    assert snapshot.delivery_success_total == 1
    assert snapshot.delivery_failed_total == 0


def test_records_failed_and_successful_fallback() -> None:
    observability = AlertObservability()

    observability.record(
        make_routing_result(
            channels=("primary", "fallback"),
            deliveries=(
                make_delivery(DeliveryStatus.FAILED, "primary"),
                make_delivery(DeliveryStatus.SUCCESS, "fallback"),
            ),
        )
    )

    snapshot = observability.snapshot()

    assert snapshot.routed_total == 1
    assert snapshot.delivery_failed_total == 1
    assert snapshot.delivery_success_total == 1
    assert snapshot.fallback_total == 1


def test_records_suppressed_delivery() -> None:
    observability = AlertObservability()

    observability.record(
        make_routing_result(deliveries=(make_delivery(DeliveryStatus.SUPPRESSED),))
    )

    snapshot = observability.snapshot()

    assert snapshot.delivery_suppressed_total == 1


def test_records_route_without_channels() -> None:
    observability = AlertObservability()

    observability.record(
        make_routing_result(
            channels=(),
            deliveries=(),
        )
    )

    snapshot = observability.snapshot()

    assert snapshot.routed_total == 1
    assert snapshot.no_route_total == 1


def test_snapshot_is_immutable_copy() -> None:
    observability = AlertObservability()

    first = observability.snapshot()

    observability.record(make_routing_result(deliveries=(make_delivery(DeliveryStatus.SUCCESS),)))

    second = observability.snapshot()

    assert first.routed_total == 0
    assert second.routed_total == 1


def test_reset_clears_all_metrics() -> None:
    observability = AlertObservability()

    observability.record(
        make_routing_result(
            channels=("primary", "fallback"),
            deliveries=(
                make_delivery(DeliveryStatus.FAILED, "primary"),
                make_delivery(DeliveryStatus.SUCCESS, "fallback"),
            ),
        )
    )

    observability.reset()
    snapshot = observability.snapshot()

    assert snapshot.routed_total == 0
    assert snapshot.delivery_success_total == 0
    assert snapshot.delivery_failed_total == 0
    assert snapshot.delivery_suppressed_total == 0
    assert snapshot.fallback_total == 0
    assert snapshot.no_route_total == 0
