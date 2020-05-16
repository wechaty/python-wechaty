"""
docstring
"""
from __future__ import annotations

import json

import requests
import os
from collections import defaultdict
import mimetypes
from typing import (
    Type,
    Optional,
    Union,
    Dict, Any
)

from .type import (
    FileBoxOptionsFile,
    FileBoxOptionsUrl,
    FileBoxOptionsStream,
    FileBoxOptionsBuffer,
    FileBoxOptionsQrCode,
    FileBoxOptionsBase64,
    FileBoxOptionsBase,
    Metadata, FileBoxType)


class FileBoxEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)


class FileBox:
    """
    # TODO -> need to implement pipeable
    maintain the file content, which is sended by wechat
    """

    def __init__(self, options: FileBoxOptionsBase):



        self.mimeType: Optional[str] = None

        self._metadata: Metadata = defaultdict()

        self.name = options.name
        self.boxType:int = options.type.value[0]

        if isinstance(options, FileBoxOptionsFile):
            self.localPath = options.path

        elif isinstance(options, FileBoxOptionsBuffer):
            self.buffer = options.buffer

        elif isinstance(options, FileBoxOptionsUrl):
            self.remoteUrl = options.url
            self.headers = options.headers

        elif isinstance(options, FileBoxOptionsStream):
            # TODO -> need to get into detail for stream sending
            pass

        elif isinstance(options, FileBoxOptionsQrCode):
            self.qrCode = options.qr_code

        elif isinstance(options, FileBoxOptionsBase64):
            self.base64 = options.base64

    @property
    def metadata(self) -> dict:
        """
        get meta data for file-box
        """
        return self._metadata

    @metadata.setter
    def metadata(self, data: Metadata):
        """
        set meta data for file-box
        :param data:
        :return:
        """
        self._metadata.update(data)

    def type(self) -> FileBoxType:
        """get filebox type"""
        return FileBoxType(self.boxType)

    def sync_remote_name(self):
        """sync remote name"""
        pass

    def to_json_str(self) -> str:
        """
        dump the file content to json object
        :return:
        """
        json_data = {}
        for key in self.__dict__:
            if getattr(self, key) is not None:
                json_data[key] = getattr(self,key)

        data = json.dumps(json_data, cls=FileBoxEncoder, indent=4)
        return data

    def to_file(self, file_path: str) -> None:
        """
        save the content to the file
        :return:
        """
        raise NotImplementedError

    def to_base64(self) -> str:
        """
        transfer file-box to base64 string
        :return:
        """
        # TODO -> need to implement other data format
        return ''

    @classmethod
    def from_url(cls: Type[FileBox], url: str, name: Optional[str],
                 headers: Optional[dict] = None) -> FileBox:
        """
        create file-box from url
        """
        if name is None:
            response = requests.get(url)
            # TODO -> should get the name of the file
            name = response.content.title().decode(encoding='utf-8')
        options = FileBoxOptionsUrl(name=name, url=url, headers=headers)
        return cls(options)

    @classmethod
    def from_file(cls: Type[FileBox], path: str, name: Optional[str]
                  ) -> FileBox:
        """
        create file-box from file
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f'{path} file not found')
        if name is None:
            name = os.path.basename(path)

        options = FileBoxOptionsFile(name=name, path=path)
        return cls(options)

    @classmethod
    def from_stream(cls: Type[FileBox], stream: bytes, name: str) -> FileBox:
        """
        create file-box from stream

        TODO -> need to implement stream detials
        """
        options = FileBoxOptionsStream(name=name, stream=stream)
        return cls(options)

    @classmethod
    def from_buffer(cls: Type[FileBox], buffer: bytes, name: str) -> FileBox:
        """
        create file-box from buffer

        TODO -> need to implement buffer detials
        """
        options = FileBoxOptionsBuffer(name=name, buffer=buffer)
        return cls(options)

    @classmethod
    def from_base64(cls: Type[FileBox], base64: str, name: Optional[str] = None
                    ) -> FileBox:
        """
        create file-box from base64 str

        :param base64:
            example data: data:image/png;base64,${base64Text}
        :param name: name the file name of the base64 data
        :return:
        """
        base64_name = 'default_file_name' if name is None else name
        # TODO -> file name is required ?
        options = FileBoxOptionsBase64(name=base64_name, base64=base64)
        return FileBox(options)

    @classmethod
    def from_qr_code(cls: Type[FileBox], qr_code: str) -> FileBox:
        """
        create file-box from base64 str
        """
        options = FileBoxOptionsQrCode(name='qrcode.png', qr_code=qr_code)
        return cls(options)

    @classmethod
    def from_json(cls: Type[FileBox], obj: Union[str, dict]) -> FileBox:
        """
        create file-box from json data

        TODO -> need to translate :
            https://github.com/huan/file-box/blob/master/src/file-box.ts#L175

        :param obj:
        :return:
        """
        raise NotImplementedError
