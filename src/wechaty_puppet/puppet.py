"""
interface for puppet
"""
from __future__ import annotations

from enum import Enum
from typing import Union
from .file_box import FileBox
from .url_link_payload import UrlLinkPayload
from .contact import ContactQueryFilter


class Puppet:
    """
    puppet interface class
    """

    def __init__(self):
        self.name: str = 'puppet'

    # pylint: disable=R0201
    async def message_image(
            self,
            message_id: str,
            image_type: Enum
    ) -> FileBox:
        """
        docstring
        :param message_id:
        :param image_type:
        :return:
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        start the puppet
        :return:
        """
        raise NotImplementedError

    async def contact_search(self, query: Union[str, ContactQueryFilter]):
        """
        search
        :param query:
        :return:
        """
        raise NotImplementedError

    async def get_contact_payload(self, contact_id: str) -> Puppet:
        """
        get
        :param contact_id:
        :return:
        """
        raise NotImplementedError

    async def delete_contact_tag(self, tag_id: str) -> None:
        """

        :return:
        """
        raise NotImplementedError

    async def tag_contact_add(self, tag_id: str, contact_id: str):
        """

        :param tag_id:
        :param contact_id:
        :return:
        """
        raise NotImplementedError

    async def tag_contact_remove(self, tag_id: str, contact_id: str):
        """

        :param tag_id:
        :param contact_id:
        :return:
        """
        raise NotImplementedError

    async def tag_contact_list(self):
        """
        get tag list
        :return: tag_list
        """
        raise NotImplementedError

    async def message_send_text(self, contact_id: str, message: str) -> str:
        """
        send text message
        :param contact_id: person contact_id
        :param message: message content
        :return: none
        """
        raise NotImplementedError

    async def message_send_contact(
            self,
            contact_id: str,
            send_contact_id: str) -> str:
        """
        send contact message
        :param contact_id: person contact_id
        :param send_contact_id: been send contact_id
        """
        raise NotImplementedError

    async def message_send_file(self, contact_id: str, file: FileBox) -> str:
        """
        send file
        :param contact_id: person contact_id
        :param file: filebox instance
        """
        raise NotImplementedError

    async def message_send_url(
            self,
            contact_id: str,
            url: UrlLinkPayload) -> str:
        """
        send url
        :param contact_id: person contact_id
        :param url: UrlLink instance
        """
        raise NotImplementedError
    # async def message_send_mini_program(
    #   self, contact_id: str, mini_program: )
