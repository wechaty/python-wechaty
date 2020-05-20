"""doc"""
from __future__ import annotations
# from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
    List
)
import collections
K = TypeVar("K")
V = TypeVar("V")


# class AsyncMap(Generic[K, V]):
class AsyncMap(Generic[K, V]):

    @property
    def size(self) -> int:
        raise NotImplementedError

    def entries(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def values(self):
        raise NotImplementedError

    def get(self, key: K):
        raise NotImplementedError

    def set(self, key: K, value: V):
        raise NotImplementedError

    def has(self, key: K) -> bool:
        raise NotImplementedError

    def delete(self, key: K):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

