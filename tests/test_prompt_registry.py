import pytest

from tmb_ai_os.prompt_models import (
    PromptDefinition,
    PromptMetadata,
)
from tmb_ai_os.prompt_registry import PromptRegistry


def make_definition(name: str) -> PromptDefinition:
    return PromptDefinition(
        metadata=PromptMetadata(name=name),
        template=f"Prompt for {name}",
    )


def test_register_and_get() -> None:
    registry = PromptRegistry()
    definition = make_definition("facebook")

    registry.register(definition)

    assert registry.get("facebook") is definition


def test_contains() -> None:
    registry = PromptRegistry()

    registry.register(make_definition("seo"))

    assert registry.contains("seo") is True
    assert registry.contains("ads") is False


def test_list_names() -> None:
    registry = PromptRegistry()

    registry.register(make_definition("b"))
    registry.register(make_definition("a"))

    assert registry.list_names() == ["a", "b"]


def test_count() -> None:
    registry = PromptRegistry()

    registry.register(make_definition("facebook"))
    registry.register(make_definition("linkedin"))

    assert registry.count() == 2


def test_duplicate_registration() -> None:
    registry = PromptRegistry()

    registry.register(make_definition("facebook"))

    with pytest.raises(ValueError):
        registry.register(make_definition("facebook"))


def test_unknown_prompt() -> None:
    registry = PromptRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")
