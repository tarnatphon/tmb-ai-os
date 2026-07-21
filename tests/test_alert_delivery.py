from __future__ import annotations

from datetime import UTC, datetime

import pytest

from tmb_ai_os.alert_delivery import (
    AlertDeliveryService,
    AlertMessage,
    DeliveryResult,
    DeliveryStatus,
    WebhookAlertChannel,
)


class SuccessfulChannel:
    @property
    def name(self) -> str:
        return "test"

    def deliver(self, alert: AlertMessage) -> DeliveryResult:
        return DeliveryResult(
            status=DeliveryStatus.SUCCESS,
            channel=self.name,
            attempted_at=datetime.now(UTC),
        )


def make_alert() -> AlertMessage:
    return AlertMessage(
        alert_id="high-error-rate",
        title="High error rate",
        message="HTTP error rate exceeded threshold.",
        severity="critical",
        created_at=datetime.now(UTC),
    )


def test_delivery_records_success() -> None:
    service = AlertDeliveryService(cooldown_seconds=60)

    result = service.deliver(make_alert(), SuccessfulChannel())

    assert result.status is DeliveryStatus.SUCCESS
    assert len(service.history) == 1


def test_duplicate_alert_is_suppressed() -> None:
    service = AlertDeliveryService(cooldown_seconds=60)
    alert = make_alert()
    channel = SuccessfulChannel()

    first = service.deliver(alert, channel)
    second = service.deliver(alert, channel)

    assert first.status is DeliveryStatus.SUCCESS
    assert second.status is DeliveryStatus.SUPPRESSED
    assert second.attempts == 0


def test_zero_cooldown_allows_repeated_delivery() -> None:
    service = AlertDeliveryService(cooldown_seconds=0)
    alert = make_alert()
    channel = SuccessfulChannel()

    first = service.deliver(alert, channel)
    second = service.deliver(alert, channel)

    assert first.status is DeliveryStatus.SUCCESS
    assert second.status is DeliveryStatus.SUCCESS


def test_webhook_rejects_invalid_url() -> None:
    with pytest.raises(ValueError, match="http or https"):
        WebhookAlertChannel("ftp://example.com/hook")


def test_webhook_requires_at_least_one_attempt() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        WebhookAlertChannel(
            "https://example.com/hook",
            max_attempts=0,
        )
