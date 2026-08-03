from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the developer CLI argument parser."""

    return argparse.ArgumentParser(
        prog="tmb",
        description="Developer tooling for TMB AI OS.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the TMB developer CLI."""

    parser = build_parser()
    parser.parse_args(argv)
    return 0
