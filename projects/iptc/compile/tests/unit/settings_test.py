"""Settings test."""

# Standard Library
from unittest import TestCase

# Source
from src.settings import get_settings


class SettingsTest(TestCase):
    """Settings test."""

    def test_initialisation(self) -> None:
        """Test initialize settings."""
        settings = get_settings()
        assert isinstance(settings.model_dump(), dict)
        assert isinstance(settings.model_dump_json(), str)
