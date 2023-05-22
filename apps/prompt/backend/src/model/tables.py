"""DynamoDB Tables"""

# 3rd party libraries
from pynamodb.attributes import UnicodeAttribute

# Source
from src.db import BaseTable


class ModelTable(BaseTable):
    """Dynamodb table for Model."""

    class Meta(BaseTable.Meta):
        table_name = "model"

    model_name = UnicodeAttribute(null=False, hash_key=True)
    parameters = UnicodeAttribute(null=True)
