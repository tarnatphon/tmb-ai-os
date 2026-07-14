from dataclasses import dataclass

from .config import Settings
from .provider_contracts import (
    ContentProvider,
    GenerationRequest,
    GenerationResponse,
)
from .providers import TextGenerator


@dataclass
class TextGeneratorProviderAdapter(ContentProvider):
    generator: TextGenerator
    settings: Settings
    name: str = "gemini"

    def generate_content(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        text = self.generator.generate(request.prompt)
        return GenerationResponse(
            text=text,
            provider=self.name,
            model=self.settings.gemini_model,
        )
