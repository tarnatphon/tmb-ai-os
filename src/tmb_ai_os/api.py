from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .admin_dashboard import router as admin_dashboard_router
from .api_v2 import router as milestone_2_router
from .api_v3 import router as milestone_3_router
from .api_v4 import router as milestone_4_router
from .api_v5 import router as milestone_5_router
from .api_v6 import router as milestone_6_router
from .api_v7 import router as milestone_7_router
from .api_v8 import router as milestone_8_router
from .api_v9 import router as milestone_9_router
from .api_v10 import router as milestone_10_router
from .api_v11 import router as milestone_11_router
from .api_v12 import router as milestone_12_router
from .api_v13 import router as milestone_13_router
from .api_v14 import router as milestone_14_router
from .api_v15 import router as milestone_15_router
from .api_v16 import router as milestone_16_router
from .api_v17 import router as milestone_17_router
from .api_v18 import router as milestone_18_router
from .api_v19 import router as milestone_19_router
from .api_v20 import router as milestone_20_router
from .api_v21 import router as milestone_21_router
from .api_v22 import router as milestone_22_router
from .api_v23 import router as milestone_23_router
from .api_v24 import router as milestone_24_router
from .config import get_settings
from .content import ContentRepository
from .providers import GeminiGenerator
from .service import ContentGenerationService

app = FastAPI(title="TMB AI OS", version="0.1.0")
app.include_router(milestone_2_router)
app.include_router(milestone_3_router)
app.include_router(milestone_4_router)
app.include_router(milestone_5_router)
app.include_router(milestone_6_router)
app.include_router(milestone_7_router)
app.include_router(milestone_8_router)
app.include_router(milestone_9_router)
app.include_router(milestone_10_router)
app.include_router(milestone_11_router)
app.include_router(milestone_12_router)
app.include_router(milestone_13_router)
app.include_router(milestone_14_router)
app.include_router(milestone_15_router)
app.include_router(milestone_16_router)
app.include_router(milestone_17_router)
app.include_router(milestone_18_router)
app.include_router(milestone_19_router)
app.include_router(milestone_20_router)
app.include_router(milestone_21_router)
app.include_router(milestone_22_router)
app.include_router(milestone_23_router)
app.include_router(milestone_24_router)
app.include_router(admin_dashboard_router)


class GenerateRequest(BaseModel):
    path: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/content")
def list_content() -> dict[str, list[str]]:
    settings = get_settings()
    repository = ContentRepository(settings.content_dir)
    return {"items": [str(path) for path in repository.list_markdown()]}


@app.post("/v1/generate")
def generate(request: GenerateRequest) -> dict[str, str]:
    settings = get_settings()
    path = Path(request.path)
    try:
        repository = ContentRepository(settings.content_dir)
        generator = GeminiGenerator(settings)
        service = ContentGenerationService(
            repository=repository,
            generator=generator,
            output_dir=settings.output_dir,
            model_name=settings.gemini_model,
        )
        result = service.generate_from_file(path)
        return {"model": result.model, "text": result.text}
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
