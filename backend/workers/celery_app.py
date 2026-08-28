
# pyrefly: ignore [missing-import]
from celery import Celery
from backend.core.config import settings

celery_app = Celery(
    "aimforge_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["backend.workers.tasks"]
)

# task_routes removed so default queue is used

from celery.schedules import crontab

# Prevent indefinitely hanging when Redis is unresponsive
celery_app.conf.broker_connection_timeout = 2.0

celery_app.conf.beat_schedule = {
    "fetch_bgmi_updates_every_30_mins": {
        "task": "backend.workers.tasks.fetch_bgmi_updates",
        "schedule": crontab(minute="*/30"),
    },
}
