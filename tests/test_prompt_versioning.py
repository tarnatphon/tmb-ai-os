import pytest

from tmb_ai_os.prompt_models import PromptDefinition, PromptMetadata
from tmb_ai_os.prompt_versioning import (
    PromptVersion,
    PromptVersionError,
    resolve_latest_prompt,
)


def make_definition(name: str, version: str) -> PromptDefinition:
    return PromptDefinition(
        metadata=PromptMetadata(
            name=name,
            version=version,
        ),
        template=f"Prompt {name} version {version}",
    )


def test_parse_prompt_version() -> None:
    version = PromptVersion.parse("1.2.3")

    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert str(version) == "1.2.3"


def test_prompt_versions_are_ordered_semantically() -> None:
    assert PromptVersion.parse("2.0.0") > PromptVersion.parse("1.99.99")
    assert PromptVersion.parse("1.10.0") > PromptVersion.parse("1.9.9")
    assert PromptVersion.parse("1.0.1") > PromptVersion.parse("1.0.0")


def test_invalid_version_component_count_is_rejected() -> None:
    with pytest.raises(PromptVersionError, match="major.minor.patch"):
        PromptVersion.parse("1.0")


def test_non_numeric_version_is_rejected() -> None:
    with pytest.raises(PromptVersionError, match="digits only"):
        PromptVersion.parse("1.beta.0")


def test_empty_version_is_rejected() -> None:
    with pytest.raises(PromptVersionError, match="non-empty string"):
        PromptVersion.parse("")


def test_negative_version_component_is_rejected() -> None:
    with pytest.raises(PromptVersionError):
        PromptVersion(major=-1, minor=0, patch=0)


def test_resolve_latest_prompt() -> None:
    definitions = [
        make_definition("marketing.facebook", "1.0.0"),
        make_definition("marketing.facebook", "2.0.0"),
        make_definition("marketing.facebook", "1.5.0"),
    ]

    latest = resolve_latest_prompt(definitions)

    assert latest.metadata.version == "2.0.0"


def test_resolve_latest_prompt_requires_definitions() -> None:
    with pytest.raises(PromptVersionError, match="At least one"):
        resolve_latest_prompt([])


def test_resolve_latest_prompt_rejects_mixed_names() -> None:
    definitions = [
        make_definition("marketing.facebook", "1.0.0"),
        make_definition("marketing.instagram", "2.0.0"),
    ]

    with pytest.raises(PromptVersionError, match="same metadata name"):
        resolve_latest_prompt(definitions)


def test_resolve_latest_prompt_rejects_invalid_version() -> None:
    definitions = [
        make_definition("marketing.facebook", "1.0.0"),
        make_definition("marketing.facebook", "invalid"),
    ]

    with pytest.raises(PromptVersionError):
        resolve_latest_prompt(definitions)
