"""Celery App."""

# 3rd party libraries
from celery.app import Celery

# Source
from src.settings import get_settings


settings = get_settings()
# Configure Celery app
celery_app = Celery(
    settings.API_NAME,
    broker=settings.REDIS_CONNECTION_STRING,  # Replace with your actual broker URL
    backend=settings.DOCUMENTDB_HOST,  # Replace with your actual result backend URL
    include=["src.prompt.functional"],
)
# Load task settings from a configuration module, if you have one
celery_app.conf.update(
    broker_url=settings.REDIS_CONNECTION_STRING,
    result_backend=settings.DOCUMENTDB_HOST,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    # Start the worker when this script is run
    celery_app.worker_main()
