"""Database table."""

# Standard Library
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# 3rd party libraries
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model
from pynamodb.settings import OperationSettings

# Source
from src.settings import settings


class BaseTable(Model):
    """Base Table."""

    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(null=False)

    class Meta:
        host = settings.DB_HOST if settings.ENVIRONMENT in ["local", "ci"] else None
        region = settings.AWS_REGION

    def save(
        self,
        condition: Optional[Condition] = None,
        settings: OperationSettings = OperationSettings.default,
    ) -> Dict[str, Any]:
        """Save elememt in table."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc)
        return super().save(condition, settings)
