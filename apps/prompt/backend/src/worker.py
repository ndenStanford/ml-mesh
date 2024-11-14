"""Celery Worker."""

# 3rd party libraries
from celery.app import Celery

# Source
from src.settings import get_settings


settings = get_settings()
# Configure Celery app
celery_app = Celery(
    settings.API_NAME,
    broker=settings.REDIS_CONNECTION_STRING, 
    backend=settings.DOCUMENTDB_HOST, 
    include=["src.prompt.functional"],
)
# define task settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)