from .config import get_settings
from .notifiers import DryRunNotifier, Notifier
from .webhook_notifier import WebhookConfig, WebhookNotifier


class UnsupportedNotifierError(ValueError):
    pass


def create_notifier() -> Notifier:
    settings = get_settings()
    provider = settings.notification_provider.strip().lower()

    if provider == "dry_run":
        return DryRunNotifier()

    if provider == "webhook":
        if not settings.webhook_url:
            raise UnsupportedNotifierError("TMB_WEBHOOK_URL is required")
        if not settings.webhook_secret:
            raise UnsupportedNotifierError("TMB_WEBHOOK_SECRET is required")
        return WebhookNotifier(
            WebhookConfig(
                url=settings.webhook_url,
                secret=settings.webhook_secret,
            )
        )

    raise UnsupportedNotifierError(f"Unsupported notification provider: {provider}")
