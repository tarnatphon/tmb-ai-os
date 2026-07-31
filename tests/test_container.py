import pytest

from tmb_ai_os.core.container import (
    DuplicateServiceError,
    ServiceContainer,
)


class DummyService:
    def __init__(self, value: str = "ok") -> None:
        self.value = value


def test_register_instance() -> None:
    container = ServiceContainer()

    service = DummyService()

    container.register_instance(DummyService, service)

    resolved = container.resolve(DummyService)

    assert resolved is service
    assert resolved.value == "ok"


def test_duplicate_registration() -> None:
    container = ServiceContainer()

    container.register_instance(DummyService, DummyService())

    with pytest.raises(DuplicateServiceError):
        container.register_instance(DummyService, DummyService())
