from __future__ import annotations

import argparse
import re
import sys

MODULE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new TMB AI OS module.")
    parser.add_argument("module_name", help="Module name in snake_case")

    args = parser.parse_args()

    if not MODULE_PATTERN.fullmatch(args.module_name):
        print(
            "ERROR: Module name must use snake_case.",
            file=sys.stderr,
        )
        return 1

    print(f"Module name accepted: {args.module_name}")
    print("Module generation will be implemented in the next step.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
