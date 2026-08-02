from __future__ import annotations

from dataclasses import dataclass, field

from .prompt_models import PromptDefinition


@dataclass(slots=True)
class PromptRegistry:
    _definitions: dict[str, PromptDefinition] = field(default_factory=dict)

    def register(self, definition: PromptDefinition) -> None:
        name = definition.metadata.name
        if name in self._definitions:
            raise ValueError(f"Prompt '{name}' is already registered.")
        self._definitions[name] = definition

    def get(self, name: str) -> PromptDefinition:
        try:
            return self._definitions[name]
        except KeyError as exc:
            raise KeyError(f"Unknown prompt '{name}'.") from exc

    def list_names(self) -> list[str]:
        return sorted(self._definitions.keys())

    def contains(self, name: str) -> bool:
        return name in self._definitions

    def count(self) -> int:
        return len(self._definitions)
