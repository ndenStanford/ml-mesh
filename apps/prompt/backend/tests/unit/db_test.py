"""Database test."""

# Standard Library
from unittest.mock import patch

# Source
from src.db import BaseTable
from src.settings import get_settings


def test_base_table():
    """Test BaseTable object."""
    assert list(BaseTable._attributes.keys()) == ["created_at", "id"]
    assert BaseTable._hash_keyname == "id"


def test_base_table_meta():
    """Test BaseTable Meta data."""
    settings = get_settings()
    assert BaseTable.Meta.host == settings.DB_HOST
    assert BaseTable.Meta.region == settings.AWS_REGION


@patch("src.db.Model.save")
def test_base_table_save(mock_save):
    """Test BaseTable Meta data."""
    _ = BaseTable().save()
    mock_save.assert_called_once()
