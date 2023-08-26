"""Storage."""

# Standard Library
import binascii
import collections
import itertools
import operator
import os
import random
import string
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


# IMPORTANT: redis has been removed from this version of the script
try:
    # Standard Library
    import logging

    # 3rd party libraries
    import cassandra
    from cassandra import cluster as c_cluster
    from cassandra import concurrent as c_concurrent

    logging.getLogger("cassandra").setLevel(logging.ERROR)
except ImportError:
    cassandra = None
    c_cluster = None
    c_concurrent = None


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
    if tp == "cassandra":
        return CassandraListStorage(config, name=name)


def unordered_storage(config: Dict[str, Any], name: Optional[bytes] = None) -> Any:
    """Return an unordered storage system based on the specified config.

    The canonical example of such a storage container is
    ``defaultdict(set)``. Thus, the return value of this method contains
    keys and values. The values are unordered sets.
    """
    tp = config["type"]
    if tp == "dict":
        return DictSetStorage(config)
    if tp == "cassandra":
        return CassandraSetStorage(config, name=name)


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
        """Return an iterator on keys in storage"""
        return []

    @abstractmethod
    def get(self, key: Any) -> Any:
        """Get list of values associated with a key

        Returns empty list ([]) if `key` is not found
        """
        pass

    def getmany(self, *keys: Any) -> Any:
        return [self.get(key) for key in keys]

    @abstractmethod
    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> Any:
        """Add `val` to storage against `key`"""
        pass

    @abstractmethod
    def remove(self, *keys: Any) -> Any:
        """Remove `keys` from storage"""
        pass

    @abstractmethod
    def remove_val(self, key: Any, val: Any) -> Any:
        """Remove `val` from list of values under `key`"""
        pass

    @abstractmethod
    def size(self) -> Any:
        """Return size of storage with respect to number of keys"""
        pass

    @abstractmethod
    def itemcounts(self, **kwargs: Any) -> Any:
        """Returns the number of items stored under each key"""
        pass

    @abstractmethod
    def has_key(self, key: Any) -> Any:
        """Determines whether the key is in the storage or not"""
        pass

    def status(self) -> Any:
        return {"keyspace_size": len(self)}

    def empty_buffer(self) -> None:
        pass

    def add_to_select_buffer(self, keys: List[Any]) -> None:
        """Query keys and add them to internal buffer"""
        if not hasattr(self, "_select_buffer"):
            self._select_buffer = self.getmany(*keys)
        else:
            self._select_buffer.extend(self.getmany(*keys))

    def collect_select_buffer(self) -> Any:
        """Return buffered query results"""
        if not hasattr(self, "_select_buffer"):
            return []
        buffer = list(self._select_buffer)
        del self._select_buffer[:]
        return buffer


class OrderedStorage(Storage):

    pass


class UnorderedStorage(Storage):

    pass


class DictListStorage(OrderedStorage):
    """This is a wrapper class around ``defaultdict(list)`` enabling
    it to support an API consistent with `Storage`
    """

    def __init__(self, config: Any) -> None:
        self._dict: Any = defaultdict(list)

    def keys(self) -> List[Any]:
        return self._dict.keys()

    def get(self, key: Any) -> List[Any]:
        return self._dict.get(key, [])

    def remove(self, *keys: Any) -> None:
        for key in keys:
            del self._dict[key]

    def remove_val(self, key: Any, val: Any) -> None:
        self._dict[key].remove(val)

    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> None:
        self._dict[key].extend(vals)

    def size(self) -> int:
        return len(self._dict)

    def itemcounts(self, **kwargs: Any) -> Dict[Any, int]:
        """Returns a dict where the keys are the keys of the container.
        The values are the *lengths* of the value sequences stored
        in this container.
        """
        return {k: len(v) for k, v in self._dict.items()}

    def has_key(self, key: Any) -> bool:
        return key in self._dict


