"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Type,
)
import requests
from lxml import etree # parse html
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
        """
        create urllink from url string
        """
        log.info('create url_link for %s', url)
        html = etree.HTML(requests.get(url).text)
        title = html.xpath('//meta[@property="og:title"]/@content')
        thumbnail_url = html.xpath('//meta[@property="og:image"]/@content')
        description = html.xpath('//meta[@property="og:description"]/@content')
        payload = UrlLinkPayload(
            title = title[0] if len(title) else url,
            url = url,
            thumbnail_url = thumbnail_url[0] if len(thumbnail_url) else "",
            description = description[0] if len(description) else ""
        )
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
