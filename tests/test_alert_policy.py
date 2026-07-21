from datetime import UTC, datetime

from tmb_ai_os.alert_delivery import AlertMessage
from tmb_ai_os.alert_policy import AlertPolicy, AlertRoute, AlertSeverity


def make_alert(severity: str) -> AlertMessage:
    return AlertMessage(
        alert_id="system-alert",
        title="System alert",
        message="System threshold exceeded.",
        severity=severity,
        created_at=datetime.now(UTC),
    )


def test_policy_resolves_route_by_severity() -> None:
    policy = AlertPolicy(
        {
            AlertSeverity.CRITICAL: AlertRoute(
                channel_names=("primary", "fallback")
            )
        }
    )

    route = policy.resolve(make_alert("critical"))

    assert route.channel_names == ("primary", "fallback")
    assert route.enabled is True


def test_policy_is_case_insensitive() -> None:
    policy = AlertPolicy(
        {
            AlertSeverity.ERROR: AlertRoute(
                channel_names=("webhook",)
            )
        }
    )

    route = policy.resolve(make_alert("ERROR"))

    assert route.channel_names == ("webhook",)


def test_unknown_severity_uses_default_route() -> None:
    policy = AlertPolicy(
        {},
        default_route=AlertRoute(channel_names=("default",)),
    )

    route = policy.resolve(make_alert("unknown"))

    assert route.channel_names == ("default",)


def test_disabled_route_returns_no_channels() -> None:
    policy = AlertPolicy(
        {
            AlertSeverity.INFO: AlertRoute(
                channel_names=("webhook",),
                enabled=False,
            )
        }
    )

    route = policy.resolve(make_alert("info"))

    assert route.channel_names == ()
    assert route.enabled is False


def test_missing_route_defaults_to_no_delivery() -> None:
    policy = AlertPolicy({})

    route = policy.resolve(make_alert("warning"))

    assert route.channel_names == ()
