import hashlib
import hmac
import json
from dataclasses import dataclass
from urllib import error, request

from .alerts import Alert
from .notifiers import NotificationResult


@dataclass(frozen=True)
class WebhookConfig:
    url: str
    secret: str
    timeout_seconds: int = 10


class WebhookNotifier:
    name = "webhook"

    def __init__(self, config: WebhookConfig) -> None:
        self.config = config

    def send(self, alert: Alert) -> NotificationResult:
        payload = json.dumps(
            {
                "code": alert.code,
                "title": alert.title,
                "detail": alert.detail,
                "severity": alert.severity.value,
                "occurred_at": alert.occurred_at.isoformat(),
            },
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")

        signature = hmac.new(
            self.config.secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        http_request = request.Request(
            self.config.url,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-TMB-Signature": signature,
            },
        )

        try:
            with request.urlopen(
                http_request,
                timeout=self.config.timeout_seconds,
            ) as response:
                status = int(response.status)
        except error.HTTPError as exc:
            return NotificationResult(
                provider=self.name,
                delivered=False,
                detail=f"HTTP {exc.code}",
            )
        except error.URLError as exc:
            return NotificationResult(
                provider=self.name,
                delivered=False,
                detail=str(exc.reason),
            )

        return NotificationResult(
            provider=self.name,
            delivered=200 <= status < 300,
            detail=f"HTTP {status}",
        )
