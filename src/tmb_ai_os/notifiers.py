from dataclasses import dataclass
from typing import Protocol

from .alerts import Alert


@dataclass(frozen=True)
class NotificationResult:
    provider: str
    delivered: bool
    detail: str


class Notifier(Protocol):
    name: str

    def send(self, alert: Alert) -> NotificationResult: ...


class DryRunNotifier:
    name = "dry_run"

    def send(self, alert: Alert) -> NotificationResult:
        return NotificationResult(
            provider=self.name,
            delivered=True,
            detail=(f"Simulated notification for {alert.code}"),
        )
