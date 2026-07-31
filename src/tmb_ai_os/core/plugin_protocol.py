from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from tmb_ai_os.core.runtime import Runtime


@runtime_checkable
class PluginProtocol(Protocol):
    """Executable runtime plugin contract."""

    def initialize(self, runtime: Runtime) -> None: ...

    def shutdown(self, runtime: Runtime) -> None: ...
