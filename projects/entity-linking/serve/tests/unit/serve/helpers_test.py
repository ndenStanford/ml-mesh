"""Helpers test."""

# 3rd party libraries
import pytest

# Source
from src.serve.helpers import entity_text_match


@pytest.mark.parametrize(
    "rhs, lhs, expected",
    [
        ("Google is awesome", "Google", True),
        ("Onclusive's automated media monitoring platform.", "Onclusive", True),
        ("apple is a fruit.", "Apple", False),
    ],
)
def test_entity_text_match(lhs, rhs, expected):
    """Test helper function entity text match."""
    assert entity_text_match(lhs, rhs) == expected
