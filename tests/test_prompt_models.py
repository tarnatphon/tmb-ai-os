from tmb_ai_os.prompt_models import (
    PromptDefinition,
    PromptMetadata,
    PromptVariable,
    RenderedPrompt,
)


def test_prompt_variable_defaults() -> None:
    variable = PromptVariable(name="topic")

    assert variable.name == "topic"
    assert variable.description == ""
    assert variable.required is True
    assert variable.default is None


def test_prompt_definition() -> None:
    metadata = PromptMetadata(name="marketing-post")
    variable = PromptVariable(name="topic")
    definition = PromptDefinition(
        metadata=metadata,
        template="Write about {topic}",
        variables=[variable],
    )

    assert definition.metadata.name == "marketing-post"
    assert definition.template == "Write about {topic}"
    assert definition.variables == [variable]


def test_rendered_prompt() -> None:
    rendered = RenderedPrompt(
        text="Write about OEM bags",
        variables={"topic": "OEM bags"},
    )

    assert rendered.text == "Write about OEM bags"
    assert rendered.variables == {"topic": "OEM bags"}
