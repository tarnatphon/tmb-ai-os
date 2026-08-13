from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import PatchValidationError
from .transaction import FileReplacement
from .validator import PythonStructureRequirement


@dataclass(frozen=True, slots=True)
class ReplaceFileOperation:
    """Spec operation that replaces one file after validation."""

    path: Path
    content: str
    python: PythonStructureRequirement | None = None

    def to_replacement(self) -> FileReplacement:
        return FileReplacement(
            path=self.path,
            content=self.content,
        )


def parse_replace_file_operation(raw: dict[str, Any], *, root: Path) -> ReplaceFileOperation:
    """Parse one replace-file operation from a JSON-compatible mapping."""

    if raw.get("type") != "replace_file":
        raise PatchValidationError("operation type must be replace_file")

    path_value = raw.get("path")
    content = raw.get("content")
    if not isinstance(path_value, str) or not path_value:
        raise PatchValidationError("replace_file operation requires a non-empty path")
    if not isinstance(content, str):
        raise PatchValidationError("replace_file operation requires string content")

    path = (root / path_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise PatchValidationError(f"patch target escapes repository root: {path_value}") from exc

    python_requirement = _parse_python_requirement(raw.get("python"))

    return ReplaceFileOperation(
        path=path,
        content=content,
        python=python_requirement,
    )


def _parse_python_requirement(raw: object) -> PythonStructureRequirement | None:
    if raw is None:
        return None
    if raw is True:
        return PythonStructureRequirement()
    if not isinstance(raw, dict):
        raise PatchValidationError("python validation must be true or an object")

    functions = _parse_string_tuple(raw.get("functions"), field_name="python.functions")
    classes = _parse_string_tuple(raw.get("classes"), field_name="python.classes")

    return PythonStructureRequirement(
        functions=functions,
        classes=classes,
    )


def _parse_string_tuple(raw: object, *, field_name: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise PatchValidationError(f"{field_name} must be a list of strings")
    return tuple(raw)
