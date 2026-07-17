from pathlib import Path

REQUIRED_FILES = (
    Path("src/tmb_ai_os/api_key_telemetry_models.py"),
    Path("src/tmb_ai_os/api_key_telemetry.py"),
    Path("src/tmb_ai_os/api_key_telemetry_middleware.py"),
    Path("src/tmb_ai_os/api_v26.py"),
)


def main() -> None:
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        raise SystemExit("Missing telemetry files:\n" + "\n".join(missing))

    api_text = Path("src/tmb_ai_os/api.py").read_text(encoding="utf-8")
    database_text = Path("src/tmb_ai_os/database.py").read_text(encoding="utf-8")

    failures: list[str] = []

    if "milestone_26_router" not in api_text:
        failures.append("milestone_26_router import")

    if "app.include_router(milestone_26_router)" not in api_text:
        failures.append("milestone_26_router registration")

    if "api_key_telemetry_models" not in database_text:
        failures.append("api_key_telemetry_models registration")

    if failures:
        raise SystemExit("API key telemetry validation failed:\n" + "\n".join(failures))

    print("API key telemetry check passed")


if __name__ == "__main__":
    main()
