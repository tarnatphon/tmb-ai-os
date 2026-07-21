"""Alert routing observability and metrics aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from tmb_ai_os.alert_delivery import DeliveryStatus
from tmb_ai_os.alert_router import RoutingResult


@dataclass(frozen=True, slots=True)
class AlertMetricsSnapshot:
    routed_total: int
    delivery_success_total: int
    delivery_failed_total: int
    delivery_suppressed_total: int
    fallback_total: int
    no_route_total: int


class AlertObservability:
    """Collect in-memory metrics for alert routing activity."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._routed_total = 0
        self._delivery_success_total = 0
        self._delivery_failed_total = 0
        self._delivery_suppressed_total = 0
        self._fallback_total = 0
        self._no_route_total = 0

    def record(self, result: RoutingResult) -> None:
        with self._lock:
            self._routed_total += 1

            if not result.channels:
                self._no_route_total += 1

            for delivery in result.deliveries:
                if delivery.status is DeliveryStatus.SUCCESS:
                    self._delivery_success_total += 1
                elif delivery.status is DeliveryStatus.FAILED:
                    self._delivery_failed_total += 1
                elif delivery.status is DeliveryStatus.SUPPRESSED:
                    self._delivery_suppressed_total += 1

            if len(result.deliveries) > 1:
                self._fallback_total += 1

    def snapshot(self) -> AlertMetricsSnapshot:
        with self._lock:
            return AlertMetricsSnapshot(
                routed_total=self._routed_total,
                delivery_success_total=self._delivery_success_total,
                delivery_failed_total=self._delivery_failed_total,
                delivery_suppressed_total=self._delivery_suppressed_total,
                fallback_total=self._fallback_total,
                no_route_total=self._no_route_total,
            )

    def reset(self) -> None:
        with self._lock:
            self._routed_total = 0
            self._delivery_success_total = 0
            self._delivery_failed_total = 0
            self._delivery_suppressed_total = 0
            self._fallback_total = 0
            self._no_route_total = 0
