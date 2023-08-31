"""Timing decorator tests."""

# Internal libraries
from onclusiveml.core.timing import timing_decorator


def test_timing_decorator(caplog):
    """Test timing decorator."""

    @timing_decorator
    def some_func(content: str) -> str:
        return "Processing content: " + content

    result = some_func("This is an example string")
    assert result == "Processing content: This is an example string"
    assert "Total Time in milliseconds =" in caplog.text


def test_timing_decorator_no_return(caplog):
    """Test timing decorator with no return."""

    @timing_decorator
    def some_func_no_return(content: str) -> str:
        print("Processing content: " + content)

    result = some_func_no_return("This is an example string")
    assert result is None
    assert "Total Time in milliseconds =" in caplog.text
