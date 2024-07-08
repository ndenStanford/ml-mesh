"""Metaclasses."""

# Standard Library
from typing import Any, Optional, cast


class Singleton(type):
    """Singleton metaclass.

    Use this metaclass to make any class into a singleton class:

    ```python
    class OneRing(metaclass=SingletonMetaclass):
        def __init__(self, owner):
            self._owner = owner
        @property
        def owner(self):
            return self._owner
    the_one_ring = OneRing('Sauron')
    the_lost_ring = OneRing('Frodo')
    print(the_lost_ring.owner)  # Sauron
    OneRing._clear() # ring destroyed
    ```
    """

    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        """Initialize a singleton class.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        cls.__singleton_instance: Optional["Singleton"] = None

    def __call__(cls, *args: Any, **kwargs: Any) -> "Singleton":
        """Create or return the singleton instance.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The singleton instance.
        """
        if not cls.__singleton_instance:
            cls.__singleton_instance = cast(
                "Singleton", super().__call__(*args, **kwargs)
            )

        return cls.__singleton_instance

    def _clear(cls) -> None:
        """Clear the singleton instance."""
        cls.__singleton_instance = None
