"""Celery app for async/background work: batch re-checks when a new
interaction is added to RxNorm's dataset, or literature re-ingestion jobs
that are too slow to run inline with a request."""
from celery import Celery

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "rxsentinel",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
