import pytest

from tools.tmb import main
from tools.tmb.cli import build_parser
from tools.tmb.registry import COMMANDS


def test_registry_contains_validate_command() -> None:
    assert [command.name for command in COMMANDS] == ["validate"]


def test_validate_appears_in_help() -> None:
    help_text = build_parser().format_help()

    assert "validate" in help_text
    assert "Validate the TMB AI OS repository." in help_text


def test_validate_command_dispatches(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["validate"]) == 0
    assert capsys.readouterr().out == "Repository validation PASSED\n"


def test_unknown_command_returns_usage_error() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["unknown-command"])

    assert exc_info.value.code == 2
