"""Production alert delivery services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol


class DeliveryStatus(StrEnum):
    """Result of an alert delivery attempt."""

    SUCCESS = "success"
    FAILED = "failed"
    SUPPRESSED = "suppressed"


@dataclass(frozen=True, slots=True)
class AlertMessage:
    """Alert payload delivered to an external channel."""

    alert_id: str
    title: str
    message: str
    severity: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    """Result returned by an alert delivery channel."""

    status: DeliveryStatus
    channel: str
    attempted_at: datetime
    detail: str | None = None


class AlertChannel(Protocol):
    """Contract implemented by alert-delivery channels."""

    @property
    def name(self) -> str:
        """Return the channel name."""

    def deliver(self, alert: AlertMessage) -> DeliveryResult:
        """Deliver an alert and return its result."""


class AlertDeliveryService:
    """Coordinates delivery of production alerts."""

    def deliver(
        self,
        alert: AlertMessage,
        channel: AlertChannel,
    ) -> DeliveryResult:
        """Deliver an alert through the selected channel."""

        result = channel.deliver(alert)

        if result.channel != channel.name:
            return DeliveryResult(
                status=DeliveryStatus.FAILED,
                channel=channel.name,
                attempted_at=datetime.now(UTC),
                detail="Channel returned an inconsistent channel name.",
            )

        return result
