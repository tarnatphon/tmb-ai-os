from typing import cast

from tmb_ai_os.core.plugin_protocol import PluginProtocol
from tmb_ai_os.core.runtime import Runtime


class DemoPlugin:
    def initialize(self, runtime: Runtime) -> None:
        del runtime

    def shutdown(self, runtime: Runtime) -> None:
        del runtime


def test_protocol() -> None:
    plugin = DemoPlugin()
    assert isinstance(plugin, PluginProtocol)

    runtime = cast(Runtime, object())

    plugin.initialize(runtime)
    plugin.shutdown(runtime)
