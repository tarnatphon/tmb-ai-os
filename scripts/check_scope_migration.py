from pathlib import Path

PROTECTED_FILES = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)


def main() -> None:
    missing: list[str] = []

    for path in PROTECTED_FILES:
        text = path.read_text(encoding="utf-8")
        if "scope_dependency" not in text:
            missing.append(f"Scope dependency missing in {path}")

    if missing:
        raise SystemExit("\n".join(missing))

    print("Scope migration check passed")


if __name__ == "__main__":
    main()
