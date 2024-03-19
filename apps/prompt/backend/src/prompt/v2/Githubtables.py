"""Github Tables."""

# 3rd party libraries
from pydantic import BaseModel


class GithubTemplateTable(BaseModel):
    """table for Project Templates."""

    alias: str
