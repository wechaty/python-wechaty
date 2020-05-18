from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Optional,
    Type,
    Any,
    Union,
    TypeVar
)


@dataclass
class StorageNopOptions:
    placeholder: Optional[Any] = None


StorageFileOptions = StorageNopOptions


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
    accessKeyId = ""
    secretAccessKey = ""
    server = ""
    bucket = ""

# TODO
@dataclass
class StorageBackendOptionsBase:
    type: Optional[Any] = None


@dataclass
class StorageFileOptionsExtends(StorageBackendOptionsBase, StorageFileOptions):
    type = "file"


@dataclass
class StorageNopOptionsExtends(StorageBackendOptionsBase, StorageNopOptions):
    type = "nop"


@dataclass
class StorageObsOptionsExtends(StorageBackendOptionsBase, StorageObsOptions):
    type = "obs"


# TypeError: Cannot instantiate typing.Union
StorageBackendOptions = Union[StorageBackendOptionsBase, StorageFileOptionsExtends,
                              StorageNopOptionsExtends, StorageObsOptionsExtends]

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

