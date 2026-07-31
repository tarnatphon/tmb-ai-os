from tmb_ai_os.core.plugin_state import PluginState


def test_plugin_state_values() -> None:
    assert PluginState.DISCOVERED == "discovered"
    assert PluginState.RUNNING == "running"
    assert PluginState.FAILED == "failed"
