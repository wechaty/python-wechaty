"""
wechaty-puppet contact module interfaces
"""
from enum import Enum
from typing import Optional


# pylint: disable=R0903
class ContactGender:
    """
    type for contact person
    """
    def __init__(self):
        """
        initialization
        """
        raise NotImplementedError


# pylint: disable=R0903
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
    def __init__(self):
        """
        initialization
        """
        raise NotImplementedError
