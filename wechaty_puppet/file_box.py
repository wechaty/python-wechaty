"""
docstring
"""
from typing import Type, TypeVar

T = TypeVar("T")


# dummy class
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

    def to_file(self, file_path: str) -> None:
        """
        save the content to the file
        :return:
        """
        raise NotImplementedError

    @classmethod
    def from_qr_code(cls: Type[T], code:str) -> "FileBox":
        """
        create filebox from qrcode
        :param code:
        :return:
        """
        raise NotImplementedError
