"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Type,
)
import logging
import requests

from wechaty_puppet import UrlLinkPayload

log = logging.getLogger('UrlLink')


class UrlLink:
    """
    url_link object which handle the url_link content
    """
    def __init__(
            self,
            payload: UrlLinkPayload,
    ):
        """
        initialization
        :param payload:
        """
        self.payload: UrlLinkPayload = payload

    @classmethod
    def create(
            cls: Type[UrlLink],
            url: str,
    ) -> UrlLink:
        """doc"""
        log.info('create url_link for %s', url)
        res = requests.get(url)

        payload = UrlLinkPayload(url)
        payload.title = res.content.title().decode(encoding='utf-8')
        payload.url = url

        # TODO -> get description, thumbnail_url of a website

        return UrlLink(payload)

    def __str__(self):
        """
        UrlLink string format output
        :return:
        """
        return 'UrlLink<%s>' % self.payload.url

    def title(self) -> str:
        """
        get UrlLink title
        :return:
        """
        return self.payload.title

    def thumbnail_url(self) -> str:
        """
        get thumbnail url
        :return:
        """
        return self.payload.thumbnail_url

    def description(self) -> str:
        """
        get description
        :return:
        """
        return self.payload.description
