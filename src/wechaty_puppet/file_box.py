"""
docstring
"""
from __future__ import annotations


class FileBox:
    """
    maintain the file content, which is sended by wechat
    """

    def to_json(self) -> dict:
        """
        dump the file content to json object
        :return:
        """
        raise NotImplementedError

    async def to_file(self, file_path: str) -> None:
        """
        save the content to the file
        :return:
        """
        raise NotImplementedError

    @classmethod
    def from_qr_code(cls: FileBox, code: str) -> FileBox:
        """
        create filebox from qrcode
        :param code:
        :return:
        """
        raise NotImplementedError
