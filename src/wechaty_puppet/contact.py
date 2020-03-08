"""
wechaty-puppet contact module interfaces
"""
from enum import Enum
from typing import Optional


# pylint: disable=R0903
class ContactGender(Enum):
    """
    type for contact person
    """
    Male = 0
    Female = 1
    Unkonwn = 2


# pylint: disable=R0903
# pylint: disable=R0902
class ContactPayload:
    """
    payload for contact person
    """
    def __init__(self):
        """
        initialization
        """
        self.name: Optional[str] = None
        self.alias: Optional[str] = None
        self.friend: Optional[bool] = None
        self.start: Optional[bool] = None
        self.type: ContactType = ContactType.Unkonwn
        # default value : false
        self.start: bool = False
        self.gender: ContactGender = ContactGender.Unkonwn
        self.province: Optional[str] = None
        self.city: Optional[str] = None
        self.weixin: Optional[str] = None


# pylint: disable=R0903
class ContactQueryFilter:
    """
    filter for contact persons
    """
    def __init__(self):
        """
        initialization
        """
        raise NotImplementedError


# pylint: disable=R0903
class ContactType(Enum):
    """
    contact person type
    """
    Unkonwn = 0
    Offical = 1
    Personal = 2
