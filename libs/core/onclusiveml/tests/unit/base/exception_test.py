"""Exception test."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class DummyException(OnclusiveException):
    """Dummy exception."""

    message_format = "Raise {code} with {description}."


def test_kwargs():
    """Test parsed keyword arguments."""
    e = DummyException(code=200, description="OK")

    assert e.kwargs == ["code", "description"]
    assert e._param_dct() == {"code": 200, "description": "OK"}


def test_simple_message():
    """Test simple message formatting."""
    e = DummyException(code=200, description="OK")
    assert e
    assert e.message == "Raise 200 with OK."
    assert str(e) == "Raise 200 with OK."
