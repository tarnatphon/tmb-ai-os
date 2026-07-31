from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any, Generic, TypeVar, cast

T = TypeVar("T")


class ServiceLifetime(Enum):
    INSTANCE = "instance"
    SINGLETON = "singleton"
    FACTORY = "factory"


@dataclass(slots=True)
class Registration(Generic[T]):
    lifetime: ServiceLifetime
    value: T | None = None
    factory: Callable[[ServiceContainer], T] | None = None


class ServiceNotFoundError(KeyError):
    """Raised when a requested service has not been registered."""


class DuplicateServiceError(ValueError):
    """Raised when attempting to register the same service twice."""


class CircularDependencyError(RuntimeError):
    """Raised when a circular dependency is detected."""


class ServiceContainer:
    """Thread-safe dependency injection container."""

    def __init__(self) -> None:
        self._services: dict[type[Any], Registration[Any]] = {}
        self._singletons: dict[type[Any], Any] = {}
        self._resolving: set[type[Any]] = set()
        self._lock = RLock()

    def register_instance(
        self,
        service_type: type[T],
        instance: T,
    ) -> None:
        with self._lock:
            if service_type in self._services:
                raise DuplicateServiceError(service_type.__name__)

            self._services[service_type] = Registration(
                lifetime=ServiceLifetime.INSTANCE,
                value=instance,
            )

    def register_singleton(
        self,
        service_type: type[T],
        factory: Callable[[ServiceContainer], T],
    ) -> None:
        with self._lock:
            if service_type in self._services:
                raise DuplicateServiceError(service_type.__name__)

            self._services[service_type] = Registration(
                lifetime=ServiceLifetime.SINGLETON,
                factory=factory,
            )

    def register_factory(
        self,
        service_type: type[T],
        factory: Callable[[ServiceContainer], T],
    ) -> None:
        with self._lock:
            if service_type in self._services:
                raise DuplicateServiceError(service_type.__name__)

            self._services[service_type] = Registration(
                lifetime=ServiceLifetime.FACTORY,
                factory=factory,
            )

    def has(self, service_type: type[Any]) -> bool:
        return service_type in self._services

    def clear(self) -> None:
        with self._lock:
            self._services.clear()
            self._singletons.clear()

    def resolve(self, service_type: type[T]) -> T:
        with self._lock:
            registration = self._services.get(service_type)

            if registration is None:
                raise ServiceNotFoundError(service_type.__name__)

            if registration.lifetime is ServiceLifetime.INSTANCE:
                return registration.value  # type: ignore[return-value]

            if registration.lifetime is ServiceLifetime.SINGLETON:
                if service_type not in self._singletons:
                    assert registration.factory is not None
                    self._singletons[service_type] = registration.factory(self)
                return cast(T, self._singletons[service_type])

            assert registration.factory is not None
            return cast(T, registration.factory(self))
