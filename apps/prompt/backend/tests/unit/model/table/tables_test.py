"""Model tables test."""

# Standard Library
from unittest.mock import patch

# Source
from src.model.tables import ModelTable
from src.settings import get_settings


def test_base_table():
    """Test BaseTable object."""
    # Note keys are returned in alphabetical order
    assert list(ModelTable._attributes.keys()) == [
        "created_at",
        "id",
        "max_tokens",
        "model_name",
        "temperature",
    ]
    assert ModelTable._hash_keyname == "id"


def test_base_table_meta():
    """Test BaseTable Meta data."""
    settings = get_settings()
    assert ModelTable.Meta.host == settings.DB_HOST
    assert ModelTable.Meta.region == settings.AWS_REGION


@patch("src.db.Model.save")
def test_base_table_save(mock_save):
    """Test BaseTable Meta data."""
    _ = ModelTable().save()
    mock_save.assert_called_once()
