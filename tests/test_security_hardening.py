from tmb_ai_os.config import Settings
from tmb_ai_os.security_hardening import (
    validate_security_config,
)


def test_default_api_key_is_reported_as_insecure() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        api_key="change-me",
        require_secure_api_key=True,
    )

    report = validate_security_config(settings)

    assert report.secure is False
    assert report.issues


def test_long_api_key_is_secure() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        api_key="x" * 64,
        require_secure_api_key=True,
    )

    report = validate_security_config(settings)

    assert report.secure is True
