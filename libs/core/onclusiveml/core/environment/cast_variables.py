"""Cast variables."""

# Internal libraries
from onclusiveml.core.logging import (
    INFO,
    OnclusiveLogMessageFormat,
    get_default_logger,
)


logger = get_default_logger(
    __name__, fmt_level=OnclusiveLogMessageFormat.DETAILED.name, level=INFO
)


def as_boolean(var_value: str) -> bool:
    """Utility function to cast environment variable values from string to bool.

    Args:
        var_value (str): The environment variable value

    Raises:
        ValueError: Raised when the bool type can not be inferred from the string

    Returns:
        bool: The inferred bool type
    """
    assert isinstance(var_value, str)

    range_true = ("true", "t", "yes", "y")
    range_false = ("false", "f", "no", "n")

    stripped_var_value = var_value.strip()

    if stripped_var_value and stripped_var_value.lower() in range_true:
        return True
    elif stripped_var_value and stripped_var_value.lower() in range_false:
        return False
    elif not stripped_var_value:
        return False
    else:
        raise ValueError(
            f'The environment variable value "{var_value}" is neither in the TRUE '
            f"range {range_true} nor in the FALSE range {range_false}. Are you sure"
            "its a bool-type environment variable?"
        )


def as_float(var_value: str) -> float:
    """Utility function to cast environment variable values from string to float.

    Args:
        var_value (str): The environment variable value

    Raises:
        ValueError: Raised when the environment variable can not be cast to float type

    Returns:
        float_var_value: The cast float value
    """
    assert isinstance(var_value, str)

    try:
        float_var_value = float(var_value)

        return float_var_value

    except ValueError as float_ve:
        logger.error(
            f"The environment variable value {var_value} could not be converted to float."
            "Are you sure its a float-type environment variable?"
        )
        raise float_ve


def as_integer(var_value: str) -> int:
    """Utility function to cast environment variable values from string to integer.

    Args:
        var_value (str): The environment variable value

    Raises:
        ValueError: Raised when the environment variable can not be cast to integer type

    Returns:
        int_var_value (int): The cast integer value
    """
    assert isinstance(var_value, str)

    try:
        int_var_value = int(var_value)

        return int_var_value

    except ValueError as int_ve:
        logger.error(
            f"The environment variable value {var_value} could not be converted to "
            "integer. Are you sure its an integer-type environment variable?"
        )

        raise int_ve
