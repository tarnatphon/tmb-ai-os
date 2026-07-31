from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any, Generic, TypeVar

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

    def resolve(self, service_type: type[T]) -> T:
        with self._lock:
            registration = self._services.get(service_type)

            if registration is None:
                raise ServiceNotFoundError(service_type.__name__)

            if registration.lifetime is ServiceLifetime.INSTANCE:
                return registration.value  # type: ignore[return-value]

            raise NotImplementedError(
                "Singleton and Factory support will be added in PR-001 Phase 2."
            )
