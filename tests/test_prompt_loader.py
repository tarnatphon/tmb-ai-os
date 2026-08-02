from pathlib import Path

import pytest

from tmb_ai_os.prompt_loader import PromptLoadError, load_prompt


def write_prompt(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_load_prompt_definition(tmp_path: Path) -> None:
    path = write_prompt(
        tmp_path / "facebook.yaml",
        """
name: marketing.facebook
version: 1.2.0
author: Marketing Team
description: Facebook content prompt
template: "Write a post about {product}"
variables:
  - name: product
    description: Product name
    required: true
  - name: tone
    required: false
    default: professional
""".strip(),
    )

    definition = load_prompt(path)

    assert definition.metadata.name == "marketing.facebook"
    assert definition.metadata.version == "1.2.0"
    assert definition.metadata.author == "Marketing Team"
    assert definition.template == "Write a post about {product}"
    assert len(definition.variables) == 2
    assert definition.variables[0].name == "product"
    assert definition.variables[0].required is True
    assert definition.variables[1].default == "professional"


def test_load_prompt_uses_metadata_defaults(tmp_path: Path) -> None:
    path = write_prompt(
        tmp_path / "minimal.yaml",
        """
name: marketing.minimal
template: "Create content"
""".strip(),
    )

    definition = load_prompt(path)

    assert definition.metadata.version == "1.0.0"
    assert definition.metadata.author == "Thai Modern Bags AI"
    assert definition.metadata.description == ""
    assert definition.variables == []


def test_missing_prompt_file() -> None:
    with pytest.raises(PromptLoadError, match="does not exist"):
        load_prompt("missing-prompt.yaml")


def test_invalid_yaml(tmp_path: Path) -> None:
    path = write_prompt(tmp_path / "invalid.yaml", "name: [broken")

    with pytest.raises(PromptLoadError, match="Invalid YAML"):
        load_prompt(path)


def test_missing_required_name(tmp_path: Path) -> None:
    path = write_prompt(
        tmp_path / "missing-name.yaml",
        """
template: "Create content"
""".strip(),
    )

    with pytest.raises(PromptLoadError, match="'name'"):
        load_prompt(path)


def test_variables_must_be_a_list(tmp_path: Path) -> None:
    path = write_prompt(
        tmp_path / "invalid-variables.yaml",
        """
name: marketing.invalid
template: "Create content"
variables: invalid
""".strip(),
    )

    with pytest.raises(PromptLoadError, match="'variables' must be a list"):
        load_prompt(path)


def test_variable_required_must_be_boolean(tmp_path: Path) -> None:
    path = write_prompt(
        tmp_path / "invalid-required.yaml",
        """
name: marketing.invalid
template: "Create content"
variables:
  - name: product
    required: "yes"
""".strip(),
    )

    with pytest.raises(PromptLoadError, match="must be a boolean"):
        load_prompt(path)
