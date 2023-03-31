"""DynamoDB Tables"""

from datetime import datetime, timezone
from pynamodb.attributes import UTCDateTimeAttribute, UnicodeAttribute
import uuid
from src.db import BaseTable


class PromptTemplateTable(BaseTable):
    """Dynamodb table for Prompt Templates."""

    class Meta(BaseTable.Meta):
        table_name = "prompt_template"

    id = UnicodeAttribute(default=str(uuid.uuid4()), hash_key=True)
    template = UnicodeAttribute(null=False)
    created_at = UTCDateTimeAttribute(default=datetime.now(timezone.utc), null=False)
