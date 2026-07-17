from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v25 import router as milestone_25_router\n"
    include_line = "app.include_router(milestone_25_router)\n"

    if import_line not in text:
        marker = "from .api_v24 import router as milestone_24_router\n"
        if marker not in text:
            raise SystemExit("Milestone 24 router import was not found")
        text = text.replace(marker, marker + import_line, 1)

    if include_line not in text:
        marker = "app.include_router(milestone_24_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 24 router registration was not found")
        text = text.replace(marker, marker + include_line, 1)

    API_FILE.write_text(text, encoding="utf-8")


def patch_database() -> None:
    text = DATABASE_FILE.read_text(encoding="utf-8")

    if "api_key_lifecycle_models" in text:
        return

    function_position = text.find("def initialize_database")
    if function_position == -1:
        raise SystemExit("initialize_database() was not found")

    import_start = text.find(
        "from . import (",
        function_position,
    )
    if import_start == -1:
        raise SystemExit("Grouped model import was not found")

    import_end = text.find("\n    )", import_start)
    if import_end == -1:
        raise SystemExit("Grouped model import end was not found")

    block = text[import_start:import_end]
    lines = block.splitlines()
    names = {line.strip().rstrip(",") for line in lines[1:] if line.strip()}
    names.add("api_key_lifecycle_models")

    rebuilt = "\n".join(
        [
            lines[0],
            *[f"        {name}," for name in sorted(names)],
        ]
    )

    text = text[:import_start] + rebuilt + text[import_end:]
    DATABASE_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_database()
    print("Milestone 6.6 API key lifecycle added")


if __name__ == "__main__":
    main()
