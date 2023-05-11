"""Test settings."""

# Source
from src.settings import KeyWordTrainSettings


def test_settings_init():
    """Test initialize settings."""
    settings = KeyWordTrainSettings()
    assert settings.NEPTUNE_PROJECT == "onclusive/keywords"
