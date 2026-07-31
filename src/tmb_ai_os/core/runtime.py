from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tmb_ai_os.core.audit import AuditTrail
from tmb_ai_os.core.capabilities import CapabilityRegistry
from tmb_ai_os.core.container import ServiceContainer
from tmb_ai_os.core.events import EventBus
from tmb_ai_os.core.plugins import PluginRegistry
from tmb_ai_os.core.queue import JobQueue


@dataclass(slots=True)
class Runtime:
    container: ServiceContainer
    capabilities: CapabilityRegistry
    events: EventBus
    queue: JobQueue
    plugins: PluginRegistry
    audit: AuditTrail


def build_runtime(base_dir: Path | None = None) -> Runtime:
    container = ServiceContainer()
    capabilities = CapabilityRegistry()

    registry = PluginRegistry()

    if base_dir is not None:
        registry.discover(base_dir / "plugins")

    events = EventBus()
    queue = JobQueue()
    audit = AuditTrail()

    container.register_instance(EventBus, events)
    container.register_instance(JobQueue, queue)
    container.register_instance(PluginRegistry, registry)
    container.register_instance(AuditTrail, audit)
    container.register_instance(CapabilityRegistry, capabilities)

    return Runtime(
        container=container,
        capabilities=capabilities,
        events=events,
        queue=queue,
        plugins=registry,
        audit=audit,
    )
