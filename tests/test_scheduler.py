from tmb_ai_os.config import Settings
from tmb_ai_os.scheduler import build_scheduler


def test_scheduler_uses_configured_timezone() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        app_timezone="Asia/Bangkok",
    )

    scheduler = build_scheduler(settings)

    assert str(scheduler.timezone) == "Asia/Bangkok"
