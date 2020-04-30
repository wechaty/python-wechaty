"""
UrlLinkPayload interface
"""
from typing import Optional

from dataclasses import dataclass

from chatie_grpc.wechaty import MessageUrlResponse


# pylint: disable=R0903
@dataclass
class UrlLinkPayload:
    """
    UrlLinkPayload object
    """
    title: str
    url: str
    thumbnail_url: str
    description: str

    def __init__(self, url: str):
        """
        create urllink from puppet response
        """
        self.url = url
