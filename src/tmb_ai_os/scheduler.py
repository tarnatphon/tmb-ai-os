from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore[import-untyped]

from .config import Settings, get_settings

JobCallable = Callable[[], Any]


@dataclass(frozen=True)
class SchedulerState:
    enabled: bool
    running: bool
    timezone: str


def build_scheduler(settings: Settings) -> BackgroundScheduler:
    return BackgroundScheduler(timezone=settings.app_timezone)


settings = get_settings()
scheduler = build_scheduler(settings)


def register_daily_job(
    function: JobCallable,
    *,
    job_id: str,
    hour: int | None = None,
    minute: int | None = None,
) -> None:
    resolved_hour = settings.scheduler_hour if hour is None else hour
    resolved_minute = settings.scheduler_minute if minute is None else minute

    scheduler.add_job(
        function,
        trigger="cron",
        id=job_id,
        replace_existing=True,
        hour=resolved_hour,
        minute=resolved_minute,
    )


def start_scheduler() -> SchedulerState:
    if not settings.scheduler_enabled:
        return get_scheduler_state()

    if not scheduler.running:
        scheduler.start()

    return get_scheduler_state()


def stop_scheduler(*, wait: bool = False) -> SchedulerState:
    if scheduler.running:
        scheduler.shutdown(wait=wait)

    return get_scheduler_state()


def get_scheduler_state() -> SchedulerState:
    return SchedulerState(
        enabled=settings.scheduler_enabled,
        running=scheduler.running,
        timezone=settings.app_timezone,
    )
