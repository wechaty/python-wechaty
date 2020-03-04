"""
docstring
"""
from enum import IntEnum
from typing import Type, TypeVar
from wechaty_puppet.file_box import FileBox
from .accessory import Accessory
from .config import LOG


class ImageType(IntEnum):
    """
    docstring ...
    """
    Thumbnail = 0
    HD = 1
    Artwork = 2


T = TypeVar("T", bound="Image")


class Image(Accessory):
    """
    docstring ...
    """

    def __str__(self):
        return "image instance : %d" % self.image_id

    def __init__(self, image_id: str) -> None:
        """
        :param image_id:
        """
        super(Image, self).__init__()
        self.image_id = image_id
        LOG.info("create image : %d", self.image_id)
        if self.puppet is None:
            raise NotImplementedError("Image class can not be instanced"
                                      " without a puppet!")

    @classmethod
    def create(cls: Type[T], image_id: str) -> T:
        """
        create image instance by image_id
        :param cls:
        :param image_id:
        :return:
        """
        LOG.info("create static image : %d", image_id)
        return cls(image_id)

    async def thumbnail(self) -> FileBox:
        """
        docstring
        :return:
        """
        LOG.info("image thumbnail for %d", self.image_id)
        puppet = self.puppet()
        if puppet is None:
            raise AttributeError
        file_box = await puppet.message_image(self.image_id,
                                              ImageType.Thumbnail)
        return file_box

    async def hd(self) -> FileBox:
        """
        docstring
        :return:
        """
        LOG.info("image hd for %d", self.image_id)
        puppet = self.puppet()
        if puppet is None:
            raise AttributeError
        file_box = await puppet.message_image(self.image_id, ImageType.HD)
        return file_box

    async def artwork(self) -> FileBox:
        """
        docstring
        :return:
        """
        LOG.info("image artwork for %d", self.image_id)
        puppet = self.puppet()
        if puppet is None:
            raise AttributeError
        file_box = await puppet.message_image(self.image_id, ImageType.Artwork)
        return file_box
