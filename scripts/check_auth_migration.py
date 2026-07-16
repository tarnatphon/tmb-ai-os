from pathlib import Path

FILES = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)


def main() -> None:
    failures: list[str] = []

    for path in FILES:
        text = path.read_text(encoding="utf-8")
        if "permission_dependency(" in text:
            failures.append(f"Legacy permission dependency remains in {path}")
        if "unified_permission_dependency(" not in text:
            failures.append(f"Unified auth dependency missing in {path}")

    if failures:
        raise SystemExit("\n".join(failures))

    print("Authentication migration check passed")


if __name__ == "__main__":
    main()
