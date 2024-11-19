"""Table tests."""

# Standard Library
import os
from unittest.mock import patch

# 3rd party libraries
import pytest
from dyntastic import Dyntastic

# Source
from src.generated.exceptions import GeneratedInvalidId
from src.generated.tables import Generated


@pytest.mark.parametrize(
    "id",
    [
        "e2978fg1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42uy-928a-c9e59k5oapt",
    ],
)
def test_valid_id(id):
    """Test valid id."""
    _ = Generated(id=id)


@pytest.mark.parametrize(
    "id",
    [
        "e2678cc1-08ec-42uy-928a-c9e59k5o*&t",
    ],
)
def test_invalid_id(id):
    """Test valid id."""
    with pytest.raises(GeneratedInvalidId):
        _ = Generated(id=id)


@pytest.mark.parametrize(
    "id",
    [
        "e2978fg1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42uy-928a-c9e59k5oapt",
    ],
)
@patch.object(Dyntastic, "save")
def test_save(mock_dyntastic_save, id):
    """Test save."""
    # call
    generated = Generated(id=id)
    generated.save()
    # asserts
    mock_dyntastic_save.assert_called_once()


@pytest.mark.parametrize(
    "id",
    [
        "e2978fg1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42uy-928a-c9e59k5oapt",
    ],
)
@patch.object(Dyntastic, "delete")
def test_delete(mock_dyntastic_delete, id):
    """Test delete."""
    # call
    generated = Generated(id=id)
    generated.delete()
    # asserts
    mock_dyntastic_delete.assert_called_once()
