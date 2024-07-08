"""Testing tools."""

# Standard Library
import contextlib
from typing import Callable, Generator

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


def get_override_settings_context_manager(
    get_settings: Callable[[], OnclusiveBaseSettings]
) -> Callable:
    """Override settings context manager.

    Args:
        get_settings (Callable[[], BaseSettings]): function that returns settings.
    """

    @contextlib.contextmanager
    def override_settings(**overrides: dict) -> Generator:
        """Overrides pydantic settings values.

        Args:
            **overrides (dict): dictionary of values to override.
        """
        settings = get_settings()
        original = dict()

        try:
            for k, v in overrides.items():
                original[k] = getattr(settings, k)
                setattr(settings, k, v)

            yield
        finally:
            for k, v in original.items():
                setattr(settings, k, v)

    return override_settings
