"""DynamoDB Tables"""

# 3rd party libraries
from pynamodb.attributes import UnicodeAttribute

# Source
from src.db import BaseTable


class ModelTemplateTable(BaseTable):
    """Dynamodb table for Model."""

    class Meta(BaseTable.Meta):
        table_name = "model_template"

    template = UnicodeAttribute(null=False)
