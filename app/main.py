from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, engine
from app.services.scheduler import scheduler, start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    if scheduler.running:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title=settings.app_name,
    version="2.0.0-m1",
    lifespan=lifespan,
)
app.include_router(router, prefix="/api")


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
            font-family: system-ui;
            max-width: 1050px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f7f4ed;
            color: #24352b;
        }

        button {
            background: #305a43;
            color: white;
            border: 0;
            padding: 12px 18px;
            border-radius: 8px;
            cursor: pointer;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 6px 0 14px;
            border: 1px solid #bbb;
            border-radius: 8px;
        }

        .toolbar {
            display: flex;
            gap: 10px;
            margin: 12px 0;
        }

        pre {
            white-space: pre-wrap;
            background: white;
            padding: 22px;
            border-radius: 10px;
            line-height: 1.65;
            min-height: 240px;
        }
    </style>
</head>
<body>
    <h1>TMB AI OS — Content-first</h1>
    <p>
        สร้างสคริปต์ Blog + Social + SEO + Image Prompt
        ในรูปแบบ Markdown พร้อมใช้งาน
    </p>

    <label for="topic">หัวข้อ</label>
    <input
        id="topic"
        placeholder="เช่น รับผลิตกระเป๋าขั้นต่ำ 100 ใบ"
    >

    <div class="toolbar">
        <button onclick="run()">สร้างคอนเทนต์</button>
        <button onclick="copyContent()">คัดลอกทั้งหมด</button>
        <button onclick="downloadContent()">ดาวน์โหลด .md</button>
    </div>

    <pre id="out">พร้อมใช้งาน</pre>

    <script>
        let current = "";

        async function run() {
            const output = document.getElementById("out");
            const topicInput = document.getElementById("topic");

            output.textContent = "กำลังสร้าง...";

            const response = await fetch(
                "/api/content/generate",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        topic: topicInput.value || null
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                output.textContent =
                    data.detail || "เกิดข้อผิดพลาด";
                return;
            }

            current = data.markdown;
            output.textContent = current;
        }

        async function copyContent() {
            if (current) {
                await navigator.clipboard.writeText(current);
            }
        }

        function downloadContent() {
            if (!current) {
                return;
            }

            const blob = new Blob(
                [current],
                {
                    type: "text/markdown;charset=utf-8"
                }
            );
            const link = document.createElement("a");
            const objectUrl = URL.createObjectURL(blob);

            link.href = objectUrl;
            link.download = "tmb-content.md";
            link.click();

            URL.revokeObjectURL(objectUrl);
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML
