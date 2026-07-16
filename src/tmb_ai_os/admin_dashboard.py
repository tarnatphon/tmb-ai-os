from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Admin Dashboard"])
HTML_FILE = Path(__file__).parent / "static" / "admin.html"


@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard() -> str:
    return HTML_FILE.read_text(encoding="utf-8")
