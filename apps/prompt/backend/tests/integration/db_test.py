"""Database test."""

# 3rd party libraries
import pytest

# Source
from src.db import BaseTable


def test_base_table_save():
    element = BaseTable()
    # cannot save with a base table class
    with pytest.raises(AttributeError):
        _ = element.save()
