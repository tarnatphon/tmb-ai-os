from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Admin Dashboard"])

STATIC_DIR = Path(__file__).parent / "static"
LOGIN_FILE = STATIC_DIR / "admin_login.html"
DASHBOARD_FILE = STATIC_DIR / "admin.html"


@router.get("/admin/login", response_class=HTMLResponse)
def admin_login() -> str:
    return LOGIN_FILE.read_text(encoding="utf-8")


@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard() -> str:
    return DASHBOARD_FILE.read_text(encoding="utf-8")
