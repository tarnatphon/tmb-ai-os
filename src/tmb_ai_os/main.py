from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .api import app as api_app


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield


app = api_app
app.title = "TMB AI OS"
app.version = "0.4.0"
app.router.lifespan_context = lifespan


DASHBOARD_HTML = """
<!doctype html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >
    <title>TMB AI OS</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            max-width: 1080px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f7f4ed;
            color: #24352b;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 18px;
        }

        code {
            background: #eef1ec;
            padding: 2px 6px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>TMB AI OS v0.4</h1>
        <p>Unified application architecture is active.</p>
        <p>
            API documentation:
            <a href="/docs"><code>/docs</code></a>
        </p>
    </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> str:
    return DASHBOARD_HTML
