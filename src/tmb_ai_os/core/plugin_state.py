from __future__ import annotations

from enum import StrEnum


class PluginState(StrEnum):
    """Lifecycle states for runtime-managed plugins."""

    DISCOVERED = "discovered"
    VALIDATED = "validated"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
