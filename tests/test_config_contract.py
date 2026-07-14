from tmb_ai_os.config import Settings


def test_settings_exposes_provider_contract() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        ai_provider="gemini",
    )

    assert settings.ai_provider == "gemini"
    assert settings.gemini_api_key == "test-key"
