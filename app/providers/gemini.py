import random
import time

from google import genai
from google.genai import types

from app.core.config import settings
from app.providers.base import AIProvider, GenerationResult
from app.providers.errors import (
    ProviderConfigurationError,
    ProviderError,
    ProviderQuotaError,
    ProviderUnavailableError,
)

_MODEL_PREFERENCES = (
    "gemini-3.5-flash",
    "gemini-3-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash-lite",
)


def normalize_model_name(name: str) -> str:
    return str(name or "").strip().strip("\"'").removeprefix("models/").strip()


def _is_text_model(model: object) -> bool:
    name = normalize_model_name(getattr(model, "name", ""))
    lowered = name.lower()
    if not name or any(
        x in lowered for x in ("embedding", "image", "imagen", "live", "tts", "audio", "aqa")
    ):
        return False
    actions = (
        getattr(model, "supported_actions", None)
        or getattr(model, "supported_generation_methods", None)
        or []
    )
    if actions:
        normalized = {str(action).replace("_", "").lower() for action in actions}
        return "generatecontent" in normalized
    return "gemini" in lowered


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ProviderConfigurationError(
                "GEMINI_API_KEY is not configured. Add a Google AI Studio API key to .env"
            )
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def _available_models(self) -> list[str]:
        try:
            return [
                normalize_model_name(model.name)
                for model in self.client.models.list()
                if _is_text_model(model)
            ]
        except Exception as exc:
            raise ProviderUnavailableError(f"Unable to list Gemini models: {exc}") from exc

    def _candidates(self) -> list[str]:
        configured = normalize_model_name(settings.ai_model or settings.gemini_model or "auto")
        available = self._available_models()
        if not available:
            raise ProviderUnavailableError(
                "No Gemini text-generation model is available for this API key."
            )

        ordered: list[str] = []
        if configured.lower() != "auto" and configured in available:
            ordered.append(configured)
        for preferred in _MODEL_PREFERENCES:
            if preferred in available and preferred not in ordered:
                ordered.append(preferred)
        for name in sorted((x for x in available if "flash" in x.lower()), reverse=True):
            if name not in ordered:
                ordered.append(name)
        for name in sorted(available, reverse=True):
            if name not in ordered:
                ordered.append(name)
        if configured.lower() != "auto" and configured not in ordered:
            ordered.insert(0, configured)
        return ordered

    def generate(self, *, system_prompt: str, user_prompt: str) -> GenerationResult:
        candidates = self._candidates()
        attempts = max(1, settings.gemini_retry_attempts)
        last_error: Exception | None = None
        tried: list[str] = []

        for model in candidates[: max(1, settings.gemini_fallback_models)]:
            if normalize_model_name(model).lower() == "auto":
                continue
            tried.append(model)
            for attempt in range(attempts):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=settings.ai_temperature,
                            response_mime_type="text/plain",
                        ),
                    )
                    text = (response.text or "").strip()
                    if not text:
                        raise ProviderError("Gemini returned an empty response")
                    return GenerationResult(text=text, model=model, provider="gemini")
                except Exception as exc:
                    last_error = exc
                    message = str(exc)
                    retryable = any(
                        x in message for x in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED")
                    )
                    if retryable and attempt < attempts - 1:
                        delay = settings.gemini_retry_base_seconds * (2**attempt)
                        delay += random.uniform(0, min(0.5, delay / 4))
                        time.sleep(delay)
                        continue
                    break

        message = str(last_error or "Unknown Gemini error")
        if "429" in message or "RESOURCE_EXHAUSTED" in message:
            raise ProviderQuotaError(
                "Gemini quota or rate limit was exceeded after automatic retries."
            ) from last_error
        if "503" in message or "UNAVAILABLE" in message:
            raise ProviderUnavailableError(
                f"Gemini is temporarily overloaded. Models tried: {', '.join(tried)}"
            ) from last_error
        if "404" in message or "NOT_FOUND" in message:
            raise ProviderUnavailableError(
                "The configured Gemini model is unavailable. Set AI_MODEL=auto."
            ) from last_error
        if "API_KEY" in message.upper() or "401" in message or "403" in message:
            raise ProviderConfigurationError("Gemini API key was rejected.") from last_error
        raise ProviderError(f"Gemini generation failed: {message}") from last_error
