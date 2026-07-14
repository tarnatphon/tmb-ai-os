from typing import Protocol

from google import genai
from google.genai import types

from .config import Settings


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str: ...


class GeminiGenerator:
    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("TMB_GEMINI_API_KEY is not configured")
        self.settings = settings

    def generate(self, prompt: str) -> str:
        with genai.Client(api_key=self.settings.gemini_api_key) as client:
            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    top_p=0.9,
                ),
            )

        text = response.text
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response")
        return text.strip()
