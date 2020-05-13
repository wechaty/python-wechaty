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

from typing import List, Optional

from wechaty_puppet.file_box import FileBox
from wechaty_puppet.schemas.contact import (
    ContactPayload,
)
from wechaty_puppet.schemas.friendship import (
    FriendshipPayload
)
from wechaty_puppet.schemas.image import ImageType
from wechaty_puppet.schemas.message import (
    MessageQueryFilter,
    MessagePayload
)
from wechaty_puppet.schemas.mini_program import (
    MiniProgramPayload
)
# pylint: disable=R0904
from wechaty_puppet.schemas.puppet import PuppetOptions
from wechaty_puppet.schemas.room import (
    RoomQueryFilter,
    RoomPayload,
    RoomMemberPayload
)
from wechaty_puppet.schemas.room_invitation import (
    RoomInvitationPayload
)
from wechaty_puppet.schemas.url_link import UrlLinkPayload
from wechaty_puppet.state_switch import StateSwitch


class Puppet:
    """
    puppet interface class

    TODO -> StateSwitch schema

    """

    def __init__(self, options: PuppetOptions, name: str = 'puppet'):
        self.name: str = name
        self.state: StateSwitch = StateSwitch(name)
        self.options = options

    async def message_image(
            self,
            message_id: str,
            image_type: ImageType
    ) -> FileBox:
        """
        docstring
        :param message_id:
        :param image_type:
        :return:
        """
        raise NotImplementedError

    async def ding(self, data: Optional[str] = None):
        """
        set the ding event
        :param data:
        :return:
        """
        raise NotImplementedError

    def on(self, event_name: str, caller):
        """
        register event on puppet
        """
        raise NotImplementedError

    def listener_count(self, event_name: str) -> int:
        """
        get the count of a specific event listener
        """
        raise NotImplementedError

    async def start(self) -> None:
        """
        start the puppet
        :return:
        """
        raise NotImplementedError

    async def stop(self):
        """
        stop the puppet
        :return:
        """
        raise NotImplementedError

    async def contact_list(self) -> List[str]:
        """
        get all contact list
        """
        raise NotImplementedError

    async def tag_contact_delete(self, tag_id: str) -> None:
        """
        :return:
        """
        raise NotImplementedError

    async def tag_favorite_delete(self, tag_id: str) -> None:
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

    async def tag_contact_list(self, contact_id: Optional[str] = None) -> List[str]:
        """
        get tag list
        :return: tag_list
        """
        raise NotImplementedError

    async def message_send_text(self, conversation_id: str, message: str,
                                mention_ids: List[str] = None) -> str:
        """
        send text message
        :param mention_ids:
        :param conversation_id: person contact_id or room_id
        :param message: message content
        :return: message_id
        """
        raise NotImplementedError

    async def message_send_contact(
            self,
            contact_id: str,
            conversation_id: str) -> str:
        """
        send contact message
        :param conversation_id:
        :param contact_id: person contact_id
        """
        raise NotImplementedError

    async def message_send_file(self, conversation_id: str, file: FileBox
                                ) -> str:
        """
        send file
        :param conversation_id:
        :param file: filebox instance
        """
        raise NotImplementedError

    async def message_send_url(
            self,
            conversation_id: str,
            url: str) -> str:
        """
        send url
        :param conversation_id:
        :param url: UrlLink instance
        """
        raise NotImplementedError

    async def message_send_mini_program(
            self,
            conversation_id: str,
            mini_program: MiniProgramPayload) -> str:
        """
        send mini_program message
        :param conversation_id:
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

    async def contact_alias(self, contact_id: str,
                            alias: Optional[str] = None) -> str:
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

    async def contact_avatar(self, contact_id: str,
                             file_box: Optional[FileBox] = None
                             ) -> FileBox:
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

    async def friendship_search(self, weixin: Optional[str] = None,
                                phone: Optional[str] = None
                                ) -> Optional[str]:
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

    async def friendship_payload(
            self,
            friendship_id: str,
            payload: Optional[FriendshipPayload] = None) -> FriendshipPayload:
        """
        load friendship payload
        """
        raise NotImplementedError

    async def friendship_accept(self, friendship_id: str):
        """
        accept friendship
        """
        raise NotImplementedError

    async def room_list(self) -> List[str]:
        """
        get room list
        :return:
        """
        raise NotImplementedError

    async def room_create(self, contact_ids: List[str], topic: str = None
                          ) -> str:
        """
        create room with contact_ids and topic
        """
        raise NotImplementedError

    async def room_search(self, query: RoomQueryFilter = None) -> List[str]:
        """
        search room by query filter
        """
        raise NotImplementedError

    async def room_invitation_payload(self, room_invitation_id: str,
                                      payload: Optional[RoomInvitationPayload]
                                      = None) -> RoomInvitationPayload:
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

    async def room_payload(self, room_id: str) -> RoomPayload:
        """
        get room payload
        """
        raise NotImplementedError

    async def room_members(self, room_id: str) -> List[str]:
        """
        get room members
        """
        raise NotImplementedError

    async def room_add(self, room_id: str, contact_id: str):
        """
        add contact to a room
        """
        raise NotImplementedError

    async def room_delete(self, room_id: str, contact_id: str):
        """
        delete room
        """
        raise NotImplementedError

    async def room_quit(self, room_id: str):
        """
        quit from
        """
        raise NotImplementedError

    async def room_topic(self, room_id: str, new_topic: str):
        """
        set room topic
        """
        raise NotImplementedError

    async def room_announce(
            self,
            room_id: str,
            announcement: str = None) -> str:
        """
        set/get room announcement
        """
        raise NotImplementedError

    async def room_qr_code(self, room_id: str) -> str:
        """
        get room_qrcode
        """
        raise NotImplementedError

    async def room_member_payload(
            self,
            room_id: str,
            contact_id: str) -> RoomMemberPayload:
        """
        get room member payload
        """
        raise NotImplementedError

    async def room_avatar(self, room_id: str) -> FileBox:
        """
        get the avatar of the room
        """
        raise NotImplementedError
