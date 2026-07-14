from tmb_ai_os.config import Settings


def test_settings_include_database_and_scheduler_fields() -> None:
    settings = Settings(gemini_api_key="test-key")

    assert settings.database_url
    assert settings.app_timezone == "Asia/Bangkok"
    assert settings.scheduler_enabled is False
