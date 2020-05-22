"""doc"""
from __future__ import annotations
from typing import (
    Dict,
    Union,
)

PayloadDataType = Union[int, str]

MemoryCardPayload = Union[Dict[str, PayloadDataType], Dict]
