from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.schemas import GenerateRequest
from app.services.content_service import generate_content

scheduler = BackgroundScheduler(timezone=settings.app_timezone)


def daily_job():
    db = SessionLocal()
    try:
        generate_content(db, GenerateRequest())
    finally:
        db.close()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            daily_job,
            "cron",
            hour=settings.daily_run_hour,
            minute=settings.daily_run_minute,
            id="daily-content",
            replace_existing=True,
        )
        scheduler.start()
