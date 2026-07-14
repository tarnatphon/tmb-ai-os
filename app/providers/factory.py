from tmb_ai_os.config import get_settings
from tmb_ai_os.provider_adapter import TextGeneratorProviderAdapter
from tmb_ai_os.provider_factory import create_text_generator


def get_provider() -> TextGeneratorProviderAdapter:
    settings = get_settings()
    generator = create_text_generator(settings=settings)
    return TextGeneratorProviderAdapter(
        generator=generator,
        settings=settings,
    )


__all__ = ["get_provider"]
