from pathlib import Path

WRAPPERS: dict[Path, str] = {
    Path("app/core/config.py"): (
        "from tmb_ai_os.config import Settings, get_settings\n\n"
        "settings = get_settings()\n\n"
        '__all__ = ["Settings", "get_settings", "settings"]\n'
    ),
    Path("app/providers/base.py"): (
        "from tmb_ai_os.provider_contracts import (\n"
        "    ContentProvider,\n"
        "    GenerationRequest,\n"
        "    GenerationResponse,\n"
        ")\n\n"
        "__all__ = [\n"
        '    "ContentProvider",\n'
        '    "GenerationRequest",\n'
        '    "GenerationResponse",\n'
        "]\n"
    ),
    Path("app/providers/factory.py"): (
        "from tmb_ai_os.config import get_settings\n"
        "from tmb_ai_os.provider_adapter import "
        "TextGeneratorProviderAdapter\n"
        "from tmb_ai_os.provider_factory import "
        "create_text_generator\n\n"
        "\n"
        "def get_provider() -> TextGeneratorProviderAdapter:\n"
        "    settings = get_settings()\n"
        "    generator = create_text_generator(settings=settings)\n"
        "    return TextGeneratorProviderAdapter(\n"
        "        generator=generator,\n"
        "        settings=settings,\n"
        "    )\n\n"
        "\n"
        '__all__ = ["get_provider"]\n'
    ),
}


def main() -> None:
    for path, wrapper in WRAPPERS.items():
        if not path.exists():
            raise SystemExit(f"Missing expected legacy file: {path}")

        backup = path.with_suffix(path.suffix + ".milestone4_1.bak")
        current = path.read_text(encoding="utf-8")

        if not backup.exists():
            backup.write_text(current, encoding="utf-8")

        path.write_text(wrapper, encoding="utf-8")
        print(f"Migrated: {path}")
        print(f"Backup:   {backup}")

    print("Milestone 4.2 config/provider migration applied")


if __name__ == "__main__":
    main()
