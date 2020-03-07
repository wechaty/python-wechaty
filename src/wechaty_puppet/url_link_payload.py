"""
UrlLinkPayload interface
"""
from typing import Optional


# pylint: disable=R0903
class UrlLinkPayload:
    """
    UrlLinkPayload object
    """
    def __init__(self):
        self.title: str = ''
        self.url: str = ''
        self.thumbnail_url: Optional[str] = None
        self.description: Optional[str] = None
