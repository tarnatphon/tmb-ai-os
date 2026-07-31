from pathlib import Path

from tmb_ai_os.core.audit import AuditTrail
from tmb_ai_os.core.events import EventBus
from tmb_ai_os.core.plugins import PluginRegistry
from tmb_ai_os.core.queue import JobQueue
from tmb_ai_os.core.runtime import build_runtime


def test_build_runtime_default() -> None:
    runtime = build_runtime()

    assert isinstance(runtime.events, EventBus)
    assert isinstance(runtime.queue, JobQueue)
    assert isinstance(runtime.plugins, PluginRegistry)
    assert isinstance(runtime.audit, AuditTrail)


def test_build_runtime_with_base_dir(tmp_path: Path) -> None:
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    runtime = build_runtime(tmp_path)

    assert isinstance(runtime.plugins, PluginRegistry)
