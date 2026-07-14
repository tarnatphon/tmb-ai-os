from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.errors import ProviderConfigurationError
from app.providers.gemini import GeminiProvider


def get_provider() -> AIProvider:
    provider = settings.ai_provider.strip().lower()
    if provider == "gemini":
        return GeminiProvider()
    raise ProviderConfigurationError(
        f"Unsupported AI_PROVIDER '{settings.ai_provider}'. Supported providers: gemini"
    )
