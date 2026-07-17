from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def patch_router() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v24 import router as milestone_24_router\n"
    include_line = "app.include_router(milestone_24_router)\n"

    if import_line not in text:
        possible_markers = (
            "from .api_v23 import router as milestone_23_router\n",
            "from .api_v22 import router as milestone_22_router\n",
        )

        for marker in possible_markers:
            if marker in text:
                text = text.replace(
                    marker,
                    marker + import_line,
                    1,
                )
                break
        else:
            raise SystemExit("ไม่พบตำแหน่งสำหรับเพิ่ม api_v24 router import")

    if include_line not in text:
        possible_markers = (
            "app.include_router(milestone_23_router)\n",
            "app.include_router(milestone_22_router)\n",
        )

        for marker in possible_markers:
            if marker in text:
                text = text.replace(
                    marker,
                    marker + include_line,
                    1,
                )
                break
        else:
            raise SystemExit("ไม่พบตำแหน่งสำหรับลงทะเบียน milestone_24_router")

    API_FILE.write_text(text, encoding="utf-8")


def patch_database() -> None:
    text = DATABASE_FILE.read_text(encoding="utf-8")

    if "authorization_models" in text:
        return

    function_marker = "def initialize_database"
    function_position = text.find(function_marker)

    if function_position == -1:
        raise SystemExit("ไม่พบฟังก์ชัน initialize_database()")

    import_start = text.find(
        "from . import (",
        function_position,
    )

    if import_start == -1:
        raise SystemExit("ไม่พบ grouped model import ภายใน initialize_database()")

    import_end = text.find(
        "\n    )",
        import_start,
    )

    if import_end == -1:
        raise SystemExit("ไม่พบจุดสิ้นสุด grouped model import")

    import_block = text[import_start:import_end]

    lines = import_block.splitlines()
    model_lines = lines[1:]

    indentation = "        "
    model_names = {line.strip().rstrip(",") for line in model_lines if line.strip()}
    model_names.add("authorization_models")

    rebuilt_block = "\n".join(
        [
            lines[0],
            *[f"{indentation}{name}," for name in sorted(model_names)],
        ]
    )

    text = text[:import_start] + rebuilt_block + text[import_end:]

    DATABASE_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_router()
    patch_database()
    print("Milestone 6.5 authorization audit added")


if __name__ == "__main__":
    main()
