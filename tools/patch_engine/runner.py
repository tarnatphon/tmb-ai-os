from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from . import PatchValidationError


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Result from one validation command."""

    name: str
    arguments: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def run_command(
    *,
    name: str,
    root: Path,
    arguments: Sequence[str],
    env: Mapping[str, str] | None = None,
) -> CommandResult:
    """Run a validation command without shell expansion."""

    process = subprocess.run(
        tuple(arguments),
        cwd=root,
        env=_build_env(env),
        text=True,
        capture_output=True,
        check=False,
    )

    return CommandResult(
        name=name,
        arguments=tuple(arguments),
        returncode=process.returncode,
        stdout=process.stdout,
        stderr=process.stderr,
    )


def run_validation_plan(
    *,
    root: Path,
    python_paths: Sequence[Path],
    test_paths: Sequence[Path],
    run_ruff: bool = True,
    run_pytest: bool = True,
) -> tuple[CommandResult, ...]:
    """Run compile, lint, format, and test checks for a patch."""

    relative_python_paths = tuple(_relative_path(path, root=root) for path in python_paths)
    relative_test_paths = tuple(_relative_path(path, root=root) for path in test_paths)

    results: list[CommandResult] = []

    if relative_python_paths:
        results.append(
            run_command(
                name="python-compile",
                root=root,
                arguments=(sys.executable, "-m", "py_compile", *relative_python_paths),
                env=_cache_env(),
            ),
        )

    if run_ruff:
        paths = relative_python_paths + relative_test_paths
        if paths:
            results.append(
                run_command(
                    name="ruff-check",
                    root=root,
                    arguments=(sys.executable, "-m", "ruff", "check", *paths),
                    env=_cache_env(),
                ),
            )
            results.append(
                run_command(
                    name="ruff-format",
                    root=root,
                    arguments=(sys.executable, "-m", "ruff", "format", "--check", *paths),
                    env=_cache_env(),
                ),
            )

    if run_pytest:
        results.append(
            run_command(
                name="pytest",
                root=root,
                arguments=(sys.executable, "-m", "pytest", *relative_test_paths),
                env=_cache_env(),
            ),
        )

    failed = tuple(result for result in results if not result.passed)
    if failed:
        raise PatchValidationError(_format_failures(failed))

    return tuple(results)


def _relative_path(path: Path, *, root: Path) -> str:
    resolved_root = root.resolve()
    resolved_path = (root / path).resolve() if not path.is_absolute() else path.resolve()

    try:
        return str(resolved_path.relative_to(resolved_root))
    except ValueError as exc:
        raise PatchValidationError(f"validation target escapes repository root: {path}") from exc


def _build_env(env: Mapping[str, str] | None) -> dict[str, str]:
    command_env = dict(os.environ)
    if env is not None:
        command_env.update(env)
    return command_env


def _cache_env() -> dict[str, str]:
    cache_root = Path(tempfile.gettempdir())
    return {
        "PYTHONPYCACHEPREFIX": str(cache_root / "tmb-pycache"),
        "RUFF_CACHE_DIR": str(cache_root / "tmb-ruff-cache"),
    }


def _format_failures(failed: tuple[CommandResult, ...]) -> str:
    messages: list[str] = []
    for result in failed:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        messages.append(f"{result.name} failed: {detail}")
    return "validation failed: " + " | ".join(messages)
