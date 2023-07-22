# Standard Library
import copy
import warnings
from typing import Any, Callable, Generator, Iterable, List, Optional, Union

# 3rd party libraries
import numpy as np

# Source
from src.predict.datasketch.hashfunc import sha1_hash32


# The size of a hash value in number of bytes
hashvalue_byte_size = len(bytes(np.int64(42).data))
# http://en.wikipedia.org/wiki/Mersenne_prime
_mersenne_prime = np.uint64((1 << 61) - 1)
_max_hash = np.uint64((1 << 32) - 1)
_hash_range = 1 << 32


class MinHash(object):
    """MinHash is a probabilistic data structure for computing
    `Jaccard similarity`_ between sets.

    Args:
        num_perm (int, optional): Number of random permutation functions.
            It will be ignored if `hashvalues` is not None.
        seed (int, optional): The random seed controls the set of random
            permutation functions generated for this MinHash.
        hashfunc (optional): The hash function used by this MinHash.
            It takes the input passed to the `update` method and
            returns an integer that can be encoded with 32 bits.
            The default hash function is based on SHA1 from hashlib_.
        hashobj (**deprecated**): This argument is deprecated since version
            1.4.0. It is a no-op and has been replaced by `hashfunc`.
        hashvalues (`numpy.array` or `list`, optional): The hash values is
            the internal state of the MinHash. It can be specified for faster
            initialization using the existing state from another MinHash.
        permutations (optional): The permutation function parameters. This argument
            can be specified for faster initialization using the existing
            state from another MinHash.

    Note:
        To save memory usage, consider using :class:`datasketch.LeanMinHash`.

    Note:
        Since version 1.1.1, MinHash will only support serialization using
        `pickle`_. ``serialize`` and ``deserialize`` methods are removed,
        and are supported in :class:`datasketch.LeanMinHash` instead.
        MinHash serialized before version 1.1.1 cannot be deserialized properly
        in newer versions (`need to migrate? <https://github.com/ekzhu/datasketch/issues/18>`_).

    Note:
        Since version 1.1.3, MinHash uses Numpy's random number generator
        instead of Python's built-in random package. This change makes the
        hash values consistent across different Python versions.
        The side-effect is that now MinHash created before version 1.1.3 won't
        work (i.e., ``jaccard``, ``merge`` and ``union``)
        with those created after.

    .. _`Jaccard similarity`: https://en.wikipedia.org/wiki/Jaccard_index
    .. _hashlib: https://docs.python.org/3.5/library/hashlib.html
    .. _`pickle`: https://docs.python.org/3/library/pickle.html
    """

    def __init__(
        self,
        num_perm: int = 128,
        seed: int = 1,
        hashfunc: Optional[Callable[[bytes], int]] = sha1_hash32,
        hashobj: Optional[Any] = None,
        hashvalues: Optional[Union[np.ndarray, List[Any]]] = None,
        permutations: Optional[np.ndarray] = None,
    ):
        if hashvalues is not None:
            num_perm = len(hashvalues)

        if num_perm > _hash_range:
            raise ValueError(
                "Cannot have more than %d number of permutation functions" % _hash_range
            )

        self.seed = seed
        self.num_perm = num_perm
        # Check the hash function.
        if not callable(hashfunc):
            raise ValueError("The hashfunc must be a callable.")
        self.hashfunc = hashfunc
        # Check for use of hashobj and issue a warning.
        if hashobj is not None:
            warnings.warn(
                "hashobj is deprecated, use hashfunc instead.", DeprecationWarning
            )
        # Initialize hash values
        if hashvalues is not None:
            self.hashvalues = self._parse_hashvalues(hashvalues)
        else:
            self.hashvalues = self._init_hashvalues(num_perm)
        # Initialize permutation function parameters
        if permutations is not None:
            self.permutations = permutations
        else:
            self.permutations = self._init_permutations(num_perm)

        if len(self) != len(self.permutations[0]):
            raise ValueError("Numbers of hash values and permutations mismatch")

    def _init_hashvalues(self, num_perm: int) -> np.ndarray:
        """
        Initialize hash values for the MinHash."""
        return np.ones(num_perm, dtype=np.uint64) * _max_hash

    def _init_permutations(self, num_perm: int) -> np.ndarray:
        """
        Initialize permutation function parameters for the MinHash."""
        gen = np.random.RandomState(self.seed)
        return np.array(
            [
                (
                    gen.randint(1, _mersenne_prime, dtype=np.uint64),
                    gen.randint(0, _mersenne_prime, dtype=np.uint64),
                )
                for _ in range(num_perm)
            ],
            dtype=np.uint64,
        ).T

    def _parse_hashvalues(self, hashvalues: Union[List[int], np.ndarray]) -> np.ndarray:
        """
        Parse the given hash values and convert them into a numpy array of uint64 data type."""
        return np.array(hashvalues, dtype=np.uint64)

    def update(self, b: bytes) -> None:

        hv = self.hashfunc(b)
        a, b = self.permutations
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, _max_hash)
        self.hashvalues = np.minimum(phv, self.hashvalues)

    def update_batch(self, b: List[bytes]) -> None:
        """Update this MinHash with new values.
        The values will be hashed using the hash function specified by
        the `hashfunc` argument in the constructor."""
        hv = np.array([self.hashfunc(_b) for _b in b], dtype=np.uint64)
        a, b = self.permutations
        phv = np.bitwise_and(
            ((hv * np.tile(a, (len(hv), 1)).T).T + b) % _mersenne_prime, _max_hash
        )
        self.hashvalues = np.vstack([phv, self.hashvalues]).min(axis=0)

    def jaccard(self, other: Any) -> float:
        """Estimate the `Jaccard similarity`_ (resemblance) between the sets
        represented by this MinHash and the other."""
        if other.seed != self.seed:
            raise ValueError(
                "Cannot compute Jaccard given MinHash with different seeds"
            )
        if len(self) != len(other):
            raise ValueError(
                "Cannot compute Jaccard given MinHash with different numbers of permutation func."
            )
        return float(np.count_nonzero(self.hashvalues == other.hashvalues)) / float(
            len(self)
        )

    def count(self) -> int:
        """Estimate the cardinality count based on the technique described in the paper."""
        k = len(self)
        return int(float(k) / np.sum(self.hashvalues / float(_max_hash)) - 1.0)

    def merge(self, other: Any) -> None:
        """Merge the other MinHash with this one, making this one the union of both."""
        if other.seed != self.seed:
            raise ValueError("Cannot merge MinHash with different seeds")
        if len(self) != len(other):
            raise ValueError(
                "Cannot merge MinHash with different numbers of permutation functions"
            )
        self.hashvalues = np.minimum(other.hashvalues, self.hashvalues)

    def digest(self) -> np.ndarray:
        """
        Export the hash values, which is the internal state of the MinHash.

        Returns:
            numpy.ndarray: The hash values represented as a Numpy array.
        """
        return copy.copy(self.hashvalues)

    def is_empty(self) -> bool:
        """
        Check if the current MinHash is empty, at the state of just initialized.

        Returns:
            bool: True if the current MinHash is empty, False otherwise.
        """
        if np.any(self.hashvalues != _max_hash):
            return False
        return True

    def clear(self) -> None:
        """
        Clear the current state of the MinHash.
        All hash values are reset to their initial state.
        """
        self.hashvalues = self._init_hashvalues(len(self))

    def copy(self) -> Any:
        """
        Returns:
            datasketch.MinHash: A copy of this MinHash by exporting its state.
        """
        return MinHash(
            seed=self.seed,
            hashfunc=self.hashfunc,
            hashvalues=self.digest(),
            permutations=self.permutations,
        )

    def __len__(self) -> int:
        """
        Returns:
            int: The number of hash values.
        """
        return len(self.hashvalues)

    def __eq__(self, other: Any) -> bool:
        """Returns: bool: If their seeds and hash values are both equal: two are equivalent."""
        return (
            type(self) is type(other)  # noqa
            and self.seed == other.seed  # noqa
            and np.array_equal(self.hashvalues, other.hashvalues)  # noqa
        )

    @classmethod
    def union(cls, *mhs: Any) -> Any:
        """Create a MinHash which is the union of the MinHash objects passed as arguments."""
        if len(mhs) < 2:
            raise ValueError("Cannot union less than 2 MinHash")
        num_perm = len(mhs[0])
        seed = mhs[0].seed
        if any((seed != m.seed or num_perm != len(m)) for m in mhs):
            raise ValueError(
                "The unioning MinHash must have the same seed and number of permutation functions"
            )
        hashvalues = np.minimum.reduce([m.hashvalues for m in mhs])
        permutations = mhs[0].permutations
        return cls(
            num_perm=num_perm,
            seed=seed,
            hashvalues=hashvalues,
            permutations=permutations,
        )

    @classmethod
    def bulk(cls, b: Iterable[List[bytes]], **minhash_kwargs: Any) -> List[Any]:
        """Compute MinHashes in bulk."""
        return list(cls.generator(b, **minhash_kwargs))

    @classmethod
    def generator(
        cls, b: Iterable[List[bytes]], **minhash_kwargs: Any
    ) -> Generator[Any, None, None]:
        """Compute MinHashes in a generator."""
        m = cls(**minhash_kwargs)
        for _b in b:
            _m = m.copy()
            _m.update_batch(_b)
            yield _m
