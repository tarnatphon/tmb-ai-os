import pytest

from tmb_ai_os.config import Settings
from tmb_ai_os.provider_factory import (
    UnsupportedProviderError,
    create_text_generator,
)
from tmb_ai_os.providers import GeminiGenerator


def test_factory_creates_gemini_generator() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        ai_provider="gemini",
    )

    generator = create_text_generator(settings=settings)

    assert isinstance(generator, GeminiGenerator)


def test_factory_rejects_unknown_provider() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        ai_provider="gemini",
    )

    with pytest.raises(UnsupportedProviderError):
        create_text_generator(
            provider="unknown",
            settings=settings,
        )
