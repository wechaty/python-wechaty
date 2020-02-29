from src.wechaty.accessory import Accessory
from src.wechaty.config import FileBox,log
from typing import Optional,Type,TypeVar
import asyncio
from enum import IntEnum


class ImageType(IntEnum):
    """
    docstring ...
    """
    Thumbnail = 0,
    HD = 1,
    Artwork = 2

class Image(Accessory):
    """
    docstring ...
    """
    def __init__(self,id:str) -> None:
        super(Image,self).__init__()
        self.id = id
        log.info(f"create image : {self.__name__}")

        if self.puppet is None:
            raise NotImplementedError("Image class can not be instanciated without a puppet!")


    @staticmethod
    def create(cls:Image,id:str) -> Image:
        """
        docstring
        :param cls:
        :param id:
        :return:
        """
        log.info(f"create static image : {id}")
        return cls(id)

    async def thumbnail(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info(f"image thumbnail for {self.id}")
        file_box = await self.puppet.message_image(self.id, ImageType.Thumbnail)
        return file_box

    async def hd(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info(f"image hd for {self.id}")
        file_box = await self.puppet.message_image(self.id,ImageType.HD)
        return file_box

    async def artwork(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info(f"image artwork for {self.id}")
        file_box = await self.puppet.message_image(self.id, ImageType.Artwork)
        return file_box



