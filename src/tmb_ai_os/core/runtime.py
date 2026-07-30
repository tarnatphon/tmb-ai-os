from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tmb_ai_os.core.audit import AuditTrail
from tmb_ai_os.core.events import EventBus
from tmb_ai_os.core.plugins import PluginRegistry
from tmb_ai_os.core.queue import JobQueue


@dataclass(slots=True)
class Runtime:
    events: EventBus
    queue: JobQueue
    plugins: PluginRegistry
    audit: AuditTrail


def build_runtime(base_dir: Path | None = None) -> Runtime:
    registry = PluginRegistry()
    if base_dir is not None:
        registry.discover(base_dir / "plugins")
    return Runtime(
        events=EventBus(),
        queue=JobQueue(),
        plugins=registry,
        audit=AuditTrail(),
    )
