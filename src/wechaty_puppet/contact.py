"""
wechaty-puppet contact module interfaces
"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass


# pylint: disable=R0903
from chatie_grpc.wechaty import (
    ContactPayloadResponse,
    ContactGender,
    ContactType
)


# pylint: disable=R0903
# pylint: disable=R0902
@dataclass
class ContactPayload:
    """
    payload for contact person
    """
    def __init__(self, response: ContactPayloadResponse):
        """
        initialization
        """
        self.name: str = response.name
        self.alias: str = response.alias
        self.friend: bool = response.friend
        self.start: bool = response.star
        self.type: ContactType = response.type
        self.gender: ContactGender = response.gender
        self.province: str = response.province
        self.city: str = response.city
        self.weixin: str = response.weixin


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
