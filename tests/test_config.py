from tmb_ai_os.core.config import get_settings


def test_default_settings() -> None:
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.api_prefix.startswith("/")
    assert settings.app_name
