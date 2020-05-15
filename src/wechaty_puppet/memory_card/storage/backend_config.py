from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Optional,
    Type,
    Dict,
    Union,
    TypeVar
)


@dataclass
class StorageNopOptions:
    placeholder: Optional = None


StorageFileOptions = Type[StorageNopOptions]


# @dataclass
# class StorageS3Options:
#     accessKeyId: str
#     secretAccessKey: str
#     region: str
#     bucket: str


@dataclass
class StorageObsOptions:
    accessKeyId: str
    secretAccessKey: str
    server: str
    bucket: str


# TODO
@dataclass
class StorageFileOptionsExtends(StorageFileOptions):
    type: Optional = "file"


@dataclass
class StorageNopOptionsExtends(StorageNopOptions):
    type: Optional = "nop"


@dataclass
class StorageObsOptionsExtends(StorageObsOptions):
    type: Optional = "obs"


# StorageBackendOptions = Union[StorageFileOptionsExtends,
#                               StorageNopOptionsExtends,
#                               StorageObsOptionsExtends]
StorageBackendOptions = TypeVar('StorageBackendOptions', StorageFileOptionsExtends,
                                StorageNopOptionsExtends, StorageObsOptionsExtends, Dict)

from .file import StorageFile
from .nop import StorageNop
from .obs import StorageObs
# from .s3 import StorageS3

BACKEND_DICT = {"file": StorageFile,
                "nop": StorageNop,
                "obs": StorageObs}

file = TypeVar('file')
nop = TypeVar('nop')
obs = TypeVar('obs')

StorageBackendType = Union[file, nop, obs]
