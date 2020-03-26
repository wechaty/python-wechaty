"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Union, List, Optional

from .file_box import FileBox
from .url_link_payload import UrlLinkPayload
from .contact import (
    ContactQueryFilter,
    ContactPayload,
)
from .friendship import (
    FriendshipSearchQueryFilter,
    FriendshipPayload
)
from .message import (
    MessageQueryFilter,
    MessagePayload
)

from .room import (
    RoomQueryFilter
)

from .room_invitation import (
    RoomInvitationPayload
)

from .mini_program import (
    MiniProgramPayload
)


# pylint: disable=R0904
class Puppet(ABC):
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

    async def contact_search(
            self,
            query: Union[str, ContactQueryFilter] = None):
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

    async def delete_favorite_tag(self, tag_id: str) -> None:
        """
        delete favorite tag from favorite
        """
        raise NotImplementedError

    async def tag_contact_add(self, tag_id: str, contact_id: str):
        """
        add tag to contact
        :param tag_id:
        :param contact_id:
        :return:
        """
        raise NotImplementedError

    async def tag_favorite_add(self, tag_id: str, contact_id: str):
        """
        add tag to favorite
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

    async def message_send_text(self, conversation_id: str, message: str) -> str:
        """
        send text message
        :param conversation_id: person contact_id or room_id
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

    async def message_send_mini_program(
            self,
            contact_id: str,
            mini_program: MiniProgramPayload) -> str:
        """
        send mini_program message
        :param contact_id:
        :param mini_program:
        :return:
        """
        raise NotImplementedError

    async def message_search(
            self,
            query: Optional[MessageQueryFilter] = None) -> List[str]:
        """
        search message
        """
        raise NotImplementedError

    async def message_recall(self, message_id: str) -> bool:
        """
        send recall message
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_payload(self, message_id: str) -> MessagePayload:
        """
        get message payload
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_forward(self, to_id: str, message_id: str):
        """
        forward message
        :param to_id: type of Room/Contact
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_file(self, message_id: str) -> FileBox:
        """
        convert message to filebox
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_contact(self, message_id: str) -> str:
        """
        get message's contact card
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_url(self, message_id: str) -> UrlLinkPayload:
        """
        get message' url payload
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def message_mini_program(self, message_id: str) -> MiniProgramPayload:
        """
        get message payload
        :param message_id:
        :return:
        """
        raise NotImplementedError

    async def contact_alias(
            self,
            contact_id: str,
            new_alias: str):
        """
        set contact alias
        """
        raise NotImplementedError

    async def contact_payload_dirty(self, contact_id: str):
        """
        refresh contact payload
        """
        raise NotImplementedError

    async def contact_payload(self, contact_id: str) -> ContactPayload:
        """
        get contact payload
        """
        raise NotImplementedError

    async def contact_avatar(self, contact_id: str) -> FileBox:
        """
        get the avatar of the account
        """
        raise NotImplementedError

    async def contact_tag_ids(self, contact_id: str) -> List[str]:
        """
        get tag_ids of the account
        """
        raise NotImplementedError

    def self_id(self) -> str:
        """
        get self_id
        """
        raise NotImplementedError

    async def friendship_search(
            self,
            query_filter: FriendshipSearchQueryFilter) -> Optional[str]:
        """
        search friend by query
        :params:
        :return:
        """
        raise NotImplementedError

    async def friendship_add(self, contact_id: str, hello: str):
        """
        add friendship with hello
        """
        raise NotImplementedError

    def friendship_payload(
            self,
            friendship_id: str,
            payload: Optional[FriendshipPayload]):
        """
        load friendship payload
        """
        raise NotImplementedError

    def friendship_accept(self, friendship_id: str):
        """
        accept friendship
        """
        raise NotImplementedError

    async def room_create(self, contact_ids: List[str], topic: str = None):
        """
        create room with contact_ids and topic
        """
        raise NotImplementedError

    async def room_search(self, query: RoomQueryFilter = None) -> List[str]:
        """
        search room by query filter
        """
        raise NotImplementedError

    async def room_invitation_payload(self, room_invitation_id: str) -> RoomInvitationPayload:
        """
        get room invitation payload
        """
        raise NotImplementedError

    async def room_invitation_accept(self, room_invitation_id: str):
        """
        get room invitation payload
        """
        raise NotImplementedError

    async def contact_self_qr_code(self) -> str:
        """
        get login qrcode
        """
        raise NotImplementedError

    async def contact_self_name(self, name: str):
        """
        change bot contact name
        """
        raise NotImplementedError

    async def contact_signature(self, signature: str):
        """
        change signature
        """
        raise NotImplementedError
