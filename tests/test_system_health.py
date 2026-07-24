from datetime import datetime

from tmb_ai_os.system_health import get_system_health


def test_get_system_health_returns_healthy_snapshot() -> None:
    health = get_system_health()

    assert health["status"] == "healthy"
    assert health["api"]["readiness"] is True
    assert health["services"]["application"] == "healthy"
    assert health["services"]["alert_metrics"] == "healthy"


def test_get_system_health_returns_process_information() -> None:
    process = get_system_health()["process"]

    assert process["uptime_seconds"] >= 0
    assert process["python_version"]
    assert process["platform"]


def test_get_system_health_returns_timezone_aware_timestamp() -> None:
    generated_at = get_system_health()["generated_at"]
    parsed = datetime.fromisoformat(generated_at)

    assert parsed.tzinfo is not None
