from tmb_ai_os.config import Settings
from tmb_ai_os.deployment import validate_deployment


def test_production_deployment_passes_with_secure_config() -> None:
    settings = Settings(
        env="production",
        gemini_api_key="test-key",
        api_key="x" * 64,
        require_secure_api_key=True,
    )

    report = validate_deployment(settings)

    assert report.ready is True


def test_deployment_rejects_non_production_environment() -> None:
    settings = Settings(
        env="development",
        gemini_api_key="test-key",
        api_key="x" * 64,
        require_secure_api_key=True,
    )

    report = validate_deployment(settings)

    assert report.ready is False
