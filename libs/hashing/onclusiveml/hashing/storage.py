"""Storage."""

# Standard Library
import random
import string
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Optional


def ordered_storage(config: Dict[str, Any], name: Optional[bytes] = None) -> Any:
    """Return ordered storage system based on the specified config.

    The canonical example of such a storage container is
    ``defaultdict(list)``. Thus, the return value of this method contains
    keys and values. The values are ordered lists with the last added
    item at the end.
    """
    tp = config["type"]
    if tp == "dict":
        return DictListStorage(config)


def unordered_storage(config: Dict[str, Any], name: Optional[bytes] = None) -> Any:
    """Return an unordered storage system based on the specified config.

    The canonical example of such a storage container is
    ``defaultdict(set)``. Thus, the return value of this method contains
    keys and values. The values are unordered sets.
    """
    tp = config["type"]
    if tp == "dict":
        return DictSetStorage(config)


class Storage(ABC):
    """Base class for key, value containers where the values are sequences."""

    def __getitem__(self, key: Any) -> Any:
        return self.get(key)

    def __delitem__(self, key: Any) -> Any:
        return self.remove(key)

    def __len__(self) -> Any:
        return self.size()

    def __iter__(self) -> Any:
        for key in self.keys():
            yield key

    def __contains__(self, item: Any) -> Any:
        return item in self

    @abstractmethod
    def keys(self) -> Any:
        """Return an iterator on keys in storage."""
        return []

    @abstractmethod
    def get(self, key: Any) -> Any:
        """Get list of values associated with a key.

        Returns empty list ([]) if `key` is not found
        """
        pass

    def getmany(self, *keys: Any) -> Any:
        """Retrieves many keys."""
        return [self.get(key) for key in keys]

    @abstractmethod
    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> Any:
        """Add `val` to storage against `key`."""
        pass

    @abstractmethod
    def remove(self, *keys: Any) -> Any:
        """Remove `keys` from storage."""
        pass

    @abstractmethod
    def remove_val(self, key: Any, val: Any) -> Any:
        """Remove `val` from list of values under `key`."""
        pass

    @abstractmethod
    def size(self) -> Any:
        """Return size of storage with respect to number of keys."""
        pass

    @abstractmethod
    def itemcounts(self, **kwargs: Any) -> Any:
        """Returns the number of items stored under each key."""
        pass

    @abstractmethod
    def has_key(self, key: Any) -> Any:
        """Determines whether the key is in the storage or not."""
        pass

    def status(self) -> Any:
        """Storage status."""
        return {"keyspace_size": len(self)}

    def empty_buffer(self) -> None:
        """Empty buffer."""
        pass

    def add_to_select_buffer(self, keys: List[Any]) -> None:
        """Query keys and add them to internal buffer."""
        if not hasattr(self, "_select_buffer"):
            self._select_buffer = self.getmany(*keys)
        else:
            self._select_buffer.extend(self.getmany(*keys))

    def collect_select_buffer(self) -> Any:
        """Return buffered query results."""
        if not hasattr(self, "_select_buffer"):
            return []
        buffer = list(self._select_buffer)
        del self._select_buffer[:]
        return buffer


class OrderedStorage(Storage):
    """Ordered storage class."""

    pass


class UnorderedStorage(Storage):
    """Unordered storage class."""

    pass


class DictListStorage(OrderedStorage):
    """This is a wrapper class around ``defaultdict(list)``."""

    def __init__(self, config: Any) -> None:
        self._dict: Any = defaultdict(list)

    def keys(self) -> List[Any]:
        """Return all stored keys."""
        return self._dict.keys()

    def get(self, key: Any) -> List[Any]:
        """Retrieve key from storage."""
        return self._dict.get(key, [])

    def remove(self, *keys: Any) -> None:
        """Remove key from storage."""
        for key in keys:
            del self._dict[key]

    def remove_val(self, key: Any, val: Any) -> None:
        """Remove by value match."""
        self._dict[key].remove(val)

    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> None:
        """Insert multiple values."""
        self._dict[key].extend(vals)

    def size(self) -> int:
        """Dictionary length."""
        return len(self._dict)

    def itemcounts(self, **kwargs: Any) -> Dict[Any, int]:
        """Returns a dict where the keys are the keys of the container.

        The values are the *lengths* of the value sequences stored
        in this container.
        """
        return {k: len(v) for k, v in self._dict.items()}

    def has_key(self, key: Any) -> bool:
        """Checks that key exists in storage."""
        return key in self._dict


class DictSetStorage(UnorderedStorage, DictListStorage):
    """Storage class with python backend.

    This is a wrapper class around ``defaultdict(set)`` enabling
    it to support an API consistent with `Storage`
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self._dict = defaultdict(set)

    def get(self, key: Any) -> List[Any]:
        """Retrieve key value."""
        return self._dict.get(key, set())

    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> None:
        """Insert key values pair in storage."""
        self._dict[key].update(vals)


def _random_name(length: int) -> bytes:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length)).encode(
        "utf8"
    )
