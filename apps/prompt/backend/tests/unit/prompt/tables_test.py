"""Prompt tables test."""

# Standard Library
from unittest.mock import patch

# Source
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


def test_base_table():
    """Test BaseTable object."""
    assert list(PromptTemplateTable._attributes.keys()) == [
        "alias",
        "created_at",
        "id",
        "parameters",
        "template",
        "version",
    ]
    assert PromptTemplateTable._hash_keyname == "alias"


def test_base_table_meta():
    """Test BaseTable Meta data."""
    settings = get_settings()
    assert PromptTemplateTable.Meta.host == settings.DB_HOST
    assert PromptTemplateTable.Meta.region == settings.AWS_REGION


@patch("src.db.Model.save")
def test_base_table_save(mock_save):
    """Test BaseTable Meta data."""
    _ = PromptTemplateTable().save()
    mock_save.assert_called_once()
