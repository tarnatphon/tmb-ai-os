from pathlib import Path

from tmb_ai_os.core.plugins import PluginRegistry


def test_plugin_discovery() -> None:
    registry = PluginRegistry()
    plugins = registry.discover(Path(__file__).parents[1] / "plugins")
    assert len(plugins) == 1
    assert plugins[0].name == "example-foundation"
