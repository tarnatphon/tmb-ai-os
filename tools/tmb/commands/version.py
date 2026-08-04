from __future__ import annotations

import ast
import subprocess
import tomllib
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]

GitRunner = Callable[
    [Path, tuple[str, ...]],
    subprocess.CompletedProcess[str],
]


def run_git(
    root: Path,
    arguments: tuple[str, ...],
) -> subprocess.CompletedProcess[str]:
    """Run Git without raising for a non-zero exit code."""

    return subprocess.run(
        ("git", *arguments),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


@dataclass(frozen=True, slots=True)
class VersionInfo:
    """Version information collected from project sources."""

    package_version: str
    module_version: str
    latest_tag: str | None

    @property
    def synchronized(self) -> bool:
        """Return whether all available version sources agree."""

        if self.latest_tag is None:
            return False

        tag_version = self.latest_tag.removeprefix("v")
        return self.package_version == self.module_version == tag_version


@dataclass(frozen=True, slots=True)
class VersionService:
    """Read and compare project version sources."""

    root: Path
    git_runner: GitRunner = field(
        default=run_git,
        repr=False,
        compare=False,
    )

    def collect(self) -> VersionInfo:
        """Collect package, module, and Git tag versions."""

        return VersionInfo(
            package_version=self._read_package_version(),
            module_version=self._read_module_version(),
            latest_tag=self._read_latest_tag(),
        )

    def _read_package_version(self) -> str:
        pyproject_path = self.root / "pyproject.toml"
        data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
        version = data["project"]["version"]

        if not isinstance(version, str) or not version.strip():
            raise ValueError("Invalid project.version in pyproject.toml")

        return version

    def _read_module_version(self) -> str:
        module_path = self.root / "src" / "tmb_ai_os" / "__init__.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))

        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if not any(
                isinstance(target, ast.Name) and target.id == "__version__"
                for target in node.targets
            ):
                continue
            if isinstance(node.value, ast.Constant) and isinstance(
                node.value.value,
                str,
            ):
                return node.value.value

        raise ValueError("Missing __version__ in tmb_ai_os.__init__")

    def _read_latest_tag(self) -> str | None:
        result = self.git_runner(
            self.root,
            ("tag", "--sort=-version:refname"),
        )
        if result.returncode != 0:
            return None

        tags = [line.strip() for line in result.stdout.splitlines()]
        return next((tag for tag in tags if tag), None)


def register(subparsers: Any) -> None:
    """Register the project version command."""

    parser = subparsers.add_parser(
        "version",
        help="Show and compare TMB AI OS version sources.",
        description="Show and compare TMB AI OS version sources.",
    )
    parser.set_defaults(handler=run)


def format_report(info: VersionInfo) -> str:
    """Format version information for terminal output."""

    latest_tag = info.latest_tag or "NONE"
    status = "OK" if info.synchronized else "OUT OF SYNC"

    return "\n".join(
        (
            "TMB Version",
            "=" * 60,
            f"Package Version : {info.package_version}",
            f"Module Version  : {info.module_version}",
            f"Latest Git Tag  : {latest_tag}",
            f"Status          : {status}",
            "=" * 60,
        )
    )


def run(args: Any) -> int:
    """Display current project version information."""

    del args

    try:
        info = VersionService(ROOT).collect()
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"Version inspection FAILED: {exc}")
        return 1

    print(format_report(info))
    return 0
