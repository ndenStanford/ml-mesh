"""Exception test."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class DummyException(OnclusiveException):
    message_format = "Raise {code} with {description}."


def kwargs_test():
    """Test parsed keyword arguments."""
    e = DummyException(code=200, description="OK")

    assert e.kwargs == ["code", "description"]
    assert e._param_dct() == {"code": 200, "description": "OK"}


def simple_message_test():
    """Test simple message formatting."""
    e = DummyException(code=200, description="OK")
    assert e
    assert e.message == "Raise 200 with OK."
    assert str(e) == "Raise 200 with OK."
