from pathlib import Path


def test_dashboard_uses_scoped_authentication() -> None:
    for filename in ("api_v18.py", "api_v19.py"):
        text = (Path("src/tmb_ai_os") / filename).read_text(encoding="utf-8")

        assert "scope_dependency" in text
        assert "from .scoped_auth import scope_dependency" in text
        assert "unified_permission_dependency" not in text
        assert "from .security_dependencies import permission_dependency" not in text
