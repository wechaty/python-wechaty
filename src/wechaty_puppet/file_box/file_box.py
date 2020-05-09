"""
docstring
"""
from __future__ import annotations
import requests
import os
from collections import defaultdict
from typing import (
    Type,
    Optional,
    Union
)

from .type import (
    FileBoxFileOptions,
    FileBoxUrlOptions,
    FileBoxStreamOptions,
    FileBoxBufferOptions,
    FileBoxQrCodeOptions,
    FileBoxBase64Options,
    FileBoxOptionsBase
)


class FileBox:
    """
    # TODO -> need to implement pipeable
    maintain the file content, which is sended by wechat
    """

    def __init__(self, options: FileBoxOptionsBase):
        self.box_type = options.type
        self.name = options.name

        self.mimi_type: Optional[str] = None

        self.options = options

        self._metadata: dict = defaultdict()

    def metadata(self, data: Optional[dict] = None) -> dict:
        """
        set/get meta data for file-box
        """
        if data is None:
            return self._metadata
        self._metadata.update(data)
        return self._metadata

    @classmethod
    def to_json(cls) -> dict:
        """
        dump the file content to json object
        :return:
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        options = FileBoxUrlOptions(name=name, url=url, headers=headers)
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

        options = FileBoxFileOptions(name=name, path=path)
        return cls(options)

    @classmethod
    def from_stream(cls: Type[FileBox], stream: bytes, name: str) -> FileBox:
        """
        create file-box from stream

        TODO -> need to implement stream detials
        """
        options = FileBoxStreamOptions(name=name, stream=stream)
        return cls(options)

    @classmethod
    def from_buffer(cls: Type[FileBox], buffer: bytes, name: str) -> FileBox:
        """
        create file-box from buffer

        TODO -> need to implement buffer detials
        """
        options = FileBoxBufferOptions(name=name, buffer=buffer)
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
        base64_name = '' if name is None else name
        # TODO -> file name is required ?
        options = FileBoxBase64Options(name=base64_name, base64=base64)
        return FileBox(options)

    @classmethod
    def from_qr_code(cls: Type[FileBox], qr_code: str) -> FileBox:
        """
        create file-box from base64 str
        """
        options = FileBoxQrCodeOptions(name='qrcode.png', qr_code=qr_code)
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
