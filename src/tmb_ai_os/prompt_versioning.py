from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .prompt_models import PromptDefinition


class PromptVersionError(ValueError):
    """Raised when a prompt version is invalid or cannot be resolved."""


@dataclass(frozen=True, order=True, slots=True)
class PromptVersion:
    """Semantic version used by prompt definitions."""

    major: int
    minor: int
    patch: int

    def __post_init__(self) -> None:
        if self.major < 0 or self.minor < 0 or self.patch < 0:
            raise PromptVersionError("Prompt version components must not be negative.")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, value: str) -> PromptVersion:
        """Parse a strict major.minor.patch semantic version."""

        if not isinstance(value, str) or not value.strip():
            raise PromptVersionError("Prompt version must be a non-empty string.")

        parts = value.split(".")
        if len(parts) != 3:
            raise PromptVersionError("Prompt version must use major.minor.patch format.")

        if any(not part.isdigit() for part in parts):
            raise PromptVersionError("Prompt version components must contain digits only.")

        major, minor, patch = (int(part) for part in parts)
        return cls(major=major, minor=minor, patch=patch)


def resolve_latest_prompt(
    definitions: Iterable[PromptDefinition],
) -> PromptDefinition:
    """Return the definition containing the highest semantic version."""

    candidates = list(definitions)

    if not candidates:
        raise PromptVersionError("At least one prompt definition is required.")

    prompt_names = {definition.metadata.name for definition in candidates}
    if len(prompt_names) != 1:
        raise PromptVersionError("All prompt definitions must have the same metadata name.")

    return max(
        candidates,
        key=lambda definition: PromptVersion.parse(definition.metadata.version),
    )
