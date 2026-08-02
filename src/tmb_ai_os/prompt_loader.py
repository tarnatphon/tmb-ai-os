from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .prompt_models import PromptDefinition, PromptMetadata, PromptVariable


class PromptLoadError(ValueError):
    """Raised when a prompt definition cannot be loaded or validated."""


def _require_mapping(value: object, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PromptLoadError(f"Field '{field_name}' must be a mapping.")
    return value


def _require_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PromptLoadError(f"Field '{field_name}' must be a non-empty string.")
    return value


def _load_variable(value: object, index: int) -> PromptVariable:
    data = _require_mapping(value, f"variables[{index}]")
    name = _require_string(data.get("name"), f"variables[{index}].name")

    description = data.get("description", "")
    if not isinstance(description, str):
        raise PromptLoadError(f"Field 'variables[{index}].description' must be a string.")

    required = data.get("required", True)
    if not isinstance(required, bool):
        raise PromptLoadError(f"Field 'variables[{index}].required' must be a boolean.")

    return PromptVariable(
        name=name,
        description=description,
        required=required,
        default=data.get("default"),
    )


def load_prompt(path: str | Path) -> PromptDefinition:
    """Load a prompt definition from a YAML file."""

    prompt_path = Path(path)

    if not prompt_path.is_file():
        raise PromptLoadError(f"Prompt file does not exist: {prompt_path}")

    try:
        raw_data = yaml.safe_load(prompt_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PromptLoadError(f"Invalid YAML in prompt file: {prompt_path}") from exc

    data = _require_mapping(raw_data, "root")

    name = _require_string(data.get("name"), "name")
    template = _require_string(data.get("template"), "template")

    version = data.get("version", "1.0.0")
    author = data.get("author", "Thai Modern Bags AI")
    description = data.get("description", "")

    if not isinstance(version, str):
        raise PromptLoadError("Field 'version' must be a string.")
    if not isinstance(author, str):
        raise PromptLoadError("Field 'author' must be a string.")
    if not isinstance(description, str):
        raise PromptLoadError("Field 'description' must be a string.")

    raw_variables = data.get("variables", [])
    if not isinstance(raw_variables, list):
        raise PromptLoadError("Field 'variables' must be a list.")

    variables = [_load_variable(variable, index) for index, variable in enumerate(raw_variables)]

    return PromptDefinition(
        metadata=PromptMetadata(
            name=name,
            version=version,
            author=author,
            description=description,
        ),
        template=template,
        variables=variables,
    )
