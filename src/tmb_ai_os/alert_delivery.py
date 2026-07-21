"""Production alert delivery services."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from collections.abc import Callable
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class DeliveryStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    SUPPRESSED = "suppressed"


@dataclass(frozen=True, slots=True)
class AlertMessage:
    alert_id: str
    title: str
    message: str
    severity: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    status: DeliveryStatus
    channel: str
    attempted_at: datetime
    detail: str | None = None
    attempts: int = 1


class AlertChannel(Protocol):
    @property
    def name(self) -> str:
        ...

    def deliver(self, alert: AlertMessage) -> DeliveryResult:
        ...


class WebhookAlertChannel:
    """Deliver alerts to an HTTP webhook endpoint."""

    def __init__(
        self,
        webhook_url: str,
        *,
        timeout_seconds: float = 5.0,
        max_attempts: int = 3,
        backoff_seconds: float = 0.25,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        if not webhook_url.startswith(("http://", "https://")):
            raise ValueError("webhook_url must use http or https")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self._webhook_url = webhook_url
        self._timeout_seconds = timeout_seconds
        self._max_attempts = max_attempts
        self._backoff_seconds = backoff_seconds
        self._sleep_fn = sleep_fn

    @property
    def name(self) -> str:
        return "webhook"

    def deliver(self, alert: AlertMessage) -> DeliveryResult:
        payload = json.dumps(
            {
                "alert_id": alert.alert_id,
                "title": alert.title,
                "message": alert.message,
                "severity": alert.severity,
                "created_at": alert.created_at.isoformat(),
            }
        ).encode("utf-8")

        last_error: str | None = None

        for attempt in range(1, self._max_attempts + 1):
            request = Request(
                self._webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            try:
                with urlopen(request, timeout=self._timeout_seconds) as response:
                    status_code = response.getcode()

                if 200 <= status_code < 300:
                    return DeliveryResult(
                        status=DeliveryStatus.SUCCESS,
                        channel=self.name,
                        attempted_at=datetime.now(UTC),
                        attempts=attempt,
                    )

                last_error = f"Unexpected HTTP status: {status_code}"

            except (HTTPError, URLError, TimeoutError) as exc:
                last_error = str(exc)

            if attempt < self._max_attempts:
                self._sleep_fn(self._backoff_seconds * attempt)

        return DeliveryResult(
            status=DeliveryStatus.FAILED,
            channel=self.name,
            attempted_at=datetime.now(UTC),
            detail=last_error,
            attempts=self._max_attempts,
        )


class AlertDeliveryService:
    """Coordinates alert delivery and duplicate suppression."""

    def __init__(self, *, cooldown_seconds: int = 300) -> None:
        if cooldown_seconds < 0:
            raise ValueError("cooldown_seconds cannot be negative")

        self._cooldown = timedelta(seconds=cooldown_seconds)
        self._last_delivered_at: dict[tuple[str, str], datetime] = {}
        self._history: list[DeliveryResult] = []

    @property
    def history(self) -> tuple[DeliveryResult, ...]:
        return tuple(self._history)

    def deliver(
        self,
        alert: AlertMessage,
        channel: AlertChannel,
    ) -> DeliveryResult:
        now = datetime.now(UTC)
        key = (alert.alert_id, channel.name)
        last_delivery = self._last_delivered_at.get(key)

        if last_delivery is not None and now - last_delivery < self._cooldown:
            result = DeliveryResult(
                status=DeliveryStatus.SUPPRESSED,
                channel=channel.name,
                attempted_at=now,
                detail="Alert suppressed during cooldown period.",
                attempts=0,
            )
            self._history.append(result)
            return result

        result = channel.deliver(alert)

        if result.channel != channel.name:
            result = DeliveryResult(
                status=DeliveryStatus.FAILED,
                channel=channel.name,
                attempted_at=now,
                detail="Channel returned an inconsistent channel name.",
            )

        if result.status is DeliveryStatus.SUCCESS:
            self._last_delivered_at[key] = result.attempted_at

        self._history.append(result)
        return result
