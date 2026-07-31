from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Capability:
    """Represents a capability that can be registered with the runtime."""

    name: str
    version: str = "1.0.0"
    tags: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


class CapabilityRegistry:
    """Registry for runtime capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        if capability.name in self._capabilities:
            raise ValueError(f"Capability '{capability.name}' already registered.")
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> Capability:
        try:
            return self._capabilities[name]
        except KeyError as exc:
            raise KeyError(f"Capability '{name}' not found.") from exc

    def has(self, name: str) -> bool:
        return name in self._capabilities

    def list(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities.values())
