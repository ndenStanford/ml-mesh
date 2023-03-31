"""Database table."""

from pynamodb.models import Model
from src.settings import settings


class BaseTable(Model):
    """Base Table."""

    class Meta:
        host = settings.DB_HOST if settings.ENVIRONMENT in ["local", "ci"] else None
        region = settings.AWS_REGION
