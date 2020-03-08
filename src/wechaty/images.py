"""
docstring
"""
from __future__ import annotations

from enum import IntEnum
from typing import (
    Type,
)

from wechaty_puppet import FileBox
from .accessory import Accessory
from .config import (
    logging,
)

log = logging.getLogger('Image')


class ImageType(IntEnum):
    """
    docstring ...
    """
    Thumbnail = 0
    HD = 1
    Artwork = 2


class Image(Accessory):
    """
    docstring ...
    """

    def __str__(self):
        return 'image instance : %d' % self.id

    def __init__(self, image_id: str) -> None:
        """
        :param image_id:
        """
        super().__init__()
        log.info('__init__(%d)', image_id)

        self.id = image_id
        if self.puppet is None:
            raise NotImplementedError('Image class can not be instanced'
                                      ' without a puppet!')

    @classmethod
    def create(cls: Type[Image], image_id: str) -> Image:
        """
        create image instance by image_id
        :param cls:
        :param image_id:
        :return:
        """
        log.info('@classmethod create(%s, %d)', cls, image_id)
        obj = super().__new__(cls)
        obj.__init__(image_id)
        return obj
        # return cls(image_id)

    async def thumbnail(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('thumbnail() for %d', self.id)
        file_box = await self.puppet() \
            .message_image(self.id, ImageType.Thumbnail)
        return file_box

    async def hd(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('image hd for %d', self.id)
        file_box = await self.puppet() \
            .message_image(self.id, ImageType.HD)
        return file_box

    async def artwork(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('image artwork for %d', self.id)
        file_box = await self.puppet() \
            .message_image(self.id, ImageType.Artwork)
        return file_box
