from abc import ABCMeta,abstractclassmethod
from typing import Any
from enum import Enum

class Puppet(object):

    def messageImage(self,id:int,image_type : Enum):
        pass

class Accessory(object):
    """

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.puppet =

    @abstractclassmethod
    def __str__(self):
        raise NotImplementedError
