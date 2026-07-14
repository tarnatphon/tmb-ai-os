from tmb_ai_os.config import Settings
from tmb_ai_os.provider_adapter import TextGeneratorProviderAdapter
from tmb_ai_os.provider_contracts import GenerationRequest


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        return f"generated: {prompt}"


def test_adapter_preserves_legacy_response_contract() -> None:
    settings = Settings(
        gemini_api_key="test-key",
        gemini_model="test-model",
    )
    adapter = TextGeneratorProviderAdapter(
        generator=FakeGenerator(),
        settings=settings,
    )

    response = adapter.generate_content(GenerationRequest(prompt="hello"))

    assert response.text == "generated: hello"
    assert response.provider == "gemini"
    assert response.model == "test-model"
