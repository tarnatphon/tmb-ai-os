from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .api_v2 import router as milestone_2_router
from .config import get_settings
from .content import ContentRepository
from .providers import GeminiGenerator
from .service import ContentGenerationService

app = FastAPI(title="TMB AI OS", version="0.1.0")
app.include_router(milestone_2_router)


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
