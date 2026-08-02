import pytest

from tmb_ai_os.prompt_models import (
    PromptDefinition,
    PromptMetadata,
    PromptVariable,
)
from tmb_ai_os.prompt_renderer import PromptRenderError, render_prompt


def make_definition(
    template: str,
    variables: list[PromptVariable],
) -> PromptDefinition:
    return PromptDefinition(
        metadata=PromptMetadata(name="marketing.test"),
        template=template,
        variables=variables,
    )


def test_render_prompt_with_required_variable() -> None:
    definition = make_definition(
        "Write about {product}",
        [PromptVariable(name="product")],
    )

    rendered = render_prompt(definition, {"product": "OEM backpack"})

    assert rendered.text == "Write about OEM backpack"
    assert rendered.variables == {"product": "OEM backpack"}


def test_render_prompt_uses_default_value() -> None:
    definition = make_definition(
        "Use a {tone} tone",
        [
            PromptVariable(
                name="tone",
                required=False,
                default="professional",
            )
        ],
    )

    rendered = render_prompt(definition)

    assert rendered.text == "Use a professional tone"
    assert rendered.variables == {"tone": "professional"}


def test_optional_variable_without_default_uses_empty_string() -> None:
    definition = make_definition(
        "Additional note: {note}",
        [PromptVariable(name="note", required=False)],
    )

    rendered = render_prompt(definition)

    assert rendered.text == "Additional note: "
    assert rendered.variables == {"note": ""}


def test_missing_required_variable_is_rejected() -> None:
    definition = make_definition(
        "Write about {product}",
        [PromptVariable(name="product")],
    )

    with pytest.raises(PromptRenderError, match="Missing required"):
        render_prompt(definition)


def test_unknown_supplied_variable_is_rejected() -> None:
    definition = make_definition(
        "Write about {product}",
        [PromptVariable(name="product")],
    )

    with pytest.raises(PromptRenderError, match="Unknown prompt variables"):
        render_prompt(
            definition,
            {
                "product": "OEM backpack",
                "unknown": "value",
            },
        )


def test_undeclared_template_variable_is_rejected() -> None:
    definition = make_definition(
        "Write about {product}",
        [],
    )

    with pytest.raises(PromptRenderError, match="undeclared variables"):
        render_prompt(definition)


def test_duplicate_placeholder_is_rendered() -> None:
    definition = make_definition(
        "{product} is a custom {product}",
        [PromptVariable(name="product")],
    )

    rendered = render_prompt(definition, {"product": "bag"})

    assert rendered.text == "bag is a custom bag"


def test_complex_placeholder_is_rejected() -> None:
    definition = make_definition(
        "Write about {product.name}",
        [PromptVariable(name="product")],
    )

    with pytest.raises(PromptRenderError, match="Complex placeholder"):
        render_prompt(definition, {"product": "bag"})


def test_invalid_template_syntax_is_rejected() -> None:
    definition = make_definition(
        "Write about {product",
        [PromptVariable(name="product")],
    )

    with pytest.raises(PromptRenderError, match="invalid placeholder syntax"):
        render_prompt(definition, {"product": "bag"})
