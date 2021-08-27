"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Optional,
    Type
)
import requests
from lxml import etree
from wechaty_puppet import UrlLinkPayload, get_logger

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
        url: str, title: Optional[str], thumbnail_url: Optional[str], description: Optional[str]
    ) -> UrlLink:
        """
        create urllink from url string
        """
        log.info('create url_link for %s', url)
        html = etree.HTML(requests.get(url).text)
        if not title:
            title = html.xpath('//meta[@property="og:title"]/@content')
            assert title is not None
            title = title[0] if len(title) else url
        if not thumbnail_url:
            thumbnail_url = html.xpath('//meta[@property="og:image"]/@content')
            assert thumbnail_url is not None
            thumbnail_url = thumbnail_url[0] if len(thumbnail_url) else ""
        if not description:
            description = html.xpath('//meta[@property="og:description"]/@content')
            assert description is not None
            description = description[0] if len(description) else ""
        payload = UrlLinkPayload(
            title=title,
            url=url,
            thumbnailUrl=thumbnail_url,
            description=description
        )
        return UrlLink(payload)

    def __str__(self) -> str:
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
    def thumbnailUrl(self) -> str:
        """
        get thumbnail url
        :return:
        """
        if self.payload.thumbnailUrl is None:
            return ''
        return self.payload.thumbnailUrl

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
