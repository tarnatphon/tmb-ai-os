from __future__ import annotations

from string import Formatter

from .prompt_models import PromptDefinition


class PromptValidationError(ValueError):
    """Raised when a prompt definition is structurally invalid."""


def _require_non_empty(value: str, field_name: str) -> None:
    if not value.strip():
        raise PromptValidationError(f"Field '{field_name}' must not be empty.")


def _extract_placeholders(template: str) -> tuple[str, ...]:
    placeholders: list[str] = []

    try:
        parsed_fields = Formatter().parse(template)

        for _, field_name, format_spec, conversion in parsed_fields:
            if field_name is None:
                continue

            if not field_name:
                raise PromptValidationError("Anonymous placeholders are not supported.")

            if "." in field_name or "[" in field_name or "]" in field_name:
                raise PromptValidationError(f"Complex placeholder '{field_name}' is not supported.")

            if conversion is not None:
                raise PromptValidationError(
                    f"Conversion is not supported for placeholder '{field_name}'."
                )

            if format_spec:
                raise PromptValidationError(
                    f"Format specification is not supported for '{field_name}'."
                )

            if field_name not in placeholders:
                placeholders.append(field_name)
    except PromptValidationError:
        raise
    except ValueError as exc:
        raise PromptValidationError("Prompt template contains invalid placeholder syntax.") from exc

    return tuple(placeholders)


def validate_prompt_definition(definition: PromptDefinition) -> None:
    """Validate prompt metadata, variables, and template placeholders."""

    _require_non_empty(definition.metadata.name, "metadata.name")
    _require_non_empty(definition.metadata.version, "metadata.version")
    _require_non_empty(definition.metadata.author, "metadata.author")
    _require_non_empty(definition.template, "template")

    variable_names: list[str] = []

    for variable in definition.variables:
        _require_non_empty(variable.name, "variables.name")

        if variable.name in variable_names:
            raise PromptValidationError(f"Duplicate prompt variable: {variable.name}")

        variable_names.append(variable.name)

    placeholders = _extract_placeholders(definition.template)
    undeclared = sorted(set(placeholders) - set(variable_names))

    if undeclared:
        names = ", ".join(undeclared)
        raise PromptValidationError(f"Template uses undeclared variables: {names}")
