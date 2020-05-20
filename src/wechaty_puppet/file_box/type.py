"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2018-now @copyright Wechaty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import collections
from enum import Enum
from dataclasses import dataclass

from typing import (
    Optional,
    Any, Dict
)


Metadata = Dict[str, Any]


class FileBoxType(Enum):
    """
    option config for file box
    """
    Unknown = 0,

    # Serializable by toJSON()

    Base64 = 1,
    Url = 2,
    QRCode = 3,

    # Not serializable by toJSON()
    # Need to convert to FileBoxType.Base64 before call toJSON()
    Buffer = 4,
    File = 5,
    Stream = 6,


@dataclass
class FileBoxOptionsBase:
    name: str
    type: FileBoxType


@dataclass
class FileBoxOptionsUrl(FileBoxOptionsBase):
    """
    url file-box options
    """
    url: str = ''
    headers: Optional[dict] = None
    type: FileBoxType = FileBoxType.Url


@dataclass
class FileBoxOptionsFile(FileBoxOptionsBase):
    """
    file file-box options
    """
    path: Optional[str] = None
    type: FileBoxType = FileBoxType.File


@dataclass
class FileBoxOptionsBuffer(FileBoxOptionsBase):
    """
    file file-box options
    """
    # TODO -> recheck the buffer data type
    buffer: bytes = b''
    type: FileBoxType = FileBoxType.Buffer


@dataclass
class FileBoxOptionsStream(FileBoxOptionsBase):
    """
    stream file-box options
    """
    # TODO -> recheck the stream data type
    stream: bytes = b''
    type: FileBoxType = FileBoxType.Stream


@dataclass
class FileBoxOptionsQrCode(FileBoxOptionsBase):
    """
    qr-code file-box options
    """
    qr_code: str = ''
    type: FileBoxType = FileBoxType.QRCode


@dataclass
class FileBoxOptionsBase64(FileBoxOptionsBase):
    """
    base64 file-box options
    """
    base64: str = ''
    type: FileBoxType = FileBoxType.Base64
