from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from typing import cast

from .registry import register_commands

CommandHandler = Callable[[argparse.Namespace], int]


def build_parser() -> argparse.ArgumentParser:
    """Build the developer CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="tmb",
        description="Developer tooling for TMB AI OS.",
    )
    subparsers = parser.add_subparsers(dest="command")
    register_commands(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the TMB developer CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)

    if handler is None:
        parser.print_help()
        return 0

    return cast(CommandHandler, handler)(args)
