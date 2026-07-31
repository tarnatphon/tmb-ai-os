from tmb_ai_os.core.capabilities import CapabilityRegistry
from tmb_ai_os.core.container import ServiceContainer
from tmb_ai_os.core.plugin_bootstrap import PluginBootstrap
from tmb_ai_os.core.plugins import PluginRegistry


def test_bootstrap_starts_empty() -> None:
    bootstrap = PluginBootstrap(
        registry=PluginRegistry(),
        capabilities=CapabilityRegistry(),
        container=ServiceContainer(),
    )

    assert bootstrap.loaded_plugins == []


def test_shutdown_clears_loaded_plugins() -> None:
    bootstrap = PluginBootstrap(
        registry=PluginRegistry(),
        capabilities=CapabilityRegistry(),
        container=ServiceContainer(),
    )

    bootstrap.loaded_plugins.append("demo")

    bootstrap.shutdown()

    assert bootstrap.loaded_plugins == []
