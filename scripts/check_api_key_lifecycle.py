from pathlib import Path

REQUIRED_FILES = (
    Path("src/tmb_ai_os/api_key_lifecycle_models.py"),
    Path("src/tmb_ai_os/api_key_lifecycle.py"),
    Path("src/tmb_ai_os/lifecycle_auth.py"),
    Path("src/tmb_ai_os/api_v25.py"),
)


def main() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise SystemExit("Missing lifecycle files:\n" + "\n".join(missing))

    api_text = Path("src/tmb_ai_os/api.py").read_text(encoding="utf-8")
    database_text = Path("src/tmb_ai_os/database.py").read_text(encoding="utf-8")

    required_fragments = (
        "milestone_25_router",
        "app.include_router(milestone_25_router)",
    )

    failures = [fragment for fragment in required_fragments if fragment not in api_text]

    if "api_key_lifecycle_models" not in database_text:
        failures.append("api_key_lifecycle_models registration")

    if failures:
        raise SystemExit("API key lifecycle validation failed:\n" + "\n".join(failures))

    print("API key lifecycle check passed")


if __name__ == "__main__":
    main()
