from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from . import PatchValidationError


@dataclass(frozen=True, slots=True)
class ParsedPythonModule:
    """Parsed Python source and AST tree."""

    path: Path
    source: str
    tree: ast.Module


def parse_python_source(source: str, *, path: Path) -> ParsedPythonModule:
    """Parse Python source and raise a patch validation error on syntax issues."""

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise PatchValidationError(f"{path}: invalid Python syntax: {exc.msg}") from exc

    return ParsedPythonModule(
        path=path,
        source=source,
        tree=tree,
    )


def parse_python_file(path: Path) -> ParsedPythonModule:
    """Read and parse a Python file."""

    return parse_python_source(
        path.read_text(encoding="utf-8"),
        path=path,
    )
