from __future__ import annotations

import ast
from collections.abc import Iterable
from dataclasses import dataclass

from . import PatchValidationError
from .parser import ParsedPythonModule


@dataclass(frozen=True, slots=True)
class PythonStructureRequirement:
    """Expected top-level structure in a Python module."""

    functions: tuple[str, ...] = ()
    classes: tuple[str, ...] = ()


def _top_level_names(
    module: ParsedPythonModule,
    node_type: type[ast.FunctionDef] | type[ast.AsyncFunctionDef] | type[ast.ClassDef],
) -> set[str]:
    return {node.name for node in module.tree.body if isinstance(node, node_type)}


def _missing(required: Iterable[str], existing: set[str]) -> tuple[str, ...]:
    return tuple(name for name in required if name not in existing)


def validate_python_structure(
    module: ParsedPythonModule,
    requirement: PythonStructureRequirement,
) -> None:
    """Validate expected top-level functions and classes."""

    functions = _top_level_names(module, ast.FunctionDef) | _top_level_names(
        module,
        ast.AsyncFunctionDef,
    )
    classes = _top_level_names(module, ast.ClassDef)

    missing_functions = _missing(requirement.functions, functions)
    missing_classes = _missing(requirement.classes, classes)

    messages: list[str] = []
    if missing_functions:
        messages.append(f"missing functions: {', '.join(missing_functions)}")
    if missing_classes:
        messages.append(f"missing classes: {', '.join(missing_classes)}")

    if messages:
        raise PatchValidationError(f"{module.path}: {'; '.join(messages)}")
