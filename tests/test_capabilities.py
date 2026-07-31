import pytest

from tmb_ai_os.core.capabilities import Capability, CapabilityRegistry


def test_register_and_get() -> None:
    registry = CapabilityRegistry()

    capability = Capability(name="chat")

    registry.register(capability)

    assert registry.get("chat") == capability
    assert registry.has("chat")


def test_duplicate_registration() -> None:
    registry = CapabilityRegistry()

    registry.register(Capability(name="chat"))

    with pytest.raises(ValueError):
        registry.register(Capability(name="chat"))


def test_missing_capability() -> None:
    registry = CapabilityRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")
