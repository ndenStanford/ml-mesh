"""DynamoDB Tables"""

# 3rd party libraries
from pynamodb.attributes import JSONAttribute, NumberAttribute, UnicodeAttribute

# Source
from src.db import BaseTable


class PromptTemplateTable(BaseTable):
    """Dynamodb table for Prompt Templates."""

    class Meta(BaseTable.Meta):
        table_name = "prompt_template_v2"

    template = UnicodeAttribute(null=False)
    alias = UnicodeAttribute(null=False, default="", hash_key=True)
    version = NumberAttribute(range_key=True, default=0)
    parameters = JSONAttribute(null=False, default={})
