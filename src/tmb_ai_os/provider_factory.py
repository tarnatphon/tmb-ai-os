from enum import StrEnum

from .config import Settings, get_settings
from .providers import GeminiGenerator, TextGenerator


class ProviderName(StrEnum):
    GEMINI = "gemini"


class UnsupportedProviderError(ValueError):
    pass


def create_text_generator(
    provider: str | ProviderName | None = None,
    settings: Settings | None = None,
) -> TextGenerator:
    resolved_settings = settings or get_settings()
    resolved_provider = _resolve_provider(provider, resolved_settings)

    if resolved_provider is ProviderName.GEMINI:
        return GeminiGenerator(resolved_settings)

    raise UnsupportedProviderError(f"Unsupported provider: {resolved_provider}")


def _resolve_provider(
    provider: str | ProviderName | None,
    settings: Settings,
) -> ProviderName:
    value = provider or settings.ai_provider

    try:
        return ProviderName(str(value).strip().lower())
    except ValueError as exc:
        raise UnsupportedProviderError(f"Unsupported provider: {value}") from exc
