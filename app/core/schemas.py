from pydantic import BaseModel


class GenerateRequest(BaseModel):
    topic: str | None = None
    pillar: str | None = None
    language: str = "th"
    trend_context: str | None = None


class MarkdownContent(BaseModel):
    topic: str
    pillar: str
    markdown: str
    provider: str
    model: str
