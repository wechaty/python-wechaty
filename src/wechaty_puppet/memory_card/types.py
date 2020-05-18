"""doc"""
from __future__ import annotations
from dataclasses import dataclass
import collections
from typing import (
    Dict,
    Union,
    TypeVar
)
from .async_map_type import AsyncMap

PayloadDataType = Union[int, str]

MemoryCardPayload = Union[Dict[str, PayloadDataType], Dict]

# # TODO
# @dataclass
# class MemoryCardPayload(collections.UserDict):
#
#     def __missing__(self, key: str):
#         if isinstance(key, str):
#             raise KeyError(key)
#         return self[str(key)]
#
#     def __contains__(self, key: str):
#         return str(key) in self.data
#
#     def __setitem__(self, key: str, item: PayloadDataType):
#         self.data[str(key)] = item
#
#     def __getattr__(self, key: str):
#         return self.data[str(key)]

