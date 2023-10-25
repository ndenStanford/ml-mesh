"""Pydantic base objects tests."""

# 3rd party libraries
import pytest
from pydantic import ValidationError

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSchema, OnclusiveBaseSettings


class TestSettings(OnclusiveBaseSettings):
    """Test settings."""

    setting1: str
    setting2: int


class TestModel(OnclusiveBaseSchema):
    """Test model."""

    attribute1: int
    attribute2: bool


def test_settings_init():
    """Test object initialization."""
    test = TestSettings(setting1="a", setting2=12)

    assert isinstance(test.setting1, str)
    assert isinstance(test.setting2, int)


def test_settings_type_conversion():
    """Test object modified behaviour."""
    test = TestSettings(setting1="a", setting2="123")

    assert isinstance(test.setting1, str)
    assert isinstance(test.setting2, int)


def test_settings_extras():
    """Test object modified behaviour."""
    with pytest.raises(ValidationError):
        _ = TestSettings(setting1="a", setting2=12, settings3=False)


def test_settings_type_validation():
    """Test object modified behaviour."""
    with pytest.raises(ValidationError):
        _ = TestSettings(setting1=100, setting2="qq")


def test_model_init():
    """Test object initialization."""
    test = TestModel(attribute1=100, attribute2=True)

    assert isinstance(test.attribute1, int)
    assert isinstance(test.attribute2, bool)


def test_model_type_conversion():
    """Test object modified behaviour."""
    test = TestModel(attribute1="234", attribute2="no")

    assert isinstance(test.attribute1, int)
    assert isinstance(test.attribute2, bool)


def test_model_extras():
    """Test object modified behaviour."""
    with pytest.raises(ValidationError):
        _ = TestModel(attribute1="a", attribute2=12, attribute3="ok")


def test_model_type_validation():
    """Test object modified behaviour."""
    with pytest.raises(ValidationError):
        _ = TestModel(attribute1="a", attribute2="a")
