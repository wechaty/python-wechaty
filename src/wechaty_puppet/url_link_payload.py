"""
UrlLinkPayload interface
"""
from typing import Optional

from dataclasses import dataclass

# pylint: disable=R0903
@dataclass
class UrlLinkPayload:
    """
    UrlLinkPayload object
    """
    title: str = ''
    url: str = ''
    thumbnail_url: Optional[str] = None
    description: Optional[str] = None
