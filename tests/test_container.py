import pytest

from tmb_ai_os.core.container import (
    DuplicateServiceError,
    ServiceContainer,
    ServiceNotFoundError,
)


class DummyService:
    def __init__(self) -> None:
        self.value = object()


def test_register_instance() -> None:
    container = ServiceContainer()

    service = DummyService()

    container.register_instance(DummyService, service)

    assert container.resolve(DummyService) is service


def test_duplicate_registration() -> None:
    container = ServiceContainer()

    container.register_instance(DummyService, DummyService())

    with pytest.raises(DuplicateServiceError):
        container.register_instance(DummyService, DummyService())


def test_register_singleton() -> None:
    container = ServiceContainer()

    container.register_singleton(
        DummyService,
        lambda _: DummyService(),
    )

    first = container.resolve(DummyService)
    second = container.resolve(DummyService)

    assert first is second


def test_register_factory() -> None:
    container = ServiceContainer()

    container.register_factory(
        DummyService,
        lambda _: DummyService(),
    )

    first = container.resolve(DummyService)
    second = container.resolve(DummyService)

    assert first is not second


def test_has() -> None:
    container = ServiceContainer()

    assert not container.has(DummyService)

    container.register_instance(DummyService, DummyService())

    assert container.has(DummyService)


def test_clear() -> None:
    container = ServiceContainer()

    container.register_instance(DummyService, DummyService())

    container.clear()

    with pytest.raises(ServiceNotFoundError):
        container.resolve(DummyService)
