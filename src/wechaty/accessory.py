from abc import ABCMeta,abstractclassmethod
from typing import Any
from enum import Enum

class Puppet(object):

    def message_image(self,id:int,image_type : Enum):
        """
        docstring
        :param id:
        :param image_type:
        :return:
        """
        pass

class Accessory(object):
    """

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.puppet = Puppet()

    @abstractclassmethod
    def __str__(self):
        """
        docstring
        :return:
        """
        raise NotImplementedError
