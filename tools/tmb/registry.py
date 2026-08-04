from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .commands import doctor, validate, version

CommandRegistrar = Callable[[Any], None]


@dataclass(frozen=True, slots=True)
class Command:
    """Metadata and registration callback for a CLI command."""

    name: str
    register: CommandRegistrar


COMMANDS = (
    Command(name="validate", register=validate.register),
    Command(name="doctor", register=doctor.register),
    Command(name="version", register=version.register),
)


def register_commands(
    subparsers: Any,
) -> None:
    """Register all available developer CLI commands."""

    for command in COMMANDS:
        command.register(subparsers)
