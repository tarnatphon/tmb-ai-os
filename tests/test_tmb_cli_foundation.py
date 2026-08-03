from tools.tmb import main
from tools.tmb.cli import build_parser


def test_cli_main_succeeds_without_arguments() -> None:
    assert main([]) == 0


def test_cli_parser_uses_tmb_program_name() -> None:
    parser = build_parser()

    assert parser.prog == "tmb"
    assert parser.description == "Developer tooling for TMB AI OS."
