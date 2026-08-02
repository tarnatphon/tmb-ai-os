from __future__ import annotations

from string import Formatter
from typing import Any

from .prompt_models import PromptDefinition, RenderedPrompt


class PromptRenderError(ValueError):
    """Raised when a prompt definition cannot be rendered safely."""


def _extract_placeholders(template: str) -> tuple[str, ...]:
    formatter = Formatter()
    placeholders: list[str] = []

    try:
        parsed_fields = formatter.parse(template)
        for _, field_name, format_spec, conversion in parsed_fields:
            if field_name is None:
                continue

            if not field_name:
                raise PromptRenderError("Anonymous placeholders are not supported.")

            if "." in field_name or "[" in field_name or "]" in field_name:
                raise PromptRenderError(f"Complex placeholder '{field_name}' is not supported.")

            if conversion is not None:
                raise PromptRenderError(
                    f"Conversion is not supported for placeholder '{field_name}'."
                )

            if format_spec:
                raise PromptRenderError(
                    f"Format specifications are not supported for placeholder '{field_name}'."
                )

            if field_name not in placeholders:
                placeholders.append(field_name)
    except PromptRenderError:
        raise
    except ValueError as exc:
        raise PromptRenderError("Prompt template contains invalid placeholder syntax.") from exc

    return tuple(placeholders)


def render_prompt(
    definition: PromptDefinition,
    values: dict[str, Any] | None = None,
) -> RenderedPrompt:
    """Render a prompt definition using validated variable values."""

    supplied_values = {} if values is None else dict(values)
    declared_variables = {variable.name: variable for variable in definition.variables}
    placeholders = _extract_placeholders(definition.template)

    unknown_values = sorted(set(supplied_values) - set(declared_variables))
    if unknown_values:
        unknown_names = ", ".join(unknown_values)
        raise PromptRenderError(f"Unknown prompt variables: {unknown_names}")

    undeclared_placeholders = sorted(set(placeholders) - set(declared_variables))
    if undeclared_placeholders:
        placeholder_names = ", ".join(undeclared_placeholders)
        raise PromptRenderError(f"Template uses undeclared variables: {placeholder_names}")

    resolved_values: dict[str, Any] = {}

    for variable in definition.variables:
        if variable.name in supplied_values:
            resolved_values[variable.name] = supplied_values[variable.name]
            continue

        if variable.default is not None:
            resolved_values[variable.name] = variable.default
            continue

        if variable.required:
            raise PromptRenderError(f"Missing required prompt variable: {variable.name}")

        resolved_values[variable.name] = ""

    try:
        rendered_text = definition.template.format_map(resolved_values)
    except (KeyError, ValueError) as exc:
        raise PromptRenderError("Prompt template could not be rendered.") from exc

    return RenderedPrompt(
        text=rendered_text,
        variables=resolved_values,
    )
