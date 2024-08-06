"""Metaclasses."""

# Standard Library
import threading
from abc import ABCMeta
from sys import modules
from typing import Any, List, Optional, Type, TypeVar, cast


T = TypeVar("T", bound="ContextMeta")


class Singleton(ABCMeta):
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


class Context(ABCMeta):
    """Metaclass to create objects that behave like context managers."""

    def __new__(cls, name, bases, dct):
        """Overload new operator."""

        def __enter__(self):
            self.__class__.context_class.get_context_stack().append(self)
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.__class__.context_class.get_context_stack().pop()

        dct[__enter__.__name__] = __enter__
        dct[__exit__.__name__] = __exit__

        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, namespace, context_class: Optional[Type] = None):
        if context_class is not None:
            cls._context_class = context_class
        super().__init__(name, bases, namespace)

    def get_context(cls, raise_if_none: bool = True) -> Optional[T]:
        """Returns the last in context object of type ```cls```.

        Args:
            raise_if_none (bool): if `True` raises an error if the
                context stack is empty.

        Returns:
            Optional[T]: context instance if found, None id not
        """
        candidate = None
        try:
            candidate = cls.get_context_stack()[-1]
        except IndexError:
            if raise_if_none:
                raise TypeError(f"No instance of class {cls.__name__} found on stack.")
        return candidate

    def get_context_stack(cls) -> List[T]:
        """Returns a class contexts."""
        context_class = cls.context_class
        # if the class does not have a context
        # yet it is initialized
        if not hasattr(context_class, "contexts"):
            context_class.contexts = threading.local()

        contexts = context_class.contexts
        if not hasattr(contexts, "stack"):
            contexts.stack = []
        return contexts.stack

    @property
    def context_class(cls) -> Type:
        """Resolves the context class."""
        if cls is None:
            raise ValueError(f"Cannot resolve context class {cls}")
        if isinstance(cls._context_class, str):
            cls._context_class = getattr(modules[cls.__module__], cls._context_class)
        return cls._context_class

    def __init_subclass__(cls, **kwargs):  # inherit context class from parent
        super().__init_subclass__(**kwargs)
        cls._context_class = super().context_class

    def __call__(cls, *args, **kwargs):
        """Overload call operator."""
        instance = cls.__new__(cls, *args, **kwargs)
        with instance:
            instance.__init__(*args, **kwargs)
        return instance
