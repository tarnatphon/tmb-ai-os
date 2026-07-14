"""Backward-compatible import path for the Content-first engine."""

from app.content.engine import DuplicateContentError, generate_content
from app.providers.errors import ProviderError as ContentGenerationError

__all__ = ["DuplicateContentError", "ContentGenerationError", "generate_content"]