class DictSetStorage(UnorderedStorage, DictListStorage):
    """This is a wrapper class around ``defaultdict(set)`` enabling
    it to support an API consistent with `Storage`
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self._dict = defaultdict(set)

    def get(self, key: Any) -> List[Any]:
        return self._dict.get(key, set())

    def insert(self, key: Any, *vals: Any, **kwargs: Any) -> None:
        self._dict[key].update(vals)


class CassandraSharedSession(object):
    """Cassandra session shared across all storage instances."""

    __session: Any = None
    __session_buffer: Any = None
    __session_select_buffer: Any = None

    QUERY_CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {replication}
    """

    QUERY_DROP_KEYSPACE = "DROP KEYSPACE IF EXISTS {}"

    @classmethod
    def get_session(cls, seeds: List[str], **kwargs: Any) -> Any:
        _ = kwargs
        if cls.__session is None:
            # Allow dependency injection
            session = kwargs.get("session")
            if session is None:
                cluster = c_cluster.Cluster(seeds)
                session = cluster.connect()
            keyspace = kwargs["keyspace"]
            replication = kwargs["replication"]
            if kwargs.get("drop_keyspace", False):
                session.execute(cls.QUERY_DROP_KEYSPACE.format(keyspace))
            session.execute(
                cls.QUERY_CREATE_KEYSPACE.format(
                    keyspace=keyspace,
                    replication=str(replication),
                )
            )
            session.set_keyspace(keyspace)
            cls.__session = session
        return cls.__session

    @classmethod
    def get_buffer(cls) -> List[Any]:
        if cls.__session_buffer is None:
            cls.__session_buffer = []
        return cls.__session_buffer

    @classmethod
    def get_select_buffer(cls) -> List[Any]:
        if cls.__session_select_buffer is None:
            cls.__session_select_buffer = []
        return cls.__session_select_buffer


