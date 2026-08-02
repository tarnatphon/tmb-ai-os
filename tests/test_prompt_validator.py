import pytest

from tmb_ai_os.prompt_models import (
    PromptDefinition,
    PromptMetadata,
    PromptVariable,
)
from tmb_ai_os.prompt_validator import (
    PromptValidationError,
    validate_prompt_definition,
)


def make_definition(
    template: str = "Write about {product}",
    variables: list[PromptVariable] | None = None,
) -> PromptDefinition:
    return PromptDefinition(
        metadata=PromptMetadata(name="marketing.facebook"),
        template=template,
        variables=([PromptVariable(name="product")] if variables is None else variables),
    )


def test_valid_definition_passes() -> None:
    validate_prompt_definition(make_definition())


def test_empty_prompt_name_is_rejected() -> None:
    definition = PromptDefinition(
        metadata=PromptMetadata(name=""),
        template="Create content",
    )

    with pytest.raises(PromptValidationError, match="metadata.name"):
        validate_prompt_definition(definition)


def test_empty_version_is_rejected() -> None:
    definition = PromptDefinition(
        metadata=PromptMetadata(
            name="marketing.facebook",
            version="",
        ),
        template="Create content",
    )

    with pytest.raises(PromptValidationError, match="metadata.version"):
        validate_prompt_definition(definition)


def test_empty_template_is_rejected() -> None:
    definition = make_definition(
        template=" ",
        variables=[],
    )

    with pytest.raises(PromptValidationError, match="'template'"):
        validate_prompt_definition(definition)


def test_empty_variable_name_is_rejected() -> None:
    definition = make_definition(
        template="Create content",
        variables=[PromptVariable(name="")],
    )

    with pytest.raises(PromptValidationError, match="variables.name"):
        validate_prompt_definition(definition)


def test_duplicate_variables_are_rejected() -> None:
    definition = make_definition(
        variables=[
            PromptVariable(name="product"),
            PromptVariable(name="product"),
        ],
    )

    with pytest.raises(PromptValidationError, match="Duplicate prompt variable"):
        validate_prompt_definition(definition)


def test_undeclared_placeholder_is_rejected() -> None:
    definition = make_definition(
        template="Write about {product} for {audience}",
        variables=[PromptVariable(name="product")],
    )

    with pytest.raises(PromptValidationError, match="undeclared variables"):
        validate_prompt_definition(definition)


def test_complex_placeholder_is_rejected() -> None:
    definition = make_definition(
        template="Write about {product.name}",
        variables=[PromptVariable(name="product")],
    )

    with pytest.raises(PromptValidationError, match="Complex placeholder"):
        validate_prompt_definition(definition)


def test_invalid_placeholder_syntax_is_rejected() -> None:
    definition = make_definition(
        template="Write about {product",
        variables=[PromptVariable(name="product")],
    )

    with pytest.raises(
        PromptValidationError,
        match="invalid placeholder syntax",
    ):
        validate_prompt_definition(definition)
