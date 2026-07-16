from pathlib import Path
import re

FILES = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)

LEGACY_PATTERN = re.compile(r"(?<!unified_)(?<!scoped_)permission_dependency\(")

SUPPORTED_DEPENDENCIES = (
    "unified_permission_dependency(",
    "scoped_permission_dependency(",
)


def main() -> None:
    failures: list[str] = []

    for path in FILES:
        text = path.read_text(encoding="utf-8")

        if LEGACY_PATTERN.search(text):
            failures.append(
                f"Legacy permission dependency remains in {path}"
            )

        if not any(name in text for name in SUPPORTED_DEPENDENCIES):
            failures.append(
                f"Supported auth dependency missing in {path}"
            )

    if failures:
        raise SystemExit("\n".join(failures))

    print("Authentication migration check passed")


if __name__ == "__main__":
    main()
