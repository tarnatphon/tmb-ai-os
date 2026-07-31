from __future__ import annotations

from dataclasses import dataclass, field

from tmb_ai_os.core.capabilities import CapabilityRegistry
from tmb_ai_os.core.container import ServiceContainer
from tmb_ai_os.core.plugins import PluginRegistry


@dataclass(slots=True)
class PluginBootstrap:
    """Coordinates plugin lifecycle without owning plugin discovery."""

    registry: PluginRegistry
    capabilities: CapabilityRegistry
    container: ServiceContainer
    loaded_plugins: list[str] = field(default_factory=list)

    def discover(self) -> tuple[str, ...]:
        """Return the names of discovered plugins."""
        return tuple(plugin.name for plugin in self.registry.list_plugins())

    def initialize(self) -> None:
        """Placeholder for plugin initialization."""
        self.loaded_plugins = list(self.discover())

    def shutdown(self) -> None:
        """Placeholder for plugin shutdown."""
        self.loaded_plugins.clear()
