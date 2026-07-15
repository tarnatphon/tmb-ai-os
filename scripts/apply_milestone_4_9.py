from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
AUDIT_MODELS_FILE = Path("src/tmb_ai_os/audit_models.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v8 import router as milestone_8_router\n"
    include_line = "app.include_router(milestone_8_router)\n"

    if import_line not in text:
        marker = "from .api_v7 import router as milestone_7_router\n"
        if marker not in text:
            raise SystemExit("Milestone 7 router import was not found")
        text = text.replace(
            marker,
            marker + import_line,
        )

    if include_line not in text:
        marker = "app.include_router(milestone_7_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 7 router registration was not found")
        text = text.replace(
            marker,
            marker + include_line,
        )

    API_FILE.write_text(text, encoding="utf-8")


def patch_queue_model() -> None:
    text = AUDIT_MODELS_FILE.read_text(encoding="utf-8")

    if "attempt_count:" not in text:
        marker = "    scheduled_for: Mapped[datetime | None] = mapped_column(\n"
        index = text.find(marker)
        if index == -1:
            raise SystemExit("Could not find PublishQueueItem insertion marker")

        insert_at = text.find(
            "    created_at:",
            index,
        )
        addition = (
            "    attempt_count: Mapped[int] = mapped_column(\n"
            "        Integer,\n"
            "        default=0,\n"
            "        nullable=False,\n"
            "    )\n"
            "    last_error: Mapped[str | None] = mapped_column(\n"
            "        Text,\n"
            "        nullable=True,\n"
            "    )\n"
        )
        text = text[:insert_at] + addition + text[insert_at:]

    AUDIT_MODELS_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_queue_model()
    print("Milestone 4.9 scheduled publishing added")


if __name__ == "__main__":
    main()
