from pathlib import Path


def test_dashboard_uses_unified_authentication() -> None:
    for filename in ("api_v18.py", "api_v19.py"):
        text = (Path("src/tmb_ai_os") / filename).read_text(encoding="utf-8")

        assert "unified_permission_dependency" in text
        assert "from .security_dependencies import permission_dependency" not in text
