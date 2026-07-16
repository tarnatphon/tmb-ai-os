from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")
MAIN_FILE = Path("src/tmb_ai_os/main.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v11 import router as milestone_11_router\n"
    include_line = "app.include_router(milestone_11_router)\n"

    if import_line not in text:
        marker = "from .api_v10 import router as milestone_10_router\n"
        if marker not in text:
            raise SystemExit("Milestone 10 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_10_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 10 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_config() -> None:
    text = CONFIG_FILE.read_text(encoding="utf-8")

    fields = (
        "    rate_limit_requests: int = 60\n",
        "    rate_limit_window_seconds: int = 60\n",
        "    require_secure_api_key: bool = True\n",
    )

    marker = '    api_role: str = "admin"\n'
    if marker not in text:
        raise SystemExit("Security settings marker was not found")

    addition = "".join(field for field in fields if field.strip() not in text)
    if addition:
        text = text.replace(marker, marker + addition)

    CONFIG_FILE.write_text(text, encoding="utf-8")


def patch_main() -> None:
    text = MAIN_FILE.read_text(encoding="utf-8")

    import_line = "from .middleware import RateLimitMiddleware, RequestContextMiddleware\n"
    if import_line not in text:
        marker = "from .lifecycle import application_lifespan\n"
        if marker not in text:
            raise SystemExit("Main middleware import marker was not found")
        text = text.replace(marker, marker + import_line)

    middleware_lines = (
        "app.add_middleware(RequestContextMiddleware)\napp.add_middleware(RateLimitMiddleware)\n"
    )
    if middleware_lines not in text:
        marker = "app.router.lifespan_context = application_lifespan\n"
        if marker not in text:
            raise SystemExit("Main middleware insertion marker was not found")
        text = text.replace(
            marker,
            marker + middleware_lines,
        )

    MAIN_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_config()
    patch_main()
    print("Milestone 5.2 security hardening added")


if __name__ == "__main__":
    main()