class CassandraClient(object):
    """Cassandra Client."""

    MIN_TOKEN = -(2**63)

    PAGE_SIZE = 1024

    CONCURRENCY = 100

    QUERY_CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS {}  (
            key blob,
            value blob,
            ts bigint,
            PRIMARY KEY (key, value)
        ) WITH CLUSTERING ORDER BY (value DESC)
    """

    QUERY_DROP_TABLE = "DROP TABLE IF EXISTS {}"

    QUERY_GET_KEYS = """
        SELECT DISTINCT key, TOKEN(key) as f_token
        FROM {}
        WHERE TOKEN(key) >= ? LIMIT ?
    """

    QUERY_GET_COUNTS = """
        SELECT key, COUNT(value) AS count
        FROM {}
        WHERE key = ?
    """

    QUERY_SELECT = """
        SELECT key, value, ts
        FROM {}
        WHERE key = ?
    """

    QUERY_SELECT_ONE = """
        SELECT key, value
        FROM {}
        WHERE key = ? LIMIT 1
    """

    QUERY_DELETE_KEY = """
        DELETE FROM {}
        WHERE key = ?
    """

    QUERY_DELETE_VAL = """
        DELETE FROM {}
        WHERE key = ? AND value  = ?
    """

    QUERY_UPSERT = """
        UPDATE {}
        SET ts = ?
        WHERE key = ? AND value = ?
    """

    QUERY_INSERT = "INSERT INTO {} (key, value, ts) VALUES (?, ?, ?)"

    def __init__(
        self,
        cassandra_params: Dict[str, Any],
        name: Any,
        buffer_size: Any,
    ) -> None:
        """
        Constructor.

        :param dict[str, any] cassandra_params: Cassandra parameters
        :param bytes name: the suffix to be used for the table name
        :param int buffer_size: the buffer size
        """
        self._buffer_size = buffer_size
        self._session = CassandraSharedSession.get_session(**cassandra_params)
        # This timestamp generator allows us to sort different values for the same key
        self._ts = c_cluster.MonotonicTimestampGenerator()
        # Each table (hashtable or key table is handled by a different storage; to increase
        # throughput it is possible to share a single buffer so the chances of a flush
        # are increased.
        if cassandra_params.get("shared_buffer", False):
            self._statements_and_parameters = CassandraSharedSession.get_buffer()
            self._select_statements_and_parameters_with_decoders = (
                CassandraSharedSession.get_select_buffer()
            )
        else:
            self._statements_and_parameters = []
            self._select_statements_and_parameters_with_decoders = []
        # Buckets tables rely on byte strings as keys and normal strings as values.
        # Keys tables have normal strings as keys and byte strings as values.
        # Since both data types can be reduced to byte strings without loss of data, we use
        # only one Cassandra table for both table types (so we can keep one single storage) and
        # we specify different encoders/decoders based on the table type.
        if b"bucket" in name:
            basename, _, ret = name.split(b"_")
            name = basename + b"_bucket_" + binascii.hexlify(ret)
            self._key_decoder = lambda x: x
            self._key_encoder = lambda x: x
            self._val_decoder = lambda x: x.decode("utf-8")
            self._val_encoder = lambda x: x.encode("utf-8")
        else:
            self._key_decoder = lambda x: x.decode("utf-8")
            self._key_encoder = lambda x: x.encode("utf-8")
            self._val_decoder = lambda x: x
            self._val_encoder = lambda x: x
        table_name = "lsh_" + name.decode("ascii")
        # Drop the table if are instructed to do so
        if cassandra_params.get("drop_tables", False):
            self._session.execute(self.QUERY_DROP_TABLE.format(table_name))
        self._session.execute(self.QUERY_CREATE_TABLE.format(table_name))
        # Prepare all the statements for this table
        self._stmt_insert = self._session.prepare(self.QUERY_INSERT.format(table_name))
        self._stmt_upsert = self._session.prepare(self.QUERY_UPSERT.format(table_name))
        self._stmt_get_keys = self._session.prepare(
            self.QUERY_GET_KEYS.format(table_name)
        )
        self._stmt_get = self._session.prepare(self.QUERY_SELECT.format(table_name))
        self._stmt_get_one = self._session.prepare(
            self.QUERY_SELECT_ONE.format(table_name)
        )
        self._stmt_get_count = self._session.prepare(
            self.QUERY_GET_COUNTS.format(table_name)
        )
        self._stmt_delete_key = self._session.prepare(
            self.QUERY_DELETE_KEY.format(table_name)
        )
        self._stmt_delete_val = self._session.prepare(
            self.QUERY_DELETE_VAL.format(table_name)
        )

    @property
    def buffer_size(self) -> None:
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, value: int) -> None:
        self._buffer_size = value

    @staticmethod
    def split_sequence(
        iterable: Iterable, size: int
    ) -> Generator[Iterable, None, None]:
        """
        Generator to split an iterable in chunks of given size.

        :param iterable iterable: the iterable to split
        :param int size: the size of a chunk
        :rtype: generator[iterable]
        :return: a generator
        """
        iterator = iter(iterable)
        item = list(itertools.islice(iterator, size))
        while item:
            yield item
            item = list(itertools.islice(iterator, size))

    def _select(
        self,
        statements_and_parameters: Iterable[Tuple[Tuple[Any, ...], Tuple[Any, ...]]],
    ) -> List[Any]:
        """
        Execute a list of statements and parameters returning data.

        :param iterable[tuple] statements_and_parameters: list of statements and parameters
        :rtype: list[Row]
        :return: the rows matching the queries
        """
        ret = []
        size = self.CONCURRENCY
        for sub_sequence in CassandraClient.split_sequence(
            statements_and_parameters, size
        ):
            results = c_concurrent.execute_concurrent(
                self._session,
                sub_sequence,
                concurrency=size,
            )
            for result in results:
                success, rows = result
                if success:
                    ret.append(rows)
                else:
                    raise RuntimeError
        return ret

    def _execute(self, statements_and_parameters: Any) -> None:
        """
        Execute a list of statements and parameters NOT returning data.

        :param iterable[tuple] statements_and_parameters: list of statements and parameters
        """
        size = self.CONCURRENCY
        for sub_sequence in CassandraClient.split_sequence(
            statements_and_parameters, size
        ):
            c_concurrent.execute_concurrent(
                self._session,
                sub_sequence,
                concurrency=size,
            )

    def _buffer(self, statements_and_parameters: Any) -> None:
        """
        Buffer (and execute) statements and parameters NOT returning data.

        :param iterable[tuple] statements_and_parameters: list of statements and parameters
        """
        self._statements_and_parameters.extend(statements_and_parameters)
        if len(self._statements_and_parameters) >= self._buffer_size:
            self.empty_buffer()

    def empty_buffer(self) -> None:
        """
        Empty the buffer of statements and parameters.
        """
        # copy the underlying list in a python2/3 compatible way
        buffer = list(self._statements_and_parameters)
        # delete the actual elements in a python2/3 compatible way
        del self._statements_and_parameters[:]
        self._execute(buffer)

    def insert(
        self,
        key: Union[bytes, str],
        vals: Iterable[Union[bytes, str]],
        buffer: bool = False,
    ) -> None:
        """
        Insert an iterable of values with the same key.

        :param byte|str key: the key
        :param iterable[byte|str] vals: the iterable of values
        :param boolean buffer: whether the insert statements should be buffered
        """
        statements_and_parameters = [
            (
                self._stmt_insert,
                (self._key_encoder(key), self._val_encoder(val), self._ts()),
            )
            for val in vals
        ]
        if buffer:
            self._buffer(statements_and_parameters)
        else:
            self._execute(statements_and_parameters)

    def upsert(
        self,
        key: Union[bytes, str],
        vals: Iterable[Union[bytes, str]],
        buffer: bool = False,
    ) -> None:
        """
        Upsert an iterable of values with the same key.

        Note: this is used when treating a Cassandra partition as a set. Since we upsert data
            we never store duplicates. In this case the timestamp loses its meaning as we
            are not interested in sorting records anymore (it is a set after all) and we can
            safely overwrite every time we are storing a duplicate.

        :param byte|str key: the key
        :param iterable[byte|str] vals: the iterable of values
        :param boolean buffer: whether the upsert statements should be buffered
        """
        statements_and_parameters = [
            (
                self._stmt_upsert,
                (self._ts(), self._key_encoder(key), self._val_encoder(val)),
            )
            for val in vals
        ]
        if buffer:
            self._buffer(statements_and_parameters)
        else:
            self._execute(statements_and_parameters)

    def delete_keys(
        self, keys: Iterable[Union[bytes, str]], buffer: bool = False
    ) -> None:
        """
        Delete a key (and all its values).

        :param iterable[byte|str] keys: the key
        :param boolean buffer: whether the delete statements should be buffered
        """
        statements_and_parameters = [
            (self._stmt_delete_key, (self._key_encoder(key),)) for key in keys
        ]
        if buffer:
            self._buffer(statements_and_parameters)
        else:
            self._execute(statements_and_parameters)

    def delete(
        self, key: Union[bytes, str], val: Union[bytes, str], buffer: bool = False
    ) -> None:
        """
        Delete a value from a key.

        :param byte|str key: the key
        :param byte|str val: the value
        :param boolean buffer: whether the delete statement should be buffered
        """
        statements_and_parameters = [
            (
                self._stmt_delete_val,
                (self._key_encoder(key), self._val_encoder(val)),
            )
        ]
        if buffer:
            self._buffer(statements_and_parameters)
        else:
            self._execute(statements_and_parameters)

    def get_keys(self) -> Set[Union[bytes, str]]:
        """
        Get all the keys.

        Note: selecting all keys in Cassandra via "SELECT DISTINCT key FROM table" is bound to
            time out since all nodes need to be contacted. To avoid this, we paginate through
            all keys using the TOKEN function. In this way we issue several different queries
            which alone can not time out.

        :rtype: set[byte|str]
        :return: the set of all keys
        """
        min_token = self.MIN_TOKEN
        keys = set([])
        while True:
            rows = self._session.execute(
                self._stmt_get_keys, (min_token, self.PAGE_SIZE)
            )
            if not rows:
                break
            for r in rows:
                keys.add(self._key_decoder(r.key))
                min_token = r.f_token + 1
        return keys

    def add_to_select_buffer(self, keys: Iterable[Union[bytes, str]]) -> None:
        """
        Buffer query statements and parameters with decoders to be used on returned data.

        :param iterable[byte|str] keys: the keys
        """
        statements_and_parameters_with_decoders = [
            (
                (self._stmt_get, (self._key_encoder(key),)),
                (self._key_decoder, self._val_decoder),
            )
            for key in keys
        ]
        self._select_statements_and_parameters_with_decoders.extend(
            statements_and_parameters_with_decoders
        )

    def collect_select_buffer(self) -> Any:
        """
        Perform buffered select queries

        :return: list of list of query results
        """
        if not self._select_statements_and_parameters_with_decoders:
            return []
        # copy the underlying list in a python2/3 compatible way
        buffer = list(self._select_statements_and_parameters_with_decoders)
        # delete the actual elements in a python2/3 compatible way
        del self._select_statements_and_parameters_with_decoders[:]
        statements_and_parameters, decoders = zip(*buffer)

        ret = collections.defaultdict(list)
        query_results = self._select(statements_and_parameters)
        for rows, (key_decoder, val_decoder) in zip(query_results, decoders):
            for row in rows:
                ret[key_decoder(row.key)].append((val_decoder(row.value), row.ts))
        return [
            [x[0] for x in sorted(v, key=operator.itemgetter(1))] for v in ret.values()
        ]

    def select(
        self, keys: Iterable[Union[bytes, str]]
    ) -> Dict[Union[bytes, str], List[Union[bytes, str]]]:
        """
        Select all values for the given keys.

        :param iterable[byte|str] keys: the keys
        :rtype: dict[byte|str,list[byte|str]
        :return: a dictionary of lists
        """
        statements_and_parameters = [
            (self._stmt_get, (self._key_encoder(key),)) for key in keys
        ]
        ret = collections.defaultdict(list)
        for rows in self._select(statements_and_parameters):
            for row in rows:
                ret[self._key_decoder(row.key)].append(
                    (self._val_decoder(row.value), row.ts)
                )
        return {
            k: [x[0] for x in sorted(v, key=operator.itemgetter(1))]
            for k, v in ret.items()
        }

    def select_count(
        self, keys: Iterable[Union[bytes, str]]
    ) -> Dict[Union[bytes, str], int]:
        """
        Count the values for each of the provided keys.

        :param iterable[byte|str] keys: list of keys
        :rtype: dict[byte|str,int]
        :return: the number of values per key
        """
        statements_and_parameters = [
            (self._stmt_get_count, (self._key_encoder(key),)) for key in keys
        ]
        return {
            self._key_decoder(row.key): row.count
            for rows in self._select(statements_and_parameters)
            for row in rows
        }

    def one(self, key: Union[bytes, str]) -> Optional[Union[bytes, str]]:
        """
        Select one single value of the given key.

        :param byte|str key: the key
        :rtype: byte|str|None
        :return: a single value for that key or None if the key does not exist
        """
        rows = self._session.execute(self._stmt_get_one, (self._key_encoder(key),))
        if rows:
            row = next(iter(rows))
            return self._val_decoder(row.value)
        return None


class CassandraStorage(object):
    """
    Storage implementation using Cassandra.

    Note: like other implementations, each storage has its own client. Unlike other
        implementations, all storage instances share one session and can potentially share the
        same buffer.
    """

    DEFAULT_BUFFER_SIZE = 5000

    def __init__(
        self,
        config: Dict[str, Any],
        name: Any = None,
        buffer_size: Optional[int] = None,
    ) -> None:
        """
        Constructor.

        :param dict[str, any] config: configuration following the following format:
            {
                'basename': b'test',
                'type': 'cassandra',
                'cassandra': {
                    'seeds': ['127.0.0.1'],
                    'keyspace': 'lsh_test',
                    'replication': {
                        'class': 'SimpleStrategy',
                        'replication_factor': '1'
                    },
                    'drop_keyspace': True,
                    'drop_tables': True,
                    'shared_buffer': False,
                }
            }
        :param bytes name: the name
        :param int buffer_size: the buffer size
        """
        self._config = config
        if buffer_size is None:
            buffer_size = CassandraStorage.DEFAULT_BUFFER_SIZE
        cassandra_param = self._parse_config(self._config["cassandra"])
        self._name = name if name else _random_name(11).decode("utf-8")
        self._buffer_size = buffer_size
        self._client = CassandraClient(cassandra_param, name, self._buffer_size)

    @staticmethod
    def _parse_config(config: Dict[str, Any]) -> Dict[str, str]:
        """
        Parse a configuration dictionary, optionally fetching data from env variables.

        :param dict[str, any] config: the configuration
        :rtype: dict[str, str]
        :return: the parse configuration
        """
        cfg = {}
        for key, value in config.items():
            if isinstance(value, dict):
                if "env" in value:
                    value = os.getenv(value["env"], value.get("default", None))
            cfg[key] = value
        return cfg

    @property
    def buffer_size(self) -> int:
        """
        Get the buffer size.

        :rtype: int
        :return: the buffer size
        """
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, value: Any) -> None:
        """
        Set the buffer size and propagate it to the underlying client.

        :param int value: buffer size
        """
        self._buffer_size = value
        self._client.buffer_size = value

    def __getstate__(self) -> Dict[str, Any]:
        """
        Get a pickable state by removing unpickable objects.

        :rtype: dict[str, any]
        :return: the state
        """
        state = self.__dict__.copy()
        state.pop("_client")
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        Set the state by reconnecting ephemeral objects.

        :param dict[str, any] state: the state to restore
        """
        self.__dict__ = state
        CassandraStorage.__init__(
            self, self._config, name=self._name, buffer_size=self._buffer_size
        )


class CassandraListStorage(OrderedStorage, CassandraStorage):
    """
    OrderedStorage storage implementation using Cassandra as backend.

    Note: Since we need to (i) select and delete values by both 'key' and by 'key and value',
        and (ii) allow duplicate values, we store a monotonically increasing timestamp as
        additional value.
    """

    def keys(self) -> Set[Union[bytes, str]]:
        """Implement interface."""
        return self._client.get_keys()

    def get(self, key: Union[bytes, str]) -> Any:
        """Implement interface."""
        return self._client.select([key]).get(key, [])

    def getmany(self, *keys: Union[bytes, str]) -> Any:
        """Implement interface."""
        return self._client.select(keys).values()

    def add_to_select_buffer(self, keys: Iterable[Union[bytes, str]]) -> None:
        """Implement interface."""
        self._client.add_to_select_buffer(keys)

    def collect_select_buffer(self) -> Any:
        """Implement interface."""
        return self._client.collect_select_buffer()

    def insert(
        self, key: Union[bytes, str], *vals: Union[bytes, str], **kwargs: Any
    ) -> None:
        """Implement interface."""
        buffer = kwargs.pop("buffer", False)
        self._client.insert(key, vals, buffer)

    def remove(self, *keys: Union[bytes, str], **kwargs: Any) -> None:
        """Implement interface."""
        buffer = kwargs.pop("buffer", False)
        self._client.delete_keys(keys, buffer)

    def remove_val(
        self, key: Union[bytes, str], val: Union[bytes, str], **kwargs: Any
    ) -> None:
        """Implement interface."""
        buffer = kwargs.pop("buffer", False)
        self._client.delete(key, val, buffer)

    def size(self) -> int:
        """Implement interface."""
        return len(self.keys())

    def itemcounts(self, **kwargs: Any) -> Any:
        """Implement interface."""
        return self._client.select_count(self.keys())

    def has_key(self, key: Union[bytes, str]) -> bool:
        """Implement interface."""
        return self._client.one(key) is not None

    def empty_buffer(self) -> None:
        """Implement interface."""
        self._client.empty_buffer()


class CassandraSetStorage(UnorderedStorage, CassandraListStorage):
    """
    OrderedStorage storage implementation using Cassandra as backend.

    Note: since we are interested in keeping duplicates or ordered data, we upsert the data
        ignoring what the timestamp actually means.
    """

    def get(self, key: Union[bytes, str]) -> Set[Union[bytes, str]]:
        """Implement interface and override super-class."""
        return set(super(CassandraSetStorage, self).get(key))

    def insert(
        self, key: Union[bytes, str], *vals: Union[bytes, str], **kwargs: Any
    ) -> None:
        """Implement interface and override super-class."""
        buffer = kwargs.pop("buffer", False)
        self._client.upsert(key, vals, buffer)


def _random_name(length: int) -> bytes:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length)).encode(
        "utf8"
    )
