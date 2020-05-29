"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Type,
)
import requests

from wechaty_puppet import UrlLinkPayload, get_logger   # type: ignore


log = get_logger('UrlLink')


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

        payload = UrlLinkPayload(
            title=res.content.title().decode("utf-8"),
            url=url)
        # TODO -> get description, thumbnail_url of a website
        return UrlLink(payload)

    def __str__(self):
        """
        UrlLink string format output
        :return:
        """
        return 'UrlLink<%s>' % self.payload.url

    @property
    def title(self) -> str:
        """
        get UrlLink title
        :return:
        """
        if self.payload.title is None:
            return ''
        return self.payload.title

    @property
    def thumbnail_url(self) -> str:
        """
        get thumbnail url
        :return:
        """
        if self.payload.thumbnail_url is None:
            return ''
        return self.payload.thumbnail_url

    @property
    def description(self) -> str:
        """
        get description
        :return:
        """
        if self.payload.description is None:
            return ''
        return self.payload.description

    @property
    def url(self) -> str:
        """
        get url
        :return:
        """
        if self.payload.url is None:
            return ''
        return self.payload.url
