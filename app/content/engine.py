import hashlib
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.content.prompt_loader import load_prompt
from app.core.models import ContentRun
from app.core.schemas import GenerateRequest, MarkdownContent
from app.providers.factory import get_provider
from app.services.topic_service import daily_topic


class DuplicateContentError(RuntimeError):
    pass


@dataclass(frozen=True)
class ContentContext:
    topic: str
    pillar: str
    language: str
    trend_context: str | None
    recent_topics: list[str]


def _history(db: Session, limit: int = 20) -> list[str]:
    rows = db.query(ContentRun).order_by(ContentRun.created_at.desc()).limit(limit).all()
    return [row.topic for row in rows]


def _build_user_prompt(context: ContentContext) -> str:
    recent = "\n".join(f"- {topic}" for topic in context.recent_topics) or "- ไม่มี"
    return f"""สร้างสคริปต์คอนเทนต์พร้อมใช้งานจากข้อมูลต่อไปนี้

หัวข้อ: {context.topic}
Content pillar: {context.pillar}
ภาษา: {context.language}
บริบทเทรนด์: {context.trend_context or "ไม่มี"}
หัวข้อที่ควรหลีกเลี่ยงการเขียนซ้ำ:
{recent}

ส่งกลับเป็น Markdown พร้อมใช้งานเท่านั้น ไม่ต้องส่ง JSON ไม่ต้องอธิบายโครงสร้างข้อมูล และไม่ใช้ code fence
""".strip()


def _fingerprint(markdown: str) -> str:
    normalized = " ".join(markdown.lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def generate_content(db: Session, request: GenerateRequest) -> MarkdownContent:
    default_pillar, default_topic = daily_topic()
    context = ContentContext(
        topic=request.topic or default_topic,
        pillar=request.pillar or default_pillar,
        language=request.language,
        trend_context=request.trend_context,
        recent_topics=_history(db),
    )

    provider = get_provider()
    result = provider.generate(
        system_prompt=load_prompt("content_package"),
        user_prompt=_build_user_prompt(context),
    )
    markdown = result.text.strip()
    fingerprint = _fingerprint(markdown)
    if db.query(ContentRun).filter(ContentRun.fingerprint == fingerprint).first():
        raise DuplicateContentError("Generated content duplicates an existing script")

    content = MarkdownContent(
        topic=context.topic,
        pillar=context.pillar,
        markdown=markdown,
        provider=result.provider,
        model=result.model,
    )
    row = ContentRun(
        topic=content.topic,
        pillar=content.pillar,
        fingerprint=fingerprint,
        payload_json=content.model_dump_json(),
        status="draft",
    )
    db.add(row)
    db.commit()
    return content
